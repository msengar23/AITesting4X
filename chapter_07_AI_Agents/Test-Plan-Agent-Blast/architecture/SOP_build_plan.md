# SOP — Build Plan (Content Construction & Quality Standard)

**Layer:** 1 (Architecture) · **Governs:** the *content* of a test plan · **Version:** 1.0 (2026-09-11)

---

## 1. Goal

Define **what a test plan in this project must contain, and what makes it acceptable** — the
authoring standard. This SOP owns *content and quality*.

It complements, and does not replace, the mechanics SOPs:

| SOP | Owns |
|---|---|
| `SOP_fetch_issue.md` | Getting the issue data in (deterministic intake) |
| **`SOP_build_plan.md`** *(this)* | **What the plan must say, and how good it must be** |
| `SOP_generate_plan.md` | How the LLM is called and how its output is validated |
| `SOP_render_markdown.md` | How the validated content is formatted for delivery |
| `SOP_pipeline.md` | The order the stages run in, and error routing |
| `SOP_trigger.md` | How the pipeline is activated, on demand or on a schedule |

**Golden Rule reminder:** if the content standard changes, update **this file first**, then
`SOP_generate_plan.md` (the prompt), then the code.

---

## 2. Inputs

| Input | Source | Required |
|---|---|---|
| Normalized issue (`summary`, `description`, `acceptance_criteria?`, `grounding`, metadata) | `SOP_fetch_issue` | yes |
| User instructions (optional) | CLI `--instructions` / UI textarea | no |
| This content standard | static | yes |

---

## 3. Canonical Plan Structure

A plan is **seven sections**. Every section is mandatory; a section with no content renders an
explicit `_None identified._` rather than being silently dropped.

| # | Section | Must contain | Derivation |
|---|---|---|---|
| 1 | **Objective** | One paragraph: what this plan verifies and why it matters | Issue summary + description |
| 2 | **Preconditions** | Environment, access, roles, data state required *before* testing begins | Inferred from the described feature; `"Not specified in the Jira issue."` if ungrounded |
| 3 | **Test Data** | Concrete values or data sets the steps consume | Derived from the requirement; must be specific, not "some data" |
| 4 | **Test Cases** | Summary table + per-case blocks (see §4) | The core deliverable |
| 5 | **Coverage Summary** | Counts by priority, type, technique | **Computed by code — never model-authored** |
| 6 | **Risks** | Uncertainty, gaps, and reduced grounding | Must name *reduced grounding* when it applies |
| 7 | **Out of Scope** | What this plan explicitly does **not** cover | Prevents over-read of the plan's authority |

Plus two code-computed header blocks: the **AI review banner** and **At a Glance**.

---

## 4. Test Case Standard

Every test case carries exactly these fields (mirrors `schemas/test_plan.schema.json`):

| Field | Rule |
|---|---|
| `id` | `TC-001`, `TC-002`, … — **renumbered by code**; the model's value is never trusted |
| `title` | Short, imperative, specific ("Reject end date earlier than start date"), not "Test task 1" |
| `priority` | `High` \| `Medium` \| `Low` — justification implicit in the risk of the path |
| `type` | `Positive` \| `Negative` \| `Edge` \| `Boundary` \| `Regression` \| `Integration` |
| `test_design_technique` | ISTQB vocabulary — see §5. `None` is permitted only when justified |
| `traceability` | **Non-empty.** Names the requirement or acceptance-criterion fragment the case derives from |
| `steps` | Non-empty ordered list; **one action per step**; no leading numbers (the renderer numbers) |
| `expected_result` | Single, **observable**, **verifiable** outcome — never "works correctly" |

### 4.1 Coverage minimums (enforced by code)

- `test_cases` is **non-empty**.
- At least **one non-`Positive`** case (Negative or Edge). A plan of only happy paths is rejected.
- Every case has non-empty `traceability`.

### 4.2 Case quality bar

| Reject | Require instead |
|---|---|
| "Verify Task 1 works" | Name the specific behaviour under test |
| "Expected Result: it works" | Observable state, message, or returned value |
| Steps that bundle several actions into one line | One action per step |
| Duplicate scenarios with different wording | Distinct scenario per case |
| Invented endpoints, fields, URLs, error codes | Only what the issue states, or `"Not specified in the Jira issue."` |

---

## 5. Test-Design Technique Selection (ISTQB)

Techniques are **mandatory where the data supports them**, and each case must be labelled.

