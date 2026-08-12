# Test Case Template — Jira-Board Format (IEEE 829 / ISO/IEC/IEEE 29119 Aligned)

> **Usage:** Reusable, industry-level test case template. Fill the header, copy the row template into the category tables, and replace `[ ]` placeholders with project-specific values. This template is compatible with both manual execution and automation scripting (Playwright/Postman). Follow the Anti-Hallucination Protocol (Section 6) — **never assert unverified behavior as fact**.

---

## 1. Document Control

| Field | Value |
|---|---|
| **Test Case Suite ID** | `[TC-<PROJECT>-<SEQ>]` e.g., `QA-TC-AUTH-002` |
| **Project / Feature** | `[ ]` e.g., VWO Login Dashboard — Authentication |
| **Application Under Test (AUT)** | `[ ]` e.g., `https://app.vwo.com/#/login` |
| **Suite Version** | `[x.y]` |
| **Status** | `[ ]` Draft / Under Review / Ready for Execution / Baselined |
| **Author** | `[ ]` |
| **Reviewers** | `[ ]` |
| **Standards Reference** | IEEE 829-1998, ISO/IEC/IEEE 29119, OWASP ASVS 4.0, WCAG 2.1 AA |
| **Source Requirements** | `[PRD — VWO Login Dashboard, Section/Req ID]` |
| **Date** | `[YYYY-MM-DD]` |

### 1.1 Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1 | `[ ]` | `[ ]` | Initial draft |
| 1.0 | `[ ]` | `[ ]` | Baselined after review |

---

## 2. Scope & Parameters

### 2.1 In-Scope (per PRD)

- Primary authentication (email + password) with secure validation.
- Session management with configurable timeout; Remember Me.
- Optional 2FA/MFA; Enterprise SSO (SAML, OAuth); Social login (Google, Microsoft).
- Real-time validation, email format check, password strength indicator, error handling.
- Forgot Password flow with secure token and multiple recovery options.
- Responsive/mobile UX, Light & Dark Mode, accessibility (WCAG 2.1 AA).
- Security: rate limiting / brute-force protection, HTTPS, session security.
- Performance: page load ≤ 2 s, concurrency sanity; integration: analytics, support, marketing tools.

### 2.2 Out-of-Scope

- Post-authentication platform features (A/B testing, CRO, analytics dashboards).
- Native mobile apps (browser-only testing).
- Full-scale load testing; biometric/adaptive authentication (future enhancements per PRD).

### 2.3 Test Parameters (Global)

| Parameter | Value |
|---|---|
| Target URL | `[https://app.vwo.com/#/login]` |
| Application Type | Single Page Application (SPA) |
| Authentication Methods | Email/Password, Google OAuth 2.0 SSO, Microsoft Azure AD SSO |
| Browsers | Chrome, Firefox, Safari, Edge (latest 2 stable) |
| Mobile | iOS Safari, Android Chrome (latest 2) |
| Screen Readers | NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android) |
| Test Data | **Synthetic test accounts only — no production user data** |

### 2.4 Test Data (Global)

| Data Key | Value | Status |
|---|---|---|
| Valid Email | `[ ]` | Synthetic |
| Valid Password | `[ ]` | Synthetic |
| Invalid Email | `[ ]` | Synthetic |
| Invalid Password | `[ ]` | Synthetic |
| Boundary email/password lengths | `[per actual password policy]` | Verify & document |
| SSO test domain | `[ ]` | Synthetic |
| 2FA-enabled / 2FA-disabled account | `[ ]` | Synthetic |

**Global Preconditions:**

1. Application deployed to test environment; network reachable.
2. Synthetic test accounts only.
3. Browser cache/cookies cleared before each test unless stated otherwise.

---

## 3. Row Template (copy for each test case)

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| `TC-<AREA>-<NNN>` | `[Functional / Negative / Boundary / Security / Usability / Accessibility / API / Compatibility / Performance]` | `[One-line scenario: Given → When → Then]` | `[State/environment/account required]` | `1. <numbered step><br>2. <numbered step><br>3. ...` | `[exact inputs]` | `[assertable outcome — see Section 6]` | `[Critical / High / Medium / Low]` | `[Y / N]` | `[Verified / Inference (low confidence) / Insufficient information to determine]` |

