# Taste — QA / Test Documentation Workflow
See [taste-—-qa-/-test-documentation-workflow/taste.md](taste-—-qa-/-test-documentation-workflow/taste.md)

- Formats test cases as Jira-board style tables with the exact column set: TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N). Confidence: 0.9
- Mandates comprehensive test-suite coverage for login/auth flows: negative cases (mandatory), boundary value analysis (critical), security cases (SQL injection, XSS, brute-force/lockout), usability/accessibility, and API authentication including SSO token flows. Confidence: 0.9
- Requires every test case to include numbered step-by-step reproduction steps and to be independently executable, with traceability (test case → requirement → risk) and suitability for both manual execution and automation scripting. Confidence: 0.85
- Expects test-case deliverables to close with a summary metrics table (total test cases, per-category breakdown, priority counts, automation-readiness counts). Confidence: 0.8
- Wants test data declared as synthetic test accounts only (no real user data) with explicit test parameters (target URL, auth methods, browser/mobile/screen-reader matrices). Confidence: 0.7
- When asked to analyse an existing test suite, expects a coverage-gap analysis against the actual application surface and proactive addition of missing cases: every visible auth option (Google SSO, SSO email form, Passkey, Forgot Password flow, links/logo), advanced security (CSRF, open redirect, clickjacking, timing enumeration, credential stuffing, logout/session invalidation, security headers), cross-browser/device compatibility matching the stated matrix, and performance/reliability (load, latency, slow network, concurrency). Confidence: 0.75
- Follows a strict anti-hallucination rule for QA/test deliverables: only assert facts traceable to provided input (PRD, API docs, logs, screenshots, test data, user input), explicitly label every inference as "Inference (low confidence)", respond "Insufficient information to determine" for missing/unclear info rather than guessing, never assume default or "typical" system behavior, and keep output deterministic and repeatable. Confidence: 0.95
- Prefers outputs to follow a deterministic, structured process (extract verified facts → list unknowns → generate output → self-check for hallucinations/contradictions), and to stop and report why if any step cannot be completed. Confidence: 0.9
- Applies the anti-hallucination rule to test-case creation and audits of existing suites: every test case row is labeled with its verification status (Verified / Inference (low confidence) / Insufficient information to determine), verified assertions carry traceable source tags (e.g., [DOM], [RUN], [SS]), and unverified configuration-dependent values (lockout thresholds, rate limits, timeouts, HTTP status codes, cookie flags) are reframed as "verify and document" checks rather than asserted as fact. Confidence: 0.85

# Taste — Communication & Workflow

- Communicates in short, terse instructions (e.g., "filled manually credential in .env file now continue"; "analyse these Test CAses is there any other testcases which has been added in this then add those also") and expects the agent to proceed autonomously without re-confirming or asking questions. Confidence: 0.7
- Provides highly structured task briefs for documentation work using labeled sections (Role, Instructions, Context, Example, Parameters, Output, Tone) that must be followed exactly. Confidence: 0.7
- Expects the agent to create/update README.md files for every folder in the repository (not just the root) as part of repo maintenance. Confidence: 0.8
- Expects the agent to commit and push completed work to the user's GitHub repository autonomously (per user-provided repo URL) as the final step of a task. Confidence: 0.75

# Taste — QA / Test Automation Framework
See [qa-test-automation/taste.md](qa-test-automation/taste.md)
