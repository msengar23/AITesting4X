# QA Buddy AI - START HERE 👋

Welcome to QA Buddy AI! This document is your guide to getting started.

---

## 🎯 What is QA Buddy AI?

**QA Buddy AI** is an intelligent question-answering system that understands your entire QA knowledge base:
- ✅ Test cases (CSV/XLSX)
- ✅ Jira tickets and bugs
- ✅ Company documentation (PDFs, Markdown)
- ✅ Meeting notes and transcripts
- ✅ Code and frameworks
- ✅ Diagrams and flows
- ✅ Jenkins build logs
- ✅ Requirements documents

You ask it ONE question, and it retrieves relevant information from all these sources, then generates a **cited answer** showing exactly where the information came from.

**Example:**
```
User: "Why did build #142 fail?"
QA Buddy: "Build #142 failed due to a timeout in the login test [0]. 
          The root cause was a new IP allowlist on the auth server [2]..."
          
          [0] Jenkins Build #142 Log
          [1] Error Trace Output
          [2] VWO-26 - IP Allowlist Issue
```

---

## 📋 Documentation Index

Choose the right guide based on what you need:

### 🚀 **Just Want to Get Started?**
→ Read: **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** (2-3 minutes)
- Print-friendly quick reference card
- 8-step setup process
- Key commands and quick fixes

### 📖 **Step-by-Step Setup Instructions**
→ Read: **[QUICKSTART.md](QUICKSTART.md)** (15-20 minutes)
- Detailed walkthroughs
- Explains why each step matters
- Troubleshooting for each section
- Best if you're setting up for the first time

### 🌐 **Visual Setup Guide**
→ Open: **[GETTING_STARTED.html](GETTING_STARTED.html)** (web page)
- Beautiful interactive HTML guide
- Can open in any browser
- Visual checklist
- Terminal examples
- Example questions

### 💻 **All Commands Reference**
→ Read: **[COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)** (lookup)
- Organized by purpose
- One-line descriptions
- Copy-paste ready commands
- Quick fixes for common errors
- Best as a reference while working

### 🏗️ **How It Works Technically**
→ Read: **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** (deep dive)
- Architecture diagrams
- Component descriptions
- Data flow examples
- Performance metrics
- Technical details
- Best if you're curious or debugging

### 📚 **Original Docs**
- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Detailed environment setup
- [deploy/DEPLOY.md](deploy/DEPLOY.md) - Production Docker deployment

---

## 🚀 Quick Start Path (Choose One)

### Path A: "Just Get It Running" (30 min)
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (3 min)
2. Follow the 8 setup steps (20 min)
3. Open http://localhost:8300 (2 min)
4. Start asking questions!

### Path B: "I Want to Understand Everything" (60 min)
1. Read [QUICKSTART.md](QUICKSTART.md) (20 min)
2. Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) (20 min)
3. Follow setup steps from QUICKSTART (20 min)
4. Explore the application

### Path C: "I Prefer Visual Learning" (40 min)
1. Open [GETTING_STARTED.html](GETTING_STARTED.html) in browser (5 min)
2. Complete the checklist (10 min)
3. Follow the 6 steps (20 min)
4. Test it out

---

## 📋 Pre-Setup Checklist

Before you start, make sure you have:

