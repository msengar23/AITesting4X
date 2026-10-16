# 🚀 QA BUDDY AI - START HERE NOW

**Your QA Buddy AI system is completely built and ready to go!**

---

## ⚡ Quick Start (5 minutes)

Follow these 5 steps in order:

### Step 1: Create Configuration (.env)
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
Copy-Item .env.example .env
notepad .env
```

**Edit .env and add TWO lines:**
```
GROQ_API_KEY=your_groq_key_here
QDRANT_URL=http://localhost:6333
```

💡 **Get free Groq key:** https://console.groq.com/keys

---

### Step 2: Download Embedding Model
```powershell
ollama pull qwen3-embedding:0.6b
ollama list
```
Wait for download to complete (~500MB, one-time only)

---

### Step 3: Build the Web UI
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
cd ui
npm install
npm run build
cd ..
```

Wait for "✓ built in X ms" message

---

### Step 4: Open 3 PowerShell Windows & Start Services

**WINDOW 1 - Ollama:**
```powershell
ollama serve
```
Keep open. You'll see: "API listening on 127.0.0.1:11434"

---

**WINDOW 2 - Qdrant:**
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
cd .qdrant-win
.\qdrant.exe
```
Keep open. You'll see port 6333 listening.

---

**WINDOW 3 - QA Buddy API:**
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
python -m qabuddy ingest
python -m qabuddy serve
```
Keep open. Wait for: "Uvicorn running on http://0.0.0.0:8300"

---

### Step 5: Open Browser
```
http://localhost:8300
```

**✅ DONE! Your QA Buddy is ready!**

---

## 💬 Try These Questions

```
"What are all the login test cases?"
"Why did build #142 fail?"
"Is testLoginPositiveVWO flaky?"
"Which features aren't tested?"
"Is VWO-26 a duplicate of VWO-33?"
"How do I use the BasePage class?"
```

---

## 📚 Documentation

| Want to... | Read This |
|-----------|-----------|
| Quick start | QUICKSTART.md |
| Print cheat sheet | QUICK_REFERENCE.md |
| Visual guide | GETTING_STARTED.html |
| All commands | COMMANDS_CHEATSHEET.md |
| How it works | SYSTEM_OVERVIEW.md |
| Troubleshooting | QUICKSTART.md - Troubleshooting section |

---

## ✅ What You Have

✓ **Complete Backend** - Python FastAPI  
✓ **Web Frontend** - React with modern UI  
✓ **Vector Database** - Qdrant  
✓ **Embeddings** - Qwen3 via Ollama  
✓ **Hybrid Search** - Dense + keyword  
✓ **10 Data Sources** - Tests, Jira, docs, code, logs, etc.  
✓ **Citation System** - Answer sources highlighted  
✓ **Multiple Modes** - Ask, RCA, Design, Triage, Code  

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| "Ollama is not reachable" | Make sure WINDOW 1: `ollama serve` is running |
| "Qdrant connection refused" | Make sure WINDOW 2: `.\qdrant.exe` is running |
| "Embedding model not found" | Run: `ollama pull qwen3-embedding:0.6b` |
| "Groq API error" | Get free key: https://console.groq.com/keys |
| "Port 8300 in use" | Edit .env: `PORT=8301` |

---

## 🎯 Daily Startup (After First Time)

Just run this 3 commands in 3 separate terminals:

```powershell
# Terminal 1
ollama serve

# Terminal 2  
cd .qdrant-win && .\qdrant.exe

# Terminal 3
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
python -m qabuddy serve
```

Then open: http://localhost:8300

---

## 📊 Architecture

```
Question (Browser)
    ↓
Hybrid Search
(Dense + Keyword)
    ↓
Qdrant Database
    ↓
Rerank Results
    ↓
LLM (Groq)
    ↓
Answer with Citations [1] [2] [3]
```

---

## ✨ Features

- **Hybrid Search:** Semantic + keyword matching
- **10 Data Sources:** Tests, Jira, docs, code, logs, etc.
- **Citations:** Every answer shows sources
- **Retrieval Trace:** See how answer was found
- **Multiple Modes:** Ask, RCA, Design, Triage, Code
- **Dark Mode:** Toggle theme
- **Fast:** ~4-7 seconds end-to-end
- **Secure:** Passwords auto-redacted

---

## 🎉 YOU'RE READY!

Your QA Buddy AI system is fully built with:
- ✅ Complete backend + frontend
- ✅ 10 comprehensive guides  
- ✅ Automated startup scripts
- ✅ Sample data with 10 sources
- ✅ Full documentation

**Follow the 5 steps above to start using it in 5 minutes!**

---

## 📞 Need Help?

1. Check **QUICKSTART.md** - Step-by-step with details
2. Check **COMMANDS_CHEATSHEET.md** - All commands
3. Check **SYSTEM_OVERVIEW.md** - How it works
4. Check **QUICKSTART.md - Troubleshooting** - Common fixes

---

**Created:** 2026-10-10  
**Status:** ✅ Ready to Use  
**Time to First Run:** 5 minutes
