"""Fetch and normalize a single Jira issue (deterministic, no LLM).

Implements architecture/SOP_fetch_issue.md: validate the key, call
Jira Cloud REST API v3, flatten Atlassian Document Format descriptions to
plain text, and extract only the fields actually present.
"""

from __future__ import annotations

import re
from typing import Any

import requests

from tools.config import Config
from tools.errors import (
    JiraAuthError,
    JiraInvalidKeyError,
    JiraNetworkError,
    JiraNotFoundError,
    JiraPermissionError,
    JiraTimeoutError,
)

ISSUE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")

REQUESTED_FIELDS = (
    "summary,description,status,priority,issuetype,labels,"
    "components,project,reporter,assignee,created,updated"
)

MAX_DESCRIPTION_CHARS = 12000


def validate_key(key: str) -> str:
    """Return a normalized key or raise JiraInvalidKeyError. No network call."""
    candidate = (key or "").strip().upper()
    if not ISSUE_KEY_RE.match(candidate):
        raise JiraInvalidKeyError(
            f"'{key}' is not a valid Jira issue key. Expected format like PROJ-123."
        )
    return candidate


def flatten_adf(node: Any) -> str:
    """Flatten an Atlassian Document Format tree to plain text."""
    if not isinstance(node, dict):
        return "" if node is None else str(node)

    parts: list[str] = []

    def walk(current: dict[str, Any]) -> None:
        node_type = current.get("type")
        if node_type == "text":
            parts.append(current.get("text", ""))
            return
        if node_type == "hardBreak":
            parts.append("\n")
            return
        content = current.get("content")
        if isinstance(content, list):
            for child in content:
                if isinstance(child, dict):
                    walk(child)
                elif child is not None:
                    parts.append(str(child))
        if node_type in ("paragraph", "heading", "listItem", "codeBlock"):
            parts.append("\n")

    walk(node)
    text = "".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _flatten_value(value: Any) -> str:
    """Flatten a custom field value that may be ADF, a dict, or a list."""
    if isinstance(value, dict):
        if "content" in value:
            return flatten_adf(value)
        if "value" in value:
            return str(value["value"])
        return str(value.get("name", ""))
    if isinstance(value, list):
        return ", ".join(_flatten_value(item) for item in value)
    return "" if value is None else str(value)


def _truncate(text: str) -> str:
    if len(text) <= MAX_DESCRIPTION_CHARS:
        return text
    return text[:MAX_DESCRIPTION_CHARS] + "\n\n[...truncated]"


def normalize_issue(data: dict[str, Any], ac_field: str = "") -> dict[str, Any]:
    """Extract only fields present in the Jira response, ADF-flattened."""
    fields = data.get("fields") or {}
    issue: dict[str, Any] = {"key": data.get("key", "")}

    for name in ("summary", "description", "created", "updated"):
        value = fields.get(name)
        if value is None or value == "":
            continue
        if name == "description":
            flattened = flatten_adf(value) if isinstance(value, dict) else str(value)
            flattened = _truncate(flattened)
            if flattened:
                issue["description"] = flattened
        else:
            issue[name] = value

    for name in ("status", "priority", "issuetype", "project", "reporter", "assignee"):
        value = fields.get(name)
        if isinstance(value, dict):
            resolved = value.get("name") or value.get("displayName") or ""
            if resolved:
                issue[name] = resolved

    labels = fields.get("labels")
    if isinstance(labels, list) and labels:
        issue["labels"] = [str(item) for item in labels]

    components = fields.get("components")
    if isinstance(components, list) and components:
        names = [item.get("name", "") for item in components if isinstance(item, dict)]
        if any(names):
            issue["components"] = [name for name in names if name]

    if ac_field:
        value = fields.get(ac_field)
        if value not in (None, ""):
            flattened = _flatten_value(value)
            if flattened:
                issue["acceptance_criteria"] = _truncate(flattened)

    if issue.get("acceptance_criteria"):
        issue["grounding"] = "acceptance_criteria"
    elif issue.get("description"):
        issue["grounding"] = "description_only"
    else:
        issue["grounding"] = "low"

    return issue


def list_project_issues(
    config: Config,
    project_key: str,
    limit: int = 10,
    session: requests.Session | None = None,
) -> list[str]:
    """Return issue keys for a project, ordered by key (SOP_trigger section 3).

    Uses Jira Cloud's `/rest/api/3/search/jql`; the legacy `/rest/api/3/search`
    route is retired and returns 410 Gone.
    """
    project = (project_key or "").strip().upper()
    if not project:
        raise JiraInvalidKeyError("A project key is required, e.g. SAM1.")

    bounded = max(1, min(int(limit), 50))
    http = session or requests.Session()

    try:
        response = http.get(
            f"{config.jira_url}/rest/api/3/search/jql",
            params={
                "jql": f"project={project} ORDER BY key ASC",
                "maxResults": bounded,
                "fields": "key",
            },
            auth=(config.jira_email, config.jira_api_token),
            headers={"Accept": "application/json"},
            timeout=config.timeout,
        )
    except requests.exceptions.Timeout as exc:
        raise JiraTimeoutError(
            "Jira did not respond in time. Check your connection and try again."
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        raise JiraNetworkError(
            "Could not connect to Jira. Check the Jira URL and your network connection."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise JiraNetworkError("Jira request failed unexpectedly.") from exc

    if response.status_code == 401:
        raise JiraAuthError(
            "Jira authentication failed. Check your Jira email and API token."
        )
    if response.status_code == 403:
        raise JiraPermissionError(f"You do not have permission to view project {project}.")
    if response.status_code == 404:
        raise JiraNotFoundError(f"Project '{project}' was not found.")
    if response.status_code >= 400:
        raise JiraNetworkError(
            f"Jira returned an unexpected error (HTTP {response.status_code})."
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise JiraNetworkError("Jira returned an unexpected response format.") from exc

    return [issue.get("key", "") for issue in data.get("issues", []) if issue.get("key")]


def fetch_issue(config: Config, key: str, session: requests.Session | None = None) -> dict[str, Any]:
    """Fetch and normalize one Jira issue by key (SOP_fetch_issue)."""
    normalized_key = validate_key(key)
    http = session or requests.Session()
    url = f"{config.jira_url}/rest/api/3/issue/{normalized_key}"
    params = {"fields": REQUESTED_FIELDS}
    if config.jira_ac_field:
        params["fields"] = f"{REQUESTED_FIELDS},{config.jira_ac_field}"

    try:
        response = http.get(
            url,
            params=params,
            auth=(config.jira_email, config.jira_api_token),
            headers={"Accept": "application/json"},
            timeout=config.timeout,
        )
    except requests.exceptions.Timeout as exc:
        raise JiraTimeoutError(
            "Jira did not respond in time. Check your connection and try again."
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        raise JiraNetworkError(
            "Could not connect to Jira. Check the Jira URL and your network connection."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise JiraNetworkError("Jira request failed unexpectedly.") from exc

    if response.status_code == 401:
        raise JiraAuthError(
            "Jira authentication failed. Check your Jira email and API token."
        )
    if response.status_code == 403:
        raise JiraPermissionError("You do not have permission to view this Jira issue.")
    if response.status_code == 404:
        raise JiraNotFoundError("The Jira issue was not found.")
    if response.status_code >= 400:
        raise JiraNetworkError(
            f"Jira returned an unexpected error (HTTP {response.status_code})."
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise JiraNetworkError("Jira returned an unexpected response format.") from exc

    return normalize_issue(data, ac_field=config.jira_ac_field)
