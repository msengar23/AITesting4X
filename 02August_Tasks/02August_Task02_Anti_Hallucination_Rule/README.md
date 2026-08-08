# 02August_Task02_Anti_Hallucination_Rule

Study of the Anti-Hallucination rule applied to QA/test documentation, ensuring every assertion is traceable to provided input (PRD, API docs, logs, screenshots, test data, user input).

## Structure

| Path | Description |
|---|---|
| `Assets/Anti_Hallucination_Rule.md` | The Anti-Hallucination rule definition and strict verification workflow |
| `References/Prompt_Without_Hallucination.md` | Example prompt that does not apply the rule |
| `References/Prompt_With_Anti_Hallucination.md` | Example prompt applying the rule |

## Core Principle

Only assert facts traceable to provided input; label every inference as `Inference (low confidence)`; respond `Insufficient information to determine` rather than guessing; keep output deterministic and repeatable.
