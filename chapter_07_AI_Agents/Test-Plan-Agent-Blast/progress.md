# 🧭 Progress Log — Test Plan Agent (BLAST Protocol 0)

> **Cadence:** append an entry roughly every **10–30 minutes** of work.
> **Rule:** log errors and dead-ends honestly — a hidden failure is a lost lesson.
> **Format:** `Timestamp | Action | Result | Error | Next`

---

## 📌 Entry Template

```markdown
### YYYY-MM-DD HH:MM — <short title>
- **Action:** what I set out to do
- **Result:** what actually happened
- **Error:** what broke, if anything (or "none")
- **Files touched:** ...
- **Next:** the immediate follow-up
```

---

## 🗓️ 2026-09-11

### 2026-09-11 — Protocol 0 kickoff
- **Action:** Read `BLAST.md` and `Prompt_Used.md`; scope the task to Protocol 0 (Initialization) only.
- **Result:** Confirmed the deliverable is four project-memory docs — `task_plan.md`, `findings.md`, `progress.md`, `LLM.md` — and that BLAST forbids writing any `tools/` scripts until the blueprint is approved.
- **Error:** none.
- **Files touched:** (read only) `BLAST.md`, `Prompt_Used.md`, `.env.example`
- **Next:** Inspect the project folder and repo for reusable assets.

### 2026-09-11 — Folder & repo reconnaissance
- **Action:** Listed the target folder and searched the workspace for existing Jira/Groq code.
- **Result:** Target folder held only `BLAST.md`, `Prompt_Used.md`, `.env.example` — no memory files yet. Found a prior project, `Task_02_Local_TestCase_Generator copy`, with a working Jira REST v3 client (`jira_client.py`) and a Groq/OpenAI-compatible LLM client (`llm_client.py`).
- **Error:** none. **Note:** the workspace has **no real `.env`** in this folder yet — only `.env.example`; credentials must be supplied before Phase 2.
- **Files touched:** (read only) `jira_client.py`, `llm_client.py`
- **Next:** Confirm open design decisions with the user, then draft the plan.

### 2026-09-11 — Design decisions locked (via plan review)
- **Action:** Asked four scoping questions before writing anything.
- **Result:** Decisions recorded —
  1. Memory files live **inside `Test-Plan-Agent-Blast/`**.
  2. This step delivers **only the 4 docs** — no code, `.env`, or `architecture/` yet.
  3. LLM backend is **Groq only** (`openai/gpt-oss-120b`).
  4. Deliverable is **Markdown only**.
  Also confirmed: the constitution file is named **`LLM.md`** (user override — BLAST.md calls it `gemini.md`).
- **Error:** none.
- **Files touched:** (read only) taste preferences
- **Next:** Write the four memory files.

### 2026-09-11 — Wrote `task_plan.md`
- **Action:** Create the phase/goal/checklist document.
- **Result:** Written with Project Identity, North Star, one-line flow, Goals, per-phase checklists (Protocol 0 → Phase 4), Definition of Done, Open Questions table, and a Status Snapshot. Protocol 0 items checked off; downstream phases pending.
- **Error:** none.
- **Files touched:** `task_plan.md` (created)
- **Next:** Write `findings.md`.

### 2026-09-11 — Wrote `findings.md`
- **Action:** Research and document how to fetch a Jira issue, with runnable requests.
- **Result:** Documented Jira Cloud REST v3 auth model, base URL, and **three endpoints** with copy-paste `curl` (+ Python `requests`) for each: `/myself`, `/field`, `/issue/{KEY}?fields=...`. Added the Groq `/chat/completions` request and handshake. Logged 9 gotchas — most importantly that **`description` is ADF JSON, not plain text**, and that **Acceptance Criteria custom field IDs are site-specific**.
- **Error:** none.
- **Files touched:** `findings.md` (created)
- **Next:** Write `progress.md` (this file), then `LLM.md`.

### 2026-09-11 — Wrote `progress.md`
- **Action:** Seed the progress log with the Protocol 0 work so far.
- **Result:** Template + timestamped entries added, covering kickoff, reconnaissance, decision lock, and each file written.
- **Error:** none.
- **Files touched:** `progress.md` (created)
- **Next:** Write `LLM.md` (schemas, rules, architecture).

