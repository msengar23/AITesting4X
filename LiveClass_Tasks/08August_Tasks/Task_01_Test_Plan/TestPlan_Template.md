# Test Plan Template — IEEE 829 / ISO/IEC/IEEE 29119 Aligned

> **Usage:** This is a reusable, industry-level Test Plan template for QA. Replace every bracketed placeholder `[ ]` with project-specific values before issue. The template defines the structure, mandatory content, and review gates of a Test Plan; it is a planning document and **must not** contain executable test cases (those belong in a Test Case / Test Design Specification repository).

| Field | Value |
|---|---|
| **Test Plan ID** | `[TP-<PROJECT>-<SEQ>]` e.g., `TP-AUTH-001` |
| **Project Name** | `[ ]` e.g., Wingify / VWO Login Page Authentication |
| **Application Under Test (AUT)** | `[ ]` e.g., `https://app.vwo.com/#/login` |
| **Test Plan Version** | `[x.y]` |
| **Document Status** | `[ ] Draft / Under Review / Approved` |
| **Author** | `[QA Lead / QA Automation Tester]` |
| **Reviewers** | `[Project Manager, Dev Lead, DevOps, Product Owner]` |
| **Approvers** | `[ ]` |
| **Standards Reference** | IEEE 829-1998, ISO/IEC/IEEE 29119-2, ISO 25010 (quality model) |
| **Planned Start / End Date** | `[YYYY-MM-DD] / [YYYY-MM-DD]` |

---

## 1. Document Control

### 1.1 Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1 | `[ ]` | `[ ]` | Initial draft created |
| 1.0 | `[ ]` | `[ ]` | Baseline approved for execution |

### 1.2 Distribution List

| Recipient | Role | Purpose |
|---|---|---|
| `[ ]` | Project Manager | Approval, milestone sign-off |
| `[ ]` | QA Team | Execution reference |
| `[ ]` | Dev Lead / DevOps | Environment & defect coordination |

---

## 2. Introduction

### 2.1 Purpose

Define the testing goals, scope, strategy, resources, schedule, and acceptance conditions for the `[AUT]`. This Test Plan is the controlling document for all test activities and is used for review and approval by the `[Project Manager]`.

### 2.2 Scope of the Document

Covers all planned test phases (component → integration → system → regression → acceptance), test types, entry/exit criteria, environment, automation, defect management, and reporting for the release scope defined in Section 5. It does not contain test case steps.

### 2.3 References

| Ref | Document / Standard |
|---|---|
| [R1] | IEEE 829-1998 — Standard for Software Test Documentation |
| [R2] | ISO/IEC/IEEE 29119 — Software Testing Standards |
| [R3] | ISO/IEC 25010 — Systems and software Quality Requirements and Evaluation |
| [R4] | Requirements Specification / PRD `[id]` |
| [R5] | Architecture / API contract documents `[id]` |

### 2.4 Terms, Definitions & Abbreviations

| Term | Definition |
|---|---|
| AUT | Application Under Test |
| SUT | System Under Test |
| NFR | Non-Functional Requirement |
| RTM | Requirements Traceability Matrix |
| IdP | Identity Provider (SAML/OIDC) |
| S1–S4 / P0–P3 | Defect severity / priority classifications (Sections 12.2–12.3) |

---

## 3. Application Under Test (AUT)

### 3.1 System Overview

`[Provide 2–3 sentences on the system, e.g.: The AUT is a Single Page Application (SPA) that authenticates users against backend authentication APIs. It must operate across Chrome, Firefox, Safari, and Edge on desktop, and iOS/Android mobile browsers.]`

### 3.2 Test Items

| ID | Test Item | Version/Build | Supplier |
|---|---|---|---|
| TI-01 | `[Login page / authentication module]` | `[ ]` | `[ ]` |
| TI-02 | `[Authentication API contract]` | `[ ]` | `[ ]` |

### 3.3 Test Data

`[Describe synthetic test data only — no production user data. e.g., valid/invalid email formats, boundary-length passwords, locked/unverified accounts, test IdP and OAuth accounts.]`

---

## 4. Test Objectives & Quality Targets

| Quality Attribute | Objective | Measurable Target |
|---|---|---|
| Functional Correctness | All in-scope requirements behave per specification | ≥ 98% scenario pass rate; zero open S1 defects |
| Compatibility | Cross-browser / cross-device parity | `[4 desktop browsers + 2 mobile platforms]` |
| Security | No exploitable authentication weakness | Zero unresolved Critical findings at exit |
| Performance | Acceptable response and load behaviour | `[P95 ≤ x s login API; page load ≤ y s]` |
| Accessibility | WCAG conformance | `[WCAG 2.1 AA checkpoint review]` |
| Defect Leakage | No high-severity defect to production | `[0 S1/S2 defects leaked]` |

