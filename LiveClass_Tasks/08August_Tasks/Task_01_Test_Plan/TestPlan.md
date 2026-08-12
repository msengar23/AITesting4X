# Test Plan — VWO Login Dashboard Authentication

| Field | Value |
|---|---|
| **Test Plan ID** | TP-VWO-AUTH-001 |
| **Project Name** | VWO Login Dashboard — Authentication & Login Experience |
| **Application Under Test (AUT)** | VWO login dashboard at `https://app.vwo.com/` |
| **Test Plan Version** | 0.9 (Draft) |
| **Document Status** | Under review — pending Project Manager approval |
| **Author** | QA Automation Tester (4.8 years experience) |
| **Reviewers** | Project Manager *(pending)*, Dev Lead, DevOps, Product Owner |
| **Approvers** | Project Manager, Product Owner |
| **Standards Reference** | IEEE 829-1998, ISO/IEC/IEEE 29119-2, ISO 25010, OWASP ASVS 4.0, WCAG 2.1 AA |
| **Basis of Testing** | Product Requirements Document (PRD) — VWO Login Dashboard, 7 pages |
| **Planned Start / End Date** | `[TBD — to be baselined after PM review]` |

---

## 1. Document Control

### 1.1 Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.9 | 2026-08-12 | QA Automation Tester | Draft created from PRD; submitted for PM review (not baselined) |

### 1.2 Distribution List

| Recipient | Role | Purpose |
|---|---|---|
| Project Manager | Reviewer / Approver | Plan approval, milestone sign-off |
| QA Team | Execution reference | Test scenario and execution ownership |
| Dev Lead / DevOps | Environment & defect coordination | Fixing, environment provisioning |
| Product Owner | Requirement clarification / UAT | Requirement confirmation, acceptance |

---

## 2. Introduction

### 2.1 Purpose

Define the testing goals, scope, strategy, resources, schedule, and acceptance conditions for the **VWO Login Dashboard** at `https://app.vwo.com/`. This Test Plan is the controlling document for all test activities planned against the **PRD — VWO Login Dashboard (7 pages)** and is submitted for **Project Manager review**. It is **not baselined**; estimates, timelines, and targets are to be confirmed at review.

### 2.2 Scope of the Document

Covers the planned test phases (component → integration → system → regression → acceptance), test types, entry/exit criteria, test environment, automation scope, defect management, metrics, and reporting for the login-dashboard scope defined in Section 5. It is a **planning document and contains no executable test cases** — those are maintained separately in the test case repository (Task_03, `TestCases_Login_VWO.md`).

### 2.3 References

| Ref | Document / Standard |
|---|---|
| [R1] | Product Requirements Document — VWO Login Dashboard (7 pages, provided) |
| [R2] | IEEE 829-1998 — Standard for Software Test Documentation |
| [R3] | ISO/IEC/IEEE 29119-2 — Software Testing Standards |
| [R4] | ISO/IEC 25010 — Systems and software Quality Requirements and Evaluation |
| [R5] | OWASP ASVS 4.0 / OWASP Authentication Cheat Sheet |
| [R6] | WCAG 2.1 AA — Web Content Accessibility Guidelines |
| [R7] | Test Case Repository — `TestCases_Login_VWO.md` (98 cases) |

### 2.4 Terms, Definitions & Abbreviations

| Term | Definition |
|---|---|
| AUT | Application Under Test |
| NFR | Non-Functional Requirement |
| RTM | Requirements Traceability Matrix |
| IdP | Identity Provider (SAML/OAuth) |
| SSO | Single Sign-On |
| MFA / 2FA | Multi-Factor Authentication / Two-Factor Authentication |
| CDN | Content Delivery Network |
| S1–S4 / P0–P3 | Defect severity / priority classifications (Sections 12.2–12.3) |
| WCAG | Web Content Accessibility Guidelines |

---

## 3. Application Under Test (AUT)

### 3.1 System Overview

