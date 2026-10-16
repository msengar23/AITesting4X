# 📋 Task Plan — Test Plan Agent (BLAST)

> Protocol 0 artifact. Owns **phases, goals, and checklists**.
> Companion docs: [`findings.md`](./findings.md) · [`progress.md`](./progress.md) · [`LLM.md`](./LLM.md)

---

## 🎯 Project Identity

| Field | Value |
|---|---|
| **Project name** | Test Plan Agent |
| **Protocol** | B.L.A.S.T. — Blueprint · Link · Architect · Stylize · Trigger |
| **North Star** | From a **single Jira ID**, generate a complete, professional **Test Plan** as a Markdown file. |
| **Scope** | One input (Jira ID) → one deliverable (`outputs/<JIRA-ID>_test_plan.md`). Nothing more. |
| **LLM backend** | Groq only — `openai/gpt-oss-120b` (see `.env.example`) |
| **Delivery** | Markdown file in `outputs/` |
| **Started** | 2026-09-11 |
| **Status** | 🟢 Protocol 0 — Initialization |

### One-line Flow

```
Jira ID  →  fetch + normalize issue (deterministic)  →  LLM drafts plan (JSON)  →  validate  →  render Markdown  →  outputs/<KEY>_test_plan.md
```

---

## 🏁 Goals

1. **Deterministic intake** — accept a Jira ID, validate the key format, fetch the issue via Jira Cloud REST API v3, and normalize it to a fixed JSON shape. No LLM in this path.
2. **Reliable drafting** — send only the normalized issue to Groq and receive a **strict JSON** test plan.
3. **Non-negotiable validity** — validate the LLM JSON against the schema in `LLM.md` *before* rendering; reject and retry on malformed output.
4. **Clean delivery** — render the validated object into a readable Markdown test plan written to `outputs/`.
5. **Explainability** — every step logged; errors surfaced as friendly messages, never as raw stack traces.

---

## 🟢 Protocol 0 — Initialization  *(current phase)*

- [x] Create `task_plan.md` (this file)
- [x] Create `findings.md` (research + Jira fetch mechanics)
- [x] Create `progress.md` (timestamped build log)
- [x] Initialize `LLM.md` as the Project Constitution (schemas, rules, invariants)
- [ ] Review blueprint (`task_plan.md` Phase 1) with user and get approval
- [ ] Confirm all open questions below are resolved

> **Halt Execution:** no scripts in `tools/` until Discovery questions are answered, the Data Schema is defined in `LLM.md`, and this blueprint is approved.

---

## 🏗️ Phase 1 — B · Blueprint (Vision & Logic) — ✅ Complete

- [x] **Discovery** — answer the 5 BLAST questions:
  - [x] **North Star** — From a single Jira ID, produce a complete Markdown Test Plan: **full plan structure plus a detailed test-case table**.
  - [x] **Integrations** — Jira Cloud REST API v3 (read-only) + Groq `openai/gpt-oss-120b`. **Keys ready.**
  - [x] **Source of Truth** — the Jira issue fields themselves (`summary`, `description` ADF, `status`, `priority`, `issuetype`, `labels`, `components`, `project`, `reporter`, `assignee`, `created`, `updated`, + discovered Acceptance Criteria custom field).
  - [x] **Delivery Payload** — one Markdown file at `outputs/<JIRA-ID>_test_plan.md`. **No Jira write-back.**
  - [x] **Behavioral Rules** — strict anti-hallucination; **ISTQB techniques mandated** (BVA, equivalence partitioning, negative/edge); deterministic code owns structure + coverage ledger; output is a **draft for human review**.
- [x] **Data-First Rule** — Input/Output JSON schemas confirmed and 🔒 locked in `LLM.md`
- [x] **Research** — OSS/reference art reviewed and logged in `findings.md` §6 (adopt vs defer decisions recorded)
- [x] **Approval** — user signed off on the Blueprint (2026-09-11)

---

## ⚡ Phase 2 — L · Link (Connectivity) — ✅ Complete

- [x] Create `.env` with real values (never commit `.env`) + `.gitignore` added
- [x] **Jira handshake** — `GET /rest/api/3/myself` → authenticated as **Vandana**
- [x] **Field discovery** — `GET /rest/api/3/field` scanned; **no Acceptance Criteria field exists** on this site → description becomes the grounding source
- [x] **Groq handshake** — `openai/gpt-oss-120b` confirmed available (14 models)
- [x] Minimal verify script `tools/verify_link.py` confirms both links
- [x] Results recorded in `progress.md` and `findings.md` §8

**Verified targets:** site `https://vandysengar.atlassian.net` · projects **KAN** (VWO) and **SAM1** (Timeline Tracking Initiatives) · recommended first test key **`SAM1-1`**.

> Do not proceed to full logic if either link is broken. ✅ Neither is broken.

---

