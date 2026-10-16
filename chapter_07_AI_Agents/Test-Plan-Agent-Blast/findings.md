# 🔍 Findings — Test Plan Agent (BLAST Protocol 0)

> Research log: what we discovered, how we fetch data from Jira, and the exact
> `curl` / `requests` calls we intend to use. Findings are reproducible by copy-paste.

---

## 1. Source of Truth — Jira Cloud REST API v3

| Item | Finding |
|---|---|
| **API** | Jira Cloud REST API, **v3** (fallback v2) |
| **Base URL** | `https://<your-site>.atlassian.net` |
| **Auth** | HTTP **Basic** — `email:api_token` (Base64). No OAuth needed for a personal token. |
| **Token source** | `id.atlassian.com` → Security → **API tokens** |
| **Content type** | `Accept: application/json` (v3 requests/responses are JSON) |
| **Timeout** | Use ~15s; Jira can hang on cold connections |

> **Critical:** in Jira Cloud, the API token is used with **your account email** — *not* a username, and *not* the token alone. 401 almost always means email/token mismatch.

### Config contract (already in the repo)

`.env.example` in this folder defines everything we need:

```dotenv
JIRA_URL=https://your-site.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=            # id.atlassian.com -> Security -> API tokens
GROQ_API_KEY=              # console.groq.com/keys
GROQ_MODEL=openai/gpt-oss-120b
DEFAULT_JIRA_KEY=
```

---

## 2. Endpoints We Will Use

### 2.1 Handshake — verify credentials

`GET /rest/api/3/myself` — confirms the token works and returns the caller's `accountId`.

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/3/myself"
```

Windows `cmd.exe` one-liner:

```bat
curl -s -u %JIRA_EMAIL%:%JIRA_API_TOKEN% -H "Accept: application/json" "%JIRA_URL%/rest/api/3/myself"
```

Python equivalent:

```python
import requests, os
r = requests.get(
    f"{os.environ['JIRA_URL'].rstrip('/')}/rest/api/3/myself",
    auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"]),
    headers={"Accept": "application/json"},
    timeout=15,
)
r.raise_for_status()
print(r.json()["accountId"])
```

### 2.2 Field discovery — find the Acceptance Criteria custom field

`GET /rest/api/3/field` — returns every field definition. Custom fields are named
`customfield_XXXXX` and **vary per Jira site**, so we must discover the ID rather
than hardcode it.

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/3/field" \
  | grep -i -E "acceptance|definition of done"
```

Filter to `id` + `name` with `jq`:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/3/field" \
  | jq -r '.[] | select(.name | test("acceptance|definition of done"; "i")) | "\(.id)\t\(.name)"'
```

> This is a **one-time / cached** lookup. Result gets written into `.env` (e.g. `JIRA_AC_FIELD=customfield_10042`) and into `LLM.md`.

### 2.3 Fetch the issue — the core call

`GET /rest/api/3/issue/{issueKey}?fields=...` — returns only the fields we request,
which keeps the payload small and predictable.

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/3/issue/PROJ-123?fields=summary,description,status,priority,issuetype,labels,components,project,reporter,assignee,created,updated"
```

With the acceptance-criteria custom field appended:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/3/issue/PROJ-123?fields=summary,description,status,priority,issuetype,labels,customfield_10042"
```

Python equivalent:

```python
fields = "summary,description,status,priority,issuetype,labels,components,project,reporter,assignee,created,updated"
r = requests.get(
    f"{os.environ['JIRA_URL'].rstrip('/')}/rest/api/3/issue/{key}",
    params={"fields": fields},
    auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"]),
    headers={"Accept": "application/json"},
    timeout=15,
)
issue = r.json()
```

---

## 3. Groq — LLM Backend

| Item | Finding |
|---|---|
| **API** | OpenAI-compatible chat completions |
| **Base URL** | `https://api.groq.com/openai/v1` |
| **Endpoint** | `POST /chat/completions` |
| **Auth** | `Authorization: Bearer $GROQ_API_KEY` |
| **Default model** | `openai/gpt-oss-120b` (from `.env.example`) |
| **Temperature** | ≤ `0.2` — test plans need determinism, not creativity |

Handshake (list models, confirms key + model availability):

```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

Generation call:

```bash
curl -s https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "temperature": 0.2,
    "response_format": { "type": "json_object" },
    "messages": [
      { "role": "system", "content": "You are a senior QA engineer. Return ONLY valid JSON matching the provided schema." },
      { "role": "user",   "content": "<normalized Jira issue JSON + instructions>" }
    ]
  }'
