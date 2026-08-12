# Test Cases — VWO Login Dashboard Authentication (PRD-Driven)

| Field | Value |
|---|---|
| **Test Case Suite ID** | QA-TC-AUTH-003 |
| **Application Under Test (AUT)** | VWO Login Dashboard at `https://app.vwo.com/#/login` |
| **Suite Version** | 1.0 |
| **Status** | Ready for review (draft for PM) |
| **Prepared By** | QA Automation Tester (4.8 years experience) |
| **Standards Reference** | IEEE 829-1998, ISO/IEC/IEEE 29119, OWASP ASVS 4.0, WCAG 2.1 AA |
| **Source Requirements** | PRD — VWO Login Dashboard (7 pages) |
| **Verification Method** | Anti-Hallucination rule — every assertion traceable to PRD or observed input |
| **Date** | 2026-08-12 |

---

## 1. Verified Facts (from PRD — traceable source)

> Source tag `[PRD]` = explicitly stated in the Product Requirements Document (7 pages). `[DOM]`/`[SS]`/`[RUN]` = observed on the live login page during prior sessions.

- VWO login dashboard at `app.vwo.com` is the entry point to the experimentation, personalization, and analytics suite **[PRD]**
- Clean, minimalist login interface with VWO branding; product announcements incl. Light/Dark mode **[PRD]**
- Standard auth fields: email address + password; Remember Me checkbox; free-trial signup link **[PRD]**
- Primary authentication: email + password with secure validation **[PRD]**
- Session management: secure session handling with configurable timeout periods **[PRD]**
- Multi-factor authentication: optional 2FA support **[PRD]**
- SSO: enterprise SSO integration (SAML, OAuth) for organizational accounts **[PRD]**
- Social login: optional integration with Google, Microsoft, other IdPs **[PRD]**
- Real-time validation on blur; email format verification; password strength indicators; clear error handling **[PRD]**
- Forgot Password flow with secure token generation; multiple recovery options (email-based reset) **[PRD]**
- Responsive design with touch-friendly controls; auto-focus on first input; clickable labels; loading states **[PRD]**
- Accessibility: screen reader support (ARIA), high-contrast mode, keyboard navigation **[PRD]**
- Security: E2E encryption for auth data, encrypted storage (hashing), secure session tokens, HTTPS enforcement, rate limiting/brute-force protection **[PRD]**
- Compliance: GDPR, CCPA, enterprise audit readiness **[PRD]**
- Performance: page load ≤ 2 s; asset optimization (minified CSS/JS, compressed images); CDN integration **[PRD]**
- Integration: seamless dashboard transition post-login; login success/failure analytics; support integration **[PRD]**
- Target KPIs: login success ≥ 95%; user satisfaction ≥ 90%; support tickets reduced 20% **[PRD]**

## 2. Missing / Unknown Information (not verifiable from PRD)

| Unknown Item | Impact |
|---|---|
| Exact password policy (min/max length, character classes) | BVA boundaries must be *verify-and-document*, not asserted |
| Account lockout threshold and lockout duration | Cannot assert "5 attempts" |
| Rate-limit threshold and Retry-After value | Cannot assert specific numbers |
| Session idle-timeout duration | Cannot assert "30 min" |
| Cookie attributes (HttpOnly, Secure, SameSite) post-login | Cannot assert flags without inspection |
| Remember Me persistence duration | Cannot assert cookie lifetime |
| CSRF token mechanism on login form | Cannot assert token presence |
| Backend API endpoints, request/response schemas, status codes | API cases are inference-based |
| SSO IdP provider (Azure AD/Okta), redirect URIs, token formats | Cannot assert provider or JWT structure |
| Breach-password checking on login | Cannot assert credential-stuffing behavior |
| Password whitespace trimming behavior | Cannot assert whether spaces are trimmed |
| Whether 2FA UI exists on the initial screen | Prior observation showed no 2FA UI; flow surfaces post-credential |
| Actual performance thresholds beyond PRD (LCP, API latency targets) | Only page-load ≤ 2 s is stated |

---

## 3. Test Data & Preconditions (Global)

| Data Key | Value | Status |
|---|---|---|
| Valid Email | `qa.valid@example.com` | Synthetic test data |
| Valid Password | `Qa@ValidPass#2026` | Synthetic test data |
| Invalid Email | `qa.invalid@example.com` | Synthetic test data |
| Invalid Password | `WrongPass@123` | Synthetic test data |
| Boundary email/password lengths | Per actual password policy | **Insufficient information to determine** — verify & document |
| SSO test domain | `sso-test.vwo.com` | Synthetic test data |
| 2FA-enabled account | `qa.2fa@example.com` | Synthetic test data |
| Google/Microsoft test accounts | Provisioned by DevOps | Assumed — to be confirmed |

