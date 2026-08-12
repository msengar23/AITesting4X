# 08August_Tasks

QA testing tasks for the **Wingify / VWO** login page (`https://app.wingify.com/#/login`), completed in the August 8 batch.

## Tasks

| Folder | Description |
|---|---|
| [`Task_01_Test_Plan`](Task_01_Test_Plan/) | IEEE 829-aligned industry test plan for the login page |
| [`Task_02_Playwright_Login_Automation`](Task_02_Playwright_Login_Automation/) | Enterprise Playwright + TypeScript automation framework (POM, fixtures, hooks, Allure) |
| [`Task_03_Test_Case`](Task_03_Test_Case/) | Jira-format login test cases built under the Anti-Hallucination rule |

## Test Coverage Summary

- **Test Plan** — entry/exit criteria, defect management, traceability matrix, environment, automation plan
- **Automation Framework** — 14 passing tests (7 valid + 7 invalid login flows) against the live site
- **Test Cases** — 98 cases covering functional, negative, boundary value, security (SQLi/XSS), usability, SSO API, and compatibility