## ⚙️ Phase 3 — A · Architect (3-Layer Build) — ✅ Complete

**Layer 1 — Architecture (`architecture/`)**
- [x] `architecture/SOP_fetch_issue.md` — goals, inputs, tool logic, edge cases
- [x] `architecture/SOP_generate_plan.md` — LLM contract, validation rules
- [x] `architecture/SOP_render_markdown.md` — template mapping
- [x] `architecture/SOP_pipeline.md` — end-to-end sequence + error routing (CLI & UI)
- [x] `architecture/SOP_build_plan.md` — content construction & quality standard *(added on request)*
- [x] Golden Rule respected: SOPs written **before** any code

**Layer 2 — Navigation (reasoning)**
- [x] `tools/pipeline.py` — single orchestrator shared by CLI and UI (invariant I9)
- [x] Route data between SOPs and tools in the right order
- [x] No complex task performed directly — orchestrate tools only

**Layer 3 — Tools (`tools/`)**
- [x] `tools/config.py` — load/validate `.env` (secrets never printed)
- [x] `tools/errors.py` — domain error taxonomy → friendly messages
- [x] `tools/fetch_jira_issue.py` — fetch + normalize (deterministic, testable)
- [x] `tools/build_prompt.py` — assemble system + user prompt from the normalized issue
- [x] `tools/generate_test_plan.py` — call Groq, parse JSON (via `requests`)
- [x] `tools/validate_plan.py` — apply `jsonschema` + sequencing/coverage checks
- [x] `tools/render_markdown.py` — JSON → Markdown (+ computed Coverage Summary) in `outputs/`
- [x] `tools/run.py` — thin CLI entry point
- [x] `schemas/test_plan.schema.json` — machine-readable schema (invariant I10)
- [x] All intermediates written to `.tmp/`
- [x] Secrets read **only** from `.env`

**Presentation — UI**
- [x] `app.py` — Streamlit shell: enter Jira ID, view plan, download `.md`
- [x] UI contains **no** pipeline logic — calls `tools/pipeline.py` only
- [x] UI shows the human-review banner and friendly errors

**Verified working (2026-09-11):** `py tools\run.py SAM1-1` produced `outputs/SAM1-1_test_plan.md` (3 test cases, 1 positive + 2 negative) in one live run; Streamlit served healthy on port 8599 and was stopped cleanly.

---

## ✨ Phase 4 — S · Stylize (Refinement & UI) — ✅ Complete

- [x] Polish the Markdown test-plan template (headings, tables, IDs, priorities)
- [x] Add a plain-language **At a Glance** summary block at the top of each plan (code-computed)
- [x] Add a scannable **test-case summary table** before the detailed blocks
- [x] Add Jira issue deep link, issue summary, and model to the Details table
- [x] Map grounding quality to plain language (three-state: AC / description-only / low)
- [x] Style the Streamlit UI (form, progress, metrics, tabs, download)
- [x] Present a sample plan (built from real Jira IDs) to the user for feedback
- [x] Write `README.md` with setup, config, and usage (CLI + UI)

**Styling changes verified live:** `SAM1-1` (description-only grounding) and `KAN-1` (low grounding) both re-rendered and regenerated successfully. The three-state grounding fix was validated by a real bug it caught — the renderer previously claimed "Acceptance criteria + description" on a site with no AC field.

---

## 🚀 Phase 5 — T · Trigger (Activation, Scheduling & Delivery) — ✅ Complete

> **Note:** `BLAST.md` defines Phases 1–4 only — the "T" in B.L.A.S.T. is never expanded in the
> source document. Scope was agreed with the owner (batch runner + scheduled automation +
> deploy script + commit/push) and formalised in `architecture/SOP_trigger.md`.

**Layer 1 — Architecture**
- [x] `architecture/SOP_trigger.md` — trigger surfaces, batch semantics, scheduling, secrets, exit codes

**Layer 3 — Tools**
- [x] `tools/fetch_jira_issue.py` — `list_project_issues()` via `/rest/api/3/search/jql`
- [x] `tools/pipeline.py` — `resolve_keys()`, `generate_batch()` (continue-on-error), `BatchResult`
- [x] `tools/run.py` — `--project`, `--keys`, `--limit` + batch summary + correct exit codes

**Trigger surfaces**
- [x] T1 single issue · T2 `--keys` list · T3 `--project` fan-out
- [x] T4 `trigger.bat` — Windows Task Scheduler entry point with timestamped logs
- [x] T5 `.github/workflows/test-plan-agent.yml` — cron + manual dispatch, secrets-guarded
- [x] T6 `run_ui.bat` — UI launch script

**Delivery**
- [x] README documents scheduling, CI secrets, and hosting
- [x] Streamlit Community Cloud documented as the supported host; Vercel explicitly ruled out
- [x] Project committed and pushed to GitHub

