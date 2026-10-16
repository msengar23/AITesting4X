"""Render a validated test plan to Markdown (deterministic, no LLM).

Implements architecture/SOP_render_markdown.md. The Coverage Summary is
computed here from the validated test-case array — the model never writes it.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

PRIORITY_ORDER = ("High", "Medium", "Low")
TYPE_ORDER = ("Positive", "Negative", "Edge", "Boundary", "Regression", "Integration")
TECHNIQUE_ORDER = (
    "Boundary Value Analysis",
    "Equivalence Partitioning",
    "Decision Table",
    "State Transition",
    "Error Guessing",
    "None",
)

AI_BANNER = (
    "> ⚠️ **AI-generated draft — requires human review.**\n"
    "> This test plan was produced automatically from a Jira issue. "
    "It is a starting point, not a substitute for QA judgement. "
    "Review every case and add any missing domain or business-critical scenarios."
)


def _escape(text: Any) -> str:
    """Escape pipes and collapse newlines so table/list rendering stays intact."""
    value = "" if text is None else str(text)
    value = value.replace("\n", " ").strip()
    return value.replace("|", "\\|")


def _bullet_list(items: list[str], empty_note: str = "_None identified._") -> str:
    cleaned = [str(item).strip() for item in (items or []) if str(item).strip()]
    if not cleaned:
        return empty_note
    return "\n".join(f"- {_escape(item)}" for item in cleaned)


def _counter_line(counter: Counter, order: tuple[str, ...]) -> str:
    parts = [f"{key}: {counter[key]}" for key in order if counter.get(key)]
    return " · ".join(parts) if parts else "_none_"


def coverage_summary(test_cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute the deterministic coverage ledger (invariant I5, AD3)."""
    return {
        "total": len(test_cases),
        "by_priority": Counter(case.get("priority", "") for case in test_cases),
        "by_type": Counter(case.get("type", "") for case in test_cases),
        "by_technique": Counter(case.get("test_design_technique", "") for case in test_cases),
    }


def _focus_areas(test_cases: list[dict[str, Any]], limit: int = 4) -> str:
    """Unique traceability values in first-seen order (deduplicated, capped)."""
    seen: list[str] = []
    for case in test_cases:
        value = str(case.get("traceability", "")).strip()
        if value and value not in seen:
            seen.append(value)
    if not seen:
        return "_Not specified._"
    shown = seen[:limit]
    text = " · ".join(shown)
    if len(seen) > limit:
        text += f" (+{len(seen) - limit} more)"
    return text


def _techniques_used(summary: dict[str, Any]) -> str:
    applied = [key for key in TECHNIQUE_ORDER if key != "None" and summary["by_technique"].get(key)]
    return " · ".join(applied) if applied else "_None specified._"


_GROUNDING_TEXT = {
    "acceptance_criteria": "Acceptance criteria + description",
    "description_only": "Description only — no Acceptance Criteria field on this project",
    "low": "⚠️ Low — no description or acceptance criteria on this issue",
}


def _grounding_text(issue: dict[str, Any]) -> str:
    """Map the three-state grounding flag to a plain-language phrase."""
    return _GROUNDING_TEXT.get(issue.get("grounding", ""), "Not recorded")


def _at_a_glance(
    issue: dict[str, Any],
    plan: dict[str, Any],
    summary: dict[str, Any],
) -> list[str]:
    """Plain-language, code-computed overview block (SOP section 3a)."""
    cases = plan.get("test_cases") or []
    by_type = summary["by_type"]
    positives = by_type.get("Positive", 0)
    non_positives = summary["total"] - positives

    return [
        "| | |",
        "|---|---|",
        f"| **Test cases** | {summary['total']} ({positives} positive · {non_positives} negative/edge) |",
        f"| **Focus areas** | {_escape(_focus_areas(cases))} |",
        f"| **Techniques** | {_escape(_techniques_used(summary))} |",
        f"| **Grounding** | {_escape(_grounding_text(issue))} |",
        "| **Review status** | ⚠️ Draft — human review required |",
    ]