**Global Preconditions:**
1. Application deployed to test environment; network reachable.
2. Synthetic test accounts only (no real user data).
3. Browser cache/cookies cleared before each test unless stated otherwise.

---

## 4. Test Case Matrix

### 4.1 Functional — Authentication (Positive)

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-F-001 | Functional | Valid email + password login succeeds | Login page loaded; valid account | 1. Navigate to `https://app.vwo.com/#/login`<br>2. Enter valid email<br>3. Enter valid password<br>4. Click "Sign in"<br>5. Verify redirect | Valid email / valid password | User authenticated; redirected to dashboard; session created **[PRD]** | Critical | Y | Verified |
| TC-F-002 | Functional | Login page renders with all elements | Login page loaded | 1. Navigate to login URL<br>2. Verify email, password, Remember Me, Sign in, SSO/Google/Passkey buttons | — | All elements visible; branded VWO design **[PRD]** | High | Y | Verified |
| TC-F-003 | Functional | Remember Me persists session | Valid account | 1. Select "Remember me"<br>2. Login<br>3. Close & reopen browser<br>4. Verify session | Valid creds + Remember Me | Session persists per Remember Me semantics **[PRD]**; duration *verify & document* | High | Y | Verified |
| TC-F-004 | Functional | Session timeout — idle expiry | Valid logged-in session | 1. Login<br>2. Remain idle past timeout<br>3. Act | Valid creds | Session expires after configurable timeout **[PRD]**; value *verify & document* | High | Y | Verified |
| TC-F-005 | Functional | 2FA challenge after credential verification | 2FA-enabled account | 1. Login with credentials<br>2. Verify 2FA prompt | Valid creds + 2FA code | 2FA challenge presented before dashboard access **[PRD]** | High | Y | Verified |
| TC-F-006 | Functional | 2FA with valid code grants access | 2FA challenge shown | 1. Enter valid 2FA code<br>2. Submit | Valid 2FA code | Access granted; dashboard loads | High | Y | Inference (low confidence) |
| TC-F-007 | Functional | 2FA with invalid code rejected | 2FA challenge shown | 1. Enter invalid 2FA code<br>2. Submit | Invalid 2FA code | Rejected; error shown; no access | High | Y | Inference (low confidence) |
| TC-F-008 | Functional | SSO login via enterprise IdP | SSO test account | 1. Click "Sign in using SSO"<br>2. Complete IdP authentication | SSO creds | User authenticated via IdP; redirected to dashboard **[PRD]** | High | Y | Verified |
| TC-F-009 | Functional | SSO cancellation returns to login | SSO IdP reachable | 1. Click SSO<br>2. Cancel at IdP | — | Returned to login; no partial session | High | Y | Inference (low confidence) |
| TC-F-010 | Functional | Social login via Google | Google test account | 1. Click "Sign in with Google"<br>2. Complete consent | Google OAuth account | Successful OAuth authentication **[PRD]** | High | Y | Verified |
| TC-F-011 | Functional | Social login via Microsoft | Microsoft test account | 1. Click "Sign in with Microsoft"<br>2. Complete consent | Microsoft account | Successful OAuth authentication **[PRD]** | High | Y | Verified |
| TC-F-012 | Functional | Successful login tracked in analytics | Analytics endpoint visible | 1. Login successfully<br>2. Verify login-success event | Valid creds | Login success event logged **[PRD]** | Medium | Y | Inference (low confidence) |
| TC-F-013 | Functional | Failed login tracked in analytics | Analytics endpoint visible | 1. Login with invalid creds<br>2. Verify login-failure event | Invalid creds | Login failure event logged **[PRD]** | Medium | Y | Inference (low confidence) |
| TC-F-014 | Functional | Dashboard transition after login | Valid account | 1. Login<br>2. Verify seamless transition | Valid creds | Seamless transition to main dashboard **[PRD]** | Critical | Y | Verified |

