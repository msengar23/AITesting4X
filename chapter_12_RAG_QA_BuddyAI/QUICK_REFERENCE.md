# QA Buddy AI - Quick Reference Card

Print this page and keep it handy during setup!

---

## 🚀 First-Time Setup (30 minutes)

### 1️⃣ Navigate to Project
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
```

### 2️⃣ Verify Prerequisites
```powershell
python --version          # Need 3.13+
node --version            # Need 18+
npm --version
ollama --version
```

### 3️⃣ Create .env File
```powershell
Copy-Item .env.example .env
notepad .env
```
**Fill in these 2 values:**
- `GROQ_API_KEY=` (get free key: https://console.groq.com/keys)
- `QDRANT_URL=` (either local `http://localhost:6333` or Cloud URL)

### 4️⃣ Pull Embedding Model
```powershell
ollama pull qwen3-embedding:0.6b
ollama list
```

### 5️⃣ Build UI
```powershell
cd ui
npm install
npm run build
cd ..
```

### 6️⃣ Ingest Data (5-10 minutes)
```powershell
python -m qabuddy ingest
```

### 7️⃣ Start Services

**Terminal 1: Ollama**
```powershell
ollama serve
```

**Terminal 2: Qdrant** (if local)
```powershell
cd .qdrant-win
.\qdrant.exe
```

**Terminal 3: QA Buddy**
```powershell
python -m qabuddy serve
```

### 8️⃣ Open Browser
```
http://localhost:8300
```

✅ **Done!** Start asking questions.

---

## 📋 Daily Checklist

- [ ] Start Ollama: `ollama serve`
- [ ] Start Qdrant: `.\.qdrant-win\qdrant.exe` (if local)
- [ ] Start App: `python -m qabuddy serve`
- [ ] Open: http://localhost:8300
- [ ] Ask a question!

---

## 💬 Example Questions

| Category | Question |
|----------|----------|
| **General** | "What are the login test cases?" |
| **General** | "How do I set up parallel tests?" |
| **Failure (RCA)** | "Why did build #142 fail?" |
| **Failure (RCA)** | "Is testLoginPositiveVWO flaky?" |
| **Design** | "What features aren't tested?" |
| **Design** | "Write tests for checkout" |
| **Triage** | "Is VWO-26 a duplicate?" |
| **Triage** | "What's the priority of VWO-32?" |
| **Code** | "How do I use BasePage class?" |
| **Code** | "Show me the LoginPage implementation" |

---

## ⚡ Quick Commands

| Command | What It Does |
|---------|--------------|
| `python -m qabuddy ask "question"` | Ask from terminal |
| `python -m qabuddy search "query"` | Search without LLM |
| `python -m qabuddy ingest` | Update search index |
| `python -m qabuddy ingest --full` | Rebuild index |
| `python -m qabuddy eval` | Check retrieval quality |
| `python -m qabuddy test` | Run regression tests |
| `curl.exe http://localhost:8300/api/health` | Check health |

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| **"Ollama is not reachable"** | `ollama serve` in Terminal 1 |
| **"Qdrant connection refused"** | `.\.qdrant-win\qdrant.exe` in Terminal 2 |
| **"Groq 429 Too many requests"** | Wait 60 seconds or upgrade Groq plan |
| **"UI says Build the UI"** | `cd ui && npm run build && cd ..` |
| **"Port 8300 already in use"** | Change `PORT=8301` in `.env` |
| **"Model not found"** | `ollama pull qwen3-embedding:0.6b` |

---

## 📚 Documentation

| Document | What's Inside |
|----------|---------------|
| **GETTING_STARTED.html** | Visual setup guide (open in browser) |
| **QUICKSTART.md** | Complete step-by-step with details |
| **COMMANDS_CHEATSHEET.md** | All commands organized by purpose |
| **SYSTEM_OVERVIEW.md** | Architecture & how it works |
| **README.md** | Original project overview |
| **SETUP.md** | Detailed environment setup |
| **deploy/DEPLOY.md** | Production Docker deployment |

---

## 🏗️ Architecture at a Glance

```
User Question
    ↓
FastAPI Backend
    ├── Dense Search (Qwen3)
    ├── Keyword Search (BM25)
    └── Rerank (Cross-encoder)
    ↓
    → Qdrant Database
    ↓
Answer LLM (Groq)
    ↓
React UI ← http://localhost:8300
    ↓
Answer with [1] [2] [3] Citations
```

---

## 🔑 Key Concepts

### Dense Search
- Understands **meaning**
- Uses Qwen3 embeddings (1024-dim vectors)
- Slow but smart (~160ms)
- Good for: "How do I test..."

### BM25 Search
- Understands **keywords**
- Code-aware tokenizer
- Fast (~5ms)
- Good for: "VWO-26", "testLoginPositive"

### Hybrid (Both)
- Combines dense + BM25
- Fusion: 1/rank_dense + 1/rank_bm25
- Best of both worlds
- Achieves 100% hit@6 on golden set