---

## 4. Category Templates (copy per requirement area)

### 4.1 Functional — Positive & Verified

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-F-001 | Functional | Valid email + password login succeeds and grants dashboard access | Login page loaded; valid synthetic account | 1. Navigate to `[URL]`<br>2. Enter valid email<br>3. Enter valid password<br>4. Click "Sign in"<br>5. Verify redirect | Valid creds | User is authenticated and redirected to the dashboard; session created | Critical | Y | `[Verified / Inference]` |
| TC-F-002 | Functional | Remember Me persists session | Valid account | 1. Select "Remember me"<br>2. Login<br>3. Close browser, reopen<br>4. Verify session | Valid creds | Session persists per Remember Me semantics `[verify & document duration]` | High | Y | `[ ]` |
| TC-F-003 | Functional | Session timeout — idle expiry | Valid logged-in session | 1. Login<br>2. Remain idle past timeout<br>3. Act | Valid creds | Session expires after configured timeout `[verify & document value]` | High | Y | `[ ]` |
| TC-F-004 | Functional | 2FA challenge after credential verification | 2FA-enabled account | 1. Login with credentials<br>2. Verify 2FA prompt | Valid creds + 2FA code | 2FA challenge presented before dashboard access | High | Y | `[ ]` |
| TC-F-005 | Functional | SSO login via enterprise IdP | SSO test account | 1. Click "Sign in using SSO"<br>2. Complete IdP authentication | SSO creds | User authenticated via IdP and redirected to dashboard | High | Y | `[ ]` |
| TC-F-006 | Functional | Social login via Google / Microsoft | Social test account | 1. Click "Sign in with Google/Microsoft"<br>2. Complete consent | OAuth test account | Successful OAuth authentication | High | Y | `[ ]` |

### 4.2 Functional — Negative & Error Handling

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-N-001 | Negative | Valid email + wrong password | Login page loaded | 1. Enter valid email<br>2. Enter wrong password<br>3. Click "Sign in" | Valid email / wrong pass | Clear, actionable error; user remains on login; no account-existence leak | High | Y | `[ ]` |
| TC-N-002 | Negative | Unregistered email | Login page loaded | 1. Enter unregistered email<br>2. Enter password<br>3. Click "Sign in" | Unregistered email | Error shown; message does not reveal whether email exists | High | Y | `[ ]` |
| TC-N-003 | Negative | Malformed email (no `@`) | Login page loaded | 1. Enter `[value]`<br>2. Enter password<br>3. Submit | Malformed email | Validation error on blur (real-time validation per PRD) | Medium | Y | `[ ]` |
| TC-N-004 | Negative | Empty fields submission | Login page loaded | 1. Leave fields empty<br>2. Click "Sign in" | Empty / Empty | Clear validation message; no submission with empty required fields | High | Y | `[ ]` |
| TC-N-005 | Negative | Password visibility toggle correct | Login page loaded | 1. Enter password<br>2. Toggle visibility<br>3. Verify type | Test password | Field toggles masked ↔ plaintext correctly | Medium | Y | `[ ]` |

### 4.3 Boundary Value Analysis