---

## 5. Test Scope

### 5.1 In-Scope

- `[Functional requirements, e.g., email + password login, session management with configurable timeout, optional 2FA/MFA, enterprise SSO integration]`
- `[Non-functional: security, performance, accessibility, usability]`
- `[Cross-browser and mobile compatibility matrix]`

### 5.2 Out-of-Scope

- `[e.g., post-authentication product features, billing, native mobile apps, load testing beyond baseline]`
- Any item explicitly deferred via change control.

---

## 6. Test Strategy & Approach

### 6.1 Test Levels (V-Model / IEEE 829 Phases)

| Phase | Scope | Approach | Primary Owner |
|---|---|---|---|
| Component / Unit | Individual modules and validation logic | Code-level tests; QA reviews coverage | Developers |
| Integration | AUT ↔ APIs, redirect flows, session issuance | Contract tests (REST/graphQL) + E2E | QA + Dev |
| System | Full feature against requirements set | End-to-end functional execution | QA |
| Regression | All in-scope scenarios after each change | Re-run automated suite per release | QA |
| Acceptance (UAT) | Business sign-off | Scripted scenarios from the RTM | Product Owner |

### 6.2 Test Types & Techniques

| Test Type | Technique | Primary Tools |
|---|---|---|
| Functional | Black-box: equivalence partitioning, boundary value analysis, error guessing, decision-table | `[Playwright + API scripts]` |
| UI / Visual | Layout, branding, responsive breakpoints, visual diff | `[Playwright visual regression]` |
| Cross-Browser / Device | Parallel execution on real devices | `[Playwright matrix + BrowserStack]` |
| API | Contract, status codes, error payloads, auth flows | `[Postman/Newman, REST Assured]` |
| Security | Credential validation, session cookie flags, rate limiting, brute-force, SSO/OAuth token validation | `[OWASP ZAP, Burp Suite (optional)]` |
| Performance | Load, latency, concurrency sanity | `[K6 / JMeter]` |
| Accessibility | WCAG 2.1 AA spot checks (labels, contrast, keyboard) | `[axe-core / Lighthouse]` |
| Usability / Exploratory | Unscripted testing, UX heuristics | Manual |

### 6.3 Test Design Techniques

- **Equivalence Partitioning** — valid/invalid input classes (email format, password policy).
- **Boundary Value Analysis** — min/max lengths, edge-case inputs.
- **State Transition** — session states: active → idle → expired → re-authenticated.
- **Decision Table** — combinations of auth method × credential validity × account state.
- **Error Guessing / Exploratory** — heuristic risk-based scenarios.

### 6.4 Execution Flow

1. **Preparation** — environment, test data, smoke check.
2. **Smoke Testing** — core path works on the full browser matrix.
3. **Functional Execution** — scenario priority order P0 → P1 → P2 (RTM, Section 15).
4. **Cross-Browser / Mobile Execution** — full scenario set on device matrix.
5. **Non-Functional Execution** — security, performance, accessibility.
6. **Regression & Sign-Off** — full suite re-run; exit criteria verified; PM approval.

### 6.5 Test Data Management

- Synthetic accounts only; no production data.
- Versioned, reusable test datasets; API-driven seeding where possible.
- Cleanup and masking policies defined by the Test Environment Owner.

---

## 7. Entry & Exit Criteria

### 7.1 Test Preparation Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Test Plan approved | Test scenarios and RTM baselined |
| Environment provisioned & stable | Test data created and verified |
| External accounts (SSO/OAuth/2FA) provisioned | Smoke test passed on all target browsers |

### 7.2 Functional Testing (System Test) Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Build deployed to test environment | 100% of P0/P1 scenarios executed |
| Smoke test passed | ≥ `[98]`% pass rate |
| Test data available | No open S1 defects; S2 workarounds approved |

### 7.3 Cross-Browser / Mobile Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Functional testing stable | All scenarios pass on `[4 desktop + 2 mobile]` platforms |
| Device cloud confirmed | No unresolved S1/S2 platform-specific defects |

### 7.4 Non-Functional Testing Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Feature freeze in place | Security scan clean; no Critical findings open |
| Performance baseline available | `[P95]` within agreed baseline |
| — | Accessibility blockers fixed or formally accepted |