- [ ] **Python 3.13** installed ([download here](https://www.python.org/downloads/))
  - Check: Run `python --version` in PowerShell
  
- [ ] **Ollama** installed ([download here](https://ollama.com/download))
  - Check: Run `ollama --version`
  
- [ ] **Node.js 18+** installed ([download here](https://nodejs.org))
  - Check: Run `node --version` and `npm --version`
  
- [ ] **Groq API key** (free - [get it here](https://console.groq.com/keys))
  - Takes 2 minutes to sign up
  
- [ ] **Qdrant setup ready** (choose one):
  - Option 1: Local binary (no setup needed yet, guide covers it)
  - Option 2: Qdrant Cloud account ([signup here](https://qdrant.tech/cloud), includes free tier)

✅ Have all of these? Great! Continue to next section.

---

## 🎬 The 8-Step Setup Process

**For detailed instructions on any step, see [QUICKSTART.md](QUICKSTART.md)**

### Step 1: Navigate to Project Folder
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
```

### Step 2: Create `.env` Configuration File
```powershell
Copy-Item .env.example .env
notepad .env
```
Add your `GROQ_API_KEY` (required) and configure `QDRANT_URL`

### Step 3: Pull the Embedding Model
```powershell
ollama pull qwen3-embedding:0.6b
```

### Step 4: Set Up Qdrant Vector Database
- **Option A:** Local Windows binary (see QUICKSTART.md)
- **Option B:** Use Qdrant Cloud (update `.env` with URL)

### Step 5: Build the Web UI
```powershell
cd ui
npm install
npm run build
cd ..
```

### Step 6: Ingest Your Data (5-10 minutes)
```powershell
python -m qabuddy ingest
```

### Step 7: Start the Services

**Open 3 PowerShell terminals and run these:**

| Terminal | Command | Keep Running? |
|----------|---------|---------------|
| Terminal 1 | `ollama serve` | ✅ Yes |
| Terminal 2 | `.\.qdrant-win\qdrant.exe` | ✅ Yes (if local) |
| Terminal 3 | `python -m qabuddy serve` | ✅ Yes |

### Step 8: Open Your Browser
```
http://localhost:8300
```

✅ **Setup Complete!**

---

## 💬 Try These Questions

Once you're running, try asking:

```
"What are all the login test cases?"
"Why did build #142 fail?"
"Is testLoginPositiveVWO flaky?"
"Which features don't have automated tests?"
"Is VWO-26 a duplicate of VWO-33?"
"How do I use the BasePage class?"
```

---

## 🆘 Something Not Working?

### Issue: Can't find `.env` file
**Solution:** In Step 2, make sure you're in the project root:
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
Copy-Item .env.example .env
```

### Issue: "Ollama is not reachable"
**Solution:** Make sure you ran Terminal 1:
```powershell
ollama serve  # Must be running in its own terminal
```

### Issue: "Qdrant connection refused"
**Solution:** Make sure you ran Terminal 2:
```powershell
cd .qdrant-win
.\qdrant.exe  # Must be running in its own terminal
```

### Issue: "UI says Build the UI"
**Solution:** Build the UI:
```powershell
cd ui
npm run build
cd ..
python -m qabuddy serve  # Restart
```

### Still stuck?
→ See **Troubleshooting** section in [QUICKSTART.md](QUICKSTART.md)

---

## 🎓 Learning Resources

### Understand the Architecture
1. Read the **Data Flow** section in [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
2. Look at the architecture diagram
3. Understand the 5 key decisions explained in [README.md](README.md)

### Learn the Commands
Keep [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md) handy for:
- Common commands
- Startup checklist
- Emergency fixes

### Deep Dive Topics
- **Hybrid Search:** See [SYSTEM_OVERVIEW.md - Hybrid Search](SYSTEM_OVERVIEW.md#5-hybrid-search)
- **Chunking Strategy:** See [README.md - Chunk Strategy](README.md#3-chunk-size-and-overlap-per-source)
- **Data Normalization:** See [README.md - Preprocessing](README.md#4-preprocessing-and-normalization)

---

## 🗂️ File Structure

```
chapter_12_RAG_QA_BuddyAI/

📄 Documentation (READ THESE):
  ├── START_HERE.md ..................... This file (you are here)
  ├── QUICK_REFERENCE.md ................ Print-friendly card
  ├── QUICKSTART.md ..................... Step-by-step guide
  ├── GETTING_STARTED.html .............. Visual guide (open in browser)
  ├── COMMANDS_CHEATSHEET.md ............ All commands reference
  ├── SYSTEM_OVERVIEW.md ................ Architecture details
  ├── README.md ......................... Project overview
  ├── SETUP.md .......................... Detailed setup

⚙️ Configuration:
  ├── .env.example ....................... Copy to .env and customize
  └── .env ............................... Your secrets (git-ignored)

🐍 Backend (Python):
  ├── qabuddy/ ........................... Main package
  ├── requirements.txt ................... Python dependencies
  └── tests/ ............................. Regression tests

⚛️ Frontend (React):
  ├── ui/src/ ............................ React components
  ├── ui/dist/ ........................... Built version
  └── ui/package.json .................... Node dependencies

📊 Data:
  ├── data/00_TestCases/ ................. Test cases
  ├── data/01_JIRA_Tickets/ .............. Jira issues
  ├── data/02_Company_Docs/ .............. Documentation
  ├── data/03_Meeting_Notes/ ............ Transcripts
  ├── data/04_Lucid_charts/ .............. Diagrams
  ├── data/05_PRD_SRS_BRD/ ............... Requirements
  ├── data/06_Figma_Designs/ ............ Design specs
  ├── data/06_Jenkins_Logs/ .............. Build logs
  └── data/07_Source_Codes/ .............. Frameworks

🚀 Deployment:
  ├── deploy/Dockerfile .................. Container image
  ├── deploy/docker-compose.yml .......... Full stack
  └── deploy/DEPLOY.md ................... Deployment guide

📈 Evaluation:
  ├── eval/golden.yaml ................... Test questions
  └── eval/last_run.json ................. Results

🔧 Helpers:
  ├── START_QABUDDY.bat .................. Auto-startup script
  ├── run.sh ............................ Unix startup script
  ├── sources.yaml ....................... Data source config
  └── glossary.yaml ...................... Team terminology

🤝 Extras:
  ├── .claude/ ........................... Claude AI context
  ├── api/ ............................... Vercel demo functions
  └── docs/ .............................. Screenshots & diagrams
```

---

## 🎯 Your Next Steps

1. **Right now:**
   - Read this file (you're doing it! ✓)
   - Choose your learning path above

2. **Next 5 minutes:**
   - Check prerequisites (do you have Python 3.13, Ollama, Node.js?)
   - Get a Groq API key

3. **Next 30 minutes:**
   - Follow one of the setup paths
   - Get the app running

4. **After setup:**
   - Ask some example questions
   - Check [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md) for other useful commands
   - Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) if you want to understand how it works

---

## 💡 Key Concepts (TL;DR)

- **RAG:** Retrieval-Augmented Generation - get answers from your data
- **Embedding:** Converting text to vectors (1024 numbers)
- **Vector Search:** Finding similar texts using embeddings
- **BM25:** Fast keyword matching (like Google search)
- **Hybrid Search:** Combines embedding + keyword for best results
- **Reranking:** Re-scoring results by relevance
- **Citations:** [1] [2] [3] showing exactly where answer came from

---

## 🚀 Quick Commands

```powershell
# Ask a question from terminal
python -m qabuddy ask "Why did build #142 fail?"

# Search without generating answer
python -m qabuddy search "login test cases"

# Update search index
python -m qabuddy ingest

# Check if everything works
curl.exe http://localhost:8300/api/health

# Run quality tests
python -m qabuddy eval
```

See [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md) for complete list.

---

## 📞 Support & Help

| Question | Answer in... |
|----------|--------------|
| "How do I install?" | [QUICKSTART.md](QUICKSTART.md) |
| "What's the quick version?" | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| "What command do I run?" | [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md) |
| "How does it work?" | [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) |
| "I prefer visual learning" | [GETTING_STARTED.html](GETTING_STARTED.html) |
| "The original docs" | [README.md](README.md) |
| "My X isn't working" | [SETUP.md - Troubleshooting](SETUP.md#troubleshooting) |

---

## ✨ Features at a Glance

✅ **Hybrid Search** - Dense + keyword for best results  
✅ **10 Data Sources** - Test cases, Jira, docs, code, logs, etc.  
✅ **Ranked Results** - Most relevant answer first  
✅ **Cited Answers** - Every answer shows its sources  
✅ **Multiple Modes** - Ask, analyze failures, design tests, triage bugs  
✅ **Retrieval Trace** - See exactly how answer was found  
✅ **Local Embeddings** - Qwen3 0.6B on Ollama (your machine)  
✅ **Open Source** - Qdrant vector database (Apache 2.0)  
✅ **Fast** - ~4-7 seconds end-to-end  
✅ **Secure** - Passwords and tokens automatically redacted  

---

## 🎉 Welcome!

You're about to have a powerful QA assistant at your fingertips. Let's get started!

**Choose your learning path:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md), [QUICKSTART.md](QUICKSTART.md), or [GETTING_STARTED.html](GETTING_STARTED.html)

Happy QA'ing! 🤖

---

**Version:** 1.0  
**Created:** 2026-10-10  
**Last Updated:** 2026-10-10