The AUT is the **VWO login dashboard** — the critical entry point to VWO (Visual Website Optimizer), a digital experience optimization platform used by over 4,000 brands across 90 countries. The dashboard provides a clean, minimalist login interface with standard authentication fields, Remember Me functionality, a free-trial registration path, and product announcements (including Light/Dark mode). It is the gateway to VWO's experimentation, personalization, and analytics suite.

### 3.2 Test Items

| ID | Test Item | Version/Build | Supplier |
|---|---|---|---|
| TI-01 | VWO login page (UI form, validation, Remember Me, forgot password entry, theme support) | `[TBD]` | VWO Frontend |
| TI-02 | Authentication API / session endpoints (login, token issuance, session timeout) | `[TBD]` | VWO Backend |
| TI-03 | SSO / social login integration (SAML, OAuth — Google, Microsoft) | `[TBD]` | IdP / VWO Backend |
| TI-04 | Password reset flow (token generation, email delivery, recovery) | `[TBD]` | VWO Backend |

### 3.3 Test Data

- **Synthetic test accounts only — no production user data.**
- Valid / invalid email formats (format, length, case, Unicode).
- Boundary-length passwords, special characters, whitespace.
- Locked, disabled, and unverified accounts (via test tenant).
- Test SSO / Google / Microsoft identity provider accounts.
- 2FA-enabled and 2FA-disabled accounts.
- Password-reset tokens (valid, expired, reused, malformed).

---

## 4. Test Objectives & Quality Targets

| Quality Attribute | Objective | Measurable Target | Source |
|---|---|---|---|
| Functional Correctness | All PRD functional requirements behave per specification | ≥ 98% scenario pass rate; zero open S1 defects | [R1] |
| Login Success Rate | Successful authentication attempts | ≥ 95% (KPI) | [R1] |
| Performance — Page Load | Login page load time on standard connection | ≤ 2 seconds (PRD KPI) | [R1] |
| Availability | Global uptime support | 99.9% high availability (verify & document) | [R1] |
| Security | No successful brute force / unauthorized access; OWASP-aligned | Zero S1 security findings at exit | [R1],[R5] |
| Compliance | GDPR / CCPA data handling; enterprise audit support | 100% compliance-audit requirements at exit | [R1] |
| Accessibility | WCAG conformance | WCAG 2.1 AA compliance | [R1],[R6] |
| User Satisfaction | Login experience quality | ≥ 90% satisfaction (UAT survey) | [R1] |
| Support Volume | Login-related support tickets | Reduced by 20% (post-release trend, out of test scope) | [R1] |
| Defect Leakage | No high-severity defect to production | 0 S1/S2 defects leaked | This plan |

---

## 5. Test Scope

### 5.1 In-Scope

**Functional:**

- **Primary Authentication** — email + password login with secure validation.
- **Session Management** — secure session handling with **configurable timeout periods**.
- **Multi-Factor Authentication** — **optional 2FA** support.
- **Single Sign-On (SSO)** — enterprise SSO integration (SAML, OAuth).
- **Social Login** — optional integration with Google, Microsoft, and other identity providers.
- **User Input Validation** — real-time validation on blur, email format verification, password strength indicators, clear error messages.
- **Password Management** — Forgot Password flow, secure token generation, multiple recovery options, enforced password complexity.
- **User Experience** — responsive/mobile-optimized design, touch-friendly controls, auto-focus, clickable labels, loading states.
- **Accessibility** — screen reader support (ARIA), high-contrast mode, full keyboard navigation.
- **Branding & Visual Design** — VWO design system consistency, Light and Dark Mode.

**Non-Functional:**

- **Security** — encryption (E2E for auth data transmission), secure password storage (hashing), secure session tokens, HTTPS enforcement, rate limiting / brute-force protection.
- **Performance** — page load ≤ 2 s, asset optimization (compressed images, minified CSS/JS), CDN integration, concurrency sanity.
- **Compliance** — GDPR, CCPA, enterprise audit readiness.
- **Accessibility** — WCAG 2.1 AA.
- **Integration** — VWO core platform (dashboard transition), analytics (login success/failure tracking), customer support integration, marketing tools.

