# Task_03_Test_Case — Wingify/VWO Login Test Cases

Jira-format login page test cases for the Wingify/VWO platform, developed under the **Anti-Hallucination rule**.

## File

| File | Description |
|---|---|
| `TestCases_Login_VWO.md` | 98 test cases in Jira table format with verification status per case |

## Coverage

| Category | Count |
|---|---|
| Functional — Verified (live observation) | 14 |
| Functional — Negative | 7 |
| Boundary Value Analysis | 18 |
| Security — Injection (SQLi/XSS/Command) | 11 |
| Security — Auth & Session | 14 |
| Usability & Accessibility | 12 |
| API — SSO & Auth | 12 |
| Compatibility & Performance | 10 |
| **Total** | **98** |

## Anti-Hallucination Method

- **Verified** rows are traceable to live DOM capture, screenshots, and actual test runs (tagged `[DOM]` / `[SS]` / `[RUN]`)
- Every unobserved assertion is labeled `Inference (low confidence)` or `Insufficient information to determine`
- Configuration-dependent values (lockout thresholds, rate limits, cookie flags, API schemas) are framed as "verify and document" rather than asserted as fact

## Table Format

`TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N)`