### 7.5 Regression & Release Exit Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Defects fixed and verified | Full regression suite ≥ `[98]`% pass |
| Code freeze in place | Zero open S1/S2 defects |
| UAT environment ready | UAT signed off by Product Owner |
| — | Test Summary Report approved; PM release sign-off |

---

## 8. Test Environment

### 8.1 Hardware & Software

| Component | Specification |
|---|---|
| Desktop Browsers | `[Chrome/Firefox/Edge latest 2 stable; Safari latest 2]` |
| Mobile Browsers | `[iOS Safari, Android Chrome — real devices]` |
| Operating Systems | `[Windows 11, macOS latest, iOS 16+, Android 13+]` |
| Viewports | `[1920×1080, 1366×768, 768×1024, 375×667, 390×844]` |

### 8.2 Configurations

- Production-like environment with valid TLS/HTTPS.
- Test tenant with provisioned accounts (valid, invalid, locked, unverified).
- Test IdP (SAML/OIDC), OAuth test client, and FIDO2/passkey test tooling.
- Documented API endpoints for contract testing.

### 8.3 Tools

| Tool | Purpose |
|---|---|
| `[Playwright]` | UI automation, cross-browser execution |
| `[BrowserStack / Sauce Labs]` | Real-device cloud |
| `[Postman / Newman]` | API contract testing |
| `[OWASP ZAP]` | Security scanning |
| `[K6 / JMeter]` | Performance baseline |
| `[Jira / Xray]` | Test management, defect tracking |
| `[Allure / ReportPortal]` | Reporting |
| `[Git + CI (GitHub Actions/Jenkins)]` | Automation pipeline |

### 8.4 Access & Support

`[Environment owner, credentials, and support SLA for the test environment.]`

---

## 9. Test Schedule & Estimation

| Phase | Activity | Effort (person-days) | Milestone |
|---|---|---|---|
| P1 | Planning, scenario design, RTM | `[3]` | Test Plan approved |
| P2 | Automation framework & smoke scripts | `[5]` | Framework ready |
| P3 | Functional execution + regression | `[6]` | Execution report |
| P4 | Cross-browser / mobile | `[4]` | Device matrix report |
| P5 | Non-functional (security/perf/accessibility) | `[3]` | NFR report |
| P6 | Defect fixes, re-testing | `[4]` | Defect closure |
| P7 | Summary report & sign-off | `[2]` | Release sign-off |

**Total:** `[~27 person-days]` (parallelizable across 2–3 resources).

**Key Dependencies:** environment availability, external account provisioning, configuration freeze.

---

## 10. Roles & Responsibilities (RACI)

| Role | Test Plan | Test Design | Execution | Automation | Defect Fix | Acceptance |
|---|---|---|---|---|---|---|
| QA Lead / Automation Tester | A/R | R | R | R | — | C |
| Project Manager | A | C | I | I | — | A |
| QA Analyst / Manual Tester | C | C | R | I | — | C |
| Developer (Frontend/Backend) | C | C | C | C | R | C |
| DevOps / Environment Owner | I | — | C | C | I | — |
| Product Owner | C | C | I | — | — | R |
| Security Specialist | C | — | R | I | — | — |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

## 11. Test Automation Plan

### 11.1 Automation Scope

- **In-Scope:** core login flows, validation/error assertions, session persistence, redirect flows, cross-browser smoke and regression, visual regression.
- **Manual:** penetration testing, exploratory/usability, complex MFA flows.

### 11.2 Framework & Tooling

- Framework: `[Playwright (TypeScript) + Page Object Model]`
- Data: environment-seeded synthetic accounts; API-driven setup.
- Reporting: `[Allure/HTML]` with failure artifacts (video, screenshot, trace).

### 11.3 CI/CD Integration

- Trigger: on merge to `[test branch]`; scheduled nightly regression.
- Artifacts published to CI; flaky-network retry policy (max `[2]` retries with logging).
- Anti-bot pacing applied between login attempts to avoid lockout/rate limiting.

### 11.4 Automation Governance

- Estimated automation coverage: `[60–70%]` of functional suite in first cycle.
- Page objects and helpers shared; no test logic duplication; code review required.

---

## 12. Defect Management

### 12.1 Defect Lifecycle

```
FOUND (tester logs in Jira)
   ▼
TRIAGE (Lead/PM validates; assigns severity & priority)
   ▼
ASSIGNED (developer)
   ▼
IN PROGRESS
   ▼
FIXED / READY FOR VERIFICATION
   ▼
VERIFIED (re-test on latest build)
   ├─ PASS ─▶ CLOSED
   └─ FAIL ─▶ REOPENED ──────────┐
   ▼                             │
Not a defect / Duplicate / Won't Fix / Deferred (triage decision, reason required)
```