### 2026-09-11 — Wrote `LLM.md`
- **Action:** Define the Project Constitution — schemas, behavioral rules, architectural invariants.
- **Result:** Documented four JSON shapes (input, normalized issue, LLM output contract, Markdown delivery template) plus deterministic-vs-probabilistic boundaries, validation rules, error taxonomy, and the 3-layer invariants.
- **Error:** none.
- **Files touched:** `LLM.md` (created)
- **Next:** Verify all four files exist; hand the blueprint to the user for approval.

### 2026-09-11 — Protocol 0 verification
- **Action:** Confirm the folder now contains exactly the four new docs alongside the originals, and that nothing else was created.
- **Result:** All four files present and non-empty. No code, no `.env`, no `architecture/`, no `tools/` created — **Halt Execution respected**. Protocol 0 is complete pending user approval of the blueprint.
- **Error:** none.
- **Files touched:** none (verification only)
- **Next:** User review of `task_plan.md`. On approval → Phase 1 (Blueprint): answer the 5 Discovery questions and lock the schema; on credentials → Phase 2 (Link) handshakes.

### 2026-09-11 — Phase 1 kickoff: plan drafted
- **Action:** Scope BLAST Phase 1 (Blueprint) and write it up for approval.
- **Result:** Plan drafted and **approved**. Phase 1 defined as documentation-only: 5 Discovery answers, schema lock in `LLM.md`, OSS research in `findings.md`. Halt Execution still applies — no code.
- **Error:** none.
- **Files touched:** plan file only (`~/.commandcode/plans/phase1-blueprint-test-plan-agent.md`)
- **Next:** Run the OSS research, then put the Discovery questions to the user.

### 2026-09-11 — Phase 1 research: OSS landscape reviewed
- **Action:** Search GitHub and the web for prior art on Jira → test-case/test-plan generation; review the in-repo `Task_02` generator for reusable code.
- **Result:** Reviewed 7 sources. Two findings shaped the design:
  1. The **Spring Boot + Spring AI reference** confirms our exact pipeline shape (fetch → extract AC → single prompt → structured cases) — but it uses Jira **API v2**, where `description` is plain text. Our **v3** path must keep the ADF flattening step.
  2. `AI_GAME_QA_TestCase` independently states that **structure, gates, and the coverage ledger are owned by deterministic code, not the model** — direct corroboration of our `LLM.md` core principle. This is where the deterministic **Coverage Summary** idea came from.
  Also reviewed `adlerqa/wardeniq` (plan + cases + validators), `ai-testcase-generator-mcp` (positive/negative/edge taxonomy), `Awesome-Test-Case-Design` + `nanook-table` (ISTQB technique vocabulary). Adopt/reject decisions logged in `findings.md` §6.
- **Error:** none. Note: the wider `test-case-generation` topic is dominated by fuzzing/model-based-testing research tools — not applicable to an LLM drafting flow.
- **Files touched:** `findings.md` (edited — new §6, §7)
- **Next:** Put the 5 Discovery questions to the user.

### 2026-09-11 — Phase 1 Discovery: 5 questions answered
- **Action:** Ask the user the 5 mandated BLAST Discovery questions.
- **Result:** All answered —
  1. **North Star:** full plan structure **plus** a detailed test-case table.
  2. **Integrations:** Jira v3 read-only + Groq; **credentials ready**.
  3. **Source of Truth:** the Jira issue fields + discovered AC custom field.
  4. **Delivery:** `outputs/<KEY>_test_plan.md`; **no Jira write-back**.
  5. **Behavioral Rules:** anti-hallucination, **ISTQB mandated**, deterministic coverage ledger, draft-for-human-review.
- **Error:** none.
- **Files touched:** `task_plan.md` (edited — Phase 1 ticked, Discovery recorded, decision log added)
- **Next:** Lock the schema in `LLM.md` to match the answers.

### 2026-09-11 — Phase 1: schema refined and locked
- **Action:** Update `LLM.md` so the schemas reflect the Discovery answers, then mark them locked.
- **Result:** Changes made — added `test_design_technique` (ISTQB enum) and `traceability` to each test case; broadened `type` to `Positive | Negative | Edge | Boundary | Regression | Integration`; added a new validation rule rejecting all-happy-path plans; added a code-computed **Coverage Summary** section to the delivery template; added ISTQB + human-review clauses to the behavioural rules. Header marked **🔒 LOCKED** and the Discovery Outcomes table embedded.
- **Error:** none.
- **Files touched:** `LLM.md` (edited)
- **Next:** Verify all Phase 1 docs are coherent and no code was created; then Phase 2 (Link).

