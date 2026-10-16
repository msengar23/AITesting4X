# 🧪 Test Plan Agent

Generate a complete, professional **Markdown test plan** from a single **Jira issue ID**.

Built with the **B.L.A.S.T.** protocol (Blueprint · Link · Architect · Stylize · Trigger) and a
3-layer architecture that keeps deterministic code in charge of structure while an LLM drafts
the content.

> ⚠️ **Plans are AI-generated drafts.** They are a starting point for a QA engineer, not a
> replacement for QA judgement. Every generated plan carries this banner.

---

## What it does

```
Jira ID  →  fetch + normalize issue (deterministic)  →  LLM drafts plan (JSON)
         →  validate against JSON Schema  →  render Markdown  →  outputs/<KEY>_test_plan.md
```

- Grounds every test case in the actual Jira issue — never invents requirements.
- Applies **ISTQB test-design techniques** (boundary value analysis, equivalence partitioning,
  decision table, state transition, error guessing) and labels each case.
- Requires **traceability** on every case and at least one non-positive case.
- Computes a **Coverage Summary in code** — the model cannot inflate its own coverage.
- Delivers via **CLI** or a **Streamlit UI**, both driven by one shared pipeline.

---

## Project structure

```
Test-Plan-Agent-Blast/
├── app.py                          # Streamlit UI (thin shell — no pipeline logic)
├── run_ui.bat                      # launch the Streamlit UI
├── trigger.bat                     # scheduled entry point (Task Scheduler)
├── requirements.txt                # streamlit, requests, python-dotenv, jsonschema
├── .env.example                    # configuration contract (copy to .env)
│
├── architecture/                   # Layer 1 — SOPs (written BEFORE the code)
│   ├── SOP_fetch_issue.md
│   ├── SOP_build_plan.md           # content & quality standard for a plan
│   ├── SOP_generate_plan.md
│   ├── SOP_render_markdown.md
│   ├── SOP_pipeline.md
│   └── SOP_trigger.md
│
├── schemas/
│   └── test_plan.schema.json       # machine-readable LLM output contract
│
├── tools/                          # Layer 3 — deterministic, atomic scripts
│   ├── config.py                   # load/validate .env (secrets never printed)
│   ├── errors.py                   # domain error taxonomy → friendly messages
│   ├── fetch_jira_issue.py         # Jira REST v3 fetch + ADF flatten + normalize
│   ├── build_prompt.py             # anti-hallucination + ISTQB system/user prompt
│   ├── generate_test_plan.py       # the single Groq call
│   ├── validate_plan.py            # jsonschema + ID sequencing + coverage rule
│   ├── render_markdown.py          # deterministic Markdown + computed coverage
│   ├── pipeline.py                 # Layer 2 — the shared orchestrator (single + batch)
│   ├── run.py                      # CLI entry point
│   └── verify_link.py              # Phase 2 connectivity handshakes
│
├── outputs/                        # final Markdown deliverables
├── .tmp/                           # intermediates + trigger logs (git-ignored)
│
└── task_plan.md · findings.md · progress.md · LLM.md   # project memory
```

> The scheduled GitHub Actions workflow lives at the **repository root**:
> `.github/workflows/test-plan-agent.yml`.

---

## Setup

1. **Install dependencies**

   ```bash
   py -m pip install -r requirements.txt
   ```

2. **Configure credentials** — copy the template and fill in real values:

   ```bash
   copy .env.example .env
   ```

   ```dotenv
   JIRA_URL=https://your-site.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_API_TOKEN=            # id.atlassian.com -> Security -> API tokens
   GROQ_API_KEY=              # console.groq.com/keys
   GROQ_MODEL=openai/gpt-oss-120b
   JIRA_AC_FIELD=             # optional; only if your site has an Acceptance Criteria field
   DEFAULT_JIRA_KEY=
   ```

   `.env` is **git-ignored** and must never be committed.

3. **Verify connectivity** (optional but recommended):

   ```bash
   py tools/verify_link.py
   ```

---

## Usage

### CLI

```bash
# Single issue
py tools/run.py SAM1-1
py tools/run.py SAM1-1 --instructions "Focus on boundary values and permissions"

# Explicit list (comma-separated)
py tools/run.py --keys SAM1-1,SAM1-2

# Every issue in a project
py tools/run.py --project SAM1 --limit 10

# Print only the output path
py tools/run.py SAM1-1 --quiet
```

