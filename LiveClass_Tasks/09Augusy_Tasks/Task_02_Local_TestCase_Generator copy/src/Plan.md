# Plan — Task 02: Jira-Based AI Test Case Generator (Streamlit + Ollama/Groq)

## Goal
Build a runnable two-page Streamlit app that retrieves a Jira issue via REST API and generates anti-hallucination-grounded test cases / test plans using Ollama (primary) or Groq (fallback), with Markdown/CSV/Excel download. Based on `finetune_prompt.md` (RICEPOT spec).

## Decisions (confirmed with user)
1. **Config**: `.env` file in `src/` (python-dotenv) as the single source of truth. User credentials written into `src/.env` (gitignored). Settings page reads/edits the same `.env` at runtime. `.env.example` documents the keys.
   - Real credentials provided by user (stored in `src/.env`, never committed):
     - `JIRA_BASE_URL=https://mamtasingh2326jira.atlassian.net`
     - `JIRA_EMAIL=mamtasingh2326+jira@gmail.com`
     - `JIRA_API_TOKEN=ATATT3x...` (masked; full value in `src/.env`)
     - `GROQ_API_KEY=gsk_4lA...` (masked; full value in `src/.env`)
     - `LLM_PROVIDER=ollama`, `OLLAMA_BASE_URL=http://localhost:11434`, `OLLAMA_MODEL=gemma3:1b`, `GROQ_MODEL=llama-3.3-70b-versatile`
2. **LLM calls**: OpenAI-compatible SDK (`openai` package) for both Ollama (`base_url=http://localhost:11434/v1`) and Groq (`https://api.groq.com/openai/v1`). One client code path.
3. **Jira**: Read-only retrieval only (GET issue). Jira Cloud API `/rest/api/3` with fallback to `/rest/api/2`, Basic auth (email + API token).
4. **Downloads**: Markdown + CSV + Excel (`pandas` + `openpyxl`).

## Project Structure (all under `LiveClass_Tasks/09Augusy_Tasks/Task_02_Local_TestCase_Generator/`)
```
src/
├── app.py                    # Streamlit entry — 2 pages via sidebar radio
├── config_manager.py         # Load/save .env, masked UI values, validation
├── jira_client.py            # requests-based REST client, ADF flattening, error mapping
├── llm_client.py             # OpenAI-compatible client (Ollama + Groq), provider/model verification
├── prompt_builder.py         # Grounded prompt from templates/testcase_creator.md + anti-hallucination rules
├── test_case_generator.py    # Orchestrates: validate → fetch → build prompt → verify LLM → generate → parse
├── output_exporter.py        # .md / .csv / .xlsx exports + st.download_button helpers
├── errors.py                 # Domain exceptions with friendly user messages
├── utils.py                  # Logging setup with secret-redaction filter, markdown table parser
├── .env                      # GITIGNORED — real credentials (user-provided)
├── .env.example              # Documented keys (committed)
├── .gitignore                # .env, __pycache__, logs
├── requirements.txt
├── README.md
└── tests/                    # pytest, all HTTP mocked
    ├── conftest.py
    ├── test_config_manager.py
    ├── test_jira_client.py
    ├── test_llm_client.py
    ├── test_prompt_builder.py
    └── test_output_exporter.py
```
`templates/testcase_creator.md` (already present at task root) is the base generation template; `prompt_builder` loads it from `Path(__file__).parent.parent / "templates"`.

## Key Implementation Details

### config_manager.py
- Keys: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `LLM_PROVIDER` (ollama|groq), `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `GROQ_API_KEY`, `GROQ_MODEL`.
- `ConfigManager(env_path=None)` — default path `src/.env`; loads via `python-dotenv`. Methods: `get_all()`, `get(key)`, `save(updates)` (writes .env atomically, preserving comments), `is_configured(provider)`, `validate()`.
- Settings page writes `src/.env` then `st.rerun()`; note shown if restart needed.
- Defaults: `OLLAMA_BASE_URL=http://localhost:11434`, `OLLAMA_MODEL=gemma3:1b`, `GROQ_MODEL=llama-3.3-70b-versatile` (configurable, never assumed exact).

### jira_client.py
- `JiraClient(base_url, email, api_token)` with `requests.Session`, Basic auth, timeout 15s.
- `get_issue(key) -> dict`: validates key with regex `^[A-Z][A-Z0-9]*-\d+$`; GETs `/rest/api/3/issue/{key}?fields=<standard list>`; falls back to `/rest/api/2` on 404 of the endpoint.
- Flattens Jira description ADF (Atlassian Document Format) to plain text via a small `_flatten_adf` walker; extracts only fields actually present: summary, description, status, priority, issuetype, labels, components, project, reporter, assignee, created/updated, plus any custom field whose name contains "acceptance" / "definition of done".
- Error mapping (in `errors.py`): 401 → `JiraAuthError`, 403 → `JiraPermissionError`, 404 → `JiraNotFoundError`, timeout → `JiraTimeoutError`, connection errors → `JiraNetworkError`, missing key → `ConfigError`. Messages user-friendly, never echo tokens.