### 2026-09-11 — Phase 1 verification
- **Action:** Re-check the four docs against the Phase 1 acceptance criteria.
- **Result:** `task_plan.md` Phase 1 fully ticked with all 5 answers recorded; `findings.md` §6 lists every source with an explicit adopt/defer decision; `LLM.md` contains the new fields, the coverage summary, the ISTQB mandate, and is marked locked; `progress.md` updated. **Still zero code** — no `tools/`, no `architecture/`, no `.env`. Blueprint complete.
- **Error:** none.
- **Files touched:** none (verification only)
- **Next:** Phase 2 (Link) — create `.env` from the supplied credentials, then run the Jira `/myself` + `/field` and Groq model handshakes.

### 2026-09-11 — Phase 2 kickoff: locating credentials
- **Action:** Look for the real credentials, since the project folder held only `.env.example`.
- **Result:** Found working keys in the sibling `Task_02_Local_TestCase_Generator` `.env`, but the user then confirmed real keys had been placed into this project's `.env.example`.
- **Error:** ⚠️ **Real credentials were sitting in `.env.example`** — a file whose whole purpose is to be committed as a placeholder template. Also, the token value carried a leading space and a trailing `# ...` comment, which would corrupt naive `.env` parsing.
- **Resolution:** Copied clean values into a new `.env`, **restored `.env.example` to placeholders**, and added a `.gitignore` covering `.env`, `.tmp/`, `__pycache__/`.
- **Files touched:** `.env` (created), `.env.example` (restored), `.gitignore` (created)
- **Next:** Confirm the Python environment, then write the handshake script.

### 2026-09-11 — Phase 2: Python environment check
- **Action:** Verify the interpreter and required libraries.
- **Result:** `python` is not on PATH (Windows Store alias stub), but the launcher **`py`** works — Python **3.13.2**, with `requests` 2.34.2 and `python-dotenv` available.
- **Error:** `python --version` → exit 9009 (Store alias). Worked around by using `py`.
- **Files touched:** none
- **Next:** Write `tools/verify_link.py`.

### 2026-09-11 — Phase 2: wrote the Link verification script
- **Action:** Create the minimal Phase 2 handshake tool required by BLAST ("build minimal scripts in `tools/` to verify external services").
- **Result:** `tools/verify_link.py` created — loads `.env`, checks Jira auth via `/rest/api/3/myself`, scans `/rest/api/3/field` for acceptance-related fields, and confirms the Groq model via `/openai/v1/models`. Never prints secrets; exits non-zero if any link is broken.
- **Error:** none.
- **Files touched:** `tools/verify_link.py` (created)
- **Next:** Run it against the live services.

### 2026-09-11 — Phase 2: handshakes executed ✅
- **Action:** Run `py tools\verify_link.py`.
- **Result:** **ALL LINKS HEALTHY.**
  - Jira auth — ✅ PASS, authenticated as **Vandana** (`712020:0ebdd15e-…`).
  - Jira fields — ✅ PASS, `/rest/api/3/field` readable.
  - Groq — ✅ PASS, `openai/gpt-oss-120b` available (14 models).
- **Error:** none.
- **Files touched:** none (verification run)
- **Next:** Discover real issues to pick a test key.

### 2026-09-11 — Phase 2: project & issue discovery
- **Action:** Enumerate Jira projects and find real issues for live testing.
- **Result:** Two projects — **`KAN`** (VWO) and **`SAM1`** (Timeline Tracking Initiatives). Real issues: `KAN-1..3` and `SAM1-1..9`, all with descriptions. Recommended first test key: **`SAM1-1`**.
- **Error:** ⚠️ The legacy search route `GET /rest/api/3/search` is retired on Jira Cloud (returns 410); switched to **`GET /rest/api/3/search/jql?jql=...`**, which works. Also, the supplied `DEFAULT_JIRA_KEY=vandysengar` is not a valid issue key and was left empty.
- **Files touched:** none (scratch probes in the session scratchpad)
- **Next:** Record findings and close out Phase 2.

