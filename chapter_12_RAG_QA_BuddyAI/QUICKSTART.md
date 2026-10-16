# QA Buddy AI - Complete Step-by-Step Guide

**Table of Contents:**
1. [Architecture Overview](#architecture-overview)
2. [System Requirements & Setup](#system-requirements--setup)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Running the Application](#running-the-application)
5. [Using the UI](#using-the-ui)
6. [CLI Commands](#cli-commands)
7. [Data Sources & Customization](#data-sources--customization)
8. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### What is QA Buddy AI?

QA Buddy AI is a **Retrieval Augmented Generation (RAG)** system designed specifically for QA teams. It answers questions by:
1. **Retrieving** relevant information from 10 different data sources (test cases, Jira tickets, code, docs, etc.)
2. **Ranking** results using AI-powered reranking
3. **Answering** with citations showing exactly where the information came from

### The Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUESTION                            │
└────────────────────────────┬────────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                │                            │
        ┌───────▼────────┐          ┌───────▼────────┐
        │  Dense Search  │          │   BM25 Search  │
        │  (Qwen3 0.6B)  │          │  (Code-aware)  │
        └───────┬────────┘          └───────┬────────┘
                │                            │
                └─────────────┬──────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Rerank Results   │
                    │ (Cross-encoder)    │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  LLM (Groq API)    │
                    │  Generate Answer   │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────▼────────────────────────┐
        │  ANSWER WITH [CITATIONS] + RETRIEVAL TRACE  │
        └──────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **Embeddings** | Convert text to vectors for semantic search | Qwen3-Embedding 0.6B (Ollama) |
| **Vector Database** | Store and retrieve embeddings | Qdrant (local or Cloud) |
| **Sparse Search** | Fast keyword matching | BM25 with code-aware tokenizer |
| **Reranker** | Score results by relevance | MS-Marco MiniLM cross-encoder |
| **LLM** | Generate citations + answers | Groq API (gpt-oss-120b) |
| **UI** | Interactive interface | React + Vite |
| **API** | Backend processing | FastAPI + Python |

---

## System Requirements & Setup

### 1. Prerequisites Check

Run this to verify what's already installed:

```powershell
# Python version (need 3.13)
python --version

# Node.js (needed for UI)
node --version
npm --version

# Check if Ollama is installed
ollama --version

# Check if Git is available
git --version
```

### 2. Required Software (If Not Installed)

| Software | Download Link | Purpose |
|----------|---------------|---------|
| Python 3.13+ | https://www.python.org/downloads/ | Core application |
| Node.js 18+ | https://nodejs.org | Build the web UI |
| Ollama | https://ollama.com/download | Run embeddings locally |
| Git | https://git-scm.com | Clone repositories |

### 3. API Keys Required

- **Groq API Key** (Free): https://console.groq.com/keys
  - Used for generating answers
  - Free tier: ~8,000 tokens/minute (2 answers/minute)

---

## Step-by-Step Installation

### STEP 1: Navigate to Project Folder

```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
```

### STEP 2: Install Python Dependencies

**Option A: Using Global Python (Recommended)**

```powershell
# Check dependencies are installed
python -m pip check

# List installed packages
python -m pip list | grep -E "fastapi|torch|qdrant|sentence"
```

**Option B: Create Virtual Environment (Isolated)**

```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# If activation fails due to execution policy:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Install dependencies
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r requirements.txt
pip install pytest
```

### STEP 3: Start Ollama (Embeddings Server)

Open a **new PowerShell terminal** and run:

```powershell
# Start Ollama server (if not already running)
ollama serve

# In another terminal, pull the embedding model
ollama pull qwen3-embedding:0.6b

# Verify it's loaded
ollama list
# Should show: qwen3-embedding:0.6b    767B
```

**Note:** Ollama must stay running in its own terminal. Leave it open.

### STEP 4: Set Up Qdrant (Vector Database)

**Option A: Local Qdrant (Windows Native)**

```powershell
# Create folder for Qdrant
New-Item -ItemType Directory -Force -Path .qdrant-win | Out-Null
cd .qdrant-win

# Download Qdrant Windows binary
curl.exe -L -o qdrant.zip https://github.com/qdrant/qdrant/releases/download/v1.19.1/qdrant-x86_64-pc-windows-msvc.zip

# Extract it
Expand-Archive -Force qdrant.zip .

# Run it in this terminal
.\qdrant.exe

# Keep this terminal open
```

**Option B: Use Qdrant Cloud (No Local Server)**

1. Go to https://qdrant.tech/cloud/
2. Sign up for free (includes a free cluster)
3. Copy your cluster URL and API key
4. Set them in `.env` (Step 5)

### STEP 5: Create & Configure `.env` File

From the project root:

```powershell
# Copy the example
Copy-Item .env.example .env

# Edit it (opens in Notepad)
notepad .env
```

**Fill in these values:**

```dotenv
# ---- QDRANT (Vector Database) ----
# LOCAL OPTION:
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# CLOUD OPTION (uncomment to use instead):
# QDRANT_URL=https://<your-id>.<region>.aws.cloud.qdrant.io:6333
# QDRANT_API_KEY=your_cloud_key_here

QDRANT_COLLECTION=qabuddy

# ---- OLLAMA (Embeddings) ----
OLLAMA_URL=http://localhost:11434
EMBED_MODEL=qwen3-embedding:0.6b
EMBED_DIM=1024

# ---- RERANKER ----
RERANK_ENABLED=true
RERANK_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

# ---- LLM (Answer Generation) ----
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=your_groq_key_here    # Get from https://console.groq.com/keys

# ---- Application ----
PORT=8300
PREFETCH_K=40
RERANK_CANDIDATES=24
FINAL_K=6
CONTEXT_TOKENS=3500
```

Save the file (Ctrl+S, then close).

### STEP 6: Build the Web UI

Open a **new PowerShell terminal** in the project folder:

```powershell
cd ui
npm install
npm run build
cd ..
```

This creates the `ui/dist` folder that the server will serve.

### STEP 7: Ingest the Data (Build the Search Index)

**Make sure Ollama and Qdrant are both running.** Then:

```powershell
# Ingest all data sources
python -m qabuddy ingest

# This will:
# 1. Read files from data/
# 2. Split them into chunks using source-specific rules
# 3. Embed each chunk using Qwen3 (via Ollama)
# 4. Store in Qdrant with BM25 index
```

**First run takes ~5-10 minutes.** Subsequent runs are incremental (only changed files).

Progress output will show:
```
✓ 00_TestCases      1 files → 600 chunks
✓ 01_JIRA_Tickets   5 files → 45 chunks
✓ 02_Company_Docs   3 files → 80 chunks
...
Total: 838 chunks indexed
```

### STEP 8: Start the Application

```powershell
# From the project root
python -m qabuddy serve
```

You should see:
```
INFO:     Started server process [####]
INFO:     Uvicorn running on http://0.0.0.0:8300
INFO:     Application startup complete
```

### STEP 9: Open the UI

Open your browser and go to:

```
http://localhost:8300
```

You should see the QA Buddy interface!

---

## Running the Application

### Daily Startup Checklist

**Terminal 1 - Ollama:**
```powershell
ollama serve
```

**Terminal 2 - Qdrant (if using local):**
```powershell
cd .qdrant-win
.\qdrant.exe
```

**Terminal 3 - QA Buddy API:**
```powershell
python -m qabuddy serve
```

Then open `http://localhost:8300`

### Verify It's Working

```powershell
# Check health status
curl.exe http://localhost:8300/api/health

# Should return:
# {
#   "status": "healthy",
#   "qdrant": true,
#   "ollama": true,
#   "embed_model_ready": true,
#   "llm_configured": true,
#   "points": 838
# }
```

---

## Using the UI

### Main Interface

The web UI has these sections:

1. **Question Input** - Type your question at the top
2. **Mode Selector** - Choose how to answer:
   - 💬 **Ask anything** - General Q&A
   - 🧯 **Failure analysis (RCA)** - Debug build failures
   - 🧪 **Test design** - Find test gaps
   - 🐞 **Bug triage** - Categorize issues
   - 🛠️ **Framework help** - Coding questions
   - 🧭 **Traceability (RTM)** - Link requirements to tests

3. **Answer Display** - Shows:
   - Generated answer
   - Source citations [1] [2] [3]
   - Confidence score
   - Retrieval trace (for debugging)

4. **Source Viewer** - Click [1] to see the exact chunk used

### Example Questions

```
# General QA
"What are the login test cases?"
"How do I set up parallel tests?"

# Failure Analysis
"Why did build #142 fail?"
"Is testLoginPositiveVWO flaky?"

# Test Design
"What features are not covered by automated tests?"
"Write a test case for two-factor authentication"

# Bug Triage
"Is VWO-26 a duplicate of VWO-33?"
"What's the priority and severity of VWO-32?"

# Traceability
"Which tests cover the login feature?"
"What requirements relate to checkout?"
```

### Reading the Trace

Each answer includes a **retrieval trace** showing:
- How many chunks were retrieved
- Which retriever found the best match (dense/BM25/hybrid)
- Reranker scores
- Final ranking

This helps debug why an answer might be wrong.

---

## CLI Commands

### Ask a Question (Directly in Terminal)

```powershell
python -m qabuddy ask "Why did build #142 fail?" --mode rca
```

### Search Only (No Answer)

Returns the top chunks without generating an answer:

```powershell
python -m qabuddy search "login authentication flow"
```

### Re-index Data

```powershell
# Incremental (only changed files)
python -m qabuddy ingest

# Full rebuild
python -m qabuddy ingest --full

# Specific source only
python -m qabuddy ingest --source jira
```

### Evaluate Retrieval Quality

Tests retrieval accuracy on golden questions:

```powershell
python -m qabuddy eval
```

Shows hit rate and ranking quality (MRR).

### Run Tests

```powershell
python -m qabuddy test
```

Runs 18 regression tests to catch bugs.

### Sync Jira Issues

Pulls tickets from Jira and ingests them:

```powershell
python -m qabuddy sync-jira --jql "project = VWO AND type = Bug"
```

(Requires JIRA_* credentials in `.env`)

---

## Data Sources & Customization

### Where to Add Your Data

```
data/
├── 00_TestCases/                 # Excel/CSV with test cases
├── 01_JIRA_Tickets/              # Exported Jira issues (.md)
├── 02_Company_Docs/              # PDFs, Markdown handbook
├── 03_Meeting_Notes/             # Transcripts, minutes
├── 04_Lucid_charts/              # Diagrams, flow charts
├── 05_PRD_SRS_BRD_FRDs/          # Requirements documents
├── 06_Figma_Designs/             # Design specs (phase 2)
├── 06_Jenkins_Logs/              # Build logs
└── 07_Source_Codes/              # Selenium/Playwright frameworks
```

### Adding Your Own Data

**Step 1:** Copy files into the appropriate `data/NN_*` folder

**Step 2:** Register the source in `sources.yaml`

```yaml
sources:
  - id: custom_docs
    label: "Custom Documentation"
    path: data/02_Company_Docs
    chunker: docs
    extensions: [".md", ".pdf"]
```

**Step 3:** Re-ingest

```powershell
python -m qabuddy ingest
```

### Removing Data

1. Delete files from `data/` folders
2. Files starting with `_` (underscore) are ignored
3. Rename instead of delete to keep backups:
   ```
   Old_Guide.md  →  _archive_Old_Guide.md
   ```

### Supported File Types

- **Test Cases:** CSV, XLSX
- **Jira:** Markdown exports
- **Docs:** PDF, Markdown (.md)
- **Code:** Python, Java, TypeScript, etc.
- **Diagrams:** JSON, CSV, TXT (Lucid charts)
- **Logs:** Plain text
- **Transcripts:** VTT (WebVTT format)

---

## Troubleshooting

### "Ollama is not reachable"

```powershell
# Check if Ollama is running
curl.exe http://localhost:11434/api/version

# If it fails, start Ollama
ollama serve

# Pull the model
ollama pull qwen3-embedding:0.6b
```

### "Qdrant connection refused"

```powershell
# Check if local Qdrant is running
curl.exe http://localhost:6333/

# If using local, start it
cd .qdrant-win
.\qdrant.exe

# If using Cloud, verify QDRANT_URL and QDRANT_API_KEY in .env
```

### "pip install <pkg>" fails with "Access is denied"

```powershell
# Option 1: Run PowerShell as Administrator
# Then try: pip install <pkg>

# Option 2: Use --user flag
pip install --user <pkg>

# Option 3: Use virtual environment (see Step 2)
```

### "Groq 429 - Too many requests"

Groq's free tier is ~8,000 tokens/min (~2 answers/minute).

**Solutions:**
1. Wait a minute between answers
2. Upgrade Groq plan at https://console.groq.com
3. Switch to local LLM: `LLM_PROVIDER=ollama` and `ollama pull gpt-oss:20b`

### "UI says 'Build the UI'"

```powershell
cd ui
npm run build
cd ..

# Then restart the API
python -m qabuddy serve
```

### "First answer is slow"

The reranker downloads on first use (~90 MB from Hugging Face). Subsequent answers are faster.

### Port Already in Use

```powershell
# If 8300 is in use, change it in .env
PORT=8301

# Or kill the process using it
# (Find what's using port 8300 and stop it)
```

---

## What's Next?

### Phase 2 Features (Planned)

- [ ] Figma design specs ingestion
- [ ] Hourly auto-ingest from Jira
- [ ] Docker deployment (VPS)
- [ ] Team login + RBAC
- [ ] Export answers to PDF
- [ ] Batch question answering

### Performance Tuning

Adjust in `.env` for your hardware:

```dotenv
# Fewer candidates = faster but less accurate
RERANK_CANDIDATES=12    # default 24

# More = better results but slower
PREFETCH_K=60          # default 40
FINAL_K=8              # default 6
```

### Advanced: Self-Hosted LLM

For fully offline operation:

```dotenv
LLM_PROVIDER=ollama
LLM_MODEL=gpt-oss:20b
```

Then pull the model:
```powershell
ollama pull gpt-oss:20b
```

---

## Support & Documentation

- **Architecture details:** See `README.md`
- **Detailed setup:** See `SETUP.md`
- **Deployment guide:** See `deploy/DEPLOY.md`
- **Known issues:** See `PENDING_TASKS.md`
- **Evaluation results:** See `eval/`

---

**Created:** 2026-10-10
**Last Updated:** 2026-10-10
**Version:** 1.0