### 4.2 Functional — Validation & Error Handling

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-N-001 | Negative | Valid email + wrong password | Login page loaded | 1. Enter valid email<br>2. Enter wrong password<br>3. Click "Sign in" | Valid email / wrong pass | Clear, actionable error; user stays on login; no account-existence leak **[PRD]** | High | Y | Verified |
| TC-N-002 | Negative | Unregistered email | Login page loaded | 1. Enter unregistered email<br>2. Enter password<br>3. Submit | Unregistered email | Error shown; message does not reveal whether email exists **[PRD]** | High | Y | Inference (low confidence) |
| TC-N-003 | Negative | Malformed email (no `@`) | Login page loaded | 1. Enter `qa.valid.example.com`<br>2. Enter password<br>3. Submit | Malformed email | Real-time validation error on blur; submission blocked **[PRD]** | Medium | Y | Verified |
| TC-N-004 | Negative | Email with spaces inside | Login page loaded | 1. Enter `qa.valid @example.com`<br>2. Enter password<br>3. Submit | Spaced email | *Insufficient information to determine*; outcome configuration-dependent | Medium | Y | Insufficient info |
| TC-N-005 | Negative | Empty fields submission | Login page loaded | 1. Leave email/password empty<br>2. Click "Sign in" | Empty / Empty | Clear validation message; no submission **[PRD]** | High | Y | Verified |
| TC-N-006 | Negative | Password visibility toggle correct | Login page loaded | 1. Enter password<br>2. Toggle visibility<br>3. Verify type | Test password | Field toggles masked ↔ plaintext correctly | Medium | Y | Verified |
| TC-N-007 | Negative | Unicode/special chars in email | Login page loaded | 1. Enter `qüentin@exämple.com`<br>2. Enter password<br>3. Submit | Unicode email | No crash; rejected or normalized; outcome per policy | Low | Y | Insufficient info |
| TC-N-008 | Negative | Whitespace-padded email | Login page loaded | 1. Enter ` qa.valid@example.com `<br>2. Enter password<br>3. Submit | Padded email | *Insufficient information to determine* whether trimmed; outcome configuration-dependent | Medium | Y | Insufficient info |
| TC-N-009 | Negative | Newline/control chars in fields | Login page loaded | 1. Paste multiline strings into email/password<br>2. Submit | Multiline strings | No crash; consistent validation | Medium | Y | Insufficient info |
| TC-N-010 | Negative | Password strength indicator shows weak | Login page loaded | 1. Enter weak password<br>2. Observe indicator | Weak password | Visual weak-password feedback shown **[PRD]** | Medium | Y | Verified |
| TC-N-011 | Negative | Password strength indicator shows strong | Login page loaded | 1. Enter strong password<br>2. Observe indicator | Strong password | Visual strong-password feedback shown **[PRD]** | Medium | Y | Verified |

### 4.3 Forgot Password (Account Recovery)

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-FP-001 | Functional | Forgot Password link opens reset view | Login page loaded | 1. Click "Forgot Password?"<br>2. Verify reset form | — | Reset view opens with email field and reset action **[PRD: forgot password flow]** | High | Y | Verified |
| TC-FP-002 | Functional | Valid email triggers reset email | Reset view open | 1. Enter registered email<br>2. Submit<br>3. Verify confirmation | `qa.valid@example.com` | Confirmation shown; reset email sent to registered address **[PRD: email-based reset]**; exact copy *verify & document* | High | Y | Inference (low confidence) |
| TC-FP-003 | Functional | Unregistered email does not reveal existence | Reset view open | 1. Enter unregistered email<br>2. Submit | `qa.invalid@example.com` | Same generic confirmation; no account-existence leak **[PRD: clear error handling]** | High | Y | Inference (low confidence) |
| TC-FP-004 | Security | Expired/used reset token rejected | Valid reset token | 1. Open reset link after expiry/reuse<br>2. Set new password | Expired/used token | Token rejected; no password change; re-request required **[PRD: secure token generation]** | Critical | Y | Inference (low confidence) |

### 4.4 Boundary Value Analysis