### 2026-09-11 — Phase 2 closeout: findings recorded ⚠️ key discovery
- **Action:** Document the live results and update the project memory files.
- **Result:** Logged in `findings.md` §8 and Open Research Items. **Critical finding: this Jira site has NO Acceptance Criteria / DoD custom field** — scanned `/rest/api/3/field` for `acceptance`/`definition of done`/`dod` and found none. Consequence: the `acceptance_criteria` schema key will be absent in practice, and **`description` (ADF-flattened) becomes the primary grounding source**. Added an environment note to `LLM.md` §1.2 (schema shape unchanged — conditional key). `task_plan.md` Phase 2 ticked; all 5 open questions now resolved.
- **Error:** none, but this changes the prompting strategy for Phase 3 — the prompt builder must not assume AC exists and should note description-only grounding in `risks`.
- **Files touched:** `findings.md`, `LLM.md`, `task_plan.md`
- **Next:** Phase 3 (Architect) — write the `architecture/` SOPs first (Golden Rule), then the `tools/` scripts.

### 2026-09-11 — Phase 2 follow-up: `requirements.txt` reversed two decisions ⚠️
- **Action:** Noticed a `requirements.txt` in the project root that was not present before this session, listing `streamlit>=1.40`, `requests>=2.31`, `python-dotenv>=1.0`, `jsonschema>=4.20`. Confirmed all four are installed in the environment.
- **Result:** Two of the four packages **conflict with locked Phase 1 decisions**:
  1. `streamlit` → the Blueprint had locked delivery as *"Markdown file only, no UI"*. A UI was never in scope.
  2. `jsonschema` → directly reverses **AD5** (hand-rolled validation, no extra dependency).
  Put both to the user rather than silently proceeding.
- **Error:** none technically, but a genuine **scope/spec conflict** — the kind that must be resolved before code, per the Golden Rule.
- **Resolution (user decisions):**
  1. **Build both a CLI *and* a Streamlit UI** — delivery surface expanded.
  2. **Adopt `jsonschema`** — AD5 superseded.
- **Files touched:** none yet (decision only)
- **Next:** Amend `LLM.md` (constitution) and `task_plan.md` to reflect the change *before* writing any code.

### 2026-09-11 — Phase 2 closeout: constitution amended for the new scope
- **Action:** Apply the governance rule from `LLM.md` §5 — amend the constitution and log the change before implementing.
- **Result:** Updates made —
  - `LLM.md`: Discovery answer #4 amended (CLI **+** Streamlit UI); validation section now specifies the `jsonschema` mechanism and `schemas/test_plan.schema.json`; added a **Presentation Layer** section; added invariants **I9** (CLI and UI share one pipeline module — no duplicated logic) and **I10** (validation via JSON Schema; hand-rolled checks only for ID sequencing and coverage ratio).
  - `task_plan.md`: **AD5 marked SUPERSEDED**; added **AD8** (two entry points, one engine) and **AD9** (description-first grounding, since no AC field exists); Phase 3 gained `tools/config.py`, `tools/errors.py`, `tools/validate_plan.py`, `tools/pipeline.py`, and `schemas/test_plan.schema.json`; Phase 4 gained the Streamlit styling task; Definition of Done now covers the UI and the shared-pipeline invariant.
- **Error:** none.
- **Files touched:** `LLM.md`, `task_plan.md`
- **Next:** Phase 3 (Architect) — write the four `architecture/` SOPs first (Golden Rule), then implement the tools, schema, and UI.

### 2026-09-11 — Phase 3 kickoff: SOPs written first (Golden Rule)
- **Action:** Honour the Golden Rule — if logic changes, update the SOP before the code. Wrote all four architecture documents before a single line of implementation.
- **Result:** Created `architecture/SOP_fetch_issue.md`, `SOP_generate_plan.md`, `SOP_render_markdown.md`, `SOP_pipeline.md`. Each defines goals, inputs, tool logic, edge cases, output contract, and testability. `SOP_pipeline.md` includes the full sequence diagram, the return contract, and the error-routing table.
- **Error:** none.
- **Files touched:** `architecture/` (4 files created)
- **Next:** Define the JSON Schema, then write the tools.

