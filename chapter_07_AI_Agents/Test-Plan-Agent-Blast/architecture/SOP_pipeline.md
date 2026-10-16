# SOP — Pipeline (End-to-End Navigation)

**Layer:** 1 (Architecture) + 2 (Navigation) · **Files:** `tools/pipeline.py`, `tools/run.py`, `app.py` · **Version:** 1.0 (2026-09-11)

---

## 1. Goal

Define the canonical end-to-end sequence and the single shared engine used by **both** entry
points. Invariant **I9**: the CLI and the UI must call the same pipeline module — logic is
never duplicated in `app.py`.

## 2. Entry Points

| Entry point | Command | Role |
|---|---|---|
| CLI | `py tools/run.py <JIRA-ID> [--instructions "..."]` | Headless, scriptable |
| UI | `py -m streamlit run app.py` | Interactive |

Both delegate to `tools/pipeline.generate_test_plan(...)`.

## 3. Canonical Sequence

```
        ┌──────────────────────────────────────────────┐
        │ 0. load_config()      tools/config.py        │  .env → Config, validate
        └───────────────────────┬──────────────────────┘
                                │
        ┌───────────────────────▼──────────────────────┐
        │ 1. fetch_issue()      SOP_fetch_issue        │  DETERMINISTIC
        └───────────────────────┬──────────────────────┘
                                │  normalized issue dict
        ┌───────────────────────▼──────────────────────┐
        │ 2. build_prompt()     SOP_generate_plan      │  DETERMINISTIC
        └───────────────────────┬──────────────────────┘
                                │  (system, user)
        ┌───────────────────────▼──────────────────────┐
        │ 3. generate()         SOP_generate_plan      │  ★ LLM (only here)
        └───────────────────────┬──────────────────────┘
                                │  raw JSON text
        ┌───────────────────────▼──────────────────────┐
        │ 4. validate_plan()    SOP_generate_plan      │  DETERMINISTIC (jsonschema)
        └───────────────────────┬──────────────────────┘
                                │  validated dict → .tmp/<KEY>_plan.json
        ┌───────────────────────▼──────────────────────┐
        │ 5. render_markdown()  SOP_render_markdown    │  DETERMINISTIC
        └───────────────────────┬──────────────────────┘
                                │
                        outputs/<KEY>_test_plan.md
```

**Single responsibility per step.** The pipeline orchestrates; it performs no business logic itself.

## 4. Return Contract

`generate_test_plan()` returns a result object:

```
PipelineResult:
    issue         : dict     # normalized issue
    plan          : dict     # validated plan
    markdown      : str      # rendered output
    output_path   : Path     # outputs/<KEY>_test_plan.md
    model         : str      # GROQ_MODEL actually used
```

## 5. Error Routing

All domain errors derive from `AppError` (`tools/errors.py`) and carry a **user-safe message**
(no secrets, no stack traces, no raw response bodies).

| Stage | Error | Message (friendly) |
|---|---|---|
| 0 | `ConfigError` | "Configuration is incomplete. Missing: …" |
| 1 | `JiraInvalidKeyError` | "'XYZ' is not a valid Jira issue key. Expected format like PROJ-123." |
| 1 | `JiraAuthError` | "Jira authentication failed. Check your Jira email and API token." |
| 1 | `JiraPermissionError` | "You do not have permission to view this Jira issue." |
| 1 | `JiraNotFoundError` | "The Jira issue was not found." |
| 1 | `JiraTimeoutError` | "Jira did not respond in time. Check your connection and try again." |
| 1 | `JiraNetworkError` | "Could not connect to Jira. Check the Jira URL and your network connection." |
| 3 | `LLMAuthError` | "Groq authentication failed. Check your Groq API key." |
| 3 | `LLMRateLimitError` | "Groq rate limit exceeded. Please try again shortly." |
| 3 | `LLMModelNotFoundError` | "Model '<m>' is not available on Groq." |
| 3 | `LLMUnavailableError` | "Groq is not reachable. Check your network connection." |
| 3/4 | `PlanValidationError` | "The model returned an invalid test plan after a retry. Please try again." |

- CLI: catch `AppError` → print `[ERROR] <message>`, exit code **1**.
- UI: catch `AppError` → `st.error(<message>)` — never a traceback.
- Unexpected exceptions: log internally, show a generic message.

## 6. File & Directory Rules

| Path | Purpose | Committed? |
|---|---|---|
| `.env` | secrets | ❌ never (git-ignored) |
| `.env.example` | config contract | ✅ |
| `.tmp/` | intermediates (`<KEY>_plan.json`, raw LLM text) | ❌ git-ignored |
| `outputs/` | final Markdown deliverables | ✅ |
| `schemas/` | `test_plan.schema.json` | ✅ |
| `architecture/` | SOPs | ✅ |
| `tools/` | deterministic scripts | ✅ |
| `app.py` | Streamlit UI | ✅ |

## 7. Idempotency & Re-runs

Same key + same model + same prompt ⇒ materially the same plan. Re-running overwrites
`outputs/<KEY>_test_plan.md` and `.tmp/<KEY>_plan.json`. No append/build-up.

## 8. What the Pipeline Must NOT Do

1. Duplicate logic in `app.py` (I9).
2. Log or display credentials.
3. Call the LLM more than once per stage (retry for validation counts as the same stage).
4. Write anywhere except `.tmp/` and `outputs/`.
5. Proceed past a broken link — fail fast with a friendly message.

## 9. UI Requirements (`app.py`)

- A form: Jira ID input, optional instructions, Generate button.
- Progress feedback per stage.
- Render the result: metadata, the **AI-review banner**, the full Markdown preview.
- A download button for the `.md`, and display the `outputs/` path.
- No pipeline logic — imports `tools/pipeline.py` only.
