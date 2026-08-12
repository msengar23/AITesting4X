# Taste — QA / Test Automation Framework

- Prefers enterprise-grade Playwright + TypeScript automation frameworks built with Page Object Model (POM), custom fixtures, and hooks / setup-teardown logic. Confidence: 0.9
- Requires all element selection to use only Playwright locators and XPath; explicitly forbids CSS selectors, IDs, names, and other selector types in automation code. Confidence: 0.95
- Wants Page Object classes with constructor initialization and reusable functions. Confidence: 0.9
- Requires credentials and config to come from environment variables (.env / process.env) with session storage handling; hardcoded credentials are forbidden. Confidence: 0.95
- Wants robust exception handling in both page objects and spec files, with structured test.describe blocks. Confidence: 0.85
- Prefers separating valid and invalid login flows into distinct spec files (e.g., a valid spec and an invalid spec) rather than one combined script. Confidence: 0.85
- When generating automation code, wants output to be runnable code only — no comments, explanations, or extra text in the deliverables. Confidence: 0.8
- Expects a modular framework layout with separate files for: page object, spec files, fixture, .env, and hooks. Confidence: 0.8
- When explicitly scoping a request (e.g., "give only template for .env file"), wants just that artifact — a .env template with keys but empty values (no sample/dummy credentials or test values filled in), no extra files or surrounding commentary. Confidence: 0.9
- Wants Allure reporting integrated for test execution, wired into the Playwright config and package.json (e.g., allure-playwright reporter + scripts). Confidence: 0.85
- Expects the framework configuration to support multiple environments (external URLs, staging URLs) with credentials supplied externally at runtime via .env — never hardcoded. Confidence: 0.7
- Authorizes the agent to install any required dependencies (reporter packages, browsers) as part of delivering the framework rather than asking first. Confidence: 0.6
- Prefers to enter real credentials into .env manually himself; the agent should not write real credential values and should just continue once the user confirms they are filled. Confidence: 0.7
- Treats `.env` as strictly private: never commits `.env` or `.env.example` to version control; if a template is needed, only a sanitized placeholder template (empty values, no real credentials) may be made, and `.env.example` should stay in sync with every key in `.env` — `.env` is the sole runtime config that matters for tests. Explicitly confirmed: when a tracked `.env.example` contains real-looking credentials and is about to be committed/pushed, the user approves replacing those values with placeholders (e.g., `<your-valid-username@example.com>`) so no real credentials ever land in the repo. Confidence: 0.97
- Wants env files left exactly as they exist on disk: when told "use only template of .env file" / "skip all .env file content keep template" / "skip .env and .env.example file", the agent must not rewrite or sanitize `.env.example` (even to strip real-looking credentials) and must not touch the real `.env` — use the existing template as-is and continue without further edits, no matter how many times it is restated. Confidence: 0.95