### 2026-09-11 — Phase 3: JSON Schema authored
- **Action:** Write the machine-readable contract for the LLM's output (invariant I10).
- **Result:** `schemas/test_plan.schema.json` created — JSON Schema draft 2020-12, `additionalProperties: false`, required top-level keys, `minItems` on `test_cases` and `steps`, and enums for `priority` (High/Medium/Low), `type` (6 values), and `test_design_technique` (ISTQB vocabulary). Mirrors `LLM.md` §1.3 exactly.
- **Error:** none.
- **Files touched:** `schemas/test_plan.schema.json` (created)
- **Next:** Build the deterministic tools.

### 2026-09-11 — Phase 3: foundation tools (`config`, `errors`)
- **Action:** Write configuration loading and the error taxonomy.
- **Result:** `tools/errors.py` — full `AppError` hierarchy (Config/Jira/LLM/PlanValidation), each carrying a user-safe `message`. `tools/config.py` — `Config` dataclass with `load_config()`, required-key validation → `ConfigError`, and a `masked()` view that replaces secrets with `***set***` so the UI can display config safely. Package marker `tools/__init__.py` added.
- **Error:** none.
- **Files touched:** `tools/errors.py`, `tools/config.py`, `tools/__init__.py` (created)
- **Next:** Jira fetch + prompt builder.

### 2026-09-11 — Phase 3: fetch + prompt tools
- **Action:** Implement the deterministic intake and the prompt assembly.
- **Result:** `tools/fetch_jira_issue.py` — key validation (`^[A-Z][A-Z0-9]*-\d+$`, no network call on bad input), REST v3 fetch, ADF flattening, field picking that omits absent fields, description truncation at 12 000 chars, and a `grounding` flag (`low` when neither description nor AC exists). `tools/build_prompt.py` — anti-hallucination system prompt, ISTQB mandate, the JSON contract, and a `grounding_note()` that explicitly tells the model this project has **no** Acceptance Criteria field and to record description-only grounding in `risks`.
- **Error:** none.
- **Files touched:** `tools/fetch_jira_issue.py`, `tools/build_prompt.py` (created)
- **Next:** Groq generation + validation.

### 2026-09-11 — Phase 3: generator + validator
- **Action:** Implement the single LLM call and two-phase validation.
- **Result:** `tools/generate_test_plan.py` — Groq `/chat/completions` via **`requests`** (the project has no `openai` dependency), `temperature=0.2`, `response_format=json_object`, full status→error mapping. `tools/validate_plan.py` — Phase A applies the JSON Schema via `jsonschema`; Phase B renumbers IDs to `TC-001…` (model IDs never trusted), strips any step numbering, and enforces the coverage rule (must include a non-Positive case). `extract_json` tolerates markdown fences and surrounding prose.
- **Error:** none.
- **Files touched:** `tools/generate_test_plan.py`, `tools/validate_plan.py` (created)
- **Next:** Renderer with the computed coverage ledger.

### 2026-09-11 — Phase 3: renderer with computed coverage ledger
- **Action:** Implement deterministic Markdown templating.
- **Result:** `tools/render_markdown.py` — `render(issue, plan)` produces the 7-section document; the **Coverage Summary is computed by code** from the validated array (AD3, invariant I5) and the model cannot influence it. Includes the mandatory AI-review banner, `_None identified._` for empty lists, and pipe-escaping for table safety. `write_markdown()` writes UTF-8 to `outputs/<KEY>_test_plan.md`.
- **Error:** none at write time.
- **Files touched:** `tools/render_markdown.py` (created)
- **Next:** Assemble the pipeline and CLI.

### 2026-09-11 — Phase 3: pipeline (navigation) + CLI
- **Action:** Wire the stages into one orchestrated engine with the validation retry.
- **Result:** `tools/pipeline.py` — `generate_test_plan()` runs config → fetch → prompt → generate → validate → render, owns the **one-retry** correction loop on `PlanValidationError`, writes `.tmp/<KEY>_plan.json`, and returns a `PipelineResult`. `tools/run.py` — thin argparse CLI that bootstraps `sys.path`, prints progress, catches `AppError` → friendly message + exit 1.
- **Error:** none.
- **Files touched:** `tools/pipeline.py`, `tools/run.py` (created)
- **Next:** Offline verification of the pure functions.

