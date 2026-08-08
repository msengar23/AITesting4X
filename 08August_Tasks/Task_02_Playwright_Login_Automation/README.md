# Task_02_Playwright_Login_Automation — Wingify Login Automation Framework

Enterprise-grade Playwright + TypeScript automation framework for the Wingify login page (`https://app.wingify.com/#/login`).

## Tech Stack

- **Playwright Test** (`@playwright/test`)
- **TypeScript** with strict mode
- **Page Object Model (POM)** + Page Factory
- **Fixtures** (extended `test` with `pageFactory`, `credentials`, `invalidCredentials`)
- **Hooks** (global setup / teardown)
- **Allure** reporting + HTML reporter
- **dotenv** environment configuration

## Project Structure

```
.
├── src/
│   ├── pages/
│   │   ├── LoginPage.ts        # POM with constructor initialization + reusable actions
│   │   └── PageFactory.ts      # Page factory exposing page objects
│   ├── fixtures/
│   │   └── fixtures.ts         # Extended test fixtures (pageFactory, credentials)
│   ├── hooks/
│   │   ├── global-setup.ts     # Global setup: validate login page + seed session
│   │   └── global-teardown.ts  # Global teardown: clear session state
│   └── utils/
│       ├── env-config.ts       # dotenv loader + typed env access
│       └── session-storage.ts  # Credential seeding/reading via sessionStorage
├── tests/
│   ├── login-valid.spec.ts     # 7 valid-login test cases
│   └── login-invalid.spec.ts   # 7 invalid-login test cases
├── .env.example                # Environment template (fill values into .env)
├── playwright.config.ts        # Playwright config (Allure + HTML + list reporters)
├── package.json
└── tsconfig.json
```

## Setup

```bash
npm install
npx playwright install chromium
cp .env.example .env   # then fill in credentials
```

## Running Tests

| Command | Description |
|---|---|
| `npm test` | Run the full suite |
| `npm run test:valid` | Run valid-login spec |
| `npm run test:invalid` | Run invalid-login spec |
| `npm run test:headed` | Run in headed mode |
| `npm run test:debug` | Run with Playwright debugger |
| `npm run allure:generate` | Generate Allure report from `allure-results` |
| `npm run allure:open` | Open the generated Allure report |
| `npm run allure:serve` | Serve Allure results live |

## Environment Variables (`.env`)

| Key | Description |
|---|---|
| `BASE_URL` | Application under test URL |
| `VALID_USERNAME` / `VALID_PASSWORD` | Valid credentials (stored in sessionStorage, never hardcoded) |
| `INVALID_USERNAME` / `INVALID_PASSWORD` | Invalid credentials for negative tests |
| `INVALID_CREDENTIALS_MESSAGE` | Expected error message text |
| `FORGOT_PASSWORD_EMAIL` | Email used in forgot-password flow |
| `CI` | CI flag (enables retries + forbidOnly) |
| `HEADLESS` | Run headless (`true`) or headed (`false`) |
| `REPORTER` | Reporter selection |

> **Security:** `.env` is git-ignored and never committed. Only `.env.example` (empty template) is version-controlled. Real credentials stay local.

## Verification Status

All 14 tests (7 valid + 7 invalid) verified passing against the live Wingify login page.
