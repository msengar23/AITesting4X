## PROMPT:

Role -> You are a QA automation tester with 5 years of experience, You have a very good understanding of IT,  projects like ( https://app.vwo.com/#/login). You need to create a Test Plan, it should be industry-level test plan that we need to create.



I  -> Instructions

 - [Critical] - Define clear entry and exit criteria for each test phase.
- [Critical] - Include a defect management workflow and severity classification.
- [Mandatory] - Test Plan should follow IEEE standards and all phases of testing with entry and exit criteria,      tools for testing, scope of testing, environment for testing. 
Include a traceability matrix mapping requirements to test scenarios
- [Do]- Primary Authentication: Email and password-based login with secure validation
-  [Do]- Session Management: Secure session handling with configurable timeout periods 
- [Do]- Multi-Factor Authentication: Optional 2FA support for enhanced security.
 - [Do]- Single Sign-On (SSO): Enterprise SSO integration capabilities for organizational accounts
- [Don't] - Do not include actual test cases — this is a Test Plan, not test execution scripts.
- [Don't] - Do not make assumptions about VWO's internal architecture beyond what is publicly visible.
- [Generate] - Generate a  industry-level Test Plan for the VWO login page at https://app.vwo.com/#/login.



C -> Context
You are creating a test plan of https://app.vwo.com/#/login. VWO (Visual Website Optimizer) is a leading A/B testing and conversion optimization platform used by enterprises worldwide, it has:


The login page is a Single Page Application (SPA) built with a modern JavaScript framework. It communicates with VWO's backend authentication APIs. The page must work across Chrome, Firefox, Safari, and Edge on desktop, and mobile browsers on iOS and Android.





**P -> PARAMETERS**
The page must work across Chrome, Firefox, Safari, and Edge on desktop, and mobile browsers on iOS and Android.


O -> Output: Provide test plan in the format:
 
Objective: Defines testing goals and quality targets.
Scope: Specifies in-scope and out-of-scope features.
Test Strategy & Approach: Describes testing types, techniques, and execution flow.
Assumptions & Risks: Lists assumptions and potential risks with mitigation plans.
Roles & Responsibilities: Defines duties of team members involved in testing.
Schedule & Estimation: Specifies timelines and effort required.
Test Environment: Details hardware, software, and configurations needed.
Defect Management: Explains defect tracking and reporting process.
Entry & Exit Criteria: Defines conditions to start and complete testing.
Test Automation Plan: Identifies scope and tools for automation.
Test Deliverables: Lists outputs like test cases, reports, and logs.
Templates & Standards: Ensures consistency in documentation.

T -> Tone 
Technical, precisely, enterprise-grade, ready for review. Write as this Test Plan will be reviewed by Project Manager. 

Follow Anti Hallucination Rule:

ROLE: You are a QA assistant operating under strict verification rules. SCOPE OF KNOWLEDGE

You may ONLY use information explicitly provided in: Screen shot of page 

STRICT RULES (MANDATORY) DO NOT invent features, APIs, error codes, UI elements, or behavior. DO NOT assume default or "typical" system behavior. If information is missing or unclear, respond with: "Insufficient information to determine." Every assertion must be traceable to provided input. If a detail is inferred, label it explicitly as: "Inference (low confidence)". Output must be deterministic and repeatable.

PROCESS YOU MUST FOLLOW Step 1: Extract verifiable facts from the input. Step 2: List unknown or missing information. Step 3: Generate output ONLY from Step 1 facts. Step 4: Perform a self-check for hallucinations or contradictions. OUTPUT FORMAT (STRICT) Verified Facts: Missing / Unknown Information: Generated Output: Self-Validation Check: If you cannot complete a step, stop and report why.




## RESPONSE: 

# Test Plan — Wingify / VWO Login Page Authentication

| Field | Value |
|---|---|
| **Application Under Test (AUT)** | Wingify platform login page (formerly VWO) |
| **Test URL** | `https://app.wingify.com/#/login` (redirects from `https://app.vwo.com/#/login`) |
| **Test Plan ID** | QA-TP-AUTH-001 |
| **Version** | 1.0 |
| **Status** | Draft for review |
| **Prepared By** | QA Automation Tester |
| **Reviewed By** | Project Manager *(pending)* |
| **Standard Reference** | IEEE 829-1998 (IEEE Standard for Software Test Documentation), IEEE 29119 |
| **Date** | 2026-08-08 |

---

## 1. Objective

Define the testing goals and quality targets for the Wingify/VWO login page and its associated authentication flows:

- Validate that a user can securely sign in with **email address and password** and be granted access to the platform.
- Validate **session handling** behavior, including idle-timeout and session persistence via the **"Remember me"** option.
- Validate **alternative authentication entry points** visible on the login screen: **Sign in with Google**, **Sign in using SSO**, and **Sign in with Passkey**.
- Validate **account recovery** entry point via the **"Forgot Password?"** link.
- Validate **2FA/MFA** support per requirements, recognizing that no MFA UI is visible on the captured login screen (see Section 3, Out-of-Scope note and Section 4, Assumptions).
- Verify cross-browser and cross-device compatibility: **Chrome, Firefox, Safari, Edge (desktop)** and **iOS/Android mobile browsers**.
- Verify that the login page is functional, secure, accessible, responsive, and performant before release.

### Quality Targets (Measurable)

| Quality Attribute | Target |
|---|---|
| Functional test pass rate | ≥ 98% of planned scenarios executed with no open Critical/High defects |
| Browser/platform coverage | 4 desktop browsers × latest 2 stable versions; iOS Safari & Android Chrome |
| Defect leakage (severity 1–2 to production) | 0 |
| API response time (login authentication endpoint) | P95 ≤ 2 s under baseline load *(inference — no baseline published)* |
| Accessibility | WCAG 2.1 AA checkpoint review completed |
| Security | No Critical security findings unresolved at exit |

---

## 2. Scope

### 2.1 In-Scope

The scope is limited to functionality and attributes observable at the public login page and its authentication contract. It is derived from the verified page contents:

- **Primary Authentication — Email & Password**
  - Email address field (label "Email address", placeholder "Enter email ID").
  - Password field (label "Password", placeholder "Enter password", with an eye icon visibility toggle).
  - Primary **"Sign in"** action button.
  - Client-side validation, field-level error handling, and disabled-state behavior.
- **Session Management**
  - **"Remember me"** checkbox behavior (session persistence semantics).
  - Configurable session timeout periods and idle-session handling.
- **Alternative Sign-In Options (as displayed)**
  - **"Sign in with Google"** — OAuth-based social login entry.
  - **"Sign in using SSO"** — enterprise SSO entry.
  - **"Sign in with Passkey"** — passkey/fIDO2-based authentication entry.
- **Account Recovery**
  - **"Forgot Password?"** link and resulting recovery flow.
- **Account Onboarding Entry**
  - **"Start a free trial"** link and redirection behavior.
- **Page-Level Verification**
  - Page branding (VWO + ABTasty logos, "Sign in to Wingify platform" subheading).
  - Platform transition notice panel: "app.vwo.com has transitioned to app.wingify.com Your plans, features, and data remain unchanged." and the **"Learn More →"** link.
  - Responsive layout across desktop and mobile viewports.
- **Cross-Browser / Cross-Device Compatibility**
  - Chrome, Firefox, Safari, Edge on desktop; iOS Safari and Android Chrome.
- **Non-Functional Testing**
  - Performance, security, accessibility, and usability checks as applicable to the login page.

### 2.2 Out-of-Scope

- **MFA/2FA runtime screens** — No MFA UI (e.g., OTP/authenticator entry) is visible on the captured login screen. The requirement is documented (Section 4, Assumptions), and MFA flow validation will be **explicitly de-scoped or planned as a follow-up** pending confirmation of MFA configuration screens.
- **In-product functionality** — A/B testing, campaign management, reporting, and all post-authentication dashboard features.
- **Backend architecture internals** — VWO/Wingify's internal authentication services, databases, and infrastructure. No assumptions are made about internal architecture.
- **Billing, subscriptions, or plan management**.
- **Mobile native applications** — Testing is limited to mobile *browsers* (iOS Safari, Android Chrome), not native apps.
- **Load/volume testing beyond baseline** — Basic load sanity only; full-scale load testing is out of scope for this release.
- **Non-English locale testing** — Out of scope unless localized builds are provided.

---

## 3. Test Strategy & Approach

### 3.1 Test Levels (All Phases per IEEE 829)

| Phase | Scope | Approach |
|---|---|---|
| **Unit/Component Testing** | Individual login form components and validation logic | Performed by the development team; QA reviews coverage of validation, visibility toggle, and API-client error handling |
| **Integration Testing** | Login page ↔ authentication APIs; Google/SSO/Passkey redirect flows; session cookie issuance | API-level integration tests (REST/graphQL) plus end-to-end flow tests through the UI |
| **System Testing** | Full login feature against the requirements set | End-to-end functional testing across the supported matrix |
| **Regression Testing** | All authentication scenarios after each change | Re-run of the full automated regression suite per release |
| **Acceptance Testing** | Business sign-off on login flows | UAT performed by product owners using scripted scenarios from the traceability matrix |

### 3.2 Testing Types & Techniques

| Testing Type | Technique | Tools |
|---|---|---|
| Functional Testing | Black-box; equivalence partitioning, boundary value analysis, error-guessing on email/password inputs | Playwright (primary), Postman/API scripts |
| UI/UX Testing | Visual layout, branding, responsive breakpoints, contrast | Playwright visual regression, BrowserStack/Sauce Labs screenshots |
| Cross-Browser Testing | Parallel execution on real device/browser cloud | Playwright matrix + BrowserStack |
| Mobile Testing | iOS Safari, Android Chrome (portrait/landscape) | BrowserStack real devices |
| Security Testing | Credential validation, session cookie flags, rate limiting, brute-force protection, SSO/OAuth token validation | OWASP ZAP, Burp Suite (optional), manual review |
| Performance Testing | Page load time, authentication API response time, concurrency sanity | K6 / JMeter (baseline), browser DevTools |
| Accessibility Testing | WCAG 2.1 AA spot checks on form fields and contrast | axe-core / Lighthouse |
| API Testing | Authentication endpoint contract, status codes, error payloads | Postman / Newman, REST Assured |

### 3.3 Execution Flow

1. **Test Preparation** — Test environment configuration, test data creation, and environment smoke check.
2. **Smoke Testing** — Verify the page loads, renders, and the "Sign in" button is actionable across the browser matrix.
3. **Functional Execution** — Execute test scenarios by requirement (see Traceability Matrix, Section 11) in priority order (P0 → P1).
4. **Cross-Browser / Mobile Execution** — Run the same scenario set across the full device matrix.
5. **Non-Functional Execution** — Security scan, performance baseline, accessibility checks.
6. **Regression & Sign-Off** — Re-run automation suite; collate results; obtain PM sign-off against exit criteria.

### 3.4 Test Data Strategy

- Valid and invalid email addresses (format, length, case, Unicode).
- Valid and invalid passwords (boundary lengths, special characters, whitespace).
- Locked/disabled accounts, unverified accounts (where obtainable via test tenants).
- Test SSO/Google accounts provisioned for federated login testing.
- No production user data is used.

---

## 4. Assumptions & Risks

### 4.1 Assumptions

> **Anti-Hallucination Note:** Facts below prefixed **[Verified]** are taken directly from the captured screenshot of the login page. Items prefixed **[Inference]** are logical deductions labeled for reviewer verification and must be confirmed before test execution.

- **[Verified]** The page URL is `app.wingify.com/#/login` and the right panel states "app.vwo.com has transitioned to app.wingify.com. Your plans, features, and data remain unchanged."
- **[Verified]** The login form contains: Email address field, Password field with visibility toggle, "Forgot Password?" link, "Remember me" checkbox, and a primary "Sign in" button.
- **[Verified]** Alternative sign-in buttons: "Sign in with Google", "Sign in using SSO", "Sign in with Passkey".
- **[Verified]** Footer link "Start a free trial" is present.
- **[Inference]** Successful authentication redirects to the Wingify platform dashboard (destination page not visible in the screenshot).
- **[Inference]** "Remember me" controls session persistence vs. session-only cookies. Exact timeout values are **not published** and must be confirmed by the product team.
- **[Inference]** MFA/2FA is configurable per account (per the stated requirement), but no MFA UI is visible on the initial login screen; its flow surfaces post-credential-verification.
- **[Inference]** SSO, Google, and Passkey buttons redirect to the respective identity providers.
- Test tenants, SSO test accounts, and Google test accounts are provided by the project team.
- A stable test environment mirroring production configuration (HTTPS, same DNS) is available.

### 4.2 Risks & Mitigations

| # | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| R1 | MFA/2FA flow not visible in the UI; configuration may vary by plan | Incomplete MFA coverage | Medium | Confirm MFA configuration access; schedule MFA validation as a follow-up sprint if unavailable |
| R2 | SSO/Google/Passkey require external IdP and test accounts | Environment delays | Medium | Pre-provision IdP test accounts; mock IdP for offline automation |
| R3 | Transition from app.vwo.com to app.wingify.com may cause redirect/behavioral changes | Regression risk | High | Include redirect verification in regression; monitor release notes |
| R4 | Captcha/rate-limiting or anti-bot measures may throttle automated login attempts | Automation flakiness | Medium | Use test-only environment allowances; insert pacing between login attempts |
| R5 | Browser/OS matrix availability on device cloud | Schedule slippage | Low | Reserve BrowserStack devices in advance; parallelize runs |
| R6 | Session timeout configuration not documented | Ambiguous expected behavior | Medium | Freeze session settings with the product team before test execution |

---

## 5. Roles & Responsibilities

| Role | Responsibilities |
|---|---|
| **Test Lead / QA Automation Tester** | Test planning, test scenario design, automation framework development, execution, reporting |
| **Project Manager** | Test plan approval, resource allocation, schedule and milestone sign-off |
| **QA Analysts / Manual Testers** | Manual exploratory testing, cross-browser verification, defect triage support |
| **Developer (Frontend)** | Fixing login UI defects; unit testing of form components |
| **Developer (Backend/Auth)** | Fixing authentication API, session, SSO/OAuth defects; API contract support |
| **DevOps / Test Environment Owner** | Test environment provisioning, test data management, CI/CD pipeline support |
| **Product Owner** | Requirement clarification, UAT, acceptance sign-off |
| **Security Specialist** | Security test execution (ZAP/Burp), security findings review |

---

## 6. Schedule & Estimation

> Effort is provided in person-days and is an estimate for planning. Timelines will be baselined after environment and test data readiness are confirmed.

| Phase | Activity | Effort (person-days) | Milestone |
|---|---|---|---|
| P1 | Test planning, scenario design, traceability matrix | 3 | Test Plan approved |
| P2 | Automation framework setup, page objects, smoke scripts | 5 | Framework ready |
| P3 | Functional test execution (all phases incl. regression) | 6 | Test execution report |
| P4 | Cross-browser / mobile execution | 4 | Device matrix report |
| P5 | Non-functional testing (security, performance, accessibility) | 3 | NFR report |
| P6 | Defect fixing cycles, re-testing, regression | 4 | Defect closure |
| P7 | Test summary report, release sign-off | 2 | Sign-off |

**Total estimated effort: ~27 person-days** (parallelizable across 2–3 resources).

**Key Dependencies:** Test environment availability, SSO/Google/Passkey test account provisioning, session timeout configuration freeze.

---

## 7. Test Environment

### 7.1 Hardware & Software

| Component | Specification |
|---|---|
| Desktop Browsers | Chrome (latest 2 stable), Firefox (latest 2 stable), Edge (Chromium, latest 2 stable), Safari (latest 2 stable on macOS) |
| Mobile Browsers | iOS Safari (latest 2), Android Chrome (latest 2) — real devices via BrowserStack |
| Operating Systems | Windows 11, macOS (latest), Android 13+, iOS 16+ |
| Devices | Laptop/Desktop (x86), iPhone (recent), Android phone/tablet |
| Viewports | 1920×1080, 1366×768, 768×1024, 375×667, 390×844 |

### 7.2 Configurations

- Production-like test environment with valid TLS (HTTPS) certificates.
- Test tenant with provisioned test accounts (valid, invalid, locked, unverified).
- SSO identity provider configured with test federation (e.g., SAML/OIDC test IdP).
- Google OAuth test client for "Sign in with Google".
- Passkey/fIDO2 test environment (e.g., Chrome virtual authenticator, YubiKey).
- API test environment with documented authentication endpoints for contract testing.
- Network: standard broadband; note any corporate proxy/vpn restrictions.

### 7.3 Tools

| Tool | Purpose |
|---|---|
| Playwright | UI automation, cross-browser execution |
| BrowserStack / Sauce Labs | Real-device cloud testing |
| Postman / Newman | API contract and integration testing |
| OWASP ZAP | Security scanning (baseline + active) |
| K6 / JMeter | Performance baseline and concurrency sanity |
| axe-core / Lighthouse | Accessibility checks |
| Jira / Xray | Test management and defect tracking |
| Git + CI (GitHub Actions/Jenkins) | Automation pipeline |
| Allure / ReportPortal | Test reporting |

---

## 8. Defect Management

### 8.1 Defect Workflow

```
FOUND (Logged by tester in Jira)
   │
   ▼
TRIAGE (Lead/PM reviews; validates, assigns severity & priority)
   │
   ▼
ASSIGNED (to responsible developer)
   │
   ▼
IN PROGRESS (developer working on fix)
   │
   ▼
FIXED / READY FOR VERIFICATION
   │
   ▼
VERIFIED (tester re-tests in fixed build) ──┐
   │                                        │
   ├─ PASS ─▶ CLOSED                        │
   └─ FAIL ─▶ REOPENED ─────────────────────┘
   │
   └─ Not a defect / Duplicate / Won't Fix / Deferred (by triage, with reason)
```

**Rules:**
- Every defect must contain: title, environment, browser/device, steps to reproduce, expected vs actual result, severity, priority, attachments (logs, screenshots, HAR).
- Re-tests are performed on the latest build only.
- Deferred defects require PM + PO sign-off.

### 8.2 Severity Classification

| Severity | Label | Definition | Example |
|---|---|---|---|
| **S1** | Critical/Blocker | System unusable; security vulnerability; data loss; core auth failure | Sign-in fails for all valid users; credential exposure; session hijack |
| **S2** | High | Major function broken with a workaround unavailable; security concern | Remember-me persistence broken; SSO flow fails; password reset unusable |
| **S3** | Medium | Function works but deviates from spec; workaround available | Wrong error message text; validation message inconsistency |
| **S4** | Low | Cosmetic/UI polish issues | Alignment of logos; minor spacing on mobile viewport |

### 8.3 Priority Classification

| Priority | Label | Definition |
|---|---|---|
| **P0** | Urgent | Fix immediately; blocks release |
| **P1** | High | Fix in current sprint/release |
| **P2** | Medium | Fix in next release |
| **P3** | Low | Fix when convenient |

### 8.4 Defect Reporting Cadence

- **Daily** defect triage during test execution.
- **Weekly** defect summary to PM (open count by severity, aging, reopened rate).
- **Release readiness** review of all open S1/S2 defects before exit.

---

## 9. Entry & Exit Criteria

### 9.1 Phase-Wise Entry & Exit Criteria (IEEE 829)

#### Phase 1 — Test Preparation
| Entry Criteria | Exit Criteria |
|---|---|
| Test Plan approved by PM | Test scenarios and traceability matrix reviewed and baselined |
| Test environment provisioned and stable | Test data created and verified (valid/invalid accounts) |
| Test accounts (SSO, Google, Passkey) provisioned | Smoke test passed on all 4 desktop browsers |

#### Phase 2 — Functional Testing (System Test)
| Entry Criteria | Exit Criteria |
|---|---|
| Smoke test passed | 100% of P0 and P1 scenarios executed |
| Login build deployed to test environment | ≥ 98% scenario pass rate |
| Test data available | No open S1 defects; S2 defects have PM-approved workarounds or target dates |

#### Phase 3 — Cross-Browser & Mobile Testing
| Entry Criteria | Exit Criteria |
|---|---|
| Functional testing stable (no build churn) | All scenarios executed on 4 desktop browsers + 2 mobile platforms |
| Device cloud availability confirmed | Cross-browser defects logged and triaged; no unresolved S1/S2 layout/functional defects |

#### Phase 4 — Non-Functional Testing
| Entry Criteria | Exit Criteria |
|---|---|
| Feature freeze in place | Security scan complete; no unresolved Critical findings |
| Performance baseline data available | P95 login API response within agreed baseline |
| Accessibility audit complete | WCAG 2.1 AA blockers fixed or formally accepted |

#### Phase 5 — Regression & Acceptance (Release Exit)
| Entry Criteria | Exit Criteria |
|---|---|
| All severity-appropriate defects fixed | Full regression suite passes (≥ 98%) |
| Code freeze in place | Zero open S1/S2 defects |
| UAT environment ready | UAT signed off by Product Owner |
| | Test Summary Report approved; release sign-off by PM |

---

## 10. Test Automation Plan

### 10.1 Automation Scope

**In-Scope (Automated):**
- End-to-end login with valid/invalid credentials (email + password).
- Field-level validation and error-message assertions.
- Remember-me persistence behavior.
- Forgot Password flow entry and redirection.
- Google / SSO / Passkey button redirection and successful authentication (with test IdPs).
- Session timeout behavior (configurable, via test hooks).
- Cross-browser smoke and regression suite (Playwright parallel matrix).
- Visual regression on desktop + mobile breakpoints.

**Out-of-Scope (Manual):**
- Security penetration testing (ZAP active scan is semi-automated; manual review required).
- Exploratory and usability testing.
- Complex MFA flows (pending MFA UI confirmation).

### 10.2 Automation Approach

- **Framework:** Playwright (TypeScript) with Page Object Model.
- **CI Integration:** Test suite triggered on merge to the test branch; scheduled nightly regression run.
- **Data:** Test accounts managed via environment-seeded test tenants; API-driven test data setup where available.
- **Reporting:** Allure/HTML reports published to CI; failure artifacts (video, screenshot, trace) auto-attached to defects.
- **Stability:** Retry policy for flaky network-dependent steps (max 2 retries, with reporting); anti-bot pacing between login attempts.

### 10.3 Automation Estimation

- ~60–70% of the functional login suite is automatable in the first release cycle.
- Remaining 30–40% (MFA, exploratory, security) executed manually.

---

## 11. Requirements Traceability Matrix (RTM)

Maps stated requirements to test scenario groups. **Individual test cases are out of scope for this document** (this is a Test Plan, not test execution scripts); the matrix references scenario groups that will be detailed in the test case repository.

| Req ID | Requirement | Scenario Group / Coverage | Priority | Test Phase | Verified Against (Page Fact) |
|---|---|---|---|---|---|
| RQ-01 | Primary Authentication: Email + password login with secure validation | TC-AUTH-01: Valid login; TC-AUTH-02: invalid email/password; TC-AUTH-03: field validation & boundaries; TC-AUTH-04: password visibility toggle; TC-AUTH-05: error handling | P0 | Functional + Regression | Email address field, Password field, eye icon, "Sign in" button **[Verified]** |
| RQ-02 | Session Management: secure session with configurable timeout | TC-SESS-01: Remember me persistence; TC-SESS-02: session idle timeout; TC-SESS-03: session expiry on logout; TC-SESS-04: cookie/security attributes | P0 | Functional + Non-Functional | "Remember me" checkbox **[Verified]**; timeout behavior **[Inference]** |
| RQ-03 | MFA: Optional 2FA support | TC-MFA-01..03: 2FA enrollment, challenge, recovery ***(pending MFA UI confirmation — see Assumptions R1)*** | P1 | Functional (follow-up) | No MFA UI visible on captured screen **[Verified absence]** |
| RQ-04 | SSO: Enterprise SSO integration | TC-SSO-01: SSO button redirect; TC-SSO-02: successful federated login; TC-SSO-03: SSO failure handling | P0 | Functional + Integration | "Sign in using SSO" button **[Verified]** |
| RQ-05 | Social Login | TC-GGL-01: Google sign-in flow; TC-GGL-02: Google cancellation/failure | P1 | Functional + Integration | "Sign in with Google" button **[Verified]** |
| RQ-06 | Passwordless Authentication | TC-PKEY-01: Passkey sign-in; TC-PKEY-02: passkey unavailable fallback | P1 | Functional + Integration | "Sign in with Passkey" button **[Verified]** |
| RQ-07 | Account Recovery | TC-FP-01: Forgot password link; TC-FP-02: reset email/flow; TC-FP-03: invalid token handling | P1 | Functional | "Forgot Password?" link **[Verified]** |
| RQ-08 | Account Onboarding | TC-TRIAL-01: "Start a free trial" link navigation | P2 | Functional | Footer link **[Verified]** |
| RQ-09 | Platform Transition Notice | TC-TRANS-01: Transition notice content and "Learn More →" link | P2 | Functional + UI | Right-panel notice and button **[Verified]** |
| RQ-10 | Branding & Layout | TC-BRAND-01: VWO/ABTasty logos, subheading, split-screen layout | P3 | UI/UX + Visual | Logos, "Sign in to Wingify platform" **[Verified]** |
| RQ-11 | Cross-Browser & Mobile Compatibility | TC-COMPAT-01: full suite on Chrome/Firefox/Safari/Edge; TC-COMPAT-02: iOS Safari & Android Chrome; TC-COMPAT-03: responsive layout at key viewports | P0 | Cross-Browser + Mobile | Page must work across named browsers/platforms (stated requirement) |
| RQ-12 | Security (non-functional) | TC-SEC-01: credential validation; TC-SEC-02: rate limiting/brute force; TC-SEC-03: session cookie security; TC-SEC-04: no sensitive data in client-side payloads | P0 | Security | — |
| RQ-13 | Performance (non-functional) | TC-PERF-01: page load; TC-PERF-02: auth API response time; TC-PERF-03: concurrency sanity | P1 | Performance | — |
| RQ-14 | Accessibility (non-functional) | TC-ACC-01: WCAG 2.1 AA spot checks (labels, contrast, keyboard nav) | P2 | Accessibility | — |

---

## 12. Test Deliverables

| # | Deliverable | Owner | Due |
|---|---|---|---|
| 1 | Test Plan (this document) | QA Lead | Plan approval milestone |
| 2 | Test Scenarios & Test Case Repository (linked from RTM) | QA Team | Pre-execution |
| 3 | Test Data Sheet (accounts, environments) | Test Environment Owner | Pre-execution |
| 4 | Automated Test Suite (Playwright) | QA Automation Tester | Framework ready milestone |
| 5 | Test Execution Report (per phase) | QA Team | Per phase exit |
| 6 | Defect Report & Metrics (open/closed by severity, aging) | Test Lead | Weekly |
| 7 | Security Scan Report (ZAP) | Security Specialist | Non-functional phase |
| 8 | Performance Report (K6/JMeter baseline) | Performance Tester | Non-functional phase |
| 9 | Accessibility Report (axe/Lighthouse) | QA Team | Non-functional phase |
| 10 | Cross-Browser/Device Matrix Report | QA Team | Cross-browser phase |
| 11 | Test Summary Report (incl. release recommendation) | Test Lead | Release exit |
| 12 | Sign-off Checklist | PM / PO | Release exit |

---

## 13. Templates & Standards

- **Documentation Standard:** IEEE 829-1998 (Test Plan, Test Design, Test Procedure, Test Log, Test Summary Report) aligned with IEEE 29119 terminology.
- **Test Case Template:** Requirement ID, scenario ID, priority, precondition, test data, steps, expected result, status, defect link.
- **Defect Template:** Summary, environment (browser/OS/version), severity (S1–S4), priority (P0–P3), steps to reproduce, expected vs actual, attachments.
- **Traceability Standard:** Every requirement ID maps to scenario groups (see RTM); every scenario group maps back to a requirement — no orphan scenarios.
- **Naming Conventions:** Scenario IDs as `TC-<AREA>-<NN>`; defect IDs from Jira sequence.
- **Version Control:** All test artifacts under Git; test plan changes via version bumps with a change log.
- **Review Cycle:** Test Plan → reviewed by PM; Test Summary Report → reviewed by PM & PO before release sign-off.

---

## 14. Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 1.0 | 2026-08-08 | QA Automation Tester | Initial release for PM review |

---

## Appendix A — Verified Facts & Anti-Hallucination Self-Check

**Source of facts:** Screenshot of the login page captured at test URL `app.wingify.com/#/login`.

| Fact | Status |
|---|---|
| URL shown is `app.wingify.com/#/login`; right panel states app.vwo.com transitioned to app.wingify.com | Verified |
| Split-screen layout: left white login form panel, right dark-purple informational panel | Verified |
| VWO (purple) + ABTasty (purple) logos at top of left panel; subheading "Sign in to Wingify platform" | Verified |
| Email address field (placeholder "Enter email ID") | Verified |
| Password field (placeholder "Enter password") with eye-icon visibility toggle | Verified |
| "Forgot Password?" link (blue text) | Verified |
| "Remember me" checkbox (unchecked) | Verified |
| Primary "Sign in" button (purple, white text); "Or" divider | Verified |
| Buttons: "Sign in with Google", "Sign in using SSO", "Sign in with Passkey" | Verified |
| Footer: "Don't have an account? Start a free trial" | Verified |
| Right panel: "Welcome to Wingify!" heading; "Learn More →" button | Verified |
| No error messages, validation states, or 2FA/MFA prompts visible on the captured screen | Verified (absence) |
| MFA flow, session timeout values, redirect destinations, auth API endpoints | Inference — to be confirmed |

**Self-Validation Check:**

1. **Fact extraction** — All UI elements asserted in this plan are present in the screenshot description above. ✔
2. **No invented features** — No error codes, API names, endpoints, or UI elements beyond the screenshot and the stated requirements have been introduced. ✔
3. **Inferences labeled** — Every non-observable behavior (redirect target, timeout semantics, MFA location, IdP behavior) is explicitly labeled **[Inference]** or placed in Assumptions (Section 4). ✔
4. **Contradiction check** — Requirements reference the URL `https://app.vwo.com/#/login`, while the captured page resolves to `app.wingify.com/#/login`; this is handled as a verified platform transition (RQ-09) rather than a contradiction. ✔
5. **Missing-information handling** — Items that could not be verified are flagged as dependencies/assumptions pending product-team confirmation before test execution. ✔