### llm_client.py
- `LLMClient(provider, config)` using `openai.OpenAI`:
  - Ollama: `OpenAI(base_url=f"{OLLAMA_BASE_URL}/v1", api_key="ollama")`
  - Groq: `OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)`
- `verify_available()`: Ollama → GET `/api/tags` (requests) to confirm service + model present; Groq → `client.models.list()` to confirm key + model. Friendly errors: `LLMUnavailableError`, `LLMModelNotFoundError`, `LLMAuthError`, `LLMRateLimitError`.
- `generate(messages) -> str`: `chat.completions.create(model=..., messages=..., temperature=0.2)`. Returns provider + model label for UI display.

### prompt_builder.py
- `build_prompt(issue_data, user_request, template_path)` → `(system_prompt, user_prompt)`.
- System prompt: Senior QA role + strict anti-hallucination policy (from `finetune_prompt.md` §4 and `chapter_01/ANTI-HALLUCINATION.rules.md`): only use supplied Jira data + user input; missing info must be stated as "Not specified in the Jira issue." / "Not provided in the available information."; no invented fields/APIs/status codes/UI elements.
- User prompt: fills `templates/testcase_creator.md` placeholders — `[PASTE REQUIREMENTS HERE]` ← labeled Jira issue data (key, summary, description, fields), `[NUMBER]` ← count if user asked. No credentials ever included.

### test_case_generator.py
- `generate(user_message, config)`: extract issue key via regex `\b[A-Z][A-Z0-9]{1,9}-\d{1,6}\b` from the natural-language message; remaining text = instructions; validate config → fetch issue → verify provider → build prompt → generate → parse result.
- `parse_markdown_table(md) -> list[dict]` in `utils.py`: split lines, drop separator row, strip pipes; graceful fallback to raw markdown if unparseable.

### output_exporter.py
- `to_markdown(md)`, `to_csv(rows)`, `to_xlsx(rows)` (pandas + openpyxl, `BytesIO`). `render_download_buttons(...)` using `st.download_button` under each generated response.

### app.py (two pages, sidebar radio)
- **Page 1 — AI Test Case Generator**: ChatGPT-style via `st.chat_message` history (session_state) + `st.chat_input`. Example chips ("Create positive and negative test cases for PROJ-123 using BVA and EP"). On send: run generator, append assistant message showing provider/model used ("Generated by Ollama / gemma3:1b"), and download buttons. Repeated requests supported without restart.
- **Page 2 — Jira & AI Configuration**: form with masked password fields for secrets (`type="password"`), selects for provider, Save → `config.save()` + `st.rerun()`. A "Validate connection" button pings Jira and the selected LLM and reports status.
- Provider indicator always shown; clear error display via `st.error` from the error taxonomy.

### Security
- No hard-coded secrets in source; `.env` gitignored; masked UI inputs; logs redacted (a `SecretRedactionFilter` masks `JIRA_API_TOKEN` / `GROQ_API_KEY` / `Authorization` values in all log records); Jira credentials never included in prompts; downloads contain no secrets.

## Files That Already Exist (reuse)
- `src/finetune_prompt.md`, `src/prompt.md` — spec inputs (no changes).
- `templates/testcase_creator.md` — base generation template (no changes).
- `src/Plan.md` (empty) — after approval, this plan will be copied here.
- `src/.env` (exists, gitignored) — credentials written here at implementation start.
- `src/.gitignore` (created) — excludes `.env`, `.streamlit/secrets.toml`, `__pycache__`, logs.
- Root `.gitignore` already covers `.env`.

## requirements.txt
`streamlit`, `requests`, `openai`, `python-dotenv`, `pandas`, `openpyxl`, `pytest`

## Verification
1. `pip install -r requirements.txt`
2. `python -m pytest tests/ -v` — all mocked unit tests pass.
3. `streamlit run app.py` (runs locally; check both pages render, no import errors).
4. Live check with real credentials: confirm `ollama list` shows `gemma3:1b`, generate test cases for a real ticket on Page 1, verify download buttons produce valid .md/.csv/.xlsx, verify settings save + validate connection on Page 2.
5. Confirm no secrets appear in logs, UI, or downloaded files.

## Implementation Order
1. Scaffold: `.env` (credentials), `.env.example`, `requirements.txt`, dirs
2. `errors.py`, `utils.py`
3. `config_manager.py`
4. `jira_client.py`
5. `llm_client.py`
6. `prompt_builder.py`
7. `test_case_generator.py`, `output_exporter.py`
8. `app.py`
9. `tests/` + run pytest
10. `README.md`
11. Live verification with real Jira ticket + Ollama
12. Copy this plan to `src/Plan.md`