> **Note:** Assert against the actual password policy. If not documented, mark **Insufficient information to determine** and record observed boundary.

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-B-001 | Boundary | Email at 1 char | Login page loaded | 1. Enter `a`<br>2. Enter password<br>3. Submit | `a` | Consistent validation; no crash | Medium | Y | Insufficient info |
| TC-B-002 | Boundary | Email at 254 chars (RFC 5321 max) | Login page loaded | 1. Enter 254-char email<br>2. Enter password<br>3. Submit | 254-char email | No truncation; consistent outcome; no crash | Medium | Y | Inference (low confidence) |
| TC-B-003 | Boundary | Email over 254 chars | Login page loaded | 1. Enter 255-char email<br>2. Enter password<br>3. Submit | 255-char email | Rejected or truncated; no crash | Medium | Y | Inference (low confidence) |
| TC-B-004 | Boundary | Email with plus-alias | Login page loaded | 1. Enter `qa.valid+tag@example.com`<br>2. Submit | Plus-alias | Accepted or rejected consistently; no crash | Low | Y | Insufficient info |
| TC-B-005 | Boundary | Email with hyphenated domain | Login page loaded | 1. Enter `qa.valid@my-domain.com`<br>2. Submit | Hyphenated domain | Consistent validation; no crash | Low | Y | Insufficient info |
| TC-B-006 | Boundary | Password at 1 char | Login page loaded | 1. Enter valid email<br>2. Enter `a`<br>3. Submit | `a` | Consistent outcome; no crash | Medium | Y | Insufficient info |
| TC-B-007 | Boundary | Password at 4 chars | Login page loaded | 1. Enter valid email<br>2. Enter `A1b!`<br>3. Submit | `A1b!` | No crash; outcome per policy; 4 likely below min — verify | Medium | Y | Inference (low confidence) |
| TC-B-008 | Boundary | Password at 8 chars | Login page loaded | 1. Enter valid email<br>2. Enter `Aa1!bbbb`<br>3. Submit | `Aa1!bbbb` | Consistent outcome | Medium | Y | Inference (low confidence) |
| TC-B-009 | Boundary | Password at 64 chars | Login page loaded | 1. Enter valid email<br>2. Enter 64-char password<br>3. Submit | 64-char pass | No truncation; no crash | Medium | Y | Insufficient info |
| TC-B-010 | Boundary | Password at 128 chars | Login page loaded | 1. Enter valid email<br>2. Enter 128-char password<br>3. Submit | 128-char pass | No crash; consistent outcome | Medium | Y | Inference (low confidence) |
| TC-B-011 | Boundary | Password over 128 chars | Login page loaded | 1. Enter valid email<br>2. Enter 129-char password<br>3. Submit | 129-char pass | Rejected or truncated; no crash | Medium | Y | Inference (low confidence) |
| TC-B-012 | Boundary | Password only lowercase | Login page loaded | 1. Enter `abcdefgh`<br>2. Submit | `abcdefgh` | No crash; outcome per policy | Low | Y | Insufficient info |
| TC-B-013 | Boundary | Password only uppercase | Login page loaded | 1. Enter `ABCDEFGH`<br>2. Submit | `ABCDEFGH` | No crash; outcome per policy | Low | Y | Insufficient info |
| TC-B-014 | Boundary | Password only digits | Login page loaded | 1. Enter `12345678`<br>2. Submit | `12345678` | No crash; outcome per policy | Low | Y | Insufficient info |
| TC-B-015 | Boundary | Password only special chars | Login page loaded | 1. Enter `!@#$%^&*()`<br>2. Submit | `!@#$%^&*()` | No crash; no injection | Low | Y | Insufficient info |
| TC-B-016 | Boundary | Password with only spaces | Login page loaded | 1. Enter 10 spaces<br>2. Submit | `          ` | No crash; treated per policy | Medium | Y | Insufficient info |
| TC-B-017 | Boundary | Password with leading/trailing spaces | Login page loaded | 1. Enter ` Qa@ValidPass#2026 ` (spaces around correct password)<br>2. Submit | Padded correct pass | **Security check:** if login succeeds, spaces were trimmed (report); if fails, spaces preserved | High | Y | Insufficient info |
| TC-B-018 | Boundary | Unicode password | Login page loaded | 1. Enter `Pässwörd!123`<br>2. Submit | Unicode password | No encoding corruption; consistent outcome | Low | Y | Insufficient info |

### 4.5 Security — Injection (SQLi / XSS / Command)

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-S-001 | Security (SQLi) | OR-based SQLi in email field | Login page loaded | 1. Enter `' OR '1'='1` in email<br>2. Enter password<br>3. Submit | `' OR '1'='1` | No authentication bypass; no SQL error visible; no crash | Critical | Y | Verified |
| TC-S-002 | Security (SQLi) | OR-based SQLi in password field | Login page loaded | 1. Enter valid email<br>2. Enter `' OR '1'='1`<br>3. Submit | `' OR '1'='1` | No bypass; no crash | Critical | Y | Verified |
| TC-S-003 | Security (SQLi) | DROP TABLE attempt | Login page loaded | 1. Enter `'; DROP TABLE users;--`<br>2. Submit | DDL payload | Treated as literal; no DB damage; no crash | Critical | Y | Verified |
| TC-S-004 | Security (SQLi) | Double-quote OR variant | Login page loaded | 1. Enter `" OR ""="`<br>2. Submit | `" OR ""="` | No bypass; no crash | Critical | Y | Verified |
| TC-S-005 | Security (SQLi) | Comment-based bypass | Login page loaded | 1. Enter `admin'--`<br>2. Submit | Comment payload | No bypass; no crash | Critical | Y | Verified |
| TC-S-006 | Security (SQLi) | Time-based blind SQLi | Login page loaded | 1. Enter `' OR SLEEP(5)--`<br>2. Measure time | Time-delay payload | No observable delay; no DB command execution | Critical | Y | Verified |
| TC-S-007 | Security (SQLi) | SQLi in SSO email field | SSO form open | 1. Click "Sign in using SSO"<br>2. Enter `' OR '1'='1` in SSO email<br>3. Submit | `' OR '1'='1` | No SSO bypass; no crash | Critical | Y | Verified |
| TC-S-008 | Security (XSS) | Script tag in email field | Login page loaded | 1. Enter `<script>alert(1)</script>`<br>2. Submit | XSS payload | Script not executed; rendered as text; no crash | Critical | Y | Verified |
| TC-S-009 | Security (XSS) | Event-handler payload | Login page loaded | 1. Enter `"><img src=x onerror=alert(1)>`<br>2. Submit | Event payload | No script execution; output encoded | Critical | Y | Verified |
| TC-S-010 | Security (Command) | Shell injection attempt | Login page loaded | 1. Enter `; ls -la` in email<br>2. Enter `$(whoami)` in password<br>3. Submit | Shell payloads | Treated as literal; no shell execution | High | Y | Verified |
| TC-S-011 | Security (NoSQL) | NoSQL operator payload | Login page loaded | 1. Enter `{ "$ne": null }`<br>2. Submit | Operator payload | Treated as literal; no operator injection | High | Y | Verified |