> **Note:** Assert against the **actual** password policy (min/max length, character classes). If the policy is not documented, mark Verification Status **Insufficient information to determine** and record the observed boundary.

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-B-001 | Boundary | Email at minimum length | Login page loaded | 1. Enter `[min]`<br>2. Submit | Min-length email | Consistent validation; no crash | Medium | Y | `[ ]` |
| TC-B-002 | Boundary | Email at 254 chars (RFC 5321 max) | Login page loaded | 1. Enter 254-char email<br>2. Submit | 254-char email | No truncation; consistent outcome | Medium | Y | `[ ]` |
| TC-B-003 | Boundary | Email over 254 chars | Login page loaded | 1. Enter 255-char email<br>2. Submit | 255-char email | Rejected or truncated; no crash | Medium | Y | `[ ]` |
| TC-B-004 | Boundary | Password at min length | Login page loaded | 1. Enter min-length password<br>2. Submit | Min-length pass | Consistent outcome per policy | Medium | Y | `[ ]` |
| TC-B-005 | Boundary | Password at max length | Login page loaded | 1. Enter max-length password<br>2. Submit | Max-length pass | Accepted without truncation | Medium | Y | `[ ]` |
| TC-B-006 | Boundary | Password over max length | Login page loaded | 1. Enter max+1 password<br>2. Submit | Max+1 pass | Rejected or truncated; no crash | Medium | Y | `[ ]` |
| TC-B-007 | Boundary | Password character-class variants (lower / upper / digit / special / space / Unicode) | Login page loaded | 1. Enter variant<br>2. Submit | Variant per policy | No crash; consistent outcome; no encoding corruption | Low | Y | `[ ]` |
| TC-B-008 | Boundary | Whitespace-padded correct password | Login page loaded | 1. Enter correct password with surrounding spaces<br>2. Submit | Padded correct pass | **Security check:** if login succeeds, spaces were trimmed (report); if fails, spaces preserved | High | Y | `[ ]` |

### 4.4 Security — Injection (SQLi / XSS / Command)

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-S-001 | Security (SQLi) | OR-based SQLi in email field | Login page loaded | 1. Enter `' OR '1'='1` in email<br>2. Enter password<br>3. Submit | `' OR '1'='1` | No authentication bypass; no SQL error visible; no crash | Critical | Y | `[ ]` |
| TC-S-002 | Security (SQLi) | OR-based SQLi in password field | Login page loaded | 1. Enter valid email<br>2. Enter `' OR '1'='1`<br>3. Submit | `' OR '1'='1` | No bypass; no crash | Critical | Y | `[ ]` |
| TC-S-003 | Security (SQLi) | DROP TABLE attempt | Login page loaded | 1. Enter `'; DROP TABLE users;--`<br>2. Submit | DDL payload | Treated as literal; no DB damage | Critical | Y | `[ ]` |
| TC-S-004 | Security (SQLi) | Comment-based bypass | Login page loaded | 1. Enter `admin'--`<br>2. Submit | Comment payload | No bypass; no crash | Critical | Y | `[ ]` |
| TC-S-005 | Security (SQLi) | Time-based blind SQLi | Login page loaded | 1. Enter `' OR SLEEP(5)--`<br>2. Measure response time | Time-delay payload | No observable delay; no DB command execution | Critical | Y | `[ ]` |
| TC-S-006 | Security (XSS) | Script tag in email field | Login page loaded | 1. Enter `<script>alert(1)</script>`<br>2. Submit | XSS payload | Script not executed; rendered as text; no crash | Critical | Y | `[ ]` |
| TC-S-007 | Security (XSS) | Event-handler payload | Login page loaded | 1. Enter `"><img src=x onerror=alert(1)>`<br>2. Submit | Event payload | No script execution; output encoded | Critical | Y | `[ ]` |
| TC-S-008 | Security (Command) | Shell injection attempt | Login page loaded | 1. Enter `; ls -la` / `$(whoami)`<br>2. Submit | Shell payloads | Treated as literal; no shell execution | High | Y | `[ ]` |
| TC-S-009 | Security (NoSQL) | NoSQL operator payload | Login page loaded | 1. Enter `{ "$ne": null }`<br>2. Submit | Operator payload | Treated as literal; no operator injection | High | Y | `[ ]` |

