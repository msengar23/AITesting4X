"""Prompt builder: constructs evidence-grounded prompts for the LLM.

Only Jira issue data, user instructions, and template content are ever
included. Credentials are never part of any prompt. The system prompt
enforces the strict anti-hallucination policy from the spec.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "testcase_creator.md"

SYSTEM_PROMPT = """You are a Senior QA Engineer and test-case design expert.

STRICT ANTI-HALLUCINATION POLICY (MANDATORY):
1. Use ONLY the information provided in the Jira issue data and the user's instructions below.
2. Do NOT invent requirements, Jira fields, acceptance criteria, APIs, URLs, database tables,
   error messages, HTTP status codes, UI elements, business rules, or authentication mechanisms.
3. Do NOT assume "typical" application behavior. If something is not documented, say so.
4. When required information is unavailable, state exactly one of:
   - "Not specified in the Jira issue."
   - "Not provided in the available information."
5. Every test case must be traceable to the provided Jira content or the explicit user request.
6. Only generate test categories that are relevant to the Jira requirement or explicitly requested.
7. If the Jira issue has no usable requirement content, say so instead of inventing scenarios.

OUTPUT FORMAT:
- Prefer a markdown table with these columns when generating test cases:
  | Test Case ID | Test Scenario | Preconditions | Test Data | Steps to Reproduce | Expected Result | Test Type | Priority |
- Test Case IDs follow TC-001, TC-002, ... format.
- Priority must be one of: High, Medium, Low.
- Steps must be a numbered list inside the cell: 1. ... 2. ... 3. ...
- For a test plan, use structured sections (Objective, Scope, Out of Scope, Requirements,
  Test Strategy, Test Scenarios, Test Data, Dependencies, Risks, Assumptions) only when
  supported by the source information.
- Do not include any preamble or closing notes outside the table/plan.
"""


def _format_issue_data(issue: dict[str, Any]) -> str:
    """Render the normalized Jira issue as labeled text for the prompt."""
    lines = [f"Jira Issue Key: {issue.get('key', '')}"]
    for label, key in (
        ("Summary", "summary"),
        ("Description", "description"),
        ("Status", "status"),
        ("Priority", "priority"),
        ("Issue Type", "issuetype"),
        ("Project", "project"),
        ("Reporter", "reporter"),
        ("Assignee", "assignee"),
        ("Created", "created"),
        ("Updated", "updated"),
    ):
        value = issue.get(key)
        if value:
            lines.append(f"{label}: {value}")
    if issue.get("labels"):
        lines.append(f"Labels: {', '.join(issue['labels'])}")
    if issue.get("components"):
        lines.append(f"Components: {', '.join(issue['components'])}")
    for key, value in issue.items():
        if key.startswith("custom_"):
            lines.append(f"{key.replace('custom_', '').replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def build_prompt(
    issue_data: dict[str, Any],
    user_request: str,
    template_path: Path | None = None,
) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) grounded in the Jira issue."""
    template = DEFAULT_TEMPLATE
    if template_path is not None:
        template = template_path
    if not template.exists():
        template = DEFAULT_TEMPLATE

    try:
        template_text = template.read_text(encoding="utf-8")
    except OSError:
        template_text = ""

    issue_text = _format_issue_data(issue_data)
    requirements = f"Jira Issue Data (evidence only):\n{issue_text}" if issue_text else "Jira Issue Data: (no usable content returned)"

    user_prompt = template_text
    user_prompt = user_prompt.replace("[PASTE REQUIREMENTS HERE]", requirements)
    user_prompt = user_prompt.replace("[NUMBER]", "as many as relevant")
    user_prompt += f"\n\nUSER REQUEST:\n{user_request}"

    return SYSTEM_PROMPT, user_prompt