### 5.2 Out-of-Scope

- Post-authentication product functionality (A/B testing, CRO, analytics dashboards, personalization features) — tested by platform team.
- Native mobile applications — testing limited to mobile *browsers*.
- Full-scale load testing beyond concurrency sanity (scalability targets are verify-and-document).
- Biometric authentication, adaptive (risk-based) authentication, and PWA — **future enhancements per PRD**, not in this release.
- Third-party IdP internal behavior (tested at the integration boundary only).
- Billing / subscription management.

---

## 6. Test Strategy & Approach

### 6.1 Test Levels (V-Model / IEEE 829 Phases)

| Phase | Scope | Approach | Primary Owner |
|---|---|---|---|
| Component / Unit | Form components, validation logic, password-strength indicator | Code-level tests; QA reviews coverage | Developers |
| Integration | Login UI ↔ auth APIs; SSO/OAuth redirects; session cookie issuance; analytics events | Contract tests (REST) + E2E | QA + Dev |
| System | Full login feature set against PRD requirements | End-to-end functional execution | QA |
| Regression | All in-scope scenarios after each change | Re-run automated suite per release | QA |
| Acceptance (UAT) | Business sign-off on login flows | Scripted scenarios from RTM; satisfaction survey | Product Owner |

### 6.2 Test Types & Techniques

| Test Type | Technique | Primary Tools |
|---|---|---|
| Functional | Black-box: equivalence partitioning, boundary value analysis, error guessing, decision tables | Playwright, Postman/Newman |
| UI / Visual | Layout, branding, Light/Dark mode, responsive breakpoints, visual diff | Playwright visual regression |
| Cross-Browser / Device | Parallel execution on real devices | Playwright matrix + BrowserStack |
| API | Auth contract, status codes, error payloads, token handling | Postman/Newman, REST Assured |
| Security | Credential validation, rate limiting/brute force, session cookie flags, SSO/OAuth token validation, injection (SQLi/XSS) | OWASP ZAP, Burp Suite (optional) |
| Performance | Page load, auth API response, concurrency sanity | K6 / JMeter, Lighthouse |
| Accessibility | WCAG 2.1 AA spot checks (labels, contrast, keyboard, screen reader) | axe-core, Lighthouse, screen reader (NVDA/VoiceOver) |
| Usability / Exploratory | Unscripted testing, UX heuristics, mobile touch targets | Manual |

### 6.3 Test Design Techniques

- **Equivalence Partitioning** — valid/invalid input classes (email, password).
- **Boundary Value Analysis** — min/max password lengths, edge-case emails.
- **State Transition** — session states: active → idle → expired → re-authenticated; password-reset token states.
- **Decision Table** — auth method × credential validity × account state × 2FA state.
- **Error Guessing / Exploratory** — heuristic risk-based scenarios on the login boundary.

### 6.4 Execution Flow

1. **Preparation** — environment, test data, smoke check.
2. **Smoke Testing** — core login path on full browser matrix.
3. **Functional Execution** — P0 → P1 → P2 per RTM (Section 15).
4. **Cross-Browser / Mobile Execution** — full scenario set on device matrix.
5. **Non-Functional Execution** — security, performance, accessibility, compliance checks.
6. **Regression & Sign-Off** — full suite re-run; exit criteria verified; PM approval.

### 6.5 Test Data Management

- Synthetic accounts only; no production data.
- Versioned datasets; API-driven seeding where available.
- Cleanup and masking policies owned by Test Environment Owner.

---

## 7. Entry & Exit Criteria

### 7.1 Test Preparation Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Test Plan approved by PM | Test scenarios and RTM baselined |
| Environment provisioned & stable | Test data created and verified |
| SSO/OAuth/2FA test accounts provisioned | Smoke test passed on all target browsers |

