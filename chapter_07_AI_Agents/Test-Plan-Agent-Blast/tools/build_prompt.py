"""Build evidence-grounded prompts for the test-plan LLM call.

Implements architecture/SOP_generate_plan.md section 3. Only issue data,
the JSON contract, and user instructions are included. Credentials are
never part of any prompt.
"""

from __future__ import annotations

from typing import Any

SYSTEM_PROMPT = """You are a Senior QA Engineer and test-design expert.

STRICT ANTI-HALLUCINATION POLICY (MANDATORY):
1. Use ONLY the information provided in the Jira issue data and the user's instructions.
2. Do NOT invent requirements, Jira fields, acceptance criteria, APIs, URLs, database tables,
   error messages, HTTP status codes, UI elements, business rules, or authentication mechanisms.
3. Do NOT assume "typical" application behaviour. If something is not documented, say so.
4. When required information is unavailable, use exactly: "Not specified in the Jira issue."
5. Every test case must be traceable to the provided Jira content or the explicit user request.

TEST DESIGN (ISTQB — MANDATORY):
- Apply recognised techniques deliberately and label each case's test_design_technique:
  "Boundary Value Analysis", "Equivalence Partitioning", "Decision Table",
  "State Transition", "Error Guessing", or "None".
- Include at least one NON-Positive case (type "Negative" or "Edge").
- Cover positive, negative, boundary, and edge behaviour where the issue supports it.
- Expected results must be single, observable, and verifiable.

OUTPUT FORMAT (STRICT):
- Return ONLY a single JSON object. No prose, no markdown fences, no commentary.
- Exactly these top-level keys:
  title, objective, preconditions, test_data, test_cases, risks, out_of_scope
- Each test case has exactly:
  id, title, priority, type, test_design_technique, traceability, steps, expected_result
- priority is one of: High, Medium, Low
- type is one of: Positive, Negative, Edge, Boundary, Regression, Integration
- steps is a non-empty array of strings, each a single action (no leading numbers).
- traceability names the requirement fragment the case derives from; never leave it empty.
- If the issue is thin, produce FEWER well-grounded cases and record the gaps in risks.
  Never pad with invented scenarios.
"""

JSON_CONTRACT = """{
  "title": "Test Plan - <KEY>: <summary>",
  "objective": "One paragraph stating what this plan verifies.",
  "preconditions": ["Environment/access/data state required before testing"],
  "test_data": ["Concrete input values or data sets required"],
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Short imperative title",
      "priority": "High",
      "type": "Positive",
      "test_design_technique": "Equivalence Partitioning",
      "traceability": "Acceptance criterion or requirement fragment",
      "steps": ["Do this", "Then this"],
      "expected_result": "Single, observable, verifiable outcome"
    }
  ],
  "risks": ["Area of uncertainty or risk"],
  "out_of_scope": ["Explicitly excluded behaviour"]
}"""


def format_issue(issue: dict[str, Any]) -> str:
    """Render the normalized issue as labelled text for the prompt."""
    lines = [f"Jira Issue Key: {issue.get('key', '')}"]
    for label, key in (
        ("Summary", "summary"),
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

    description = issue.get("description")
    lines.append("")
    lines.append("Description:")
    lines.append(description if description else "(no description provided)")

    ac = issue.get("acceptance_criteria")
    lines.append("")
    lines.append("Acceptance Criteria:")
    lines.append(ac if ac else "(no acceptance criteria field exists for this project)")

    return "\n".join(lines)


def grounding_note(issue: dict[str, Any]) -> str:
    """Explain which fields the plan may be grounded on (SOP_generate_plan section 3).

    Selects from the three-state `grounding` flag so the prompt never claims a
    source that is not actually present on the issue.
    """
    grounding = issue.get("grounding", "")

    if grounding == "acceptance_criteria":
        return (
            "GROUNDING: Acceptance Criteria is the primary source of expected results; "
            "the description is supporting context."
        )
    if grounding == "description_only":
        return (
            "GROUNDING: This project has NO Acceptance Criteria field. The DESCRIPTION is the "
            "primary source of expected results and the Summary is secondary. Because grounding "
            "is description-only, include a risk entry stating that the plan is based solely on "
            "the ticket description and should be reviewed against the real requirements."
        )
    return (
        "GROUNDING: MINIMAL — this issue has NO description and NO acceptance criteria; only a "
        "summary is available. Ground strictly on the summary, produce only a small number of "
        "high-level cases, and write \"Not specified in the Jira issue.\" for any unknown "
        "expected result. Include a prominent risk entry stating that grounding is minimal and "
        "the plan is near-speculative."
    )


def build_prompt(
    issue: dict[str, Any],
    instructions: str = "",
) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) grounded in the Jira issue."""
    sections = [
        "Jira Issue Data (evidence only):",
        format_issue(issue),
        "",
        grounding_note(issue),
        "",
        "Required JSON shape:",
        JSON_CONTRACT,
    ]
    if instructions.strip():
        sections += ["", "ADDITIONAL USER INSTRUCTIONS:", instructions.strip()]

    sections += [
        "",
        "Produce the test plan now as a single JSON object and nothing else.",
    ]
    return SYSTEM_PROMPT, "\n".join(sections)