### 4.5 Security — Authentication, Session & Compliance

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-S-010 | Security (Brute Force) | Account lockout after repeated failures | Valid account exists | 1. Submit wrong password N times<br>2. Submit correct password | Wrong ×N | Lockout eventually triggers `[verify & document threshold N]` | Critical | Y | `[ ]` |
| TC-S-011 | Security (Rate Limit) | Rapid failed logins throttled | Login page loaded | 1. Submit 10 rapid failed logins<br>2. Observe | 10 attempts | No unbounded throughput; throttle applies `[verify & document limit]` | Critical | Y | `[ ]` |
| TC-S-012 | Security (Enumeration) | Error message does not reveal account existence | Login page loaded | 1. Valid email + wrong pass<br>2. Invalid email + wrong pass<br>3. Compare | Both cases | Identical (or non-revealing) error message | High | Y | `[ ]` |
| TC-S-013 | Security (Transport) | HTTPS enforced | Login page loaded | 1. Attempt HTTP URL<br>2. Observe redirect | HTTP URL | Redirect to HTTPS; TLS on all auth traffic | High | Y | `[ ]` |
| TC-S-014 | Security (Cookies) | Session cookie flags post-login | Valid logged-in session | 1. Login<br>2. Inspect cookies | Valid creds | HttpOnly/Secure/SameSite per policy `[verify & document]` | Critical | Y | `[ ]` |
| TC-S-015 | Security (Session) | Session fixation — cookie regenerated on login | Valid account | 1. Capture pre-login cookie<br>2. Login<br>3. Compare | Pre-auth cookie | Cookie value changes after login (no fixation) | High | Y | `[ ]` |
| TC-S-016 | Security (Session) | Idle timeout expires session | Valid logged-in session | 1. Login<br>2. Wait idle<br>3. Act | — | Session expires per configurable timeout `[verify & document]` | High | Y | `[ ]` |
| TC-S-017 | Security (Logout) | Logout invalidates session | Valid logged-in session | 1. Login<br>2. Log out<br>3. Reuse old token | Valid session | Session no longer valid after logout | Critical | Y | `[ ]` |
| TC-S-018 | Security (CSRF) | Login submission protected from cross-origin forgery | Intercepting proxy | 1. Inspect for CSRF token<br>2. Submit forged cross-origin request | Forged request | Forged cross-origin login rejected `[verify & document mechanism]` | High | Y | `[ ]` |
| TC-S-019 | Security (Open Redirect) | Post-login redirect restricted to same-origin | Login page loaded | 1. Craft redirect param to external domain<br>2. Login | Malicious redirect | No redirect to external domain | Critical | Y | `[ ]` |
| TC-S-020 | Security (Headers) | Security headers on login response | Login page loaded | 1. Inspect response headers | — | Headers per policy (CSP, HSTS, X-Frame-Options, etc.) `[verify & document]` | High | Y | `[ ]` |
| TC-S-021 | Security (Timing) | Response timing does not reveal account existence | Timing capture | 1. Time valid vs invalid email responses<br>2. Compare | Two cases | No gross timing difference | Medium | Y | `[ ]` |
| TC-S-022 | Security (Clickjacking) | Page cannot be framed | Login page loaded | 1. Load page in iframe from other origin | — | Framing blocked; clickjacking protection present | High | Y | `[ ]` |
| TC-S-023 | Security (Credential Stuffing) | Breach-password check on login | Valid account exists | 1. Login with known-breached password | Breached pass | Blocked or flagged per policy `[verify & document]` | High | Y | `[ ]` |
| TC-S-024 | Security (Compliance) | GDPR / CCPA data-handling review | Login page loaded | 1. Inspect data collection/consent surfaces | — | No unnecessary PII collection; consent options available | High | N | `[ ]` |