**Rules:** every defect includes title, environment, browser/OS, steps to reproduce, expected vs actual, severity, priority, and attachments (logs, screenshots, HAR). Deferred defects require PM + PO sign-off.

### 12.2 Severity Classification

| Severity | Label | Definition | Example |
|---|---|---|---|
| S1 | Critical/Blocker | System unusable; security vulnerability; data loss; core auth failure | Sign-in fails for all valid users; credential exposure |
| S2 | High | Major function broken, no workaround | Session persistence broken; SSO flow fails |
| S3 | Medium | Deviates from spec, workaround available | Wrong error message text |
| S4 | Low | Cosmetic / UI polish | Spacing or alignment issues |

### 12.3 Priority Classification

| Priority | Label | Definition |
|---|---|---|
| P0 | Urgent | Fix immediately; blocks release |
| P1 | High | Fix in current sprint/release |
| P2 | Medium | Fix in next release |
| P3 | Low | Fix when convenient |

### 12.4 Reporting Cadence

- Daily triage during execution; weekly summary to PM (open count by severity, aging, reopened rate); release-readiness review of open S1/S2 before exit.

---

## 13. Test Metrics & Reporting

| Metric | Definition | Target |
|---|---|---|
| Execution Progress | % scenarios executed vs planned | 100% by phase exit |
| Pass Rate | % passed vs executed | ≥ `[98]`% |
| Defect Density | defects per scenario/requirement | `[ ]` |
| Defect Age | open days per severity | `[ ]` |
| Reopened Rate | % reopened after verification | `[< 10%]` |
| Automation Coverage | % automated vs total | `[60–70]`% |
| Defect Leakage | S1/S2 reaching production | `[0]` |

---

## 14. Risk, Assumptions, Constraints & Dependencies

### 14.1 Risk Register

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | `[e.g., MFA config unavailable]` | `[Incomplete coverage]` | `[Medium]` | `[Schedule follow-up; confirm access]` | `[ ]` |
| R2 | `[External IdP/test accounts delay]` | `[Environment slippage]` | `[Medium]` | `[Pre-provision; mock IdP offline]` | `[ ]` |
| R3 | `[Rate limiting / anti-bot on auth]` | `[Automation flakiness]` | `[Medium]` | `[Test-tenant allowances; pacing]` | `[ ]` |
| R4 | `[Undocumented timeout/session config]` | `[Ambiguous expectations]` | `[Medium]` | `[Freeze config before execution]` | `[ ]` |

### 14.2 Assumptions

- `[List verified facts and stated assumptions, each tagged: Verified / Inference (low confidence) / Insufficient information to determine.]`

### 14.3 Constraints

- `[e.g., test-only environments only; no production data; fixed release date; limited device budget.]`

### 14.4 Dependencies

- `[Environment readiness, external account provisioning, configuration freeze, API contract availability.]`

---

## 15. Requirements Traceability Matrix (RTM)

Maps each requirement to its scenario group, priority, and phase. **Individual test cases are detailed in the Test Case repository**, not in this plan.

| Req ID | Requirement | Scenario Group / Coverage | Priority | Phase | Verification Source |
|---|---|---|---|---|---|
| RQ-01 | `[e.g., Primary authentication (email + password)]` | `[TC-AUTH-01..NN]` | P0 | Functional + Regression | `[Verified / Inference]` |
| RQ-02 | `[Session management w/ configurable timeout]` | `[TC-SESS-01..NN]` | P0 | Functional + NFR | `[ ]` |
| RQ-03 | `[Optional MFA/2FA]` | `[TC-MFA-01..NN]` | P1 | Functional (follow-up) | `[ ]` |
| RQ-04 | `[Enterprise SSO]` | `[TC-SSO-01..NN]` | P0 | Functional + Integration | `[ ]` |
| RQ-05 | `[Security (NFR)]` | `[TC-SEC-01..NN]` | P0 | Security | `[ ]` |
| RQ-06 | `[Performance (NFR)]` | `[TC-PERF-01..NN]` | P1 | Performance | `[ ]` |
| RQ-07 | `[Accessibility (NFR)]` | `[TC-ACC-01..NN]` | P2 | Accessibility | `[ ]` |
| RQ-08 | `[Compatibility matrix]` | `[TC-COMPAT-01..NN]` | P0 | Cross-Browser + Mobile | `[ ]` |