```

> `response_format: {"type": "json_object"}` forces JSON-only output, but it is **not** a schema guarantee — we still validate locally before rendering.

---

## 4. Gotchas & Constraints

1. **Description is not plain text.** In API v3 the `description` field is **Atlassian Document Format (ADF)** — a nested JSON tree, not a string. It must be flattened before it reaches the LLM.
2. **Custom field IDs are site-specific.** Acceptance Criteria may be `customfield_10042` on one site and absent (or different) on another. Discover, don't assume.
3. **Issue key format.** Validate against `^[A-Z][A-Z0-9]*-\d+$` before making a network call — saves round-trips on typos.
4. **HTTP status mapping.** `401` → bad email/token · `403` → no permission on the issue · `404` → issue not found / wrong key · `>=400` → generic Jira error.
5. **Only extract fields that exist.** Jira omits absent fields entirely; the normalizer must not assume every field is present.
6. **Rate limits.** Jira and Groq both rate-limit. Fail with a friendly message, don't retry in a tight loop.
7. **`labels` / `components` differ in shape.** `labels` is an array of strings; `components` is an array of objects (`{name: ...}`), so it needs mapping to names.
8. **Large descriptions.** Long ADF bodies can blow the prompt size. Truncate/summarize deterministically before sending if needed.
9. **Never log secrets.** `.env` is the only credential source and must be git-ignored.

---

## 5. Reuse — Don't Reinvent

An existing project in this repo already solves the Jira + Groq plumbing:

- `LiveClass_Tasks/09Augusy_Tasks/Task_02_Local_TestCase_Generator copy/src/jira_client.py`
  - Basic-auth session setup, `ISSUE_KEY_RE`, field-picking normalizer, `_flatten_adf()`, `verify_connection()`, and a clean error taxonomy (`JiraAuthError`, `JiraNotFoundError`, `JiraPermissionError`, `JiraTimeoutError`, `JiraNetworkError`).
- `LiveClass_Tasks/09Augusy_Tasks/Task_02_Local_TestCase_Generator copy/src/llm_client.py`
  - OpenAI-compatible Groq client, provider/model verification, error mapping to friendly messages, `GenerationResult` dataclass.

**Plan:** copy these patterns into `tools/`, trimmed to the test-plan use case — do not rewrite from scratch.

---

## 6. Phase 1 — OSS & Reference Research

BLAST Phase 1 requires searching GitHub and other sources for reusable prior art.
Findings below are grouped by what we **adopt** vs **reject/defer**.

### 6.1 Sources reviewed

| Source | Stack | What it does | Verdict |
|---|---|---|---|
| [`asecurityguru/genai-rest-api-jira-integration-for-testcase-creation`](https://asecurityguru.com/building-a-genai-test-case-generator-jira-rest-api-spring-ai-ollama/) | Spring Boot + Spring AI + Ollama | `GET /rest/api/2/issue/{key}` → extract acceptance criteria → single prompt → cases with ID/Steps/Test Data/Description/Expected Result | **Adopt the shape** — mirrors our pipeline. Uses **API v2** (plain-text `description`); our **v3** path must ADF-flatten. Reinforces `.gitignore` + example-config secrets practice we already follow. |
| [`nobles92ts-ship-it/AI_GAME_QA_TestCase`](https://github.com/nobles92ts-ship-it/AI_GAME_QA_TestCase) | JS, ISTQB-based | Pipeline whose README states **structure, gates, and the coverage ledger are owned by deterministic code, not the model** | **Adopt** — independent corroboration of our `LLM.md` core principle. Source of the deterministic **coverage summary** idea. |
| [`adlerqa/wardeniq`](https://github.com/adlerqa/wardeniq) | Python | Requirements/docs → test cases **and test plans**, coverage insights, gap analysis, validators, RAG | **Adopt the pattern** — validates "plan + cases" scope and the validator-before-render step. **Defer** its RAG/Confluence retrieval. |
| [`Mallikarjun-Roddannavar/ai-testcase-generator-mcp`](https://github.com/Mallikarjun-Roddannavar/ai-testcase-generator-mcp) | TypeScript, MCP | Generates positive / negative / edge cases from endpoint metadata | **Adopt** the case-type taxonomy. **Defer** the MCP server itself. |
| [`Treeify-ai/Awesome-Test-Case-Design`](https://github.com/Treeify-ai/Awesome-Test-Case-Design) + [`xhubio/nanook-table`](https://github.com/xhubio/nanook-table) | Docs / TS | Test-design references: BVA, equivalence partitioning, decision tables, pairwise, state transition | **Adopt** as the source of our mandated `test_design_technique` vocabulary. |
| Hash Agile JIRA-MCP writeup | MCP + LLM | Ticket → structured cases, driven by **Acceptance Criteria**, custom template | **Adopt** AC-first grounding (already in our schema). |
| [`MGdaasLab/WHartTest`](https://github.com/MGdaasLab/WHartTest) | Python | Requirements → executable test-case platform | **Reference only** — far broader scope than ours. |

### 6.2 What we adopt

1. **ISTQB technique tagging** — every test case carries an explicit `test_design_technique` (BVA, equivalence partitioning, decision table, state transition, error guessing).
2. **Deterministic coverage ledger** — the render step computes a coverage summary (counts by priority / type / technique). Code owns it; the model never authors it.
3. **Validator-before-render** — the LLM's JSON is validated against the schema before any Markdown is produced (matches `wardeniq`).
4. **Acceptance-Criteria-first grounding** — AC is the primary source of expected results; description is supporting context.
5. **Single-prompt pipeline shape** — fetch → normalize → prompt → validate → render, as the reference implementation confirms.

### 6.3 What we reject / defer

| Idea | Why not now |
|---|---|
| RAG + Confluence retrieval | Requires extra credentials and an index; the Jira issue alone is sufficient for v1. |
| Writing results back to Jira (comments/sub-tasks) | Discovery answer: **read-only**. Keeps permissions minimal. |
| MCP / function-calling architecture | Adds moving parts; a linear script pipeline is deterministic and simpler. |
| Executable Playwright test output | Out of scope — we produce a Markdown plan, not runnable code. |

---

## 7. Open Research Items

- [x] Research OSS/GitHub prior art for Jira → test-case/test-plan generation.
- [x] Decide adopted vs deferred capabilities (see §6).
- [x] Confirm the target Jira site + project key prefix → `https://vandysengar.atlassian.net`; projects **KAN**, **SAM1** (see §8).
- [x] Acceptance Criteria custom field ID → **does not exist on this site**; description is the grounding source (see §8.3).
- [ ] Confirm the payload size of a real issue description and decide on a truncation threshold.
- [ ] Check whether the team has a mandated test-plan template / test-case ID scheme.
- [x] Decide on JSON validation approach — `response_format=json_object` + hand-rolled schema validation (no extra dependency).

