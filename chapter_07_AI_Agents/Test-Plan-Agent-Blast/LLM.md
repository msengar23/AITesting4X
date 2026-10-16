# 🧠 LLM.md — Project Constitution

> **This is the highest-authority document in the project.**
> It defines the **Data Schemas**, **Behavioral Rules**, and **Architectural Invariants**.
> If code and this document disagree, **this document wins** — fix the code.
> (BLAST.md calls this file `gemini.md`; the project owner renamed it `LLM.md`.)

**Project:** Test Plan Agent · **North Star:** Jira ID → Markdown Test Plan
**Backend:** Groq `openai/gpt-oss-120b` · **Delivery:** `outputs/<KEY>_test_plan.md`
**Schema status:** 🔒 **LOCKED** (BLAST Phase 1 Blueprint approved, 2026-09-11)

---

## Phase 1 — Discovery Outcomes (approved)

The Blueprint's five mandated questions, answered and locked:

| # | Question | Answer |
|---|---|---|
| 1 | **North Star** | From a single Jira ID, produce a complete Markdown Test Plan — **full plan structure plus a detailed test-case table**. |
| 2 | **Integrations** | Jira Cloud REST API v3 (**read-only**) + Groq `openai/gpt-oss-120b`. Credentials ready. |
| 3 | **Source of Truth** | The Jira issue fields: `summary`, `description` (ADF), `status`, `priority`, `issuetype`, `labels`, `components`, `project`, `reporter`, `assignee`, `created`, `updated`, + the discovered Acceptance Criteria custom field. |
| 4 | **Delivery Payload** | One Markdown file at `outputs/<JIRA-ID>_test_plan.md`. **Amended (Phase 2):** delivered via a **CLI pipeline *and* a Streamlit UI**; still no Jira write-back. **Clarified:** the *agent* performs no Jira writes. Attaching a finished plan to an issue is a **manual, one-off action** performed outside the pipeline, not a feature of the tool. |
| 5 | **Behavioral Rules** | Strict anti-hallucination; **ISTQB techniques mandatory**; deterministic code owns structure and the coverage ledger; output is a **draft for human review**. |

---

## 0. Core Principle — Separate the Probabilistic from the Deterministic

> *"LLMs are probabilistic; business logic must be deterministic."* — BLAST.md

| Concern | Owner | Rule |
|---|---|---|
| Fetching, validating, normalizing Jira data | **Code** | Deterministic. Never delegated to the LLM. |
| Deciding *what* the plan contains | **LLM** | Drafts content from the issue only. |
| Validating the LLM's structure | **Code** | Schema validation. LLM output is untrusted input. |
| Rendering Markdown | **Code** | Pure templating — no LLM. |

**Boundary rule:** the LLM is called in **exactly one place** in the pipeline (drafting the test plan JSON). Everything upstream and downstream is deterministic code.

---

## 1. Data Schemas (Data-First Rule)

> Coding begins only once these shapes are confirmed. All schemas are JSON.

### 1.1 Input Schema — the only user input

```json
{
  "jira_id": "PROJ-123"
}
```

**Validation:**
- `jira_id` is required.
- Must match `^[A-Z][A-Z0-9]*-\d+$`.
- Invalid input fails **before** any network call, with a friendly message.

### 1.2 Normalized Issue Schema — deterministic output of the Jira tool

This is the **only** thing sent to the LLM (as JSON). Only fields present on the
issue are included; absent fields are omitted, not nulled.

```json
{
  "key": "PROJ-123",
  "summary": "Short issue title",
  "description": "Plain text (ADF flattened by code)",
  "status": "In Progress",
  "priority": "High",
  "issuetype": "Story",
  "labels": ["regression", "api"],
  "components": ["Payments"],
  "project": "Payments Platform",
  "reporter": "Jane Doe",
  "assignee": "John Smith",
  "created": "2026-08-01T09:14:00.000+0000",
  "updated": "2026-09-09T11:02:00.000+0000",
  "acceptance_criteria": "Plain text (from the discovered custom field, if present)"
}
```

**Field rules:**
| Field | Type | Notes |
|---|---|---|
| `key` | string | Always present |
| `summary` | string | Always present |
| `description` | string | **ADF flattened to plain text by code** |
| `status`, `priority`, `issuetype`, `project` | string | Extract `.name` |
| `reporter`, `assignee` | string | Extract `.displayName` |
| `labels` | string[] | Array of strings as-is |
| `components` | string[] | Map objects → `.name` |
| `created`, `updated` | string | ISO-8601 as returned by Jira |
| `acceptance_criteria` | string | Custom field discovered at runtime; omit when absent |