*No orphan scenarios: every scenario group maps back to a requirement, and every requirement to a scenario group.*

---

## 16. Test Deliverables

| # | Deliverable | Owner | Due |
|---|---|---|---|
| 1 | Test Plan (this document) | QA Lead | Plan approval |
| 2 | Test Scenarios & Case Repository (linked from RTM) | QA Team | Pre-execution |
| 3 | Test Data Sheet | Environment Owner | Pre-execution |
| 4 | Automated Test Suite | QA Automation | Framework ready |
| 5 | Test Execution Report (per phase) | QA Team | Per phase exit |
| 6 | Defect Report & Metrics | Test Lead | Weekly |
| 7 | Security Scan Report | Security Specialist | NFR phase |
| 8 | Performance Report | Performance Tester | NFR phase |
| 9 | Accessibility Report | QA Team | NFR phase |
| 10 | Cross-Browser/Device Matrix Report | QA Team | Cross-browser phase |
| 11 | Test Summary Report (with release recommendation) | Test Lead | Release exit |
| 12 | Sign-off Checklist | PM / PO | Release exit |

---

## 17. Templates & Standards

- **Documentation standard:** IEEE 829-1998 aligned with ISO/IEC/IEEE 29119 terminology (Test Plan, Test Design, Test Procedure, Test Log, Test Summary Report).
- **Test Case template:** Requirement ID, scenario ID, priority, precondition, test data, steps, expected result, status, defect link.
- **Defect template:** Summary, environment, severity (S1–S4), priority (P0–P3), reproduction steps, expected vs actual, attachments.
- **Naming conventions:** Scenario IDs `TC-<AREA>-<NN>`; defect IDs from tracker sequence.
- **Version control:** All test artifacts under Git; plan changes via version bump with change log.
- **Review cycle:** Test Plan → PM; Test Summary Report → PM & PO before release sign-off.

---

## 18. Approvals

| Role | Name | Signature / Date |
|---|---|---|
| QA Lead (Author) | `[ ]` | `[ ]` |
| Project Manager | `[ ]` | `[ ]` |
| Product Owner | `[ ]` | `[ ]` |
| DevOps / Environment Owner | `[ ]` | `[ ]` |

---

## 19. Appendix A — Verification & Anti-Hallucination Protocol

Every assertion in this plan and in its downstream test cases is labelled with one of:

| Label | Meaning |
|---|---|
| **Verified** | Directly traceable to a provided source (PRD, screenshot, API doc, run result) with a source tag, e.g., `[DOM]`, `[RUN]`, `[SS]`, `[PRD]` |
| **Inference (low confidence)** | Logical deduction that must be confirmed before execution |
| **Insufficient information to determine** | Cannot be asserted from available input — record as an open question, do not guess |

**Process (mandatory, deterministic):**

1. Extract verifiable facts from the provided input only.
2. List unknown or missing information.
3. Generate output strictly from Step 1 facts; label every inference.
4. Self-check for hallucinations or contradictions.
5. Configuration-dependent values (lockout thresholds, rate limits, timeouts, HTTP status codes, cookie flags) are recorded as *verify-and-document* checks, never asserted as fact.
6. If any step cannot be completed, stop and report why.

**Self-Validation Check:**

- [ ] All UI elements / behaviours asserted are present in the provided source.
- [ ] No error codes, endpoints, or features invented.
- [ ] Every inference labelled `Inference (low confidence)`.
- [ ] No contradictions between sections; discrepancies escalated as assumptions.
- [ ] Missing information flagged as dependencies / open questions.

---

## 20. Appendix B — Reference Use Case (Wingify/VWO Login)

> Exemplar only — replace with project data. If the AUT is the VWO/Wingify login page (`https://app.vwo.com/#/login`), the following verified facts were captured from the login screen and should drive Section 3 and 15 content:

- URL resolves to `app.wingify.com/#/login` with a transition notice from `app.vwo.com` **[Verified]**
- Email address + password fields, visibility toggle, "Forgot Password?" link, "Remember me" checkbox, "Sign in" button **[Verified]**
- Alternative entry points: "Sign in with Google", "Sign in using SSO", "Sign in with Passkey" **[Verified]**
- No MFA/2FA UI visible on the initial screen; MFA flow surfaces post-credential-verification **[Verified absence → treat as Inference for scheduling]**
- Session timeout values, redirect destinations, and auth API endpoints are not published **[Insufficient information → verify and document]**