### 7.2 Functional Testing (System Test) Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Build deployed to test environment | 100% of P0/P1 scenarios executed |
| Smoke test passed | ≥ 98% pass rate |
| Test data available | No open S1 defects; S2 workarounds approved |

### 7.3 Cross-Browser / Mobile Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Functional testing stable | All scenarios pass on 4 desktop + 2 mobile platforms |
| Device cloud confirmed | No unresolved S1/S2 platform-specific defects |

### 7.4 Non-Functional Testing Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Feature freeze in place | Security scan clean; zero Critical findings open |
| Performance baseline available | Page load ≤ 2 s; P95 auth API within baseline |
| — | WCAG 2.1 AA blockers fixed or formally accepted |

### 7.5 Regression & Release Exit Phase

| Entry Criteria | Exit Criteria |
|---|---|
| Defects fixed and verified | Full regression suite ≥ 98% pass |
| Code freeze in place | Zero open S1/S2 defects |
| UAT environment ready | UAT signed off by Product Owner |
| — | Test Summary Report approved; PM release sign-off |

---

## 8. Test Environment

### 8.1 Hardware & Software

| Component | Specification |
|---|---|
| Desktop Browsers | Chrome, Firefox, Edge (latest 2 stable); Safari (latest 2) |
| Mobile Browsers | iOS Safari, Android Chrome (real devices) |
| Operating Systems | Windows 11, macOS latest, iOS 16+, Android 13+ |
| Viewports | 1920×1080, 1366×768, 768×1024, 375×667, 390×844 |

### 8.2 Configurations

- Production-like test environment with valid HTTPS/TLS.
- Test tenant with provisioned accounts (valid, invalid, locked, unverified, 2FA on/off).
- Test SSO IdP (SAML + OAuth), Google/Microsoft test clients.
- Documented auth API endpoints for contract testing.
- Simulated slow-network / low-bandwidth profile for load-time verification.

### 8.3 Tools

| Tool | Purpose |
|---|---|
| Playwright | UI automation, cross-browser execution |
| BrowserStack / Sauce Labs | Real-device cloud |
| Postman / Newman | API contract testing |
| OWASP ZAP | Security scanning |
| K6 / JMeter | Performance baseline, concurrency sanity |
| Lighthouse / axe-core | Accessibility & page-load checks |
| Jira / Xray | Test management, defect tracking |
| Allure / ReportPortal | Test reporting |
| Git + CI (GitHub Actions/Jenkins) | Automation pipeline |

### 8.4 Access & Support

Environment owner, credentials, and support SLA for the test environment `[to be defined by DevOps]`.

---

## 9. Test Schedule & Estimation

> Estimates are **draft and not baselined** — to be confirmed at PM review.

| Phase | Activity | Effort (person-days) | Milestone |
|---|---|---|---|
| P1 | Planning, scenario design, RTM | 3 | Test Plan approved |
| P2 | Automation framework & smoke scripts | 5 | Framework ready |
| P3 | Functional execution + regression | 6 | Execution report |
| P4 | Cross-browser / mobile | 4 | Device matrix report |
| P5 | Non-functional (security/perf/accessibility) | 3 | NFR report |
| P6 | Defect fixes, re-testing | 4 | Defect closure |
| P7 | Summary report & sign-off | 2 | Release sign-off |

**Total:** ~27 person-days (draft; parallelizable across 2–3 resources).

**Key Dependencies:** environment availability, SSO/OAuth/2FA account provisioning, session-timeout configuration freeze, and PM approval of the plan.

---

## 10. Roles & Responsibilities (RACI)

| Role | Test Plan | Test Design | Execution | Automation | Defect Fix | Acceptance |
|---|---|---|---|---|---|---|
| QA Lead / Automation Tester (Author) | A/R | R | R | R | — | C |
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

- **In-Scope:** core email/password login, validation & error-message assertions, Remember Me persistence, Forgot Password entry, SSO/OAuth redirect flows (with test IdPs), session-timeout behavior, cross-browser smoke/regression, visual regression (Light/Dark mode).
- **Manual:** penetration testing, exploratory & usability, screen-reader accessibility verification, complex 2FA flows.