### 4.6 Usability & Accessibility

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-U-001 | Usability | Fields have visible labels | Login page loaded | 1. Inspect fields | — | "Email address" and "Password" labels visible | High | Y | `[ ]` |
| TC-U-002 | Usability | Password visibility toggle operable | Login page loaded | 1. Click toggle<br>2. Verify type switch | — | Toggle switches masked ↔ plaintext; accessible name present | High | Y | `[ ]` |
| TC-U-003 | Usability | Enter key submits the form | Login page loaded | 1. Type credentials<br>2. Press Enter | Valid creds | Form submits via Enter | High | Y | `[ ]` |
| TC-U-004 | Usability | Keyboard Tab order covers all controls | Login page loaded | 1. Tab through page | — | Focus order logical; no focus trap | High | Y | `[ ]` |
| TC-U-005 | Usability | Auto-focus on first input | Login page loaded | 1. Load page | — | First input (email) auto-focused per PRD | Medium | Y | `[ ]` |
| TC-U-006 | Usability | Loading state during authentication | Login page loaded | 1. Submit credentials<br>2. Observe button | Valid creds | Clear loading feedback; no double submission | Medium | Y | `[ ]` |
| TC-U-007 | Usability | Responsive at 375px viewport | Mobile viewport | 1. Set 375×667<br>2. Inspect layout | Mobile | No horizontal scroll; touch-friendly controls (≥44px targets) | Medium | Y | `[ ]` |
| TC-U-008 | Usability | Responsive at 768px viewport | Tablet viewport | 1. Set 768×1024<br>2. Inspect | Tablet | Layout adapts; no overlap | Medium | Y | `[ ]` |
| TC-U-009 | Usability | Content usable at 200% zoom | Login page loaded | 1. Zoom to 200%<br>2. Interact | 200% zoom | No clipping; no horizontal scroll (WCAG 1.4.4) | Medium | Y | `[ ]` |
| TC-U-010 | Accessibility | Screen reader announces labels | NVDA/VoiceOver/TalkBack | 1. Navigate with screen reader | — | ARIA labels announced; controls have accessible names | High | N | `[ ]` |
| TC-U-011 | Accessibility | High-contrast mode | Login page loaded | 1. Enable high-contrast<br>2. Verify contrast | — | Text contrast ≥ WCAG 2.1 AA (4.5:1); theme adapts | High | N | `[ ]` |
| TC-U-012 | Accessibility | Full keyboard navigation | Login page loaded | 1. Operate all controls with keyboard only | — | All interactive elements reachable & operable via keyboard | High | Y | `[ ]` |
| TC-U-013 | Usability | Light & Dark Mode | Login page loaded | 1. Toggle theme<br>2. Verify both states | Light / Dark | Both themes render; no contrast/layout regressions | Medium | Y | `[ ]` |

### 4.7 API — Authentication & SSO

> **Note:** No API endpoints/schemas are provided. Verify *behavioral contracts* (valid succeeds, invalid fails, no leakage) and label status codes as **Inference (low confidence)** until the contract is supplied.

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-A-001 | API | Valid credentials authenticate | API client ready; endpoint known | 1. POST valid credentials<br>2. Inspect response | Valid creds | Success; token/session returned `[Inference: HTTP 200]` | High | Y | `[ ]` |
| TC-A-002 | API | Invalid credentials rejected | API client ready | 1. POST invalid credentials<br>2. Inspect response | Invalid creds | Failure; no sensitive detail leaked `[Inference: HTTP 401]` | High | Y | `[ ]` |
| TC-A-003 | API | Empty/malformed payload rejected | API client ready | 1. POST missing-field payload<br>2. Inspect | Malformed | Validation error `[Inference: HTTP 400/422]` | High | Y | `[ ]` |
| TC-A-004 | API | SSO token exchange with valid code | SSO IdP mock | 1. Exchange valid auth code<br>2. Inspect | Valid code | Token returned | Critical | Y | `[ ]` |
| TC-A-005 | API | SSO with invalid auth code rejected | SSO IdP mock | 1. Exchange forged/invalid code<br>2. Inspect | Invalid code | Rejected; no token issued | Critical | Y | `[ ]` |
| TC-A-006 | API | SSO with expired auth code rejected | SSO IdP mock | 1. Wait past expiry<br>2. Exchange | Expired code | Rejected | High | Y | `[ ]` |
| TC-A-007 | API | Tampered/forged SSO token rejected | API client ready | 1. Obtain token<br>2. Tamper<br>3. Call protected endpoint | Tampered token | Rejected; resource not exposed | Critical | Y | `[ ]` |
| TC-A-008 | API | No token → protected resource denied | API client ready | 1. Call endpoint without token | None | Denied `[Inference: HTTP 401]` | Critical | Y | `[ ]` |
| TC-A-009 | API | Rate limiting on auth endpoint | API client ready | 1. Send rapid requests<br>2. Inspect status/headers | Rapid requests | Throttle applies `[verify & document limit]` | High | Y | `[ ]` |
| TC-A-010 | API | SQLi payload via API rejected | API client ready | 1. POST `' OR '1'='1` as email<br>2. Inspect | SQLi payload | No bypass; no SQL error in body | Critical | Y | `[ ]` |
| TC-A-011 | API | Time-based SQLi has no delay | API client ready | 1. POST `' OR SLEEP(5)--`<br>2. Measure time | SQLi payload | No observable delay | Critical | Y | `[ ]` |
| TC-A-012 | API | Union-based SQLi leaks no data | API client ready | 1. POST `' UNION SELECT ...`<br>2. Inspect | Union payload | No data leakage in response | Critical | Y | `[ ]` |