---

## 8. Live Verification Log — 2026-09-11 (BLAST Phase 2 · Link)

All checks run from `tools/verify_link.py` against the real credentials in `.env`.
**Result: ALL LINKS HEALTHY.**

### 8.1 Handshake results

| Check | Endpoint | Result |
|---|---|---|
| Jira auth | `GET /rest/api/3/myself` | ✅ PASS — authenticated as **Vandana** (`712020:0ebdd15e-bff2-4e26-b9d2-3f0bafe7e4ab`) |
| Jira fields | `GET /rest/api/3/field` | ✅ PASS — readable (but no AC field, see §8.3) |
| Groq models | `GET /openai/v1/models` | ✅ PASS — `openai/gpt-oss-120b` available (14 models total) |

**Confirmed working `curl` (replace `<TOKEN>`):**

```bash
curl -s -u "vandy.sengar@gmail.com:<TOKEN>" \
  -H "Accept: application/json" \
  "https://vandysengar.atlassian.net/rest/api/3/myself"
```

### 8.2 Projects & testable issues discovered

`GET /rest/api/3/project/search` returns two projects:

| Key | Name | Type |
|---|---|---|
| `KAN` | VWO | software |
| `SAM1` | Timeline Tracking Initiatives | software |

Real issues available for testing (via `GET /rest/api/3/search/jql?jql=project=<KEY>`):

| Project | Issues | Notes |
|---|---|---|
| `KAN` | KAN-1 (Feature), KAN-2 (Task), KAN-3 (Subtask) | Small sample; all have descriptions |
| `SAM1` | SAM1-1 … SAM1-9 | Mostly Epics (Timeline Tracking); all have descriptions |

**Recommended first live test key: `SAM1-1`** ("Define Project Timeline Framework") — an Epic with a real description.

**Search endpoint note:** Jira Cloud has moved off the legacy `GET /rest/api/3/search`; use
`GET /rest/api/3/search/jql?jql=...` instead. The legacy route returns 410 Gone.

### 8.3 ⚠️ No Acceptance Criteria field on this site

`/rest/api/3/field` was scanned for any field whose name matches `acceptance`, `definition of done`, or `dod`. **No match.** Consequences:

1. The `acceptance_criteria` key in the normalized issue schema (§1.2 of `LLM.md`) will **never be populated** on this site — it is now a *conditional* field, present only if such a field is later added.
2. **`description` (ADF-flattened) becomes the primary grounding source** for expected results, with `summary` as secondary context.
3. The prompt builder must therefore **not** assume AC exists; when it is absent, the plan's `risks` section should note the reduced grounding.
4. This resolves Open Question #2 in `task_plan.md` — not "blocked", but "field absent, fallback defined".