> **⚠️ Environment note (verified 2026-09-11, Phase 2 Link):** the target site
> `vandysengar.atlassian.net` has **no Acceptance Criteria / DoD custom field**.
> `acceptance_criteria` therefore stays a *conditional* key that will be absent in practice.
> **`description` (ADF-flattened) is the primary grounding source**, with `summary` as
> secondary context. When AC is absent, the plan's `risks` must state that grounding is
> description-only. See `findings.md` §8.3.

### 1.3 LLM Output Contract — strict JSON test plan

The model **must** return exactly this shape. No prose, no markdown fences.

```json
{
  "title": "Test Plan — PROJ-123: <summary>",
  "objective": "One paragraph stating what this plan verifies.",
  "preconditions": ["Environment/access/data state required before testing"],
  "test_data": ["Concrete input values or data set required"],
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Short imperative title",
      "priority": "High | Medium | Low",
      "type": "Positive | Negative | Edge | Boundary | Regression | Integration",
      "test_design_technique": "Boundary Value Analysis | Equivalence Partitioning | Decision Table | State Transition | Error Guessing | None",
      "traceability": "The acceptance-criterion or requirement fragment this case derives from",
      "steps": [
        "1. Do this",
        "2. Then this"
      ],
      "expected_result": "Single, observable, verifiable outcome"
    }
  ],
  "risks": ["Area of uncertainty or risk"],
  "out_of_scope": ["Explicitly excluded behaviour"]
}
```

**Validation rules (enforced before rendering):**

> **Validation mechanism (amended Phase 2, supersedes the earlier hand-rolled decision):**
> validation is declarative via the **`jsonschema`** library against a machine-readable schema at
> `schemas/test_plan.schema.json`. The rules below define that schema. Code applies the schema,
> then performs the ordering/coverage checks the schema cannot express.

- Top-level keys exactly: `title, objective, preconditions, test_data, test_cases, risks, out_of_scope`.
- `test_cases` is a non-empty array.
- Every test case has `id, title, priority, type, test_design_technique, traceability, steps, expected_result`; `steps` is a non-empty array of strings.
- `priority` ∈ {High, Medium, Low}.
- `type` ∈ {Positive, Negative, Edge, Boundary, Regression, Integration}.
- `test_design_technique` ∈ the enum above (ISTQB vocabulary — see `findings.md` §6).
- `traceability` is a non-empty string on every case.
- The collection must include at least one non-`Positive` case (negative or edge) — a plan with only happy-path cases is rejected.
- `id` values are unique and sequential (`TC-001`, `TC-002`, …) — **renumbered by code**, not trusted from the model.
- On failure: one retry with a corrective message, then fail loudly with a friendly error.

### 1.4 Delivery Schema — Markdown template

Deterministic mapping from §1.3 → `outputs/<KEY>_test_plan.md`.

```markdown
# Test Plan — PROJ-123: <summary>

| Field | Value |
|---|---|
| Jira Issue | [PROJ-123](<issue-url>) |
| Type | Story |
| Priority | High |
| Status | In Progress |
| Generated | <YYYY-MM-DD HH:MM> |

## 1. Objective
<objective>

## 2. Preconditions
- <precondition>

## 3. Test Data
- <test data item>

## 4. Test Cases

### TC-001 — <title>
- **Priority:** High
- **Type:** Positive
- **Technique:** Boundary Value Analysis
- **Traceability:** <acceptance criterion / requirement fragment>
- **Steps:**
  1. <step>
- **Expected Result:** <expected_result>

## 5. Coverage Summary
<!-- COMPUTED BY CODE — never authored by the model -->
| Dimension | Breakdown |
|---|---|
| Total cases | 12 |
| By priority | High: 5 · Medium: 5 · Low: 2 |
| By type | Positive: 6 · Negative: 3 · Edge: 2 · Boundary: 1 |
| By technique | Boundary Value Analysis: 3 · Equivalence Partitioning: 4 · Error Guessing: 2 · None: 3 |

## 6. Risks
- <risk>

## 7. Out of Scope
- <item>
```

> **Coverage Summary is a deterministic ledger.** It is computed by `tools/render_markdown.py`
> from the validated test-case array — the model never writes it and cannot inflate it.

---

## 2. Behavioral Rules

### The LLM Must
1. Draft test cases **only** from the normalized issue JSON.
2. Treat Acceptance Criteria as the primary source of expected results; treat the description as supporting context.
3. **Apply ISTQB test-design techniques deliberately** — at minimum boundary value analysis and equivalence partitioning where the data permits — and label each case's `test_design_technique`.
4. Cover positive, negative, boundary, and edge cases; include regression cases when `labels`/`components` imply a stable feature.
5. Provide a non-empty `traceability` value on every case, naming the requirement or acceptance criterion it derives from.
6. Use unambiguous, observable expected results.
7. Return **JSON only**, exactly matching §1.3.

