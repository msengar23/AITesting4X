# SOP — Generate Test Plan (LLM Call + Validation)

**Layer:** 1 (Architecture) · **Tools:** `tools/build_prompt.py`, `tools/generate_test_plan.py`, `tools/validate_plan.py` · **Version:** 1.0 (2026-09-11)

---

## 1. Goal

Turn the normalized Jira issue into a **strict, validated JSON test plan**. This is the
**only** stage where an LLM is invoked (invariant I4). Structure and correctness are owned by
deterministic code; the model only drafts content.

## 2. Inputs

| Input | Type | Source |
|---|---|---|
| `issue` | dict | `tools/fetch_jira_issue.py` (SOP_fetch_issue) |
| `config` | Config | `.env` |
| `instructions` | string (optional) | CLI flag / UI textarea |

## 3. Prompt Assembly (`build_prompt.py`)

Returns `(system_prompt, user_prompt)`.

**System prompt must enforce:**
1. Role: Senior QA Engineer / test-design expert.
2. **Ground everything in the provided issue data** — the anti-hallucination policy.
3. Never invent requirements, fields, APIs, URLs, UI elements, or business rules.
4. When information is absent, say `"Not specified in the Jira issue."` — do not guess.
5. **Apply ISTQB techniques** explicitly: boundary value analysis, equivalence partitioning,
   decision table, state transition, error guessing. Label each case.
6. Provide `traceability` on every case.
7. Include at least one **non-Positive** case (negative or edge).
8. Output **JSON only** — no prose, no markdown fences.

**User prompt must contain:**
- The normalized issue rendered as labelled text (or JSON) — **evidence only**.
- A **grounding note** selected from the three-state `issue.grounding` flag (see SOP_fetch_issue §7).
  The note must never claim a source that is not present:

| `grounding` | Note the prompt must carry |
|---|---|
| `acceptance_criteria` | AC is the primary source of expected results; description is supporting context. |
| `description_only` | This project has **no** Acceptance Criteria field. The **description** is the primary source, summary secondary. Include a risk stating the plan is based solely on the ticket description and must be reviewed against the real requirements. |
| `low` | The issue has **no description and no acceptance criteria** — only a summary. Ground strictly on the summary, produce only a small number of high-level cases, mark unknowns as `"Not specified in the Jira issue."`, and include a prominent risk stating that grounding is minimal and the plan is near-speculative. |

- The required JSON shape (mirrors `schemas/test_plan.schema.json`).
- Any user `instructions`.
- **Credentials are never included in any prompt.**

## 4. LLM Call (`generate_test_plan.py`)

```
POST https://api.groq.com/openai/v1/chat/completions
Authorization: Bearer $GROQ_API_KEY
Content-Type: application/json

{
  "model": "<GROQ_MODEL>",
  "temperature": 0.2,
  "response_format": {"type": "json_object"},
  "messages": [ {"role":"system", ...}, {"role":"user", ...} ]
}
```

- Implemented with **`requests`** (the project does not depend on the `openai` SDK).
- `temperature` ≤ **0.2** — determinism rule (`LLM.md` §2).
- `response_format=json_object` reduces but does **not** guarantee valid output — validation is mandatory.

**Error mapping:** 401 → `LLMAuthError`; 429 → `LLMRateLimitError`; 400/404 with model
message → `LLMModelNotFoundError`; other/network → `LLMUnavailableError`; empty content →
`LLMResponseError`.

## 5. Validation (`validate_plan.py`)

**Two-phase validation:**

**Phase A — JSON Schema** (`schemas/test_plan.schema.json`, applied via `jsonschema`):
- Exact top-level keys; required fields; types; enums; `minItems` on arrays.

**Phase B — Deterministic checks the schema cannot express:**
- **Renumber** `id` values to `TC-001`, `TC-002`, … in order — the model's IDs are never trusted.
- **Coverage rule:** at least one case where `type != "Positive"`.
- Non-empty `traceability` on every case.

**On failure:** one retry, appending a corrective message naming the exact violation.
On a second failure → `PlanValidationError` (friendly message; no raw dump).

## 6. Output Contract

A validated dict matching `LLM.md` §1.3, with IDs renumbered and the JSON additionally written
to `.tmp/<KEY>_plan.json` as the intermediate artefact (invariant I3).

## 7. Edge Cases

| Case | Behaviour |
|---|---|
| Model wraps JSON in ``` fences | Strip fences before parsing |
| Model returns prose around JSON | Extract outermost `{...}` then parse |
| Non-JSON | Retry once, then `PlanValidationError` |
| Missing top-level key | Schema error → retry → fail |
| Invalid enum value | Schema error → retry → fail |
| All cases `Positive` | Coverage rule error → retry → fail |
| Empty `test_cases` | Schema error → retry → fail |
| Rate limit | `LLMRateLimitError` — no tight retry loop |
| Description-only grounding | Permitted; `risks` should note reduced grounding |

## 8. Testability

`build_prompt` is pure and testable. `generate` accepts an injectable HTTP session.
`validate_plan` is pure — feed it fixtures (valid, missing key, bad enum, no-negative case).
