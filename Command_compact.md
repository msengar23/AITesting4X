/compact — Compact Conversation History

  /compact shrinks your conversation history when the context window is filling up, so the agent can keep working without losing the
  thread.

  How it works

  As you chat with the agent, every exchange (your messages + the agent's responses + tool calls + tool outputs) piles up in the context
  window. When it gets too full, the agent starts losing older context or can't process new tool output. /compact summarizes the
  conversation so far — condensing everything into a compact, lossy summary — freeing up space for fresh turns while keeping the critical
  thread intact.

  Think of it like compressing a long chat log into a dense TL;DR that the agent can still work from.

  Related: /compact-mode

  /compact-mode lets you choose how aggressively compaction happens:

  ┌─────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Mode    │ Behavior                                                                                                     │
  ├─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ default │ Standard summarization — compacts when context pressure builds up normally.                                  │
  ├─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ fast    │ Aggressive compaction — triggers sooner, keeps context leaner. Useful for long sessions or token-heavy work. │
  └─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  You can also set this persistently via config:

  /config compact-mode fast

  Related: --config compact-mode (CLI)

  You can set it on launch too:

  cmdc --config compact-mode=fast

  When to use it

  - The agent starts forgetting things you said earlier
  - You notice the context window usage creeping up (check with /context)
  - Before starting a new major task in a long session
  - You don't need to — Command Code auto-compacts when context runs low, but you can trigger it manually if you want to preempt it