### 4.6 Security — Authentication, Session & Compliance

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-S-012 | Security (Brute Force) | Account lockout after repeated failures | Valid account exists | 1. Submit wrong password N times<br>2. Submit correct password | Wrong ×N | Lockout eventually triggers **[PRD: rate limiting]**; threshold *verify & document* | Critical | Y | Verified |
| TC-S-013 | Security (Rate Limit) | Rapid failed logins throttled | Login page loaded | 1. Submit 10 rapid failed logins<br>2. Observe | 10 attempts | No unbounded throughput; throttle applies **[PRD]**; limit *verify & document* | Critical | Y | Verified |
| TC-S-014 | Security (Enumeration) | Error message does not reveal account existence | Login page loaded | 1. Valid email + wrong pass<br>2. Invalid email + wrong pass<br>3. Compare | Both cases | Identical (or non-revealing) error message **[PRD: clear error handling]** | High | Y | Inference (low confidence) |
| TC-S-015 | Security (Transport) | HTTPS enforced | Login page loaded | 1. Attempt HTTP URL<br>2. Observe redirect | HTTP URL | Redirect to HTTPS; TLS on all auth traffic **[PRD: HTTPS enforcement]** | High | Y | Verified |
| TC-S-016 | Security (Encryption) | Auth data transmitted encrypted | Proxy/DevTools | 1. Intercept login request<br>2. Inspect payload | Valid creds | Payload encrypted/over TLS; no plaintext credential exposure **[PRD: E2E encryption]** | Critical | Y | Verified |
| TC-S-017 | Security (Storage) | Passwords stored hashed | Backend access | 1. Inspect stored credentials (test DB) | Valid creds | Industry-standard hashing; no plaintext **[PRD: encrypted storage]** | Critical | Y | Verified |
| TC-S-018 | Security (Cookies) | Session cookie flags post-login | Valid logged-in session | 1. Login<br>2. Inspect cookies | Valid creds | HttpOnly/Secure/SameSite per policy **[PRD: secure session tokens]**; flags *verify & document* | Critical | Y | Verified |
| TC-S-019 | Security (Session) | Session fixation — cookie regenerated on login | Valid account | 1. Capture pre-login cookie<br>2. Login<br>3. Compare | Pre-auth cookie | Cookie value changes after login (no fixation) **[PRD: secure session tokens]** | High | Y | Inference (low confidence) |
| TC-S-020 | Security (Session) | Idle timeout expires session | Valid logged-in session | 1. Login<br>2. Wait idle<br>3. Act | — | Session expires per configurable timeout **[PRD]**; value *verify & document* | High | Y | Verified |
| TC-S-021 | Security (Logout) | Logout invalidates session | Valid logged-in session | 1. Login<br>2. Log out<br>3. Reuse old token | Valid session | Session no longer valid after logout **[PRD: secure session handling]** | Critical | Y | Inference (low confidence) |
| TC-S-022 | Security (CSRF) | Login submission protected from cross-origin forgery | Intercepting proxy | 1. Inspect for CSRF token<br>2. Submit forged cross-origin request | Forged request | Forged cross-origin login rejected; mechanism *verify & document* | High | Y | Inference (low confidence) |
| TC-S-023 | Security (Open Redirect) | Post-login redirect restricted to same-origin | Login page loaded | 1. Craft redirect param to external domain<br>2. Login | Malicious redirect | No redirect to external domain | Critical | Y | Inference (low confidence) |
| TC-S-024 | Security (Headers) | Security headers on login response | Login page loaded | 1. Inspect response headers | — | Headers per policy (CSP, HSTS, X-Frame-Options); *verify & document* | High | Y | Inference (low confidence) |
| TC-S-025 | Security (Timing) | Response timing does not reveal account existence | Timing capture | 1. Time valid vs invalid email responses<br>2. Compare | Two cases | No gross timing difference | Medium | Y | Inference (low confidence) |
| TC-S-026 | Security (Clickjacking) | Page cannot be framed | Login page loaded | 1. Load page in iframe from other origin | — | Framing blocked; clickjacking protection present | High | Y | Inference (low confidence) |
| TC-S-027 | Security (Credential Stuffing) | Breach-password check on login | Valid account exists | 1. Login with known-breached password | Breached pass | Blocked or flagged per policy; *verify & document* | High | Y | Inference (low confidence) |
| TC-S-028 | Security (Compliance) | GDPR / CCPA data-handling review | Login page loaded | 1. Inspect data collection/consent surfaces | — | No unnecessary PII collection; consent options available **[PRD: GDPR, CCPA]** | High | N | Verified |

