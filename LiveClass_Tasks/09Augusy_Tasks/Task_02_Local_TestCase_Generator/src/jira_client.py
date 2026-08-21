"""Jira REST API client (read-only).

Fetches a single issue by key using Jira Cloud REST API v3 (with v2
fallback), flattens the Atlassian Document Format description to plain
text, and extracts only fields that are actually present in the response.
"""

from __future__ import annotations

import logging
import re
from typing import Any

import requests

from errors import (
    JiraAuthError,
    JiraInvalidKeyError,
    JiraNetworkError,
    JiraNotFoundError,
    JiraPermissionError,
    JiraTimeoutError,
)

logger = logging.getLogger("tc_generator.jira")

ISSUE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")

# Fields we care about; the API returns only those present on the issue.
_REQUESTED_FIELDS = [
    "summary",
    "description",
    "status",
    "priority",
    "issuetype",
    "labels",
    "components",
    "project",
    "reporter",
    "assignee",
    "created",
    "updated",
]

_TIMEOUT = 15


class JiraClient:
    """Minimal read-only Jira REST client."""

    def __init__(self, base_url: str, email: str, api_token: str, timeout: int = _TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.get(url, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise JiraTimeoutError(
                "Jira did not respond in time. Please check your connection and try again."
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
            raise JiraPermissionError(
                "You do not have permission to view this Jira issue."
            )
        if response.status_code == 404:
            raise JiraNotFoundError("The Jira issue was not found.")
        if response.status_code >= 400:
            raise JiraNetworkError(
                f"Jira returned an unexpected error (HTTP {response.status_code})."
            )

        try:
            return response.json()
        except ValueError as exc:
            raise JiraNetworkError("Jira returned an unexpected response format.") from exc

    def get_issue(self, key: str) -> dict[str, Any]:
        """Fetch and normalize a Jira issue by key."""
        if not ISSUE_KEY_RE.match(key):
            raise JiraInvalidKeyError(
                f"'{key}' is not a valid Jira issue key. Expected format like PROJ-123."
            )

        path = f"/rest/api/3/issue/{key}"
        query = "?fields=" + ",".join(_REQUESTED_FIELDS)
        data = self._request(path + query)
        return self._normalize_issue(data)

    def _normalize_issue(self, data: dict[str, Any]) -> dict[str, Any]:
        """Extract only the fields actually present in the Jira response."""
        fields = data.get("fields") or {}
        issue: dict[str, Any] = {"key": data.get("key", ""), "self": data.get("self", "")}

        def pick(field_name: str) -> None:
            if field_name in fields:
                value = fields[field_name]
                if value is not None and value != "":
                    issue[field_name] = value

        pick("summary")
        pick("description")
        pick("created")
        pick("updated")
        pick("labels")

        for name in ("status", "priority", "issuetype", "project", "reporter", "assignee"):
            if name in fields and isinstance(fields[name], dict):
                issue[name] = fields[name].get("name") or fields[name].get("displayName", "")

        if "components" in fields and isinstance(fields["components"], list):
            issue["components"] = [c.get("name", "") for c in fields["components"] if isinstance(c, dict)]

        # Pull any custom field whose name suggests acceptance criteria / DoD.
        for field_key, value in fields.items():
            if not field_key.startswith("customfield_"):
                continue
            if value is None or value == "":
                continue
            schema = (fields.get("__schema") or {}).get(field_key, {}) if "__schema" in fields else {}
            name = (schema.get("name") or "").lower()
            if "acceptance" in name or "definition of done" in name:
                issue[f"custom_{name.replace(' ', '_')}"] = self._flatten_value(value)

        if "description" in issue and isinstance(issue["description"], dict):
            issue["description"] = self._flatten_adf(issue["description"])

        return issue

    @staticmethod
    def _flatten_adf(node: dict[str, Any]) -> str:
        """Flatten an Atlassian Document Format node to plain text."""
        parts: list[str] = []

        def walk(n: dict[str, Any]) -> None:
            node_type = n.get("type")
            if node_type == "text":
                parts.append(n.get("text", ""))
                return
            if node_type == "hardBreak":
                parts.append("\n")
                return
            content = n.get("content")
            if isinstance(content, list):
                for child in content:
                    if isinstance(child, dict):
                        walk(child)
            if node_type in ("paragraph", "heading", "listItem", "codeBlock"):
                parts.append("\n")

        walk(node)
        text = "".join(parts)
        # Collapse 3+ newlines to 2 and trim trailing whitespace.
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def _flatten_value(value: Any) -> Any:
        if isinstance(value, dict):
            if "content" in value:  # ADF
                return JiraClient._flatten_adf(value)
            if "value" in value:
                return value["value"]
            return value.get("name", str(value))
        if isinstance(value, list):
            return ", ".join(str(v.get("value", v)) for v in value if isinstance(v, dict)) or ", ".join(str(v) for v in value)
        return str(value)

    def verify_connection(self) -> bool:
        """Ping Jira to confirm credentials work (used by the Settings page)."""
        path = f"/rest/api/3/myself?fields=accountId"
        data = self._request(path)
        return bool(data and data.get("accountId"))