| Technique | Apply when the requirement describes… | Example trigger |
|---|---|---|
| **Boundary Value Analysis** | A numeric range, limit, date span, or quantity | "timeline of 1–12 months", "max 10 users" |
| **Equivalence Partitioning** | Classes of input where all members behave alike | valid vs invalid role; allowed vs disallowed template |
| **Decision Table** | Several conditions combining into distinct outcomes | permission × state × action matrices |
| **State Transition** | A lifecycle or status change | Draft → Submitted → Approved |
| **Error Guessing** | Likely failure modes not implied by structure | malformed input, missing permissions, ordering abuse |
| **None** | No technique creditably applies — allowed but should be rare and deliberate | documentation-presence checks |

**Guidance:** prefer BVA and EP on any requirement with ranges or input classes. Use `None`
only after considering the alternatives — it is a label of last resort, not a default.

---

## 6. Grounding-Aware Construction

What a plan may claim depends on the three-state `grounding` flag (`SOP_fetch_issue.md` §7).

| `grounding` | Permitted construction |
|---|---|
| `acceptance_criteria` | AC is the primary source of expected results; description is supporting context. Expected results may be specific and confident. |
| `description_only` | Description is the **only** requirement source. Cases must derive from it, and **`risks` must state** the plan rests on the description alone and needs review against real requirements. |
| `low` | **Only a summary exists.** Produce few, high-level cases; use `"Not specified in the Jira issue."` for every ungrounded expected result; **`risks` must state** grounding is minimal and the plan is near-speculative. |

**Never** present a low-grounding plan as if it were authoritative.

---

## 7. Anti-Patterns (must be rejected)

1. **Invented requirements** — any field, API, URL, status code, or business rule not in the issue.
2. **Padding** — adding cases to look thorough when the source is thin. Fewer, grounded cases win.
3. **Self-graded coverage** — the model claiming how many cases it "covered". Coverage is computed by code.
4. **Assertion-free cases** — a case whose expected result cannot be observed or verified.
5. **Orphan cases** — no `traceability` back to the issue.
6. **Happy-path-only plans** — no negative or edge coverage.
7. **Silent grounding** — failing to flag description-only or minimal grounding in `risks`.

---

## 8. Human Review (the plan is a draft)

A generated plan is **a first draft for a QA engineer**, never a finished artefact:

1. Every rendered plan carries the AI-review banner.
2. Reviewers verify each case against the real requirement, not just the ticket text.
3. Reviewers are expected to **add** domain and business-critical scenarios the model could not know.
4. A plan is only "done" when a human has reviewed it — the tool never declares a plan final.

**Do not** treat a green pipeline as a correct plan. Validation proves *structure*, not *truth*.

---

## 9. Acceptance Criteria for a Deliverable

A plan is acceptable to ship as a **draft** when ALL hold:

- [ ] All seven sections present (empty ones explicitly marked).
- [ ] Every case has all eight fields, with non-empty `traceability` and `steps`.
- [ ] At least one non-`Positive` case.
- [ ] Every case labelled with a creditable `test_design_technique` (or a deliberate `None`).
- [ ] Every expected result is observable and verifiable, or explicitly `"Not specified in the Jira issue."`
- [ ] `risks` reflects the actual grounding state.
- [ ] Coverage Summary present and computed (not model-authored).
- [ ] AI-review banner present.

---

## 10. Edge Cases

| Case | Behaviour |
|---|---|
| Issue has only a summary | Build a **short** plan; every expected result ungrounded; prominent risk entry |
| No user instructions | Build against the standard above — the default is full coverage |
| User instructions conflict with the standard | Instructions narrow or extend scope, but **never** override the anti-hallucination rule |
| Requirement describes no testable behaviour | Say so in `risks` / `out_of_scope`; do not invent behaviour |
| More cases than useful | Prefer 5 distinct grounded cases over 15 overlapping ones |
| Documentation-only requirement | `test_design_technique: "None"` is appropriate; verify presence and completeness |

---

## 11. Verification

This SOP is implemented by `build_prompt.py` (the prompt encodes §4–§7), enforced by
`validate_plan.py` (the code-enforced parts of §4.1 and §9), and rendered by
`render_markdown.py` (§3 sections and the code-computed Coverage Summary).

To confirm this SOP and the code agree, run the offline fixtures — they assert the schema
rules, the non-positive coverage rule, and the renumbering behaviour — and diff the prompt
text against §4–§7 after any change here.