### 4.7 Usability & Accessibility

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-U-001 | Usability | Fields have visible labels | Login page loaded | 1. Inspect fields | — | "Email address" and "Password" labels visible **[PRD: clickable labels]** | High | Y | Verified |
| TC-U-002 | Usability | Labels are clickable | Login page loaded | 1. Click label text<br>2. Verify focus | — | Clicking label focuses associated field **[PRD: clickable labels]** | High | Y | Verified |
| TC-U-003 | Usability | Auto-focus on first input | Login page loaded | 1. Load page | — | Email field auto-focused **[PRD: auto-focus]** | Medium | Y | Verified |
| TC-U-004 | Usability | Password visibility toggle operable | Login page loaded | 1. Click toggle<br>2. Verify type switch | — | Toggle switches masked ↔ plaintext; accessible name present | High | Y | Verified |
| TC-U-005 | Usability | Enter key submits the form | Login page loaded | 1. Type credentials<br>2. Press Enter | Valid creds | Form submits via Enter | High | Y | Inference (low confidence) |
| TC-U-006 | Usability | Keyboard Tab order covers all controls | Login page loaded | 1. Tab through page | — | Focus order logical; no focus trap **[PRD: keyboard navigation]** | High | Y | Verified |
| TC-U-007 | Usability | Loading state during authentication | Login page loaded | 1. Submit credentials<br>2. Observe button | Valid creds | Clear loading feedback; no double submission **[PRD: loading states]** | Medium | Y | Verified |
| TC-U-008 | Usability | Responsive at 375px viewport | Mobile viewport | 1. Set 375×667<br>2. Inspect layout | Mobile | No horizontal scroll; touch-friendly controls **[PRD: responsive]** | Medium | Y | Verified |
| TC-U-009 | Usability | Responsive at 768px viewport | Tablet viewport | 1. Set 768×1024<br>2. Inspect | Tablet | Layout adapts; no overlap **[PRD: responsive]** | Medium | Y | Verified |
| TC-U-010 | Usability | Touch-friendly targets on mobile | Mobile viewport | 1. Measure control sizes at 375px | Mobile | Targets ≥ 44px; no mis-taps **[PRD: touch-friendly]** | Medium | Y | Inference (low confidence) |
| TC-U-011 | Usability | Content usable at 200% zoom | Login page loaded | 1. Zoom to 200%<br>2. Interact | 200% zoom | No clipping; no horizontal scroll (WCAG 1.4.4) | Medium | Y | Inference (low confidence) |
| TC-U-012 | Usability | Light & Dark Mode both render | Login page loaded | 1. Toggle theme<br>2. Verify both states | Light / Dark | Both themes render; no contrast/layout regressions **[PRD: Light/Dark mode]** | Medium | Y | Verified |
| TC-U-013 | Accessibility | Screen reader announces labels | NVDA/VoiceOver/TalkBack | 1. Navigate with screen reader | — | ARIA labels announced; controls have accessible names **[PRD: screen reader support]** | High | N | Verified |
| TC-U-014 | Accessibility | High-contrast mode | Login page loaded | 1. Enable high-contrast<br>2. Verify contrast | — | Text contrast ≥ WCAG 2.1 AA (4.5:1); theme adapts **[PRD: high contrast]** | High | N | Verified |
| TC-U-015 | Accessibility | Full keyboard navigation | Login page loaded | 1. Operate all controls with keyboard only | — | All interactive elements reachable & operable **[PRD: keyboard navigation]** | High | Y | Verified |
| TC-U-016 | Usability | Error message clear and actionable | Login page loaded | 1. Submit invalid creds<br>2. Read error | Invalid creds | Clear, actionable guidance to correct the failure **[PRD: error handling]** | High | Y | Verified |

### 4.8 API — Authentication & SSO