### 11.2 Framework & Tooling

- Framework: Playwright (TypeScript) + Page Object Model.
- Data: environment-seeded synthetic accounts; API-driven setup.
- Reporting: Allure/HTML with failure artifacts (video, screenshot, trace).

### 11.3 CI/CD Integration

- Trigger: merge to test branch + scheduled nightly regression.
- Flaky-network retry policy (max 2 retries with logging).
- Anti-bot pacing between login attempts to avoid lockout/rate limiting.

### 11.4 Automation Governance

- Estimated coverage: 60–70% of the functional suite in the first cycle.
- Page objects shared; no test-logic duplication; code review required.

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

**Rules:** every defect includes title, environment, browser/OS, steps to reproduce, expected vs actual, severity, priority, attachments (logs, screenshots, HAR). Deferred defects require PM + PO sign-off.

### 12.2 Severity Classification

| Severity | Label | Definition | Example |
|---|---|---|---|
| S1 | Critical/Blocker | System unusable; security vulnerability; data loss; core auth failure | Login fails for all valid users; credential exposure; session hijack |
| S2 | High | Major function broken, no workaround | Remember Me broken; SSO fails; password reset unusable |
| S3 | Medium | Deviates from spec, workaround available | Wrong error message text |
| S4 | Low | Cosmetic / UI polish | Alignment, spacing, minor theme contrast issue |

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
| Pass Rate | % passed vs executed | ≥ 98% |
| Login Success Rate | Successful auth attempts (PRD KPI) | ≥ 95% |
| Page Load Time | Login page load on standard connection (PRD KPI) | ≤ 2 s |
| Defect Density | defects per scenario/requirement | `[TBD]` |
| Defect Age | open days per severity | `[TBD]` |
| Reopened Rate | % reopened after verification | < 10% |
| Automation Coverage | % automated vs total | 60–70% |
| Defect Leakage | S1/S2 reaching production | 0 |

---

## 14. Risk, Assumptions, Constraints & Dependencies

### 14.1 Risk Register

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | 2FA/MFA flow not visible in current UI; configuration may vary by plan | Incomplete MFA coverage | Medium | Confirm 2FA configuration access; schedule as follow-up | QA Lead |
| R2 | SSO/OAuth (Google, Microsoft) require external IdP test accounts | Environment delays | Medium | Pre-provision accounts; mock IdP for offline automation | DevOps |
| R3 | Rate limiting / anti-bot may throttle automated login attempts | Automation flakiness | High | Test-tenant allowances; pacing between attempts | QA Automation |
| R4 | Session timeout / Remember Me duration not documented | Ambiguous expected behavior | Medium | Freeze session config before execution | Product Owner |
| R5 | Light/Dark mode new feature may change layout/contrast | Visual regression risk | Medium | Include theme toggle in visual regression matrix | QA |
| R6 | Availability/load targets (99.9%, concurrent users) not measurable in test | Scope gap vs PRD | Medium | Baseline sanity load; document as verify-and-document | Performance Tester |

### 14.2 Assumptions

- Facts and stated assumptions below are tagged per the anti-hallucination protocol (Section 19). Items tagged **Inference** or **Insufficient information** must be confirmed before execution.

| # | Assumption | Tag |
|---|---|---|
| A1 | Test tenant with all account states (valid, invalid, locked, unverified, 2FA on/off) is provided by project team | Assumed — to be confirmed |
| A2 | SSO, Google/Microsoft test accounts provisioned by DevOps | Assumed — to be confirmed |
| A3 | "Configurable timeout periods" — exact session-timeout values are not published in the PRD | Insufficient information — verify & document |
| A4 | "99.9% uptime" and "thousands of concurrent logins" are operational targets, not testable in QA env | Inference — verify & document |
| A5 | 2FA is optional per account; flow surfaces post-credential-verification (no 2FA UI on the initial screen per prior observation) | Inference (low confidence) |
| A6 | Login success/failure analytics tracking is observable via a test analytics endpoint | Inference (low confidence) |
| A7 | GDPR/CCPA compliance is validated via data-handling review, not full legal audit | Inference — verify & document |

