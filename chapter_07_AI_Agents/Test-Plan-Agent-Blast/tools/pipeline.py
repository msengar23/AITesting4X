"""End-to-end pipeline shared by the CLI and the Streamlit UI.

Implements architecture/SOP_pipeline.md. This is the navigation layer: it
orchestrates the deterministic tools and the single LLM call, and owns the
validation retry decision. Invariant I9: both entry points call this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from tools.build_prompt import build_prompt
from tools.config import Config, load_config
from tools.errors import AppError, PlanValidationError
from tools.fetch_jira_issue import fetch_issue, list_project_issues
from tools.generate_test_plan import generate
from tools.render_markdown import render, write_markdown
from tools.validate_plan import load_and_validate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = PROJECT_ROOT / ".tmp"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MAX_ATTEMPTS = 2

StageCallback = Callable[[str], None]


@dataclass
class PipelineResult:
    """Everything a caller needs after a successful run."""

    issue: dict[str, Any]
    plan: dict[str, Any]
    markdown: str
    output_path: Path
    model: str


@dataclass
class BatchOutcome:
    """Per-key result of a batch run (SOP_trigger section 3)."""

    key: str
    ok: bool
    case_count: int = 0
    output_path: Path | None = None
    error: str = ""


@dataclass
class BatchResult:
    """Aggregate of a batch run."""

    outcomes: list[BatchOutcome]

    @property
    def succeeded(self) -> list[BatchOutcome]:
        return [outcome for outcome in self.outcomes if outcome.ok]

    @property
    def failed(self) -> list[BatchOutcome]:
        return [outcome for outcome in self.outcomes if not outcome.ok]

    @property
    def all_ok(self) -> bool:
        return not self.failed


def _noop(_: str) -> None:
    """Default progress callback."""


def _write_intermediate(key: str, plan: dict[str, Any]) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    path = TMP_DIR / f"{key}_plan.json"
    path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def generate_test_plan(
    jira_key: str,
    instructions: str = "",
    config: Config | None = None,
    on_stage: StageCallback | None = None,
) -> PipelineResult:
    """Run the full pipeline for one Jira key and return the result."""
    notify = on_stage or _noop

    notify("Loading configuration")
    cfg = config or load_config()

    notify(f"Fetching Jira issue {jira_key}")
    issue = fetch_issue(cfg, jira_key)

    notify("Building prompt")
    system_prompt, user_prompt = build_prompt(issue, instructions)

    notify(f"Generating test plan with {cfg.groq_model}")
    plan: dict[str, Any] | None = None
    last_error: PlanValidationError | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        raw = generate(cfg, system_prompt, user_prompt)
        try:
            plan = load_and_validate(raw)
            break
        except PlanValidationError as exc:
            last_error = exc
            if attempt < MAX_ATTEMPTS:
                notify("Plan failed validation — retrying once with a correction")
                user_prompt = (
                    f"{user_prompt}\n\nCORRECTION REQUIRED:\n{exc.message}\n"
                    "Return the corrected JSON object only."
                )

    if plan is None:
        raise last_error or PlanValidationError(
            "The model returned an invalid test plan. Please try again."
        )

    notify("Validating and rendering Markdown")
    key = issue.get("key", jira_key)
    _write_intermediate(key, plan)
    issue_url = f"{cfg.jira_url}/browse/{key}"
    markdown = render(issue, plan, model=cfg.groq_model, issue_url=issue_url)
    output_path = write_markdown(markdown, key, out_dir=OUTPUT_DIR)

    notify(f"Wrote {output_path.name}")
    return PipelineResult(
        issue=issue,
        plan=plan,
        markdown=markdown,
        output_path=output_path,
        model=cfg.groq_model,
    )


def resolve_keys(
    config: Config,
    project: str = "",
    keys: str | list[str] = "",
    limit: int = 10,
) -> list[str]:
    """Resolve the target key set for a batch run (SOP_trigger section 3)."""
    resolved: list[str] = []

    if keys:
        raw = keys.split(",") if isinstance(keys, str) else list(keys)
        resolved = [item.strip().upper() for item in raw if item and item.strip()]
    elif project:
        resolved = list_project_issues(config, project, limit=limit)

    unique: list[str] = []
    for key in resolved:
        if key not in unique:
            unique.append(key)
    return unique


def generate_batch(
    keys: list[str],
    instructions: str = "",
    config: Config | None = None,
    on_stage: StageCallback | None = None,
    on_key: Callable[[str, int, int], None] | None = None,
) -> BatchResult:
    """Run the pipeline for each key, continuing past individual failures."""
    cfg = config or load_config()
    outcomes: list[BatchOutcome] = []
    total = len(keys)

    for index, key in enumerate(keys, start=1):
        if on_key:
            on_key(key, index, total)
        try:
            result = generate_test_plan(
                key, instructions=instructions, config=cfg, on_stage=on_stage
            )
            outcomes.append(
                BatchOutcome(
                    key=result.issue.get("key", key),
                    ok=True,
                    case_count=len(result.plan.get("test_cases", [])),
                    output_path=result.output_path,
                )
            )
        except AppError as exc:
            outcomes.append(BatchOutcome(key=key, ok=False, error=exc.message))
        except Exception as exc:  # noqa: BLE001 - one bad key must not kill the batch
            outcomes.append(
                BatchOutcome(key=key, ok=False, error=f"Unexpected error: {type(exc).__name__}")
            )

    return BatchResult(outcomes=outcomes)
