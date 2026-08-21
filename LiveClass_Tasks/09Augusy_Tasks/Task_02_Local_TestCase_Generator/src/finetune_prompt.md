# RICEPOT Prompt: Jira-Based AI Test Case Generator Application

## R — Role

Act as a **Senior Python Application Architect, QA Automation Architect, and AI Integration Engineer** with 10+ years of experience in:

* Python application development
* Streamlit frontend development
* Jira REST API integration
* QA/Test Engineering and test-case design
* Local LLM integration using Ollama
* Groq API integration
* Secure credential and secret management
* Clean architecture and maintainable application design
* Enterprise-grade error handling and logging

Your responsibility is to design and implement a **simple, reliable, production-quality Python web application** that connects to Jira, retrieves Jira issue details, and uses an LLM to generate test cases and/or test plans from the Jira ticket.

Do not invent Jira data, requirements, APIs, fields, acceptance criteria, UI behavior, or test scenarios that are not supported by the retrieved Jira issue or user input.

---

## I — Instructions

Build a **two-page Python web application** with a simple, clean frontend. Use **Streamlit** unless there is a strong technical reason to use another lightweight Python frontend framework.

### 1. Application Pages

The application must contain exactly two primary screens.

### Page 1 — AI Test Case Generator

Provide a ChatGPT-like interface where the user can enter a natural-language request.

Example:

> Create test cases for Jira issue PROJ-123.

The application must:

1. Accept the user's Jira issue key, such as `PROJ-123`.
2. Accept natural-language instructions such as:

   * Create functional test cases.
   * Create positive and negative test cases.
   * Create test cases using Boundary Value Analysis.
   * Create test cases using Equivalence Partitioning.
   * Create security test cases.
   * Create SQL injection test cases.
   * Create a complete test plan.
3. Automatically retrieve the Jira issue from Jira using the configured Jira credentials.
4. Extract relevant Jira information, including only fields actually returned by Jira.
5. Provide the retrieved Jira information to the selected LLM.
6. Generate the requested test artifacts based strictly on the Jira content.
7. Display the generated result in the frontend.
8. Provide an option to copy or download the generated result.

The chat interface should support repeated requests without requiring the user to restart the application.

### Page 2 — Jira & AI Configuration

Provide a settings/configuration page containing fields for:

* Jira Base URL
* Jira Email
* Jira API Token
* LLM Provider
* Ollama Base URL
* Ollama Model
* Groq API Key
* Optional configuration required by the selected provider

The application must allow the user to save configuration securely.

Never hard-code Jira credentials, Jira tokens, Groq API keys, or other secrets in source code.

Prefer environment variables, `.env`, Streamlit secrets, or another secure configuration mechanism.

Passwords, API tokens, and API keys must be masked in the UI.

---

### 2. Jira Integration

Implement Jira integration using Jira's supported REST API.

The application must:

* Authenticate securely.
* Retrieve the requested Jira issue.
* Handle invalid Jira issue keys.
* Handle authentication failures.
* Handle authorization failures.
* Handle Jira API/network failures.
* Handle missing or unavailable fields gracefully.
* Return meaningful user-friendly error messages.
* Avoid exposing tokens, credentials, or sensitive response data in error messages.

Do not assume Jira fields exist unless they are actually returned by the API.

---

### 3. LLM Integration

The primary LLM provider must be **Ollama**.

The application must support an already-running local Ollama service.

Default configuration:

* Provider: Ollama
* Model: `gemma3:1b` or the exact locally installed model name supplied by the user
* Ollama URL: configurable, not hard-coded beyond a sensible default such as `http://localhost:11434`

The application must verify that the Ollama service and requested model are available before attempting generation.

### Groq Fallback

Provide **Groq API** as an optional fallback provider.

The user will provide the Groq API key through the configuration/settings mechanism.

Provider behavior:

1. Try Ollama when Ollama is selected.
2. If Groq is selected, use Groq.
3. Do not silently transmit Jira data to Groq unless the user explicitly selects Groq/fallback behavior.
4. Clearly indicate which LLM provider is being used.
5. Handle provider/API errors gracefully.

Do not expose API keys in logs, UI messages, generated output, or exceptions.

---

### 4. Anti-Hallucination Requirement