### 4.8 Compatibility & Performance

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-C-001 | Compatibility | Login works in Chrome latest 2 | Chrome installed | 1. Run core functional suite in Chrome | — | No functional regression | High | Y | `[ ]` |
| TC-C-002 | Compatibility | Login works in Firefox latest 2 | Firefox installed | 1. Run core suite in Firefox | — | No regression | High | Y | `[ ]` |
| TC-C-003 | Compatibility | Login works in Safari latest 2 | Safari installed | 1. Run core suite in Safari | — | No regression | High | Y | `[ ]` |
| TC-C-004 | Compatibility | Login works in Edge latest 2 | Edge installed | 1. Run core suite in Edge | — | No regression | High | Y | `[ ]` |
| TC-C-005 | Compatibility | Login works on iOS Safari | BrowserStack/iOS | 1. Run core suite on iOS Safari | — | No regression; touch targets usable | High | Y | `[ ]` |
| TC-C-006 | Compatibility | Login works on Android Chrome | BrowserStack/Android | 1. Run core suite on Android Chrome | — | No regression; touch targets usable | High | Y | `[ ]` |
| TC-C-007 | Performance | Page load ≤ 2 s on standard connection | Throttled network | 1. Load page, measure | Standard connection | Page load ≤ 2 s (PRD KPI) | High | Y | `[ ]` |
| TC-C-008 | Performance | Auth API response time | API client ready | 1. Time login request<br>2. Record | Valid creds | Within agreed baseline `[verify & document]` | Medium | Y | `[ ]` |
| TC-C-009 | Performance | Concurrency sanity — parallel logins | Load tool | 1. Run N concurrent logins<br>2. Observe errors | N users | No failures/crashes at sanity level `[verify & document N]` | Medium | Y | `[ ]` |

---

## 5. Traceability & Coverage

### 5.1 Requirements Traceability (Req → Scenario Group)

| Req ID | PRD Requirement | Scenario Group(s) | Priority |
|---|---|---|---|
| RQ-01 | Primary authentication (email + password) | TC-F-001, TC-N-001..005 | P0 |
| RQ-02 | Session management / configurable timeout | TC-F-002..003, TC-S-015..017 | P0 |
| RQ-03 | Optional 2FA/MFA | TC-F-004 | P1 |
| RQ-04 | Enterprise SSO (SAML, OAuth) | TC-F-005, TC-A-004..008 | P0 |
| RQ-05 | Social login (Google, Microsoft) | TC-F-006 | P1 |
| RQ-06 | Real-time validation, email format, password strength | TC-N-003, TC-B-001..008 | P1 |
| RQ-07 | Clear error handling | TC-N-001..004, TC-U-003 | P1 |
| RQ-08 | Forgot Password flow | `[TC-FP-xxx]` | P0 |
| RQ-09 | Enforced password complexity | TC-B-004..008 | P1 |
| RQ-10 | Remember Me | TC-F-002 | P0 |
| RQ-11 | Responsive/mobile UX, auto-focus, labels, loading | TC-U-005..009, TC-C-005..006 | P1 |
| RQ-12 | Accessibility (screen reader, contrast, keyboard) | TC-U-010..012 | P1 |
| RQ-13 | Light & Dark Mode | TC-U-013 | P2 |
| RQ-14 | Branding & visual consistency | `[TC-BRAND-xxx]` | P3 |
| RQ-15 | Security (encryption, hashing, tokens, HTTPS, rate limit) | TC-S-001..023 | P0 |
| RQ-16 | Performance (page load ≤ 2 s, CDN, concurrency) | TC-C-007..009 | P1 |
| RQ-17 | Compliance (GDPR, CCPA, audit) | TC-S-024 | P1 |
| RQ-18 | Integration (dashboard, analytics, support, marketing) | `[TC-INT-xxx]` | P1 |
| RQ-19 | Compatibility matrix | TC-C-001..006 | P0 |

