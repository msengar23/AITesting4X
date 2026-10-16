================================================================================
  QA Buddy AI - Multi-Source Hybrid RAG for QA Teams
================================================================================

Welcome! You're looking at the complete QA Buddy AI system.

▶ GETTING STARTED (Choose One Option):

  OPTION 1: FASTEST (30 min) - Print-Friendly Card
  ───────────────────────────────────────────────────
  📄 Open: QUICK_REFERENCE.md
  → Read the card
  → Follow 8 steps
  → Done!

  OPTION 2: VISUAL LEARNING (40 min) - Interactive Web Guide
  ──────────────────────────────────────────────────────────
  🌐 Open: GETTING_STARTED.html (double-click)
  → Beautiful interactive guide
  → Visual checklist
  → Example commands
  → Follow the steps

  OPTION 3: DETAILED WALKTHROUGH (60 min) - Complete Guide
  ──────────────────────────────────────────────────────────
  📖 Open: QUICKSTART.md
  → Read START_HERE.md first (5 min)
  → Then QUICKSTART.md (20 min)
  → Follow setup steps (35 min)
  → Test it out

  OPTION 4: AUTO SETUP - Let the Script Do It
  ────────────────────────────────────────────
  🚀 Run: START_QABUDDY.bat (double-click)
  → Checks prerequisites
  → Prompts for missing pieces
  → Builds UI automatically
  → Starts all services
  → Opens browser automatically

═══════════════════════════════════════════════════════════════════════════════

📚 ALL DOCUMENTATION:

  Essential Reading:
  • START_HERE.md ..................... Main entry point (read first!)
  • QUICK_REFERENCE.md ................ 8-step quick start
  • QUICKSTART.md ..................... Complete step-by-step
  • GETTING_STARTED.html .............. Visual interactive guide
  • COMMANDS_CHEATSHEET.md ............ Command reference
  • SYSTEM_OVERVIEW.md ................ Architecture & how it works
  • DOCUMENTATION_MANIFEST.md ......... This folder's docs explained

  Original Docs (Already Here):
  • README.md ......................... Project overview
  • SETUP.md .......................... Configuration details
  • deploy/DEPLOY.md .................. Production deployment

  Automation:
  • START_QABUDDY.bat ................. Auto setup & startup script

═══════════════════════════════════════════════════════════════════════════════

🎯 WHAT IS QA BUDDY AI?

An intelligent QA system that:
  ✓ Searches your test cases, Jira tickets, documentation, code, logs, etc.
  ✓ Finds the most relevant information using hybrid search
  ✓ Generates cited answers with exact sources [1] [2] [3]
  ✓ Explains why build #142 failed, if tests are flaky, what's not tested, etc.

Example:
  User:   "Why did build #142 fail?"
  AI:     "Build #142 failed due to a timeout in the login test [0].
           The root cause was a new IP allowlist on the auth server [2]..."

           [0] Jenkins Build #142 Log
           [1] Error Trace
           [2] VWO-26 - IP Allowlist Issue

═══════════════════════════════════════════════════════════════════════════════

✅ PREREQUISITES (Do you have these?)

  □ Python 3.13+  ..................... Run: python --version
  □ Ollama installed .................. Run: ollama --version
  □ Node.js 18+ ....................... Run: node --version
  □ Git ................................. Run: git --version
  □ Groq API key (free) ............... Get from: console.groq.com/keys

═══════════════════════════════════════════════════════════════════════════════

🚀 QUICK START (Choose ONE):

  Path A: I'm impatient
  ─────────────────────
  1. Read: QUICK_REFERENCE.md (3 min)
  2. Follow: 8-step checklist (25 min)
  3. Open: http://localhost:8300

  Path B: I prefer videos/visuals
  ─────────────────────────────────
  1. Open: GETTING_STARTED.html
  2. Follow: Interactive guide (40 min)
  3. Open: http://localhost:8300

  Path C: I want everything automated
  ────────────────────────────────────
  1. Run: START_QABUDDY.bat
  2. Answer: Prompts as they appear
  3. Browser: Opens automatically