This is a mandatory requirement.

The LLM must follow a **strict evidence-based generation policy**.

It may use only information provided by:

* Jira issue data retrieved through the Jira API
* User instructions entered in the application
* Explicit configuration
* Any test-case/template files supplied to the application

The LLM must NOT:

* Invent requirements.
* Invent Jira fields.
* Invent acceptance criteria.
* Invent APIs.
* Invent URLs.
* Invent database tables.
* Invent error messages.
* Invent HTTP status codes.
* Invent UI elements.
* Invent business rules.
* Invent authentication mechanisms.
* Assume functionality that is not documented.
* Assume typical application behavior.

When required information is unavailable, explicitly state:

> `Not specified in the Jira issue.`

or

> `Not provided in the available information.`

Do not fill missing information using assumptions.

---

### 5. Test Case Generation

Support generation of structured test cases using, where applicable:

* Functional positive test cases
* Functional negative test cases
* Boundary Value Analysis
* Equivalence Partitioning
* Security test cases
* SQL Injection test cases
* Validation test cases
* Integration test cases
* Regression test cases
* Error-handling scenarios
* Permission/authorization scenarios
* Test data requirements
* Preconditions
* Steps to reproduce
* Expected results

Only generate a test category when it is relevant to the Jira requirement or explicitly requested by the user.

---

### 6. Test Plan Generation

When the user requests a test plan, generate a structured test plan based only on Jira data.

Possible sections may include, only when supported by the source information:

* Objective
* Scope
* Out of Scope
* Requirements
* Test Strategy
* Test Scenarios
* Functional Testing
* Negative Testing
* Boundary Testing
* Equivalence Partitioning
* Security Testing
* Integration Testing
* Regression Testing
* Test Data
* Dependencies
* Risks
* Assumptions

Do not invent project-specific information.

---

### 7. Output Formats

Test cases should preferably be presented in a structured table containing fields such as:

| Test Case ID | Test Scenario | Preconditions | Test Data | Steps to Reproduce | Expected Result | Test Type | Priority |
| ------------ | ------------- | ------------- | --------- | ------------------ | --------------- | --------- | -------- |

Only include fields that are supported by the requested output or application requirements.

Allow generated results to be downloaded in at least one practical format such as:

* Markdown
* CSV
* Excel

Do not generate files containing secrets.

---

### 8. Application Architecture

Use a clean and maintainable project structure.

Prefer separation of responsibilities such as:

* `app.py` / Streamlit entry point
* Jira service/client
* LLM service
* Prompt/template service
* Configuration manager
* Test-case generator
* Utility/error-handling modules

Do not put all business logic into a single Streamlit file.

Use clear interfaces/functions/classes where appropriate so additional LLM providers can be added later.

---

### 9. Error Handling

Handle at minimum:

* Missing Jira URL
* Missing Jira email
* Missing Jira token
* Invalid Jira credentials
* Invalid Jira issue key
* Jira issue not found
* Jira permission denied
* Jira API timeout
* Jira network failure
* Ollama unavailable
* Ollama model unavailable
* Groq authentication failure
* Groq rate-limit/API failure
* Empty Jira description
* Empty user request
* Invalid configuration
* Unexpected API response

Errors should be understandable to a normal user and must not expose sensitive implementation details.

---

### 10. Security

Security is mandatory.

* Never hard-code secrets.
* Never print API tokens.
* Never log API keys.
* Mask secret values in the UI.
* Do not persist secrets in generated files.
* Validate external inputs.
* Avoid unsafe shell-command execution.
* Use secure HTTP/API practices.
* Prevent accidental leakage of Jira credentials to the LLM.
* Send only the Jira data required for test generation.
* Clearly separate configuration secrets from generated content.

---

## C — Context

The application is intended for QA engineers who want to generate test cases or test plans from Jira requirements without manually copying Jira ticket information into an AI tool.

The user will provide:

* Jira Base URL
* Jira Email ID
* Jira API Token
* Optionally a Groq API Key

The user already has a local Ollama installation running and has the required **Gemma 3 1B** model available locally.

The expected workflow is:

`User Request → Jira Issue Key → Jira REST API → Jira Requirement Data → Selected LLM → Generated Test Cases/Test Plan → Display/Download`

Example interaction:

> User: Create positive and negative test cases for PROJ-123 using Boundary Value Analysis and Equivalence Partitioning.

The application retrieves `PROJ-123`, extracts the relevant requirement information, sends the verified Jira content plus the user's instruction to the selected LLM, and displays structured test cases.

The application should remain simple and easy to run locally.

---

## E — Example

### Example User Request

```text
Create test cases for Jira issue PROJ-123.

Generate:
1. Functional positive test cases
2. Functional negative test cases
3. Boundary Value Analysis
4. Equivalence Partitioning
5. Security test cases

Include:
- Test Case ID
- Scenario
- Preconditions
- Test Data
- Steps to Reproduce
- Expected Result
- Priority
- Test Type

Do not make assumptions. If information is missing from Jira, mention "Not specified in Jira".
```

### Example Internal Processing

```text
1. Validate Jira issue key.
2. Retrieve Jira issue using Jira REST API.
3. Extract available requirement information.
4. Build a grounded prompt containing:
   - Jira issue data
   - User request
   - Anti-hallucination rules
5. Send prompt to Ollama/Groq.
6. Validate the generated response.
7. Display the result as a structured table.
8. Allow Markdown/CSV/Excel download.
```

### Example Grounding Rule

```text
Jira Requirement:
"Password must contain at least 8 characters."

Valid tests:
- 7 characters
- 8 characters
- 9 characters

Invalid assumption:
- Password must contain uppercase letters.

Reason:
The uppercase requirement was not provided by Jira.
```

---

## P — Parameters

Use the following parameters as configurable values rather than hard-coded secrets.

### Jira

```text
JIRA_BASE_URL=<provided by user>
JIRA_EMAIL=<provided by user>
JIRA_API_TOKEN=<provided by user>
```

### Ollama

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<local Gemma 3 1B model name>
```

### Groq

```text
GROQ_API_KEY=<provided by user>
GROQ_MODEL=<configurable Groq model>
```

### Application

```text
FRONTEND=Streamlit
PRIMARY_LLM=Ollama
FALLBACK_LLM=Groq
```

Do not assume the exact Ollama or Groq model name if it has not been supplied.

Make model names configurable.

---

## O — Output

Generate a complete, runnable Python application.

The response must provide:

1. A production-quality project structure.
2. Complete Python source code.
3. `requirements.txt`.
4. Configuration example such as `.env.example` or Streamlit secrets configuration.
5. Jira API integration.
6. Ollama integration.
7. Groq fallback integration.
8. Streamlit two-page UI.
9. Secure credential handling.
10. Test-case generation workflow.
11. Test-plan generation workflow.
12. Markdown/CSV/Excel download capability.
13. Error handling.
14. README with setup and execution instructions.
15. Basic unit tests for the key services.

The application must be runnable locally with a simple command such as:

```bash
streamlit run app.py
```

Do not provide pseudo-code where executable code is expected.

Ensure imports, package names, function calls, configuration handling, and project structure are internally consistent.

Do not leave placeholder functions such as:

```python
pass
```

or:

```python
# implement this later
```

unless the functionality genuinely depends on information that the user has not yet supplied.

---

## T — Tone

Use a **technical, precise, implementation-focused, enterprise-quality tone**.

Prioritize:

* Correctness
* Security
* Maintainability
* Simplicity
* Explicit configuration
* Evidence-based test generation
* Clear error handling
* Minimal assumptions

Do not add unnecessary features.

Do not introduce databases, authentication systems, Docker, Kubernetes, microservices, or other infrastructure unless it is explicitly required.

Keep the application lightweight and suitable for local execution.

---

## Critical Constraints

These constraints have the highest priority:

1. **No hallucination of Jira requirements.**
2. **No hard-coded credentials or API tokens.**
3. **Ollama is the primary LLM provider.**
4. **Groq is an optional fallback/provider.**
5. **Jira data must be retrieved automatically from the Jira issue key.**
6. **The UI must be a simple two-page Streamlit application.**
7. **The user must be able to interact using a ChatGPT-like input interface.**
8. **Generated test cases must be traceable to the Jira requirement or explicit user request.**
9. **Missing information must be explicitly identified rather than assumed.**
10. **The final application must be runnable Python code, not conceptual pseudo-code.**
