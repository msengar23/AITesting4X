/goal — Set an Agent Objective

  /goal sets a standing objective that the agent works toward across multiple turns, not just one response. It's a persistent mission, not
   a one-shot task.

  Syntax

  /goal [<objective>|clear|status]

 ┌─────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Usage               │ What it does                                                                                                  │
  ├─────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ /goal <objective>   │ Sets the objective. The agent commits to it as a long-running goal and keeps working until it's genuinely     │
  │                     │ complete.                                                                                                     │
  ├─────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ /goal clear         │ Removes the current objective.                                                                                │
  ├─────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ /goal status        │ Shows what the current objective is and its progress.                                                         │
  └─────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  How it works

  When you set a goal, the agent receives a goal-bootstrap directive that:

   1. Persists across turns — it's not a one-shot instruction. The agent treats it as an ongoing mission.
  2. Demands evidence — the agent must work from live evidence (filesystem, command output, tests), not stale conversation memory.
  3. Requires verification — the agent can't claim it's done without proving it. Completion must be signaled with `` plus concrete
  evidence (files changed, commands run, tests passing).
  4. Self-directed continuation — the agent keeps going until the objective is genuinely met, not narrowed or watered down.

  When to use it

  Use /goal for multi-step, multi-turn work like:

  - "Implement user authentication across the app"
  - "Refactor all API routes to use the new middleware"
  - "Add test coverage to all modules"

  
  It's distinct from a regular one-shot request — the agent won't stop halfway and ask "is this good enough?" It keeps pushing until
  there's verifiable proof of completion.

  vs. /plan

  - /goal — sets a persistent objective with self-directed execution
  - /plan — enters plan mode for structured exploration and planning before implementation

  You can use both together: set a goal with /goal, then use /plan to explore and design the approach.