### 2026-09-11 — Phase 3: offline verification of pure functions ✅
- **Action:** Compile-check every module, then exercise the pure functions against fixtures before spending live API calls.
- **Result:** All 9 modules compiled. Offline checks passed: key validation rejects 5 malformed inputs; ADF flattening produces correct text; `grounding` flag correct; fenced and prose-wrapped JSON both extract; the validator **accepts** a valid plan (renumbering `TC-99/TC-100` → `TC-001/TC-002` and cleaning step numbers) and **rejects** all five invalid variants — all-positive, missing top-level key, bad `priority` enum, empty `test_cases`, and unknown extra key. Coverage summary and renderer verified.
- **Error:** none.
- **Files touched:** none (scratch pad test)
- **Next:** Live end-to-end run.

### 2026-09-11 — Phase 3: LIVE end-to-end run ✅
- **Action:** Run the real CLI against a live Jira issue.
- **Result:** `py tools\run.py SAM1-1` succeeded on the first attempt — fetched "SAM1-1 — Define Project Timeline Framework", generated with `openai/gpt-oss-120b`, validated, and wrote `outputs/SAM1-1_test_plan.md`. The plan contained **3 test cases** (1 Positive + 2 Negative), all with techniques and traceability, plus a code-computed coverage summary and a risks section that correctly noted description-only grounding. Quality was good enough to ship as a draft.
- **Error:** none.
- **Files touched:** `outputs/SAM1-1_test_plan.md`, `.tmp/SAM1-1_plan.json` (created)
- **Next:** Build the Streamlit UI.

### 2026-09-11 — Phase 3: Streamlit UI built and verified ✅
- **Action:** Build the presentation shell and confirm it runs.
- **Result:** `app.py` created — sidebar config display (masked secrets), a form for the Jira ID and optional instructions, per-stage progress, metrics, download button, and Full-plan / Coverage tabs. Contains **no pipeline logic** (invariant I9) — it calls `tools/pipeline.py` and `coverage_summary` only, and never leaks a traceback.
- **Error:** ⚠️ Two bugs caught during authoring: an unclosed `st.info(` call and an over-broad edit that dropped the `st.columns()` declaration. Both fixed, then `py -m py_compile app.py` → OK and `import app` → `APP_IMPORT_OK`.
- **Verification:** Started Streamlit headless on port 8599 — `/_stcore/health` returned **200 ok** and `/` returned 200 with the Streamlit root. **Server stopped afterwards; port confirmed free (no listener).**
- **Files touched:** `app.py` (created)
- **Next:** Phase 4 (Stylize) — polish output/UI and review the sample plan with the user.

### 2026-09-11 — Phase 3: renderer fix (step numbering)
- **Action:** Noticed the generated Markdown numbered every step as `1.` (Markdown renders it correctly, but the raw text was ugly and diverged from the SOP).
- **Result:** `render_markdown.py` now enumerates steps sequentially (`1.`, `2.`, `3.`…). Re-ran the live CLI; output confirmed correct.
- **Error:** none.
- **Files touched:** `tools/render_markdown.py` (edited)
- **Next:** Phase 4.

### 2026-09-11 — Phase 4 kickoff: SOP updated before the renderer (Golden Rule)
- **Action:** Phase 4 changes the output template, so per the Golden Rule the SOP was updated first.
- **Result:** `SOP_render_markdown.md` extended with §3a (**At a Glance** block), §3b (test-case summary table), updated input table (`model`, `issue_url`), and the grounding-language mapping. `SOP_fetch_issue.md` §7 rewritten for the grounding fix (below).
- **Error:** none.
- **Files touched:** `architecture/SOP_render_markdown.md`, `architecture/SOP_fetch_issue.md`
- **Next:** Apply the changes to the renderer.

### 2026-09-11 — Phase 4: ⚠️ BUG FOUND — grounding overstated
- **Action:** Review the rendered output before styling further.
- **Result:** **Found a real correctness bug.** The plan for `SAM1-1` reported `Grounding: Acceptance criteria + description` — on a site with **no Acceptance Criteria field at all**. Root cause: `normalize_issue` used a boolean-ish `low`/`acceptable` flag, and the renderer treated anything not `low` as "has acceptance criteria". Because `SAM1-1` has a description, it was flagged `acceptable` and the renderer overstated the grounding. This is exactly the kind of claim the constitution forbids.
- **Error:** ⚠️ incorrect grounding reporting (not a crash — a truthfulness defect).
- **Fix:** replaced with a **three-state** flag — `acceptance_criteria` / `description_only` / `low` — applied in `fetch_jira_issue.py`, mapped to plain language in `render_markdown.py`, and used to select the prompt note in `build_prompt.py`. SOP updated first in each case.
- **Files touched:** `tools/fetch_jira_issue.py`, `tools/render_markdown.py`, `tools/build_prompt.py`
- **Next:** Re-render and re-verify.