### The LLM Must NOT
1. **Invent requirements** not present in the issue.
2. Assume UI specifics, endpoints, or field names that aren't in the data.
3. Include commentary, apologies, or markdown fences in its response.
4. Be trusted as an authority — its output is validated by code.

### Ambiguity Handling
- When the issue is thin, generate fewer, well-grounded cases rather than padding.
- Surface gaps in `risks` and `out_of_scope` rather than guessing.
- Never fabricate acceptance criteria. If the custom field is absent, note the limitation in `risks`.

### Determinism Rules
- `temperature ≤ 0.2` for all generation calls.
- Prompts are assembled deterministically by `tools/build_prompt.py` — no randomness, no hidden context.
- Test-case IDs are assigned by code, never by the model.
- Same issue + same model + same prompt ⇒ materially the same plan.

### Human Review (non-negotiable)
- The generated plan is a **first draft**, not a finished artefact and not a replacement for QA judgement.
- Every rendered plan must carry a banner stating it was AI-generated and requires review.
- Reviewers are expected to add cases the model missed (especially domain and business-critical scenarios).

---

## 3. Architectural Invariants (3-Layer Model)

### Layer 1 — Architecture (`architecture/`)
- Technical SOPs in Markdown: goals, inputs, tool logic, edge cases.
- **Golden Rule:** if logic changes, update the SOP *before* the code.
- One SOP per tool.

### Layer 2 — Navigation (Decision Making)
- The reasoning layer. Routes data between SOPs and tools in the correct order.
- Does **not** perform complex work itself — it orchestrates.
- Owns the pipeline sequence and retry decisions.

### Layer 3 — Tools (`tools/`)
- Deterministic Python scripts. **Atomic and testable.**
- One responsibility per script.
- Secrets/tokens come **only** from `.env`.
- All intermediate file operations use `.tmp/`.
- Every network call has an explicit timeout and mapped error.

### Presentation Layer — UI (`app.py`, Streamlit) *(added Phase 2)*
- A **thin shell** over the same pipeline. Two entry points, one engine:
  `tools/run.py` (CLI) and `app.py` (Streamlit).
- **No business logic in the UI** — it loads config, calls the pipeline, renders results.
- The UI must surface the same friendly errors as the CLI, plus the human-review banner.
- The CLI must work standalone (headless) with no Streamlit import.

### Schemas (`schemas/`)
- `schemas/test_plan.schema.json` — machine-readable JSON Schema for §1.3, applied via `jsonschema`.

### Invariants
| # | Invariant |
|---|---|
| I1 | No `tools/` script is written until the Blueprint is approved in `task_plan.md`. |
| I2 | Secrets live only in `.env`; `.env` is never committed; `.env.example` is the contract. |
| I3 | Intermediates go to `.tmp/`; final deliverables go to `outputs/`. |
| I4 | The LLM is invoked in exactly one stage; all other stages are deterministic. |
| I5 | LLM output is validated against §1.3 before it is rendered. |
| I6 | `description` is always ADF-flattened by code before reaching the LLM. |
| I7 | Custom field IDs are discovered at runtime and cached in `.env`, never hardcoded. |
| I8 | Every external call has a timeout (Jira 15s; Groq explicit) and a friendly error. |
| I9 | The CLI and the UI call the **same** pipeline module — logic is never duplicated in `app.py`. |
| I10 | Validation uses `schemas/test_plan.schema.json` via `jsonschema`; hand-rolled checks only for what JSON Schema cannot express (ID sequencing, coverage ratio). |

---

## 4. Error Taxonomy

| Condition | User-facing message |
|---|---|
| Invalid key format | "'XYZ' is not a valid Jira issue key. Expected format like PROJ-123." |
| 401 | "Jira authentication failed. Check your Jira email and API token." |
| 403 | "You do not have permission to view this Jira issue." |
| 404 | "The Jira issue was not found." |
| Timeout | "Jira did not respond in time. Check your connection and try again." |
| Network | "Could not connect to Jira. Check the Jira URL and your network connection." |
| Groq auth | "Groq authentication failed. Check your Groq API key." |
| Groq rate limit | "Groq rate limit exceeded. Please try again shortly." |
| Malformed LLM JSON | "The model returned an invalid test plan. Retrying once…" |

**Never** surface raw stack traces, response bodies, or credentials.

---

## 5. Governance

- This document is versioned with the code. Any schema change is a **breaking change** and must be recorded in `progress.md`.
- `task_plan.md` owns *what/when*; `findings.md` owns *what we learned*; `progress.md` owns *what happened*; **`LLM.md` owns *the rules*.**
- If a rule here blocks progress, amend this document first, log the change in `progress.md`, then implement.