Batch runs **continue past individual failures** and print a summary; the exit code is `1` if
any key failed, `0` if all succeeded.

### Streamlit UI

```bash
py -m streamlit run app.py
```

Or double-click `run_ui.bat`. Enter a Jira ID, optionally add instructions, and click
**Generate test plan**. The plan renders in-page with a download button.

Both entry points write `outputs/<JIRA-ID>_test_plan.md` and use the same pipeline.

---

## Scheduling (Trigger phase)

The "Trigger" phase is the activation surface: how the pipeline starts, on demand or on a
schedule. See `architecture/SOP_trigger.md` for the full contract.

| Surface | How |
|---|---|
| Single issue | `py tools/run.py SAM1-1` |
| Explicit list | `py tools/run.py --keys SAM1-1,SAM1-2` |
| Whole project | `py tools/run.py --project SAM1 --limit 10` |
| **Windows Task Scheduler** | `trigger.bat` — logs to `.tmp/trigger_<timestamp>.log` |
| **GitHub Actions (cron)** | `.github/workflows/test-plan-agent.yml` |
| Interactive UI | `run_ui.bat` |

### Windows Task Scheduler

`trigger.bat` defaults to project `SAM1` and a limit of 10; override with environment
variables `JIRA_PROJECT` and `PLAN_LIMIT`. Register it, for example, weekdays at 08:00:

```bat
schtasks /Create /TN "TestPlanAgent" /TR "<path>\trigger.bat" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 08:00
```

### GitHub Actions

The workflow runs weekdays at **03:17 UTC** and on manual dispatch. It writes `.env` from
repository **secrets** at runtime (never committed), generates plans, uploads them as a build
artifact, and commits the refreshed `outputs/` back.

**Required repository secrets** (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `JIRA_URL` | `https://<site>.atlassian.net` |
| `JIRA_EMAIL` | your Jira email |
| `JIRA_API_TOKEN` | your Jira API token |
| `GROQ_API_KEY` | your Groq key |

Optional repository **variables**: `JIRA_PROJECT` (default `SAM1`), `PLAN_LIMIT` (default `5`).

> If the secrets are not configured, the workflow **skips cleanly** with a warning instead of
> failing — so it is safe on a fresh fork.

---

## Hosting the UI

| Target | Support |
|---|---|
| **Streamlit Community Cloud** | ✅ Recommended. Deploy from the repo, set `app.py` as the entry point, and add the four secrets in the app's settings. |
| **Vercel** | ❌ **Not supported.** Vercel is serverless and cannot run a persistent Python/Streamlit server. |

---

## Output

Each plan contains:

| Section | Contents |
|---|---|
| **At a Glance** | Case counts, focus areas, techniques, grounding quality, review status |
| **Details** | Issue metadata, link, model used, generated timestamp |
| 1. Objective | What the plan verifies |
| 2. Preconditions | Environment/access/data prerequisites |
| 3. Test Data | Concrete inputs required |
| 4. Test Cases | Summary table + detailed steps and expected results |
| 5. Coverage Summary | **Computed by code** — counts by priority, type, technique |
| 6. Risks | Uncertainty, including reduced grounding |
| 7. Out of Scope | Explicitly excluded behaviour |

---

## Grounding quality

The tool reports how well-grounded a plan is, based on what the Jira issue actually contains:

| State | Meaning |
|---|---|
| `acceptance_criteria` | Strongest — AC primary, description supporting |
| `description_only` | Description is the only requirement source |
| `low` | Only a summary exists — the plan is near-speculative and flagged as such |

> **Note for `vandysengar.atlassian.net`:** this site has **no Acceptance Criteria custom
> field**. The `VWO` (`KAN`) project's issues currently have **empty descriptions**, so plans
> from those keys are `low` grounding. Add issue descriptions for materially better plans.

---

## Error handling

Every failure produces a friendly message (never a traceback or a secret):

- Invalid Jira key format · authentication failure · permission denied · issue not found
- Network/timeout failures for Jira or Groq · rate limits · unavailable model
- Malformed LLM output → **validated against the JSON Schema**, retried once, then reported

---

## Project memory

| File | Purpose |
|---|---|
| `task_plan.md` | Phases, goals, checklists, architecture decisions |
| `findings.md` | Research, Jira API mechanics, live verification results |
| `progress.md` | Timestamped build log, errors, and results |
| `LLM.md` | **Project constitution** — schemas, behavioural rules, invariants |