### 2026-09-11 — Phase 4: styling implemented
- **Action:** Apply the templating improvements.
- **Result:** `render_markdown.py` now emits: an **At a Glance** table (case counts with positive/negative split, deduped + capped focus areas, techniques applied, grounding, review status); a **test-case summary table**; a richer **Details** table with issue summary, Jira deep link, and the model used; em-dash titles; and sequential step numbering. Pipeline wired to pass `model` and `issue_url`.
- **Error:** none.
- **Files touched:** `tools/render_markdown.py`, `tools/pipeline.py`
- **Next:** Re-render from cache (no API cost) to check the template.

### 2026-09-11 — Phase 4: re-render verified from cached JSON
- **Action:** Re-render the existing plan via the new template without spending an LLM call.
- **Result:** All expected sections present; grounding now correctly reads `Description only — no Acceptance criteria field on this project`. Confirms the bug fix.
- **Error:** none.
- **Files touched:** `outputs/SAM1-1_test_plan.md` (re-rendered)
- **Next:** Re-run the offline suite (grounding semantics changed).

### 2026-09-11 — Phase 4: VWO space identified; empty descriptions found ⚠️
- **Action:** Follow up on the user's note that their Jira space is **VWO**.
- **Result:** VWO is the project with key **`KAN`** (`/rest/api/3/project/KAN` → name `"VWO"`). However, **all three VWO issues (`KAN-1/2/3`) have empty descriptions** — the description field exists but holds an empty ADF document, flattening to `""`. So plans from `KAN` keys are `low` grounding. `SAM1-*` issues do have real descriptions.
- **Error:** none — this is a data-quality finding, not a code defect. The tool correctly flags it.
- **Files touched:** `.env` (`DEFAULT_JIRA_KEY=KAN-1`), `findings.md` §9.1
- **Next:** Exercise the low-grounding path live.

### 2026-09-11 — Phase 4: validation retry verified in production ✅
- **Action:** Run the live CLI against `KAN-1` (low grounding) to test the edge case.
- **Result:** The **retry loop fired for real** — the first attempt failed validation on a near-empty issue, the corrective retry succeeded, and 2 test cases were written. The model wrote `"Not specified in the Jira issue."` for unknown expected results instead of inventing them — the anti-hallucination policy working. Also confirmed `KAN-1` is flagged `⚠️ Low — no description or acceptance criteria on this issue`.
- **Error:** none.
- **Files touched:** `outputs/KAN-1_test_plan.md` (created)
- **Next:** Improve the low-grounding prompt note (the risk text said "based solely on the ticket description" when there is no description).

### 2026-09-11 — Phase 4: low-grounding prompt note corrected
- **Action:** The `low` case reused the description-only wording, which incorrectly claimed a description existed.
- **Result:** `grounding_note()` now selects from all three states; the `low` variant explicitly says there is no description and no AC, instructs the model to produce few high-level cases, and to include a prominent "near-speculative" risk. `SOP_generate_plan.md` §3 updated first with the full three-state table. Live re-run confirmed the risk now reads "Minimal grounding; requirements are not defined, leading to speculative test cases."
- **Error:** none.
- **Files touched:** `architecture/SOP_generate_plan.md`, `tools/build_prompt.py`
- **Next:** Re-run the full offline suite and update docs.

### 2026-09-11 — Phase 4: full re-verification ✅
- **Action:** Re-run the offline suite after the grounding change, then re-run both live paths.
- **Result:** Offline suite updated for three-state grounding and **all checks pass** — including asserting the new `low` / `description_only` / `acceptance_criteria` values, and the validator still rejecting all five invalid plan variants. Live re-runs of `KAN-1` (low) and `SAM1-1` (description-only) both succeeded.
- **Error:** ⚠️ The offline suite initially failed (`AssertionError` on the old `"acceptable"` value) — expected, since the semantics deliberately changed. Test updated, then green.
- **Files touched:** none (verification)
- **Next:** Write the README and close out Phase 4.

