# Jira AI Test Case Generator

A two-page Streamlit application that retrieves a Jira issue via the Jira REST API and uses a local LLM (Ollama) — with a Groq fallback — to generate anti-hallucination-grounded test cases and test plans from the ticket content.

## Features

- **Page 1 — AI Test Case Generator**: ChatGPT-like chat interface. Enter a request such as
  `Create positive and negative test cases for PROJ-123 using Boundary Value Analysis`.
  The app extracts the issue key, fetches the issue from Jira, and generates structured test cases
  grounded strictly in the retrieved content.
- **Page 2 — Jira & AI Configuration**: configure Jira URL/email/token, LLM provider (Ollama/Groq),
  Ollama URL/model, Groq key/model. Secrets are masked in the UI and stored in a gitignored `.env`.
  A "Validate Connection" button tests both Jira and the selected LLM provider.
- **Anti-hallucination policy**: the LLM may only use the Jira issue data and user instructions.
  Missing information is explicitly flagged as *Not specified in the Jira issue.*
- **Downloads**: generated results can be downloaded as Markdown, CSV, or Excel.
- **Provider verification**: Ollama availability is checked against `GET /api/tags` and Groq against
  the models list before any generation, with friendly error messages when a service or model is missing.

## Project Structure

```
LiveClass_Tasks/09Augusy_Tasks/Task_02_Local_TestCase_Generator/
├── src/
│   ├── app.py                    # Streamlit entry point (two pages)
│   ├── config_manager.py         # .env load/save, validation, legacy alias support
│   ├── jira_client.py            # Jira REST client, ADF flattening, error mapping
│   ├── llm_client.py             # Ollama + Groq via OpenAI-compatible SDK
│   ├── prompt_builder.py         # Grounded prompt construction
│   ├── test_case_generator.py    # Orchestration pipeline
│   ├── output_exporter.py        # Markdown/CSV/Excel export
│   ├── errors.py                 # Domain exceptions
│   ├── utils.py                  # Logging redaction, markdown table parser
│   ├── templates/testcase_creator.md   # Base generation template
│   ├── tests/                    # pytest suite (all HTTP mocked)
│   ├── .env                      # Credentials (gitignored, never commit)
│   └── .env.example              # Documented keys
└── templates/testcase_creator.md # Base generation template
```

## Setup

1. Install Python 3.10+.
2. Install dependencies:

   ```bash
   cd src
   pip install -r requirements.txt
   ```

3. Create `.env` in `src/` (copy from `.env.example`) and fill in:

   ```ini
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_API_TOKEN=your-jira-api-token
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=gemma3:1b
   GROQ_API_KEY=your-groq-api-key
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

   Notes:
   - Groq model ids are namespaced, e.g. `openai/gpt-oss-120b` (include the org prefix).
   - The config manager also recognizes the legacy alias keys
     `Tesr_Case_Generator_Token` (→ `JIRA_API_TOKEN`) and `Local_TC_Generator_key`
     (→ `GROQ_API_KEY`) from earlier .env files.

4. Make sure Ollama is running with the configured model:

   ```bash
   ollama pull gemma3:1b
   ```

## Run

```bash
cd src
streamlit run app.py
```

Open the URL printed in the terminal (default `http://localhost:8501`).

## Usage

1. On the **AI Test Case Generator** page, type a request containing a Jira issue key:
   - `Create test cases for PROJ-123`
   - `Create a complete test plan for PROJ-123`
   - `Create security test cases including SQL injection for PROJ-123`
2. The app fetches the issue from Jira, verifies the selected LLM provider, generates the result,
   and shows download buttons (Markdown/CSV/Excel).
3. Use the **Jira & AI Configuration** page to change providers or credentials, then
   **Validate Connection** to confirm both Jira and the LLM are reachable.

## Tests

```bash
cd src
python -m pytest tests/ -v
```

All tests are mocked (no live network calls).

## Security Notes

- Credentials live only in the gitignored `src/.env`. Never commit real tokens.
- Secret values are masked in the UI and redacted from logs.
- Jira credentials are never included in LLM prompts.
- Downloaded files never contain secrets.
