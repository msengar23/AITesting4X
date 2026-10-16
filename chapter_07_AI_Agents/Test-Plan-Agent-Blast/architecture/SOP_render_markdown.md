# SOP — Render Markdown

**Layer:** 1 (Architecture) · **Tool:** `tools/render_markdown.py` · **Version:** 1.0 (2026-09-11)

---

## 1. Goal

Render the validated test-plan JSON into a clean, human-readable Markdown file at
`outputs/<JIRA-ID>_test_plan.md`. **Pure templating — no LLM.**

## 2. Inputs

| Input | Type | Source |
|---|---|---|
| `issue` | dict | SOP_fetch_issue |
| `plan` | validated dict | SOP_generate_plan |
| `model` | string (optional) | the Groq model actually used, shown in metadata |
| `issue_url` | string (optional) | deep link to the Jira issue, rendered when supplied |
| `out_dir` | Path | default `outputs/` |

## 3. Template Mapping

| Markdown section | Source |
|---|---|
| Title | `plan.title` (fallback: `Test Plan — <key>: <summary>`), em dash |
| **AI Review Banner** | static — must always appear |
| **At a Glance** | **computed by code** — see §3a |
| Metadata table | `issue.key`, `issue.issuetype`, `issue.priority`, `issue.status`, components, `model`, generated timestamp |
| 1. Objective | `plan.objective` |
| 2. Preconditions | `plan.preconditions[]` (bullet list) |
| 3. Test Data | `plan.test_data[]` (bullet list) |
| 4. Test Cases | summary table + per-case blocks — see §4 |
| 5. Coverage Summary | **computed by code** (see §5) |
| 6. Risks | `plan.risks[]` |
| 7. Out of Scope | `plan.out_of_scope[]` |

Empty optional arrays render as `_None identified._` rather than an empty heading.

### 3a. At a Glance — plain-language summary block *(added Phase 4)*

Rendered immediately after the banner, before the metadata table. **Fully computed by code** —
never model-authored. Provides a non-technical reader a one-screen overview:

| Row | Computation |
|---|---|
| Test cases | total, plus positive/negative split |
| Focus areas | unique `traceability` values, in first-seen order (capped at 4, then "+N more") |
| Techniques | the distinct `test_design_technique` values applied |
| Grounding | maps the three-state `issue.grounding` flag: `acceptance_criteria` → "Acceptance criteria + description"; `description_only` → "Description only — no Acceptance Criteria field…"; `low` → "⚠️ Low — no description or acceptance criteria…" (see SOP_fetch_issue §7) |
| Review status | static — "⚠️ Draft — human review required" |

### 3b. Test-case summary table *(added Phase 4)*

Section 4 opens with a scannable table before the detailed blocks:

```markdown
| ID | Test case | Priority | Type | Technique |
|---|---|---|---|---|
| TC-001 | <title> | High | Positive | Equivalence Partitioning |
```

Cells are pipe-escaped. The detailed blocks follow underneath.

## 4. Test Case Block

```markdown
### TC-001 — <title>
- **Priority:** High
- **Type:** Negative
- **Technique:** Equivalence Partitioning
- **Traceability:** <traceability>
- **Steps:**
  1. <step>
- **Expected Result:** <expected_result>
```

Steps are already numbered by the validator/model; render as an ordered list, avoiding
double numbering (strip a leading `N. ` if present before writing).

## 5. Coverage Summary — deterministic ledger (invariant I5, AD3)

**Computed from the validated array by code. The model never writes this section.**

```
total          = len(test_cases)
by_priority    = Counter(c["priority"])
by_type        = Counter(c["type"])
by_technique   = Counter(c["test_design_technique"])
```

Rendered as a table:

| Dimension | Breakdown |
|---|---|
| Total cases | N |
| By priority | High: x · Medium: y · Low: z |
| By type | ... |
| By technique | ... |

Counters include **every** enum value in a stable order (zero-count values may be omitted
from the display but the ordering must be deterministic).

## 6. Output

- Write UTF-8 to `outputs/<KEY>_test_plan.md`.
- Create `outputs/` if missing.
- Overwrite an existing file for the same key (idempotent re-runs).
- Return the rendered string so the UI can preview it without re-reading the file.

## 7. Edge Cases

| Case | Behaviour |
|---|---|
| `line breaks` inside a field | Collapse newlines; keep the table/list intact |
| Pipe `\|` inside a table cell | Escape as `\\\|` |
| Empty `preconditions` / `test_data` / `risks` | Render `_None identified._` |
| Very long step text | Wrap naturally; do not truncate (it's a deliverable) |
| `outputs/` missing | Create it |
| Windows path separators | Use `pathlib.Path` throughout |

## 8. Testability

Pure function: `(issue, plan) -> markdown str`. The file-writing wrapper is separate, so the
renderer can be unit-tested without touching disk.