### 5.2 Coverage Map (per source requirement)

| Coverage Area | Template Section | Cases |
|---|---|---|
| Functional — Positive | 4.1 | TC-F-001..006 |
| Functional — Negative | 4.2 | TC-N-001..005 |
| Boundary Value Analysis | 4.3 | TC-B-001..008 |
| Security — Injection | 4.4 | TC-S-001..009 |
| Security — Auth/Session/Compliance | 4.5 | TC-S-010..024 |
| Usability & Accessibility | 4.6 | TC-U-001..013 |
| API — Auth & SSO | 4.7 | TC-A-001..012 |
| Compatibility & Performance | 4.8 | TC-C-001..009 |

### 5.3 Execution Workflow

1. Smoke (TC-F-001) → 2. Functional P0 → 3. Negative/BVA → 4. Security → 5. Usability/Accessibility → 6. API → 7. Cross-browser/performance → 8. Regression.

---

## 6. Anti-Hallucination Protocol (Mandatory)

Every test case row must be labeled with its **Verification Status**:

| Label | Meaning |
|---|---|
| **Verified** | Directly traceable to a provided source (PRD, screenshot, DOM probe, run result) with a source tag: `[PRD]`, `[DOM]`, `[SS]`, `[RUN]` |
| **Inference (low confidence)** | Logical deduction that must be confirmed before execution; expected results phrased as "should" with alternatives |
| **Insufficient information to determine** | Cannot be asserted without app-specific config (lockout thresholds, rate limits, timeouts, cookie flags, API schemas) — record as a *verify-and-document* check |

**Process (deterministic, mandatory):**

1. Extract verifiable facts from provided input (PRD, screenshots, DOM, runs).
2. List unknown/missing information.
3. Generate output strictly from Step 1 facts; label every inference.
4. Self-check for hallucinations or contradictions.
5. Configuration-dependent values (thresholds, limits, timeouts, status codes, cookie flags) are **verify-and-document** checks — never asserted as fact.
6. If any step cannot be completed, stop and report why.

**Self-Validation Check:**

- [ ] Every scenario maps to a requirement (no orphan scenarios — Section 5.1).
- [ ] Every row has numbered, independently executable steps.
- [ ] Verification Status filled for every row.
- [ ] No error codes, endpoints, or behaviors invented.
- [ ] Synthetic test data only; no production data.

---

## 7. Summary Metrics (fill at suite completion)

| Metric | Count |
|---|---|
| Total Test Cases | `[ ]` |
| Functional (Positive) | `[ ]` |
| Functional (Negative) | `[ ]` |
| Boundary Value Analysis | `[ ]` |
| Security — Injection | `[ ]` |
| Security — Auth/Session/Compliance | `[ ]` |
| Usability & Accessibility | `[ ]` |
| API — SSO & Auth | `[ ]` |
| Compatibility & Performance | `[ ]` |
| Critical / High / Medium / Low priority | `[ ] / [ ] / [ ] / [ ]` |
| Automation Ready (Y) / (N) | `[ ] / [ ]` |
| Verified / Inference / Insufficient info | `[ ] / [ ] / [ ]` |

---

## 8. Approvals

> **Not final; not baselined** until signed.

| Role | Name | Signature / Date |
|---|---|---|
| Test Case Author | `[ ]` | `[ ]` |
| Test Lead (Reviewer) | `[ ]` | `[ ]` |
| Project Manager | `[ ]` | `[ ]` |
| Product Owner | `[ ]` | `[ ]` |
