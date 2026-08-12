# AITesting4X

QA automation and testing research repository. Contains task-based folders covering test plans, Playwright automation frameworks, test case documentation, and research on AI/ML concepts and Command Code slash commands.

## Repository Structure

| Folder | Description |
|---|---|
| [`02August_Tasks/`](02August_Tasks/) | Research on ML vs DL vs AI and the Anti-Hallucination rule for QA deliverables |
| [`08August_Tasks/`](08August_Tasks/) | Wingify/VWO login page: test plan, Playwright automation framework, and Jira-style test cases |
| [`27July_Task_Research_Command_CommandCode/`](27July_Task_Research_Command_CommandCode/) | Reference documentation for Command Code slash commands (`/goal`, `/compact`, `/mcp`) |

## Key Deliverables

- **Test Plan** — IEEE 829-aligned test plan for the Wingify/VWO login page (`08August_Tasks/Task_01_Test_Plan/TestPlan.md`)
- **Playwright Automation Framework** — Enterprise TypeScript framework with POM, fixtures, hooks, and Allure reporting (`08August_Tasks/Task_02_Playwright_Login_Automation/`)
- **Test Cases** — 98 Jira-format login test cases built under the Anti-Hallucination rule (`08August_Tasks/Task_03_Test_Case/TestCases_Login_VWO.md`)

## Security Note

Real credentials belong only in local `.env` files, which are git-ignored. `.env.example` files are documentation templates only and must never contain real values.