═══════════════════════════════════════════════════════════════════════════════

💻 THE MINIMAL 8 STEPS:

  1. Copy .env from .env.example and add GROQ_API_KEY
  2. Run: ollama pull qwen3-embedding:0.6b
  3. Set up Qdrant (local or Cloud)
  4. Run: cd ui && npm install && npm run build && cd ..
  5. Run: python -m qabuddy ingest
  6. Terminal 1: ollama serve
  7. Terminal 2: .\.qdrant-win\qdrant.exe (if local Qdrant)
  8. Terminal 3: python -m qabuddy serve
  9. Open: http://localhost:8300

═══════════════════════════════════════════════════════════════════════════════

❓ TRY THESE QUESTIONS:

  "What are all the login test cases?"
  "Why did build #142 fail?"
  "Is testLoginPositiveVWO flaky?"
  "Which features don't have automated tests?"
  "Is VWO-26 a duplicate of VWO-33?"
  "How do I use the BasePage class?"

═══════════════════════════════════════════════════════════════════════════════

🆘 QUICK FIXES:

  Problem: "Ollama is not reachable"
  → Solution: Run 'ollama serve' in Terminal 1

  Problem: "Qdrant connection refused"
  → Solution: Run '.\.qdrant-win\qdrant.exe' in Terminal 2

  Problem: "Groq 429 - too many requests"
  → Solution: Wait 60 seconds or upgrade Groq plan

  Problem: "UI says Build the UI"
  → Solution: cd ui && npm run build && cd ..

  Problem: "Port 8300 already in use"
  → Solution: Change PORT=8301 in .env

  More help? See QUICKSTART.md → Troubleshooting section

═══════════════════════════════════════════════════════════════════════════════

📊 SYSTEM ARCHITECTURE (TL;DR):

  Question
      ↓
  Hybrid Search
  (Dense + Keyword)
      ↓
  Qdrant Database
  (Vector Search)
      ↓
  Rerank Results
  (Cross-encoder)
      ↓
  LLM (Groq)
  (Generate Answer)
      ↓
  Answer with [1] [2] [3] Citations

═══════════════════════════════════════════════════════════════════════════════

🎓 LEARNING THE SYSTEM:

  Quick Understanding: Read SYSTEM_OVERVIEW.md (25 min)
  Deep Dive:          Read README.md then SYSTEM_OVERVIEW.md
  Technical Details:  Read SETUP.md and deploy/DEPLOY.md

═══════════════════════════════════════════════════════════════════════════════

📁 YOUR FILES:

  qabuddy/           ← Python backend code
  ui/                ← React frontend code
  data/              ← Your data sources (add here)
  tests/             ← Test suite
  deploy/            ← Docker deployment files
  .env               ← Configuration (SECRET - don't commit!)
  requirements.txt   ← Python dependencies

═══════════════════════════════════════════════════════════════════════════════

✨ FEATURES:

  ✓ Hybrid search (semantic + keyword)
  ✓ 10 data source types
  ✓ Cited answers with exact sources
  ✓ Retrieval trace (see how it worked)
  ✓ Multiple modes (Ask, RCA, Design, Triage, Code, RTM)
  ✓ Local embeddings (Qwen3 0.6B on Ollama)
  ✓ Fast (~4-7 seconds end-to-end)
  ✓ Secure (passwords auto-redacted)
  ✓ Configurable

═══════════════════════════════════════════════════════════════════════════════

🚀 READY TO START?

  1. Pick one of the 4 options at the top of this file
  2. Open the recommended file
  3. Follow the instructions
  4. Start asking questions!

═══════════════════════════════════════════════════════════════════════════════

Questions? Check:
  START_HERE.md ..................... Entry point
  QUICKSTART.md ..................... Step-by-step
  COMMANDS_CHEATSHEET.md ............ Commands
  SYSTEM_OVERVIEW.md ................ Architecture

Happy QA'ing! 🤖

═══════════════════════════════════════════════════════════════════════════════
Created: 2026-10-10
Version: 1.0
Status: Complete ✅