### 14.3 Constraints

- Test-only environments only; **no production user data**.
- Fixed release date `[TBD]`.
- Limited device-cloud budget — prioritize matrix.

### 14.4 Dependencies

- PM approval of this plan.
- Environment readiness; external IdP provisioning.
- Session-timeout configuration freeze.
- Auth API contract availability.

---

## 15. Requirements Traceability Matrix (RTM)

Maps PRD requirements to scenario groups. **Individual test cases are maintained in the test case repository** (`TestCases_Login_VWO.md`, 98 cases); the matrix references scenario groups, not steps.

| Req ID | PRD Requirement | Scenario Group | Priority | Phase | Verification Source |
|---|---|---|---|---|---|
| RQ-01 | Primary authentication (email + password) with secure validation | TC-AUTH-01..05 | P0 | Functional + Regression | [PRD] Verified |
| RQ-02 | Session management with configurable timeout | TC-SESS-01..04 | P0 | Functional + NFR | [PRD] Verified |
| RQ-03 | Optional 2FA / MFA | TC-MFA-01..03 | P1 | Functional (follow-up) | [PRD] Verified; flow Inference |
| RQ-04 | Enterprise SSO (SAML, OAuth) | TC-SSO-01..03 | P0 | Functional + Integration | [PRD] Verified |
| RQ-05 | Social login (Google, Microsoft, others) | TC-GGL-01..02, TC-MSDN-01 | P1 | Functional + Integration | [PRD] Verified |
| RQ-06 | Real-time validation on blur; email format verification; password strength indicator | TC-VAL-01..06 | P1 | Functional | [PRD] Verified |
| RQ-07 | Clear, actionable error handling | TC-ERR-01..03 | P1 | Functional | [PRD] Verified |
| RQ-08 | Forgot Password flow; secure token; multiple recovery options | TC-FP-01..04 | P0 | Functional | [PRD] Verified |
| RQ-09 | Enforced password complexity | TC-PWD-01..03 | P1 | Functional + Security | [PRD] Verified |
| RQ-10 | Remember Me persistent login | TC-RM-01..02 | P0 | Functional | [PRD] Verified |
| RQ-11 | Responsive / mobile-optimized; touch-friendly; auto-focus; clickable labels; loading states | TC-UX-01..05 | P1 | Cross-Browser + Mobile | [PRD] Verified |
| RQ-12 | Accessibility: screen reader (ARIA), high contrast, keyboard navigation | TC-ACC-01..04 | P1 | Accessibility | [PRD],[WCAG] Verified |
| RQ-13 | Light and Dark Mode | TC-THEME-01..02 | P2 | UI/Visual | [PRD] Verified |
| RQ-14 | Branding & visual consistency | TC-BRAND-01 | P3 | UI/Visual | [PRD] Verified |
| RQ-15 | Security: E2E encryption, hashed storage, secure tokens, HTTPS enforcement, rate limiting | TC-SEC-01..06 | P0 | Security | [PRD] Verified |
| RQ-16 | Performance: page load ≤ 2 s, asset optimization, CDN, concurrency sanity | TC-PERF-01..03 | P1 | Performance | [PRD] Verified |
| RQ-17 | Compliance: GDPR, CCPA, enterprise audit readiness | TC-COMP-01..02 | P1 | Compliance review | [PRD] Verified |
| RQ-18 | Integration: dashboard transition, analytics, support, marketing tools | TC-INT-01..03 | P1 | Integration | [PRD] Verified |
| RQ-19 | Compatibility: Chrome/Firefox/Safari/Edge desktop; iOS/Android mobile | TC-COMPAT-01..03 | P0 | Cross-Browser + Mobile | [PRD] Verified |

*No orphan scenarios: every scenario group maps to a requirement, every requirement to a scenario group.*

---

## 16. Test Deliverables