**Verified working (2026-09-11):** `--keys SAM1-1,ZZZ-99999` generated one plan, reported the 404, and exited 1 (continue-on-error proven). `trigger.bat` in project mode generated a plan and wrote `.tmp/trigger_20260912_005113.log`. Workflow YAML validated. Offline suite covers key resolution, dedupe, limit clamping, blank-project rejection, and batch error aggregation.

---

## ✅ Definition of Done (whole project)

- [ ] `py tools/run.py <JIRA-ID>` produces `outputs/<JIRA-ID>_test_plan.md`
- [ ] `py -m streamlit run app.py` opens the UI and produces the same plan for the same key
- [ ] Both entry points call the shared `tools/pipeline.py` (no duplicated logic)
- [ ] Plan contains: title, objective, preconditions, test data, test cases, risks, out-of-scope
- [ ] Plan includes a code-computed **Coverage Summary** (never model-authored)
- [ ] Every test case traces back to content actually present in the Jira issue
- [ ] LLM output is validated via `schemas/test_plan.schema.json` (`jsonschema`)
- [ ] Invalid Jira ID, auth failure, 404, network error, and malformed LLM JSON all produce friendly messages
- [ ] No credentials committed; `.env` is git-ignored
- [ ] `requirements.txt` matches the actual imports
- [ ] `README.md` updated with setup, config, and usage (CLI + UI)
- [ ] `progress.md` reflects the full build; `task_plan.md` checkboxes updated
- [ ] Work committed and pushed to the configured GitHub repository

---

## ❓ Open Questions / Blockers

| # | Question | Blocks | Status |
|---|---|---|---|
| 1 | Which Jira site (URL) and project key prefix will we target? | Phase 2 Jira handshake | ✅ Resolved — `vandysengar.atlassian.net`; projects `KAN`, `SAM1` |
| 2 | Does the target Jira project have an Acceptance Criteria / DoD custom field, and what is its ID? | Schema completeness | ✅ Resolved — **no AC field exists**; `description` is the grounding source |
| 3 | Is `openai/gpt-oss-120b` the intended default Groq model? | Prompt sizing / cost | ✅ Resolved — yes, verified available |
| 4 | Any required test-plan template/format (sections, ID scheme)? | Phase 4 template | ✅ Resolved — 7-section template + `TC-001` scheme locked in `LLM.md` |
| 5 | Multiple export formats (CSV/XLSX) or Markdown only? | Scope lock | ✅ Resolved — **Markdown only** |

---

## 🧭 Architecture Decision Log (Phase 1)

| # | Decision | Rationale | Alternative rejected |
|---|---|---|---|
| AD1 | **Read-only Jira**, local Markdown output | Minimal permissions; no write scopes needed | Posting comments / creating sub-tasks |
| AD2 | **Single LLM call** in the pipeline | Determinism; one validation point; simpler failure modes | Multi-agent / iterative self-review loops |
| AD3 | **Deterministic code owns structure and the coverage ledger** | Corroborated by OSS prior art (`findings.md` §6); models must not grade their own coverage | Letting the model count/claim its own coverage |
| AD4 | **ISTQB techniques mandated** (BVA, equivalence partitioning, negative/edge) | Produces defensible, reviewable coverage | Ad-hoc "make some tests" prompting |
| AD5 | ~~Hand-rolled schema validation, no extra dependency~~ **SUPERSEDED (Phase 2)** — use the **`jsonschema`** library | User provisioned `jsonschema` in `requirements.txt`; declarative schema is stronger and self-documenting | Hand-rolled key/enum checks (kept only for ID sequencing + coverage ratio) |
| AD6 | **Groq only**, no Ollama | Keys ready; no local service dependency; matches `.env.example` | Dual-provider fallback (as in `Task_02`) |
| AD7 | **AC-first grounding**, description as context | Matches every reference implementation reviewed | Prompting off the raw description alone |
| AD8 | **Two entry points, one engine** — CLI (`tools/run.py`) + Streamlit UI (`app.py`) | User requested both; the UI must never duplicate pipeline logic | UI-only, or CLI-only |
| AD9 | **Description-first grounding** (AC field absent on this site) | Verified in Phase 2: no AC/DoD custom field exists on `vandysengar.atlassian.net` | Assuming AC exists and sending an empty field |

---

## 📊 Status Snapshot

| Phase | Name | Status | Last Updated |
|---|---|---|---|
| 0 | Initialization | 🟢 Complete | 2026-09-11 |
| 1 | Blueprint | 🟢 Complete | 2026-09-11 |
| 2 | Link | 🟢 Complete | 2026-09-11 |
| 3 | Architect | 🟢 Complete | 2026-09-11 |
| 4 | Stylize | 🟢 Complete | 2026-09-11 |
| 5 | Trigger | 🟡 Ready to start | 2026-09-11 |