### Reranking
- Cross-encoder (MS-Marco)
- Scores top-24 by relevance
- Moves best answer to #1
- ~1 second overhead

### LLM (Answer)
- Groq gpt-oss-120b (remote)
- Gets only top-6 chunks
- Must cite sources [1] [2] [3]
- ~2-5 seconds total

---

## 📊 Performance Targets

| Operation | Time | Notes |
|-----------|------|-------|
| Embed query | 160ms | One-time per question |
| Search | 20ms | Dense + BM25 + fusion |
| Rerank | 1.2s | If enabled |
| LLM | 2-5s | Groq API call |
| **Total** | **~4-7s** | End-to-end |

---

## 🔐 What Gets Redacted

✓ Passwords  
✓ API Keys  
✓ Tokens  
✓ Database credentials  

❌ NOT redacted: Locators like `By.id("password")`

---

## 💾 Data Sources (10 folders)

| Folder | Type | Example |
|--------|------|---------|
| **00_TestCases** | CSV/XLSX | VWO_500_Test_Cases.csv |
| **01_JIRA_Tickets** | Markdown | VWO-26.md, QAB-101.md |
| **02_Company_Docs** | PDF/MD | Handbook, Standards |
| **03_Meeting_Notes** | VTT | Transcripts, Stand-ups |
| **04_Lucid_charts** | JSON/CSV/TXT | Flows, Diagrams |
| **05_PRD_SRS_BRD** | PDF | Requirements |
| **06_Figma_Designs** | Specs | (Phase 2) |
| **06_Jenkins_Logs** | Logs | Build #142, #143 |
| **07_Source_Code** | Python/Java | Frameworks (git submodules) |

---

## ⚙️ Configuration (in `.env`)

```dotenv
# LLM Answer Generation
GROQ_API_KEY=your_key_here          # Required!
LLM_MODEL=openai/gpt-oss-120b

# Embeddings (Ollama)
OLLAMA_URL=http://localhost:11434
EMBED_MODEL=qwen3-embedding:0.6b
EMBED_DIM=1024

# Vector Database (Qdrant)
QDRANT_URL=http://localhost:6333    # Local or Cloud
QDRANT_API_KEY=                      # Leave empty for local

# Search Tuning (advanced)
PREFETCH_K=40                        # Candidates before fusion
RERANK_CANDIDATES=24                 # Candidates to rerank
FINAL_K=6                            # Chunks to LLM
CONTEXT_TOKENS=3500                  # Prompt budget
```

---

## 🎯 Test Your Setup

```powershell
# 1. Check health
curl.exe http://localhost:8300/api/health

# 2. Ask a simple question
python -m qabuddy ask "What are test cases?"

# 3. Check retrieval quality
python -m qabuddy eval

# 4. Run tests (no services needed)
python -m qabuddy test

# 5. Open browser
http://localhost:8300
```

**All 5 pass?** → Setup is complete! 🎉

---

## 📱 UI Quick Tour

### 1. Question Input
Type question at top, press Enter

### 2. Mode Selector
- 💬 Ask anything
- 🧯 Failure analysis (RCA)
- 🧪 Test design & gaps
- 🐞 Bug triage
- 🛠️ Framework coding
- 🧭 Traceability (RTM)

### 3. Answer Display
- Answer text
- [1] [2] [3] Citation links
- Confidence score

### 4. Source Viewer
Click [1] to see exact chunk used

### 5. Retrieval Trace
See how the answer was found (for debugging)

---

## 🌙 Dark Mode

Click theme toggle in top-right corner

---

## 🔗 Quick Links

| Link | Purpose |
|------|---------|
| http://localhost:8300 | Main QA Buddy app |
| https://console.groq.com/keys | Get Groq API key |
| https://qdrant.tech/cloud | Qdrant Cloud signup |
| https://ollama.com | Ollama download |
| GETTING_STARTED.html | Open in browser for visual guide |

---

## 🆘 Still Stuck?

1. Check **COMMANDS_CHEATSHEET.md** for your error
2. Read **QUICKSTART.md** for detailed steps
3. Check **SYSTEM_OVERVIEW.md** for architecture
4. Review **SETUP.md** for troubleshooting section

---

## 💡 Pro Tips

✨ **Tip 1:** Files starting with `_` are ignored  
Example: `_archive_old_doc.pdf` won't be ingested

✨ **Tip 2:** `.env` is git-ignored (never committed)  
So it's safe to add secrets there

✨ **Tip 3:** First answer is slow (loads reranker)  
Subsequent answers are faster

✨ **Tip 4:** Groq free tier: ~2 answers/minute  
Upgrade tier if you need more

✨ **Tip 5:** Run `python -m qabuddy eval` to check retrieval quality  
Should show 100% Hit@6

---

## 📝 Version

**QA Buddy AI v1.0**  
**Setup Created:** 2026-10-10  
**Platform:** Windows 11  
**Python:** 3.13.15

---

**Happy QA'ing! 🤖**

*Questions? Check QUICKSTART.md or SYSTEM_OVERVIEW.md*