| # | Deliverable | Owner | Due |
|---|---|---|---|
| 1 | Test Plan (this document) | QA Lead | PM approval |
| 2 | Test Scenarios & Case Repository (Task_03) | QA Team | Pre-execution |
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

- **Documentation standard:** IEEE 829-1998 aligned with ISO/IEC/IEEE 29119 terminology.
- **Test case template:** Requirement ID, scenario ID, priority, precondition, test data, steps, expected result, status, defect link (Jira-format per Task_03 repository).
- **Defect template:** Summary, environment, severity (S1–S4), priority (P0–P3), reproduction steps, expected vs actual, attachments.
- **Naming conventions:** Scenario IDs `TC-<AREA>-<NN>`; defect IDs from tracker sequence.
- **Version control:** All test artifacts under Git; plan changes via version bump with change log.
- **Review cycle:** Test Plan → PM; Test Summary Report → PM & PO before release sign-off.

---

## 18. Approvals

> **Not yet approved — pending PM review.** This section is intentionally unsigned.

| Role | Name | Signature / Date |
|---|---|---|
| QA Lead (Author) | QA Automation Tester | `[ ]` |
| Project Manager | `[ ]` | `[ ]` |
| Product Owner | `[ ]` | `[ ]` |
| DevOps / Environment Owner | `[ ]` | `[ ]` |

---

## 19. Appendix A — Verification & Anti-Hallucination Protocol

Every assertion in this plan and its downstream test cases is labelled with one of:

| Label | Meaning |
|---|---|
| **Verified** | Directly traceable to a provided source (PRD, screenshot, API doc, run result) with a source tag, e.g., `[PRD]`, `[DOM]`, `[RUN]`, `[SS]` |
| **Inference (low confidence)** | Logical deduction that must be confirmed before execution |
| **Insufficient information to determine** | Cannot be asserted from available input — record as an open question, do not guess |

**Process (mandatory, deterministic):**

1. Extract verifiable facts from the provided input only (this plan is built on the PRD).
2. List unknown or missing information.
3. Generate output strictly from Step 1 facts; label every inference.
4. Self-check for hallucinations or contradictions.
5. Configuration-dependent values (lockout thresholds, rate limits, session timeouts, HTTP status codes, cookie flags, uptime/concurrency targets) are recorded as *verify-and-document* checks, never asserted as fact.
6. If any step cannot be completed, stop and report why.

**Self-Validation Check:**

- [ ] All requirements asserted in this plan are traceable to the PRD.
- [ ] No error codes, endpoints, or features invented.
- [ ] Every inference labelled `Inference (low confidence)`.
- [ ] No contradictions between sections; discrepancies escalated as assumptions (Section 14.2).
- [ ] Missing information flagged as dependencies / open questions.

---

## 20. Appendix B — Open Items for PM Review (Not Final)

The following are **draft/open items** that the Project Manager should confirm before this plan is baselined:

| # | Open Item | Requested Decision |
|---|---|---|
| O1 | Test plan version/ID format and change-control process | Confirm `TP-VWO-AUTH-001`; adopt version bump process |
| O2 | Release date and sprint alignment | Provide target release date for scheduling |
| O3 | Test environment availability and tenant provisioning | Confirm env owner and SLA |
| O4 | SSO/Google/Microsoft test account provisioning | Confirm availability and timeline |
| O5 | Session-timeout and Remember-Me duration values | Freeze configuration for test baseline |
| O6 | 2FA flow availability in test tenant | Confirm 2FA configuration access or defer |
| O7 | Analytics/login-tracking observability in test | Confirm analytics endpoint visibility |
| O8 | Availability (99.9%) and concurrency targets — testable scope | Confirm whether load testing is required |
| O9 | Automation coverage target (60–70%) | Confirm investment and priority |
| O10 | Accessibility verification depth (automated vs manual screen-reader) | Confirm scope and tools |

---

*End of Test Plan (Draft v0.9) — submitted for Project Manager review. Not final; not baselined.*
