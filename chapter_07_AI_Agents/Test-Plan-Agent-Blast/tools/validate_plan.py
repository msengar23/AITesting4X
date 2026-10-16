"""Parse and validate the LLM test-plan output.

Implements architecture/SOP_generate_plan.md section 5.

Phase A: JSON Schema validation via `jsonschema` (invariant I10).
Phase B: deterministic checks the schema cannot express — ID sequencing
         and the coverage rule (at least one non-Positive case).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.errors import PlanValidationError

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "test_plan.schema.json"

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)
_LEADING_NUMBER_RE = re.compile(r"^\s*\d+[.)]\s*")


def extract_json(raw: str) -> dict[str, Any]:
    """Extract a JSON object from model output, tolerating fences and prose."""
    text = (raw or "").strip()
    if not text:
        raise PlanValidationError("The model returned an empty response. Please try again.")

    cleaned = _FENCE_RE.sub("", text).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise PlanValidationError(
                "The model returned an invalid test plan. Please try again."
            )
        try:
            parsed = json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError as exc:
            raise PlanValidationError(
                "The model returned an invalid test plan. Please try again."
            ) from exc

    if not isinstance(parsed, dict):
        raise PlanValidationError(
            "The model returned an invalid test plan. Please try again."
        )
    return parsed


def _load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _clean_steps(steps: list[str]) -> list[str]:
    """Strip any numbering the model added so the renderer can number cleanly."""
    return [_LEADING_NUMBER_RE.sub("", str(step)).strip() for step in steps if str(step).strip()]


def validate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate against the JSON Schema, then apply deterministic checks.

    Returns a normalized copy with renumbered test-case IDs.
    """
    schema = _load_schema()
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(plan), key=lambda error: list(error.path))

    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "(root)"
        raise PlanValidationError(
            f"The model returned an invalid test plan ({location}: {first.message})"
        )

    cases = plan.get("test_cases") or []
    if not cases:
        raise PlanValidationError("The model returned a test plan with no test cases.")

    if not any(case.get("type") != "Positive" for case in cases):
        raise PlanValidationError(
            "The model returned a test plan with only positive cases; "
            "at least one negative or edge case is required."
        )

    normalized = dict(plan)
    normalized["test_cases"] = []
    for index, case in enumerate(cases, start=1):
        entry = dict(case)
        entry["id"] = f"TC-{index:03d}"
        entry["steps"] = _clean_steps(case.get("steps") or [])
        normalized["test_cases"].append(entry)

    return normalized


def load_and_validate(raw: str) -> dict[str, Any]:
    """Extract JSON from raw model text and validate it."""
    return validate_plan(extract_json(raw))
