# QA Buddy AI - Startup Guide

**Status Check Results:**
- ✅ Python 3.11.9 installed
- ✅ Ollama 0.35.1 installed  
- ✅ Node.js v24 installed
- ❌ .env file NOT created
- ❌ UI NOT built
- ❌ Embedding model NOT pulled

---

## Step-by-Step Startup (5 minutes)

### STEP 1: Create .env File (1 minute)

```powershell
# Navigate to project folder
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"

# Copy example to .env
Copy-Item .env.example .env

# Open in Notepad
notepad .env
```

**Edit these 2 lines:**
```dotenv
GROQ_API_KEY=your_groq_key_here
QDRANT_URL=http://localhost:6333
```

Get a free Groq key: https://console.groq.com/keys

---

### STEP 2: Pull Embedding Model (3 minutes)

```powershell
# This downloads the embedding model (one-time, ~500MB)
ollama pull qwen3-embedding:0.6b

# Verify it's downloaded
ollama list
```

Wait for this to complete - you should see `qwen3-embedding:0.6b` in the list.

---

### STEP 3: Build the UI (1 minute)

```powershell
# Navigate to project
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"

# Build UI
cd ui
npm install
npm run build
cd ..
```

Wait for "✓ built in X ms" message.

---

### STEP 4: Start 3 Services (Keep These Running)

**Open 3 separate PowerShell windows:**

**WINDOW 1: Ollama (Embedding Server)**
```powershell
ollama serve
```
Keep this running - you'll see "API listening on 127.0.0.1:11434"

---

**WINDOW 2: Qdrant (Vector Database)**
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"
cd .qdrant-win
.\qdrant.exe
```
Keep this running - you'll see port 6333 listening

---

**WINDOW 3: QA Buddy API**
```powershell
cd "C:\Users\mamta\AITESTER4XBATCH\chapter_12_RAG_QA_BuddyAI"

# First time: Ingest data
python -m qabuddy ingest

# Then: Start API
python -m qabuddy serve
```

Wait for "Uvicorn running on http://0.0.0.0:8300"

---

### STEP 5: Open Browser

Once you see "Uvicorn running on..." in WINDOW 3, open your browser:

```
http://localhost:8300
```

---

## ✅ Your QA Buddy is Ready!

You should see:
- Beautiful web interface
- Question input box at top
- Mode selector (Ask, RCA, Design, etc.)
- Example questions

---

## 💬 Try These Questions

```
"What are all the login test cases?"
"Why did build #142 fail?"
"Is testLoginPositiveVWO flaky?"
"Which features don't have automated tests?"
"Is VWO-26 a duplicate of VWO-33?"
```

---

## 🆘 If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| "Ollama is not reachable" | Make sure WINDOW 1 is running `ollama serve` |
| "Qdrant connection refused" | Make sure WINDOW 2 is running `.\qdrant.exe` |
| "Embedding model not found" | Re-run `ollama pull qwen3-embedding:0.6b` in WINDOW 1 |
| "UI says Build the UI" | Run `cd ui && npm run build && cd ..` again |
| "Port 8300 already in use" | Change `PORT=8301` in .env |

---

## 📝 Keep These Windows Open

Do NOT close:
- WINDOW 1: Ollama server
- WINDOW 2: Qdrant server  
- WINDOW 3: QA Buddy API

All three must be running for the app to work!

---

## 🎉 Done!

You now have a working QA Buddy AI system!

Happy QA'ing! 🤖
