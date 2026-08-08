# Taste — QA / Test Documentation Workflow
- Follows a strict anti-hallucination rule for QA/test deliverables: only assert facts traceable to provided input (e.g., screenshots, requirements), explicitly label every inference, and respond "Insufficient information to determine" for missing/unclear info rather than guessing. Confidence: 0.95
- Prefers outputs to follow a deterministic, structured process (extract verified facts → list unknowns → generate output → self-check for hallucinations/contradictions). Confidence: 0.9
- Prefers a technical, precise, enterprise-grade tone in deliverables, written as if they will be reviewed by a Project Manager. Confidence: 0.85
- Requires test documentation to follow industry standards (IEEE 829 / IEEE 29119) and cover all testing phases, tools, scope, and environment. Confidence: 0.9
- Wants per-phase entry and exit criteria, a defect management workflow with severity/priority classification, and a requirements traceability matrix (RTM) mapping requirements to test scenarios. Confidence: 0.9
- Keeps test plans and test cases as separate artifacts: a Test Plan must reference scenario groups only and must not contain actual test cases / execution scripts. Confidence: 0.85
- Expects structured deliverables following a defined outline (Objective, Scope, Test Strategy & Approach, Assumptions & Risks, Roles & Responsibilities, Schedule & Estimation, Test Environment, Defect Management, Entry & Exit Criteria, Test Automation Plan, Test Deliverables, Templates & Standards). Confidence: 0.9