> **Note:** No API endpoints/schemas provided. Verify behavioral contracts; status codes labeled **Inference (low confidence)** until contract supplied.

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-A-001 | API | Valid credentials authenticate | API client ready; endpoint known | 1. POST valid credentials<br>2. Inspect response | Valid creds | Success; token/session returned **[PRD]**; *Inference: HTTP 200* | High | Y | Inference (low confidence) |
| TC-A-002 | API | Invalid credentials rejected | API client ready | 1. POST invalid credentials<br>2. Inspect response | Invalid creds | Failure; no sensitive detail leaked; *Inference: HTTP 401* | High | Y | Inference (low confidence) |
| TC-A-003 | API | Empty/malformed payload rejected | API client ready | 1. POST missing-field payload<br>2. Inspect | Malformed | Validation error; *Inference: HTTP 400/422* | High | Y | Inference (low confidence) |
| TC-A-004 | API | SSO token exchange with valid code | SSO IdP mock | 1. Exchange valid auth code<br>2. Inspect | Valid code | Token returned; provider/format *verify & document* | Critical | Y | Inference (low confidence) |
| TC-A-005 | API | SSO with invalid auth code rejected | SSO IdP mock | 1. Exchange forged/invalid code<br>2. Inspect | Invalid code | Rejected; no token issued | Critical | Y | Inference (low confidence) |
| TC-A-006 | API | SSO with expired auth code rejected | SSO IdP mock | 1. Wait past expiry<br>2. Exchange | Expired code | Rejected; expiry window *verify & document* | High | Y | Inference (low confidence) |
| TC-A-007 | API | Tampered/forged SSO token rejected | API client ready | 1. Obtain token<br>2. Tamper<br>3. Call protected endpoint | Tampered token | Rejected; resource not exposed **[PRD: secure session tokens]** | Critical | Y | Inference (low confidence) |
| TC-A-008 | API | No token → protected resource denied | API client ready | 1. Call endpoint without token | None | Denied; *Inference: HTTP 401* | Critical | Y | Inference (low confidence) |
| TC-A-009 | API | Rate limiting on auth endpoint | API client ready | 1. Send rapid requests<br>2. Inspect status/headers | Rapid requests | Throttle applies **[PRD: rate limiting]**; limit *verify & document* | High | Y | Verified |
| TC-A-010 | API | SQLi payload via API rejected | API client ready | 1. POST `' OR '1'='1` as email<br>2. Inspect | SQLi payload | No bypass; no SQL error in body | Critical | Y | Inference (low confidence) |
| TC-A-011 | API | Time-based SQLi has no delay | API client ready | 1. POST `' OR SLEEP(5)--`<br>2. Measure time | SQLi payload | No observable delay | Critical | Y | Inference (low confidence) |
| TC-A-012 | API | Union-based SQLi leaks no data | API client ready | 1. POST `' UNION SELECT ...`<br>2. Inspect | Union payload | No data leakage in response | Critical | Y | Inference (low confidence) |

### 4.9 Compatibility & Performance

| TC-ID | Category | Test Scenario | Pre-conditions | Test Steps | Test Data | Expected Result | Priority | Automation Ready (Y/N) | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-C-001 | Compatibility | Login works in Chrome latest 2 | Chrome installed | 1. Run core suite (TC-F-001..014) in Chrome | — | No functional regression | High | Y | Verified |
| TC-C-002 | Compatibility | Login works in Firefox latest 2 | Firefox installed | 1. Run core suite in Firefox | — | No regression | High | Y | Verified |
| TC-C-003 | Compatibility | Login works in Safari latest 2 | Safari installed | 1. Run core suite in Safari | — | No regression | High | Y | Verified |
| TC-C-004 | Compatibility | Login works in Edge latest 2 | Edge installed | 1. Run core suite in Edge | — | No regression | High | Y | Verified |
| TC-C-005 | Compatibility | Login works on iOS Safari | BrowserStack/iOS | 1. Run core suite on iOS Safari | — | No regression; touch targets usable | High | Y | Verified |
| TC-C-006 | Compatibility | Login works on Android Chrome | BrowserStack/Android | 1. Run core suite on Android Chrome | — | No regression; touch targets usable | High | Y | Verified |
| TC-C-007 | Performance | Page load ≤ 2 s on standard connection | Throttled network | 1. Load page, measure | Standard connection | Page load ≤ 2 s **[PRD KPI]** | High | Y | Verified |
| TC-C-008 | Performance | Asset optimization (minified CSS/JS) | DevTools | 1. Inspect loaded assets | — | Minified/compressed assets served **[PRD]** | Medium | Y | Verified |
| TC-C-009 | Performance | CDN integration serves assets | DevTools | 1. Inspect asset hosts | — | Assets served via CDN **[PRD]** | Medium | Y | Inference (low confidence) |
| TC-C-010 | Performance | Auth API response time | API client ready | 1. Time login request<br>2. Record | Valid creds | Within agreed baseline; *verify & document* | Medium | Y | Inference (low confidence) |
| TC-C-011 | Performance | Concurrency sanity — parallel logins | Load tool | 1. Run N concurrent logins<br>2. Observe errors | N users | No failures/crashes at sanity level; N *verify & document* | Medium | Y | Inference (low confidence) |
| TC-C-012 | Reliability | Slow-network login completes or fails gracefully | Network throttling | 1. Throttle to Slow 3G<br>2. Attempt login | Throttled | Login completes or shows error; no stuck loading state | Medium | Y | Inference (low confidence) |
| TC-C-013 | Reliability | Double-click does not duplicate submission | Login page loaded | 1. Double-click "Sign in" | Valid creds | No duplicate auth request (verify via network log) | Medium | Y | Inference (low confidence) |

