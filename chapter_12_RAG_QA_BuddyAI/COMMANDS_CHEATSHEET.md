# QA Buddy AI - Commands Cheat Sheet

Quick reference for the most common commands used to run and manage QA Buddy AI.

## 🚀 Startup Commands (Daily)

### Terminal 1: Start Ollama (Embeddings Server)
```powershell
ollama serve
```
**Keep this running.** Verify it's working:
```powershell
curl.exe http://localhost:11434/api/version
```

### Terminal 2: Start Qdrant (Vector Database)

**Option A: Local Binary (Windows)**
```powershell
cd .qdrant-win
.\qdrant.exe
```

**Option B: Cloud (No terminal needed)**
- Just ensure `QDRANT_URL` and `QDRANT_API_KEY` are set in `.env`

Verify connection:
```powershell
curl.exe http://localhost:6333/
```

### Terminal 3: Start QA Buddy API
```powershell
# From project root
python -m qabuddy serve
```

Then open in browser: **http://localhost:8300**

---

## 🛠️ Setup Commands (One-time or Occasional)

### Initial Setup
```powershell
# Navigate to project
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"

# Create environment file
Copy-Item .env.example .env

# Edit environment (add GROQ_API_KEY, QDRANT_URL, etc.)
notepad .env
```

### Pull Embedding Model
```powershell
ollama pull qwen3-embedding:0.6b
ollama list
```

### Build the UI (After code changes or first setup)
```powershell
cd ui
npm install      # First time only
npm run build
cd ..
```

### Ingest Data (Build the search index)
```powershell
# Incremental ingest (only changed files)
python -m qabuddy ingest

# Full rebuild (deletes and rebuilds everything)
python -m qabuddy ingest --full

# Ingest specific source only
python -m qabuddy ingest --source jira
```

---

## ❓ Question & Answer Commands

### Ask from Terminal
```powershell
python -m qabuddy ask "Why did build #142 fail?" --mode rca

python -m qabuddy ask "What are the login test cases?"

python -m qabuddy ask "Is VWO-26 a duplicate?" --mode triage
```

### Available Modes
- `--mode ask` (default) - General Q&A
- `--mode rca` - Failure analysis (Root Cause Analysis)
- `--mode design` - Test design & gaps
- `--mode triage` - Bug triage
- `--mode framework` - Framework coding help
- `--mode rtm` - Traceability matrix

### Search Only (No Answer Generated)
```powershell
python -m qabuddy search "login authentication"
```

Shows retrieval hits without calling the LLM.

---

## 📊 Evaluation & Testing

### Evaluate Retrieval Quality
```powershell
python -m qabuddy eval
```

Tests retrieval accuracy on the golden question set. Shows:
- Hit@6 (does top-6 contain the answer?)
- MRR (Mean Reciprocal Rank - how high is the correct answer?)
- Ablation study (dense vs. BM25 vs. hybrid)

### Run Regression Tests
```powershell
python -m qabuddy test
```

18 unit tests to catch bugs (no services needed).

---

## 🔄 Data Management

### Add New Data
1. Copy files to appropriate `data/NN_*` folder
2. Edit `sources.yaml` if it's a new source type
3. Re-ingest:
   ```powershell
   python -m qabuddy ingest
   ```

### Remove Data
**Option A:** Delete files and re-ingest
```powershell
rm data/02_Company_Docs/old_doc.pdf
python -m qabuddy ingest
```

**Option B:** Archive by renaming (keeps backup)
```powershell
# Files starting with _ are not ingested
ren data/02_Company_Docs/old_doc.pdf _archive_old_doc.pdf
python -m qabuddy ingest
```

### Sync from Jira
```powershell
# Requires JIRA_* env vars configured
python -m qabuddy sync-jira --jql "project = VWO AND type = Bug"
```

---

## 🐛 Troubleshooting Commands

### Check Health Status
```powershell
curl.exe http://localhost:8300/api/health
```

Response should show:
```json
{
  "status": "healthy",
  "qdrant": true,
  "ollama": true,
  "embed_model_ready": true,
  "llm_configured": true,
  "points": 838
}
```

### Verify Ollama
```powershell
# Check server is running
curl.exe http://localhost:11434/api/version

# List models
ollama list

# Pull missing model
ollama pull qwen3-embedding:0.6b
```