def _summary_table(test_cases: list[dict[str, Any]]) -> list[str]:
    """Scannable overview table rendered before the detailed case blocks."""
    lines = [
        "| ID | Test case | Priority | Type | Technique |",
        "|---|---|---|---|---|",
    ]
    for case in test_cases:
        lines.append(
            f"| {_escape(case.get('id', ''))} "
            f"| {_escape(case.get('title', ''))} "
            f"| {_escape(case.get('priority', ''))} "
            f"| {_escape(case.get('type', ''))} "
            f"| {_escape(case.get('test_design_technique', ''))} |"
        )
    return lines


def _render_case(case: dict[str, Any]) -> str:
    lines = [
        f"### {case.get('id', '')} — {_escape(case.get('title', ''))}",
        "",
        f"- **Priority:** {_escape(case.get('priority', ''))}",
        f"- **Type:** {_escape(case.get('type', ''))}",
        f"- **Technique:** {_escape(case.get('test_design_technique', ''))}",
        f"- **Traceability:** {_escape(case.get('traceability', ''))}",
        "",
        "**Steps:**",
        "",
    ]
    for index, step in enumerate(case.get("steps") or [], start=1):
        lines.append(f"{index}. {_escape(step)}")
    lines += [
        "",
        f"**Expected Result:** {_escape(case.get('expected_result', ''))}",
    ]
    return "\n".join(lines)


def render(
    issue: dict[str, Any],
    plan: dict[str, Any],
    model: str = "",
    issue_url: str = "",
) -> str:
    """Render the test plan as a Markdown string."""
    key = issue.get("key", "")
    title = plan.get("title") or f"Test Plan — {key}: {issue.get('summary', '')}"
    title = title.replace(" - ", " — ", 1) if title.startswith("Test Plan - ") else title
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    cases = plan.get("test_cases") or []
    summary = coverage_summary(cases)

    issue_cell = f"[{_escape(key)}]({issue_url})" if issue_url else _escape(key)

    lines: list[str] = [
        f"# {_escape(title)}",
        "",
        AI_BANNER,
        "",
        "## At a Glance",
        "",
        *_at_a_glance(issue, plan, summary),
        "",
        "## Details",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Jira Issue | {issue_cell} |",
        f"| Summary | {_escape(issue.get('summary', '—'))} |",
        f"| Type | {_escape(issue.get('issuetype', 'Unknown'))} |",
        f"| Priority | {_escape(issue.get('priority') or '—')} |",
        f"| Status | {_escape(issue.get('status', 'Unknown'))} |",
        f"| Components | {_escape(', '.join(issue.get('components', [])) or 'None')} |",
    ]
    if model:
        lines.append(f"| Model | `{_escape(model)}` |")
    lines += [
        f"| Generated | {generated} |",
        "",
        "## 1. Objective",
        "",
        _escape(plan.get("objective", "")) or "_Not specified._",
        "",
        "## 2. Preconditions",
        "",
        _bullet_list(plan.get("preconditions")),
        "",
        "## 3. Test Data",
        "",
        _bullet_list(plan.get("test_data")),
        "",
        "## 4. Test Cases",
        "",
        "### Summary",
        "",
        *_summary_table(cases),
        "",
    ]

    for case in cases:
        lines.append(_render_case(case))
        lines.append("")

    lines += [
        "## 5. Coverage Summary",
        "",
        "<!-- Computed by code from the validated test cases — not model-authored. -->",
        "",
        "| Dimension | Breakdown |",
        "|---|---|",
        f"| Total cases | {summary['total']} |",
        f"| By priority | {_counter_line(summary['by_priority'], PRIORITY_ORDER)} |",
        f"| By type | {_counter_line(summary['by_type'], TYPE_ORDER)} |",
        f"| By technique | {_counter_line(summary['by_technique'], TECHNIQUE_ORDER)} |",
        "",
        "## 6. Risks",
        "",
        _bullet_list(plan.get("risks")),
        "",
        "## 7. Out of Scope",
        "",
        _bullet_list(plan.get("out_of_scope")),
        "",
    ]

    return "\n".join(lines)


def write_markdown(markdown: str, key: str, out_dir: Path | None = None) -> Path:
    """Write the rendered plan to outputs/<KEY>_test_plan.md and return the path."""
    directory = out_dir or (Path(__file__).resolve().parent.parent / "outputs")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{key}_test_plan.md"
    path.write_text(markdown, encoding="utf-8")
    return path
