# SOP — Fetch Jira Issue

**Layer:** 1 (Architecture) · **Tool:** `tools/fetch_jira_issue.py` · **Version:** 1.0 (2026-09-11)

---

## 1. Goal

Fetch a single Jira issue by key and normalize it into a **fixed, predictable JSON shape** for
downstream use. This stage is **deterministic** — no LLM involvement whatsoever.

## 2. Inputs

| Input | Type | Required | Source |
|---|---|---|---|
| `jira_key` | string | yes | CLI arg / UI field |
| `config` | Config | yes | `tools/config.py` (`.env`) |

**Input validation (before any network call):**
- Must match `^[A-Z][A-Z0-9]*-\d+$` (e.g. `SAM1-1`, `KAN-2`).
- Invalid → raise `JiraInvalidKeyError`. **No HTTP request is made.**

## 3. Endpoint

```
GET {JIRA_URL}/rest/api/3/issue/{key}
    ?fields=summary,description,status,priority,issuetype,labels,components,project,reporter,assignee,created,updated
```

- **Auth:** HTTP Basic `(JIRA_EMAIL, JIRA_API_TOKEN)`.
- **Headers:** `Accept: application/json`.
- **Timeout:** 15s.

> **Note:** the legacy `GET /rest/api/3/search` route is retired (410 Gone) on Jira Cloud.
> For listing issues use `GET /rest/api/3/search/jql?jql=...`. This SOP only fetches by key.

## 4. Tool Logic

```
1. validate_key(key)                    -> raise JiraInvalidKeyError on mismatch
2. GET /rest/api/3/issue/{key}?fields=  -> requests.get(timeout=15)
3. map HTTP status to a domain error    -> 401/403/404/>=400
4. parse JSON                           -> ValueError -> JiraNetworkError
5. _normalize_issue(data)               -> extract ONLY fields present
6. _flatten_adf(description)            -> plain text
7. return normalized dict
```

## 5. Normalization Rules

Extract only fields **actually present**. Absent fields are **omitted**, never null.

| Field | Rule |
|---|---|
| `key` | as-is |
| `summary` | as-is |
| `description` | **ADF → plain text** (see §6) |
| `status`, `priority`, `issuetype`, `project` | take `.name` |
| `reporter`, `assignee` | take `.displayName` |
| `labels` | array of strings as-is |
| `components` | map `[{name}]` → `[name]` |
| `created`, `updated` | ISO-8601 string as returned |
| `acceptance_criteria` | **only if** a discovered custom field exists (see §7) |

## 6. ADF Flattening (critical)

In API **v3**, `description` is **Atlassian Document Format** — a nested JSON tree, not a string.

```
walk(node):
  type == "text"      -> emit node.text
  type == "hardBreak" -> emit "\n"
  type in (paragraph, heading, listItem, codeBlock) -> emit "\n" after children
  recurse into node.content[]
```
Then collapse 3+ newlines → 2 and trim. Output is plain text safe to embed in a prompt.

## 7. Acceptance Criteria — conditional field

**Verified 2026-09-11:** the target site `vandysengar.atlassian.net` has **no**
Acceptance Criteria / DoD custom field. Therefore:

- `acceptance_criteria` will normally be **absent** from the normalized issue.
- The field name is discovered at runtime via `GET /rest/api/3/field` (names vary per site)
  and cached in `.env` as `JIRA_AC_FIELD` — never hardcoded.
- Downstream, **`description` is the primary grounding source**; `summary` is secondary.

### Grounding flag (three states — do not conflate)

`grounding` records **which fields the plan may legitimately be grounded on**. It must not
claim acceptance-criteria grounding when no AC field exists.

| `grounding` value | Condition | Meaning |
|---|---|---|
| `acceptance_criteria` | `acceptance_criteria` is present | Strongest grounding: AC primary, description supporting |
| `description_only` | no AC, but `description` present | Description is the **only** requirement source; risks must say so |
| `low` | neither AC nor description | No usable requirement content; the plan is near-speculative |

> **Superseded:** an earlier version used a boolean-ish `low`/`acceptable` flag, which caused the
> renderer to report "Acceptance criteria + description" on a site that has no AC field. The
> three-state flag above replaces it.

## 8. Edge Cases

| Case | Behaviour |
|---|---|
| Invalid key format | `JiraInvalidKeyError` — no network call |
| Issue does not exist | `JiraNotFoundError` (404) |
| No permission | `JiraPermissionError` (403) |
| Bad credentials | `JiraAuthError` (401) |
| Empty description | Omit the field; set `grounding: "low"` |
| Description is a plain string (v2-style) | Pass through unchanged — do not attempt ADF walk |
| Very large description | Truncate at `MAX_DESCRIPTION_CHARS` (default 12 000) and append `[…truncated]` |
| Timeout | `JiraTimeoutError` |
| Connection failure | `JiraNetworkError` |
| Non-JSON response | `JiraNetworkError` |

## 9. Output Contract

A dict matching `LLM.md` §1.2 (Normalized Issue Schema). This exact dict is the **only**
issue data that may reach the LLM.

## 10. Testability

`fetch_jira_issue.py` exposes pure helpers (`validate_key`, `flatten_adf`, `normalize_issue`)
that can be tested without network access, plus the network function that takes an injectable
`session` for stubbing.