### Verify Qdrant
```powershell
# Check server is running
curl.exe http://localhost:6333/

# List collections
curl.exe http://localhost:6333/collections
```

### Find What's Using a Port
```powershell
# Check port 8300
netstat -ano | findstr :8300

# Kill process if needed (PID is the number from output)
taskkill /PID <PID> /F
```

### Check Python Dependencies
```powershell
python -m pip check
python -m pip list | grep -E "fastapi|torch|qdrant"
```

### View Application Logs
The terminal where you run `python -m qabuddy serve` shows all logs. Look for:
- `ERROR` messages (problems)
- `WARNING` messages (potential issues)
- `INFO` messages (normal operation)

---

## 🔧 Configuration Commands

### Environment Variables (edit `.env`)
```powershell
# Common changes
GROQ_API_KEY=your_key_here
EMBED_MODEL=qwen3-embedding:0.6b
EMBED_DIM=1024
PORT=8300
PREFETCH_K=40
RERANK_CANDIDATES=24
FINAL_K=6
```

### Change Embedding Model (drop-in upgrade)
```powershell
# Edit .env
EMBED_MODEL=qwen3-embedding:4b    # Heavier but more accurate

# Must do full rebuild
python -m qabuddy ingest --full
```

### Switch to Offline Mode (use local LLM)
```powershell
# Pull a model
ollama pull gpt-oss:20b

# Edit .env
LLM_PROVIDER=ollama
LLM_MODEL=gpt-oss:20b

# Restart API
python -m qabuddy serve
```

### Adjust Performance
```powershell
# For slower hardware, reduce reranking
RERANK_CANDIDATES=12    # default 24

# Get more/fewer results (affects accuracy vs. speed)
PREFETCH_K=60          # default 40
FINAL_K=8              # default 6
```

---

## 📦 Dependency Management

### Check if All Dependencies Are Installed
```powershell
python -m pip check
```

### Show All Installed Packages
```powershell
python -m pip list
```

### Install Missing Package
```powershell
# For global install (might need admin)
pip install <package-name>

# For user-only install (no admin needed)
pip install --user <package-name>
```

### Update All Packages
```powershell
pip install --upgrade pip
pip install -U -r requirements.txt
```

---

## 💻 Development Commands

### Hot Reload UI (Development)
```powershell
# Keep API running in one terminal
python -m qabuddy serve

# In another terminal
cd ui
npm run dev        # http://localhost:5300
```

The dev server proxies `/api` to the running API and hot-reloads on changes.

### Build UI for Production
```powershell
cd ui
npm run build      # Creates ui/dist
cd ..
python -m qabuddy serve   # Serves the built version
```

### Run Just the Tests
```powershell
pytest tests/ -v
```

### Check Test Coverage
```powershell
pytest tests/ --cov=qabuddy --cov-report=html
# Opens htmlcov/index.html in browser
```

---

## 📝 Quick Reference Card

| What | Command |
|-----|---------|
| **Start everything** | See "Startup Commands" above (3 terminals) |
| **Ask a question** | `python -m qabuddy ask "your question"` |
| **Search without answering** | `python -m qabuddy search "query"` |
| **Rebuild search index** | `python -m qabuddy ingest` |
| **Evaluate quality** | `python -m qabuddy eval` |
| **Run tests** | `python -m qabuddy test` |
| **Check health** | `curl.exe http://localhost:8300/api/health` |
| **Open UI** | http://localhost:8300 |
| **View docs** | QUICKSTART.md, README.md, SETUP.md |

---

## 🆘 Emergency Fixes

### "Embedding model not found"
```powershell
ollama pull qwen3-embedding:0.6b
python -m qabuddy ingest --full
```

### "Qdrant connection refused"
```powershell
cd .qdrant-win
.\qdrant.exe
# Or check QDRANT_URL in .env if using Cloud
```

### "Groq 429 - Too many requests"
```powershell
# Wait 1 minute, or
# Upgrade Groq plan, or
# Use local LLM (see "Switch to Offline Mode" above)
```

### "Port 8300 already in use"
```powershell
# Option A: Change PORT in .env
PORT=8301

# Option B: Kill what's using it
netstat -ano | findstr :8300
taskkill /PID <PID> /F
```

### "UI says 'Build the UI'"
```powershell
cd ui
npm run build
cd ..
# Restart the API
```

---

**Last Updated:** 2026-10-10
**Version:** 1.0