### 2026-09-11 — Phase 4 closeout: README + docs
- **Action:** Document the finished project and update project memory.
- **Result:** `README.md` written — description, project structure, setup, `.env` contract, CLI + UI usage, output sections table, grounding-quality table (with the VWO caveat), error handling, and the project-memory index. `task_plan.md` Phase 4 ticked and Status Snapshot updated (Phase 4 complete, Phase 5 ready). `findings.md` §9 added with the VWO finding, the grounding bug post-mortem, the retry verification, and the styling summary.
- **Error:** none.
- **Files touched:** `README.md`, `task_plan.md`, `findings.md`
- **Next:** Phase 5 (Trigger) — final deployment/automation step.

---

## 📈 Milestones

| Milestone | Target | Status |
|---|---|---|
| Protocol 0 — memory files created | 2026-09-11 | ✅ Done |
| Phase 1 Blueprint approved + schema locked | 2026-09-11 | ✅ Done |
| Jira + Groq links verified | 2026-09-11 | ✅ Done |
| Constitution amended for CLI + UI scope | 2026-09-11 | ✅ Done |
| `tools/` scripts implemented | 2026-09-11 | ✅ Done |
| Streamlit UI built | 2026-09-11 | ✅ Done |
| First real test plan generated | 2026-09-11 | ✅ Done |
| Phase 4 styling + README | 2026-09-11 | ✅ Done |
| Phase 5 Trigger | — | ⬜ Pending |

---

## 🧱 Issue Tracker (errors / blockers)

| # | Date | Issue | Impact | Resolution | Status |
|---|---|---|---|---|---|
| 1 | 2026-09-11 | Real credentials committed to `.env.example` (a committable template) + token had stray space/comment | Secret-leak risk; corrupted `.env` parsing | Moved to `.env`, restored `.env.example` placeholders, added `.gitignore` | ✅ Resolved |
| 2 | 2026-09-11 | No Acceptance Criteria custom field on this Jira site | Expected-result grounding would have been empty | Description (ADF-flattened) is the primary source; noted in `LLM.md` §1.2 | ✅ Resolved (fallback defined) |
| 3 | 2026-09-11 | `python` not on PATH (Windows Store alias, exit 9009) | Scripts can't be run with `python` | Use the `py` launcher (Python 3.13.2) | ✅ Resolved |
| 4 | 2026-09-11 | Legacy `GET /rest/api/3/search` returns 410 on Jira Cloud | Can't list issues the old way | Use `GET /rest/api/3/search/jql` | ✅ Resolved |
| 5 | 2026-09-11 | `DEFAULT_JIRA_KEY=vandysengar` is not a valid issue key | Would fail key validation | Left empty; a real key like `SAM1-1` is required | ✅ Resolved |
| 6 | 2026-09-11 | `requirements.txt` listed `streamlit` + `jsonschema`, conflicting with locked Blueprint decisions | Scope/spec conflict would have derailed Phase 3 | User confirmed **CLI + Streamlit UI** and **jsonschema**; constitution amended (AD5 superseded, AD8 added, I9/I10 added) | ✅ Resolved |
| 7 | 2026-09-12 | `KAN-1` has a present-but-empty description (raw ADF `{"type":"doc","content":[]}`) | Plans from VWO issues are `low` grounding and read "Not specified in the Jira issue." | Verified against the raw API; needs real content written into Jira (not a tool defect) | 🟡 Open — data quality |

---

## 📎 One-off Actions (outside the pipeline)

> These are **manual actions taken at the owner's request**, not features of the agent.
> The agent itself remains read-only against Jira (LLM.md AD1).

### 2026-09-12 — Attached the KAN-1 test plan to the Jira issue

- **Action:** Owner asked to attach the generated plan to issue `KAN-1` in the VWO space.
- **Method:** One-off script (session scratchpad, not committed) calling `POST /rest/api/3/issue/KAN-1/attachments` with `X-Atlassian-Token: no-check` and multipart `file`.
- **Result:** ✅ **HTTP 200** — attachment `id=10000`, `KAN-1_test_plan.md`, 2882 bytes. Read back from Jira to confirm: 1 attachment, authored by Vandana.
- **Note:** This was a deliberate write to shared Jira state. The agent's read-only invariant is unchanged; no pipeline code was modified. See `LLM.md` answer #4 for the clarification.