### 8.4 Other live findings

- **Inline comments break naive `.env` parsing.** The credentials were originally supplied in `.env.example` with a leading space and a trailing `# ...` comment after the token. Values must be written cleanly into `.env` — which is why `.env` is the canonical source and `.env.example` holds placeholders only.
- **Secrets were briefly in a committable file.** Real keys sat in `.env.example`, which is *meant to be committed*. They were moved into `.env`, `.env.example` restored to placeholders, and a `.gitignore` added covering `.env`, `.tmp/`, and `__pycache__/`.
- `DEFAULT_JIRA_KEY=` was supplied as `vandysengar`, which is not a valid issue key (it is a site/project-ish token). It is left empty; a real key like `SAM1-1` is required.

---

## 9. Phase 4 — Stylize Findings & Live Re-verification

### 9.1 ⚠️ The VWO (`KAN`) project has empty issue descriptions

The user confirmed their Jira space is **VWO**, which is the project with key **`KAN`**
(`GET /rest/api/3/project/KAN` → name `"VWO"`, type `software`).

All three issues in it — `KAN-1` (Feature), `KAN-2` (Task), `KAN-3` (Subtask) — have a
**description field that is present but contains an empty ADF document**. After flattening,
the description is empty.

Confirmed against the **raw** API response for `KAN-1` (not inferred from our own flattening):

```json
"description": { "type": "doc", "version": 1, "content": [] }
```

The only populated fields on `KAN-1` are `summary` ("Task 1"), `issuetype` ("Feature"), and
`status` ("To Do").

| Key | Summary | Issuetype | Flattened description | Grounding |
|---|---|---|---|---|
| `KAN-1` | Task 1 | Feature | *(empty)* | `low` |
| `KAN-2` | Task 2 | Task | *(empty)* | `low` |
| `KAN-3` | Subtask 2.1 | Subtask | *(empty)* | `low` |

**Consequences:**
1. Plans generated from `KAN` keys are `low` grounding and flagged as near-speculative — the
   tool handles this correctly and the model writes `"Not specified in the Jira issue."`
   rather than inventing detail.
2. For materially useful plans, the VWO issues need real descriptions written into them.
3. `SAM1-*` issues **do** have usable descriptions and remain the better demo target until then.

> **Empty-vs-absent:** an empty ADF document (`{"type":"doc","content":[]}`) flattens to `""`,
> which must be treated the same as a missing description. `normalize_issue` drops the key in
> both cases, so the grounding flag is correct.

### 9.2 Bug found and fixed — grounding flag conflated two sources

**Symptom:** the rendered plan reported `**Grounding** | Acceptance criteria + description`
on `SAM1-1`, a site that has **no Acceptance Criteria field at all**.

**Cause:** `normalize_issue` used a boolean-ish `low` / `acceptable` flag, and the renderer
treated anything that was not `low` as "has acceptance criteria". Since `SAM1-1` has a
description, it was flagged `acceptable` and the renderer overstated the grounding.

**Fix:** replaced with a **three-state** flag — `acceptance_criteria` / `description_only` /
`low` — documented in `SOP_fetch_issue.md` §7, mapped to plain language in the renderer, and
used to select the correct prompt note in `SOP_generate_plan.md` §3. This is a good example of
the constitution's governance rule working: SOPs updated before the code changed.

### 9.3 Validation retry verified in production

The live `KAN-1` run exercised the retry loop for real:

```
[*] Generating test plan with openai/gpt-oss-120b
[*] Plan failed validation — retrying once with a correction
[*] Validating and rendering Markdown
[OK] Test cases: 2
```

The first attempt produced output that failed validation (the issue has almost no content);
the corrective retry succeeded. This confirms the `PlanValidationError` → single-retry →
render path works against the real API, not just in fixtures.

### 9.4 Styling improvements delivered (Phase 4)

| Change | Detail |
|---|---|
| **At a Glance** block | Code-computed: case counts, positive/negative split, focus areas (deduped traceability, capped at 4), techniques applied, grounding quality, review status |
| **Test-case summary table** | Scannable `ID / Test case / Priority / Type / Technique` table before the detailed blocks |
| **Richer Details table** | Added issue summary, Jira deep link (`/browse/<KEY>`), and the model actually used |
| **Grounding in plain language** | Three-state mapping (see §9.2) |
| **At-a-glance low-grounding flag** | Renders `⚠️ Low — no description or acceptance criteria on this issue` |
| **README.md** | Setup, config contract, CLI + UI usage, grounding table, error handling |

### 9.5 Open item

- Write real descriptions into the VWO (`KAN`) issues, or confirm a different project is the
  intended target — see §9.1.
