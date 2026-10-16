# Test Plan — SAM1-1: Define Project Timeline Framework

> ⚠️ **AI-generated draft — requires human review.**
> This test plan was produced automatically from a Jira issue. It is a starting point, not a substitute for QA judgement. Review every case and add any missing domain or business-critical scenarios.

## At a Glance

| | |
|---|---|
| **Test cases** | 5 (3 positive · 2 negative/edge) |
| **Focus areas** | Standardized templates for timeline creation · Guidelines for timeline adjustments · Roles and responsibilities for team members |
| **Techniques** | Boundary Value Analysis · Equivalence Partitioning · Decision Table · State Transition · Error Guessing |
| **Grounding** | Description only — no Acceptance Criteria field on this project |
| **Review status** | ⚠️ Draft — human review required |

## Details

| Field | Value |
|---|---|
| Jira Issue | [SAM1-1](https://vandysengar.atlassian.net/browse/SAM1-1) |
| Summary | Define Project Timeline Framework |
| Type | Epic |
| Priority | — |
| Status | To Do |
| Components | None |
| Model | `openai/gpt-oss-120b` |
| Generated | 2026-09-12 00:51 |

## 1. Objective

This test plan verifies that the timeline framework defined in the Epic supports creation of timelines using standardized templates, enforces adjustment guidelines, and respects defined roles and responsibilities for team members.

## 2. Preconditions

- Test environment with timeline management module deployed
- User accounts with defined roles (e.g., Project Manager, Team Member) available
- Standardized timeline template(s) uploaded in the system

## 3. Test Data

- Template ID: TPL-STD-001
- Timeline start date: 2026-10-01
- Timeline end date: 2026-12-31
- User credentials for Project Manager and Team Member

## 4. Test Cases

### Summary

| ID | Test case | Priority | Type | Technique |
|---|---|---|---|---|
| TC-001 | Create timeline using standardized template | High | Positive | Equivalence Partitioning |
| TC-002 | Prevent timeline creation without selecting a template | Medium | Negative | Error Guessing |
| TC-003 | Enforce adjustment guidelines on timeline dates | High | Boundary | Boundary Value Analysis |
| TC-004 | Validate role-based permission for timeline modification | High | Positive | Decision Table |
| TC-005 | Allow Project Manager to adjust timeline per guidelines | Medium | Positive | State Transition |

### TC-001 — Create timeline using standardized template

- **Priority:** High
- **Type:** Positive
- **Technique:** Equivalence Partitioning
- **Traceability:** Standardized templates for timeline creation

**Steps:**

1. Log in as Project Manager
2. Navigate to Timeline Creation page
3. Select standardized template TPL-STD-001
4. Enter required timeline details and save

**Expected Result:** Timeline is created successfully and displayed with the selected template attributes

### TC-002 — Prevent timeline creation without selecting a template

- **Priority:** Medium
- **Type:** Negative
- **Technique:** Error Guessing
- **Traceability:** Standardized templates for timeline creation

**Steps:**

1. Log in as Project Manager
2. Navigate to Timeline Creation page
3. Leave template selection empty
4. Enter required timeline details and attempt to save

**Expected Result:** System displays an error message indicating that a template must be selected and does not create the timeline

### TC-003 — Enforce adjustment guidelines on timeline dates

- **Priority:** High
- **Type:** Boundary
- **Technique:** Boundary Value Analysis
- **Traceability:** Guidelines for timeline adjustments

**Steps:**

1. Log in as Project Manager
2. Open an existing timeline
3. Attempt to change the end date to a value earlier than the start date
4. Save the changes

**Expected Result:** System rejects the change and shows a validation message that end date cannot be earlier than start date

### TC-004 — Validate role-based permission for timeline modification

- **Priority:** High
- **Type:** Positive
- **Technique:** Decision Table
- **Traceability:** Roles and responsibilities for team members

**Steps:**

1. Log in as Team Member
2. Navigate to an existing timeline owned by another user
3. Attempt to edit the timeline details

**Expected Result:** System prevents the edit and displays an access denied message

### TC-005 — Allow Project Manager to adjust timeline per guidelines

- **Priority:** Medium
- **Type:** Positive
- **Technique:** State Transition
- **Traceability:** Guidelines for timeline adjustments

**Steps:**

1. Log in as Project Manager
2. Open an existing timeline
3. Modify the end date within allowed range according to guidelines
4. Save the changes

**Expected Result:** Timeline is updated successfully and reflects the new end date

## 5. Coverage Summary

<!-- Computed by code from the validated test cases — not model-authored. -->

| Dimension | Breakdown |
|---|---|
| Total cases | 5 |
| By priority | High: 3 · Medium: 2 |
| By type | Positive: 3 · Negative: 1 · Boundary: 1 |
| By technique | Boundary Value Analysis: 1 · Equivalence Partitioning: 1 · Decision Table: 1 · State Transition: 1 · Error Guessing: 1 |

## 6. Risks

- Plan is based solely on the Epic description; detailed functional rules, UI flows, and error messages are not specified in the Jira issue
- Assumptions about role names and permission levels may not match actual implementation
- Guidelines for timeline adjustments are not detailed, so validation criteria are inferred

## 7. Out of Scope

- Performance testing of timeline operations
- Integration with external project management tools
- User interface layout and visual design verification