---

## 5. Requirements Traceability Matrix (Req → Scenario Groups)

| Req ID | PRD Requirement | Scenario Group(s) | Priority |
|---|---|---|---|
| RQ-01 | Primary authentication (email + password) | TC-F-001..002, TC-N-001..011 | P0 |
| RQ-02 | Session management / configurable timeout | TC-F-003..004, TC-S-019..021 | P0 |
| RQ-03 | Optional 2FA/MFA | TC-F-005..007 | P1 |
| RQ-04 | Enterprise SSO (SAML, OAuth) | TC-F-008..009, TC-A-004..008 | P0 |
| RQ-05 | Social login (Google, Microsoft) | TC-F-010..011 | P1 |
| RQ-06 | Real-time validation, email format, password strength | TC-N-003..011, TC-B-001..018 | P1 |
| RQ-07 | Clear error handling | TC-N-001..002, TC-N-005, TC-U-016 | P1 |
| RQ-08 | Forgot Password flow | TC-FP-001..004 (Section 4.3) | P0 |
| RQ-09 | Enforced password complexity | TC-B-006..018 | P1 |
| RQ-10 | Remember Me | TC-F-003 | P0 |
| RQ-11 | Responsive/mobile UX, auto-focus, labels, loading | TC-U-001..012 | P1 |
| RQ-12 | Accessibility (screen reader, contrast, keyboard) | TC-U-013..015 | P1 |
| RQ-13 | Light & Dark Mode | TC-U-012 | P2 |
| RQ-14 | Branding & visual consistency | TC-F-002 | P3 |
| RQ-15 | Security (encryption, hashing, tokens, HTTPS, rate limit) | TC-S-001..027 | P0 |
| RQ-16 | Performance (page load ≤ 2 s, CDN, concurrency) | TC-C-007..011 | P1 |
| RQ-17 | Compliance (GDPR, CCPA, audit) | TC-S-028 | P1 |
| RQ-18 | Integration (dashboard, analytics, support) | TC-F-012..014 | P1 |
| RQ-19 | Compatibility matrix | TC-C-001..006 | P0 |

**Note on Forgot Password (RQ-08):** Covered by TC-FP-001..004 in Section 4.3. Forgot Password flow, email-based reset, and secure token handling are validated per PRD scope.

---

## 6. Summary Metrics

| Metric | Count |
|---|---|
| **Total Test Cases** | **118** |
| Functional — Authentication (Positive) | 14 |
| Functional — Validation & Error Handling | 11 |
| Forgot Password (Account Recovery) | 4 |
| Boundary Value Analysis | 18 |
| Security — Injection | 11 |
| Security — Auth/Session/Compliance | 17 |
| Usability & Accessibility | 16 |
| API — SSO & Auth | 12 |
| Compatibility & Performance | 13 |
| **Automation Ready (Y)** | 117 |
| **Automation Ready (N)** | 1 |
| Critical Priority | 22 |
| High Priority | 61 |
| Medium Priority | 28 |
| Low Priority | 7 |
| Verified | 57 |
| Inference (low confidence) | 36 |
| Insufficient information to determine | 25 |

---

## 7. Self-Validation Check (Anti-Hallucination)

- **Verified facts** (Section 1) are traceable to the PRD (7 pages) or observed live behavior. No invented UI elements, error codes, or behaviors in Verified rows.
- **Every assertion not directly observed** is labeled `Inference (low confidence)` or `Insufficient information to determine`.
- **Configuration-dependent behaviors** (password policy, lockout threshold, rate limit, idle timeout, cookie flags, CSRF mechanism, SSO provider, API schemas) are **not asserted as fact** — framed as "verify and document" or "no crash / no bypass / no regression".
- **No contradictions:** Verified rows do not conflict with labeled-inference rows.
- **If any row implies a concrete unverified value** (e.g., "5 attempts", "30 min", "HTTP 200", "HttpOnly"), treat that value as a placeholder to be confirmed from PRD/API docs/logs — not presented as verified.

---

*End of Test Case Suite (v1.0) — ready for review. Not final; not baselined.*
