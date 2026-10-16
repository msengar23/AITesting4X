# SOP — Trigger (Activation, Scheduling & Delivery)

**Layer:** 1 (Architecture) · **Files:** `tools/run.py`, `tools/pipeline.py`, `trigger.bat`, `run_ui.bat`, `.github/workflows/test-plan-agent.yml` · **Version:** 1.0 (2026-09-11)

> **Note:** `BLAST.md` defines Phases 1–4 only; the "T" in B.L.A.S.T. (**Trigger**) is never
> expanded in the source document. This SOP defines it for this project as agreed with the
> owner: **the activation surface** — how the pipeline is *started*, on demand or on a schedule,
> and how its output is delivered.

---

## 1. Goal

Make the pipeline **runnable on demand and on a schedule**, without manual intervention, while
keeping every failure non-fatal to the batch and every secret out of the repository.

## 2. Trigger Surfaces

| # | Surface | Command | Purpose |
|---|---|---|---|
| T1 | **Single issue** | `py tools/run.py SAM1-1` | Ad-hoc, interactive |
| T2 | **Explicit list** | `py tools/run.py --keys SAM1-1,SAM1-2` | Targeted regeneration |
| T3 | **Whole project** | `py tools/run.py --project SAM1` | Fan-out across a project |
| T4 | **Scheduled (Windows)** | `trigger.bat` via Task Scheduler | Local recurring runs |
| T5 | **Scheduled (CI)** | `.github/workflows/test-plan-agent.yml` (cron) | Cloud recurring runs |
| T6 | **Interactive UI** | `py -m streamlit run app.py` / `run_ui.bat` | Human-in-the-loop |

## 3. Batch Semantics (T2/T3)

```
1. Resolve the target key set
     --keys    -> split on commas, validate each key
     --project -> GET /rest/api/3/search/jql?jql=project=<KEY> ORDER BY key ASC
2. Apply --limit if given (default 10, max 50)
3. For each key, run the standard pipeline
4. Collect (key, ok|error) without aborting the batch
5. Print a summary table; exit 1 if ANY key failed, else 0
```

**Continue-on-error is mandatory.** One unfetchable issue must not lose the other plans — this
is the reliability principle from `BLAST.md` ("prioritize reliability over speed").

### Project issue listing

```
GET {JIRA_URL}/rest/api/3/search/jql
    ?jql=project=<KEY> ORDER BY key ASC
    &maxResults=<limit>
    &fields=key
```

> The legacy `GET /rest/api/3/search` route is retired on Jira Cloud (410 Gone). Always use
> `/rest/api/3/search/jql`. See `findings.md` §8.2.

## 4. Idempotency

Every run overwrites `outputs/<KEY>_test_plan.md` and `.tmp/<KEY>_plan.json`. Re-running a key
replaces its plan — no duplication, no append. A scheduled run therefore converges rather than
accumulating files.

## 5. Scheduling

### 5.1 Windows Task Scheduler (T4)

`trigger.bat` is the entry point. It:

1. Resolves the project directory (works regardless of the working directory).
2. Invokes the pipeline for the configured project using the `py` launcher.
3. Writes a timestamped log to `.tmp/trigger_<date>.log`.
4. Exits non-zero on failure so Task Scheduler can report it.

Register it, for example, to run weekdays at 08:00:

```bat
schtasks /Create /TN "TestPlanAgent" /TR "<path>\trigger.bat" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 08:00
```

### 5.2 GitHub Actions (T5)

The workflow runs on a cron **and** on manual dispatch. It:

1. **Guards on secrets** — if `JIRA_URL` / `JIRA_API_KEY` / `GROQ_API_KEY` are not configured,
   it prints a clear message and skips (it must never fail noisily on a fresh fork).
2. Writes a `.env` from GitHub Actions **secrets** at runtime — secrets are never committed.
3. Generates plans for the configured project.
4. Uploads `outputs/` as a build artifact.
5. Commits the refreshed `outputs/` back to the branch (scheduled/dispatch runs only).

**Required repository secrets:**

| Secret | Value |
|---|---|
| `JIRA_URL` | `https://<site>.atlassian.net` |
| `JIRA_EMAIL` | your Jira email |
| `JIRA_API_TOKEN` | your Jira API token |
| `GROQ_API_KEY` | your Groq key |

## 6. Delivery & Hosting

| Target | Rule |
|---|---|
| **CLI output** | Markdown files in `outputs/` — committed so the deliverables are reviewable |
| **Streamlit Community Cloud** | Primary host for the UI. Deploy from the repo, set `app.py` as the entry point, and provide the four secrets in the app's settings. |
| **Vercel** | ❌ **Not supported.** Vercel is serverless and does not run a persistent Python/Streamlit server. Do not attempt to deploy this UI there. |

## 7. Secrets Rules (non-negotiable)

1. `.env` is **git-ignored** and never committed — enforced by `.gitignore`.
2. CI reads secrets **only** from GitHub Actions secrets, materialised into `.env` at runtime.
3. Logs must never contain tokens. `trigger.bat` redirects pipeline output only — the pipeline
   itself never prints secrets (`Config.masked()`).
4. If a real credential is ever committed, **rotate it immediately** — assume compromise.

## 8. Exit Codes

| Code | Meaning |
|---|---|
| `0` | All requested keys generated successfully |
| `1` | One or more keys failed (batch summary lists them) |
| `130` | Cancelled by the user (Ctrl+C) |

## 9. Edge Cases

| Case | Behaviour |
|---|---|
| `--project` with no issues | Print "no issues found", exit 0 |
| Unknown key in `--keys` | That key fails; the rest still run |
| `--project` and `--keys` together | Rejected — mutually exclusive |
| No target given | Usage error, exit 2 (argparse) |
| `--limit` above 50 | Clamped to 50 |
| Missing secrets in CI | Guard skips with a clear message, exit 0 |
| Partial batch failure | Exit 1, summary shows ok/error per key |
| Rate limiting mid-batch | That key fails with a friendly message; batch continues |
