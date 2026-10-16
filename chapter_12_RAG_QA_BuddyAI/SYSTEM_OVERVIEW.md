# QA Buddy AI - System Architecture & Overview

## 📊 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          USER (Question Input)                               │
│                              http://localhost:8300                            │
└──────────────────────────────────────────┬───────────────────────────────────┘
                                           │
                    ┌──────────────────────▼──────────────────────┐
                    │     FastAPI Backend (Python)                │
                    │  - Route requests                           │
                    │  - Orchestrate retrieval + answer pipeline  │
                    └──────────────────────┬──────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │                                               │
        ┌───────────▼──────────────┐                ┌─────────────▼─────────┐
        │   RETRIEVAL PIPELINE     │                │  ANSWER GENERATION    │
        └───────────┬──────────────┘                └─────────────┬─────────┘
                    │                                              │
        ┌───────────┴─────────────────┐                ┌──────────▼─────────┐
        │                               │                │                  │
   ┌────▼──────┐              ┌────────▼─────┐       ┌──▼────────────────┐ │
   │   Dense   │              │     BM25     │       │  Reranker        │ │
   │ Retrieval │              │   Retrieval  │       │ (Cross-encoder)  │ │
   │           │              │              │       │                  │ │
   │ Qwen3     │              │ Code-aware   │       │ MS-Marco         │ │
   │ 0.6B      │              │ Keywords     │       │ MiniLM-L-6-v2    │ │
   │           │              │              │       │                  │ │
   │ 1024-d    │              │ BM25 Index   │       │ Scores top-24    │ │
   │ Vectors   │              │ (In-memory)  │       │ candidates       │ │
   └─────┬─────┘              └─────┬────────┘       └─────┬────────────┘ │
         │                           │                      │              │
         └───────────┬───────────────┘                      │              │
                     │                                       │              │
              ┌──────▼──────────┐                    ┌──────▼──────────┐   │
              │   Qdrant DB     │                    │   LLM (Groq)   │   │
              │   Hybrid Search │                    │  gpt-oss-120b  │   │
              │                 │                    │                │   │
              │ - dense index   │                    │ Generates      │   │
              │ - BM25 index    │                    │ answer with    │   │
              │ - RRF fusion    │                    │ citations      │   │
              │ - Filtering     │                    │                │   │
              │                 │                    │ References [1] │   │
              └────────┬────────┘                    │ [2] [3]        │   │
                       │                             └────────┬───────┘   │
                       │                                      │           │
                       │ Top-6                              │           │
                       │ Chunks                             │           │
                       │                                     │           │
                       └─────────────────┬───────────────────┘           │
                                         │                               │
                    ┌────────────────────▼───────────────────┐           │
                    │   Response Formatter                   │           │
                    │   - Answer text                        │           │
                    │   - Citation links [1] [2] [3]        │           │
                    │   - Source viewer                      │           │
                    │   - Retrieval trace (debug info)       │           │
                    └────────────────────┬───────────────────┘           │
                                         │                               │
                    ┌────────────────────▼───────────────────┐           │
                    │     React Frontend (UI)                │           │
                    │   - Question input                     │           │
                    │   - Mode selector                      │           │
                    │   - Answer display                     │           │
                    │   - Source viewer                      │           │
                    │   - Retrieval trace                    │           │
                    └────────────────────┬───────────────────┘           │
                                         │                               │
                    ┌────────────────────▼───────────────────────────────┘
                    │
                    └──► User sees ANSWER + CITATIONS + TRACE

```

---

## 🏗️ Component Details

### 1. **Frontend (React + Vite)**
- **Location:** `ui/`
- **Tech Stack:** React, Vite, CSS
- **Served by:** FastAPI on port 8300
- **Features:**
  - Question input with auto-complete
  - Mode selector (Ask, RCA, Design, Triage, Framework, RTM)
  - Real-time answer display with streaming
  - Source viewer - click citations to see original chunks
  - Retrieval trace - debug how answer was found
  - Dark/light theme toggle

### 2. **Backend API (FastAPI)**
- **Location:** `qabuddy/api.py`
- **Tech Stack:** Python 3.13, FastAPI
- **Port:** 8300
- **Key Endpoints:**
  - `POST /api/ask` - Generate answer with citations
  - `POST /api/search` - Retrieval only (no answer)
  - `GET /api/health` - System health check
  - `GET /` - Serve built UI

### 3. **Embedding Model (Ollama)**
- **Model:** Qwen3-Embedding 0.6B
- **Dimensions:** 1024
- **Port:** 11434
- **Purpose:** Convert text to semantic vectors
- **Why Qwen3?**
  - #1 on MTEB benchmark
  - Handles code natively
  - 32K token input (longer documents)
  - Light enough for CPU
  - Instruction-aware

### 4. **Vector Database (Qdrant)**
- **Version:** 1.19.1
- **Port:** 6333 (local) or Cloud URL
- **Collections:** `qabuddy` (default)
- **Vectors per chunk:** 2
  - `dense`: Qwen3 embeddings (cosine distance)
  - `bm25`: Sparse lexical vectors (with IDF)
- **Search:** Hybrid RRF (Reciprocal Rank Fusion)
- **Filtering:** By source, module, ticket, test ID, etc.

### 5. **Hybrid Search**

#### Dense Search (Semantic)
- Uses Qwen3 embeddings
- Understands meaning and context
- Slow (~160ms for embedding + search)
- Good for: "How do I test checkout flow?"

#### BM25 Search (Keyword)
- Code-aware tokenization
- Splits camelCase identifiers
- Fast (~10ms)
- Good for: "testLoginPositiveVWO", "VWO-26"

#### Fusion Strategy
```
Score = 1/rank_dense + 1/rank_bm25
         ──────────────────────────
                    2
```
- Combines both approaches
- Achieves better recall than either alone
- Hit@6: 100% on golden set
- MRR: 0.91

### 6. **Reranker (Cross-Encoder)**
- **Model:** MS-Marco MiniLM-L-6-v2
- **Input:** Top-24 fused results
- **Output:** Re-ranked top-6
- **Purpose:** Score candidates by relevance to query
- **Cost:** ~1 second on CPU
- **Skip:** Set `RERANK_ENABLED=false` if too slow

### 7. **LLM (Large Language Model)**
- **Provider:** Groq (remote API)
- **Model:** openai/gpt-oss-120b
- **Purpose:** Generate answer with citations
- **Alternative:** Local Ollama model (gpt-oss:20b)
- **Grounding:** Receives only top-6 chunks as context
- **Output:** Answer with [1] [2] [3] citations

### 8. **Data Ingestion Pipeline**

```
data/
├── 00_TestCases/      ──┐
├── 01_JIRA_Tickets/   ──┤
├── 02_Company_Docs/   ──┤
├── 03_Meeting_Notes/  ──┼──> Source-aware Chunkers
├── 04_Lucid_charts/   ──┤
├── 05_PRD_SRS_BRD/    ──┤
├── 06_Jenkins_Logs/   ──┤
└── 07_Source_Codes/   ──┘
         │
         ├──> Text Normalization
         │    ├─ Encoding (NFKC)
         │    ├─ Secret redaction
         │    └─ PDF/Excel parsing
         │
         ├──> Semantic Chunking
         │    ├─ Test cases: one row per chunk
         │    ├─ Docs: heading-aware sections
         │    ├─ Code: AST-aware methods
         │    └─ Logs: failure windows
         │
         ├──> Embedding (Qwen3)
         │    └─ 1024-d vectors
         │
         ├──> BM25 Indexing
         │    └─ Code-aware tokenization
         │
         └──> Qdrant Storage
              ├─ Dense index
              ├─ BM25 index
              ├─ Metadata (source, module, etc.)
              └─ Payload filters
```

---

## 📁 Directory Structure

```
chapter_12_RAG_QA_BuddyAI/
│
├── qabuddy/                    # Backend Python package
│   ├── __main__.py            # CLI entry point
│   ├── api.py                 # FastAPI server
│   ├── answer.py              # Answer generation + citations
│   ├── retrieve.py            # Retrieval orchestration
│   ├── embed.py               # Embedding via Ollama
│   ├── rerank.py              # Cross-encoder reranking
│   ├── llm.py                 # LLM clients (Groq, Ollama, OpenAI)
│   ├── store.py               # Qdrant vector DB client
│   ├── sparse.py              # BM25 in-memory index
│   ├── ingest.py              # Data ingestion
│   ├── config.py              # Environment configuration
│   ├── models.py              # Pydantic models
│   ├── text.py                # Text normalization
│   ├── jira_sync.py           # Jira API integration
│   ├── evaluate.py            # Evaluation on golden questions
│   │
│   └── chunkers/              # Source-specific chunking logic
│       ├── testcases.py       # CSV/XLSX test case chunker
│       ├── docs.py            # PDF/Markdown doc chunker
│       ├── jira.py            # Jira ticket chunker
│       ├── code.py            # Source code (tree-sitter)
│       ├── logs.py            # Jenkins log chunker
│       ├── diagram.py         # Lucid chart chunker
│       └── transcript.py      # VTT transcript chunker
│
├── ui/                         # Frontend React app
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── client.js          # API client
│   │   ├── bm25.js            # Client-side BM25 search
│   │   ├── styles.css         # Main styles
│   │   │
│   │   ├── components/
│   │   │   ├── Message.jsx    # Chat message display
│   │   │   ├── Answer.jsx     # Answer with citations
│   │   │   ├── Sidebar.jsx    # Mode/history sidebar
│   │   │   ├── SourceViewer.jsx    # Click [1] to view chunk
│   │   │   └── Trace.jsx      # Retrieval trace debug
│   │   │
│   │   └── theme/
│   │       ├── theme.js       # Theme configuration
│   │       ├── dark.css       # Dark mode
│   │       └── ThemeToggle.jsx # Theme switcher
│   │
│   ├── dist/                  # Built/production version (created by npm run build)
│   ├── public/
│   │   └── demo/              # Demo data for hosted version
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── data/                       # Data sources (10 folders)
│   ├── 00_TestCases/          # Test case CSV/XLSX
│   ├── 01_JIRA_Tickets/       # Jira exports (Markdown)
│   ├── 02_Company_Docs/       # PDFs, Markdown handbook
│   ├── 03_Meeting_Notes/      # VTT transcripts
│   ├── 04_Lucid_charts/       # Diagrams (JSON, CSV, TXT)
│   ├── 05_PRD_SRS_BRD_FRDs/   # Requirements documents
│   ├── 06_Figma_Desings/      # Design specs (phase 2)
│   ├── 06_Jenkins_Logs/       # Build logs
│   └── 07_Source_Codes/       # Selenium/Playwright frameworks (git submodules)
│
├── eval/                       # Evaluation & golden questions
│   ├── golden.yaml            # 24 golden question-answer pairs
│   └── last_run.json          # Latest evaluation results
│
├── tests/                      # Regression test suite
│   ├── test_pipeline.py       # 18 tests covering bugs found
│   └── conftest.py            # Pytest fixtures
│
├── deploy/                     # Production deployment
│   ├── Dockerfile             # Container image
│   ├── docker-compose.yml     # Compose file (Ollama + app + Caddy)
│   ├── DEPLOY.md              # Deployment guide
│   └── hourly-ingest.cron     # Auto-ingest scheduled task
│
├── api/                        # Vercel serverless functions (demo)
│   ├── demo-chat.js           # Edge function for demo
│   └── _prompt.js             # Prompt template
│
├── docs/                       # Documentation images
│   ├── rca-answer.png         # Example RCA answer
│   └── retrieval-trace.png    # Trace example
│
├── QUICKSTART.md              # Step-by-step setup guide (NEW)
├── SYSTEM_OVERVIEW.md         # This file
├── COMMANDS_CHEATSHEET.md     # Command reference (NEW)
├── GETTING_STARTED.html       # Visual guide (NEW)
├── START_QABUDDY.bat          # Automated startup (NEW)
├── README.md                  # Project overview
├── SETUP.md                   # Detailed setup
├── CLAUDE.md                  # AI assistant context
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── sources.yaml               # Data source configuration
├── glossary.yaml              # QA team terminology
│
├── .qdrant-win/               # Local Qdrant binary (created by setup)
│
└── .venv/                     # Virtual environment (optional)
```

---

## 🔄 Data Flow Example

**User Question:** "Why did build #142 fail?"

### Step 1: Query Processing
```
Input: "Why did build #142 fail?"
   │
   └──> Query Expansion
        - Add instruction: "Retrieve information about Jenkins build failures"
        - Expand abbreviations: "RC" → "Root Cause"
```

### Step 2: Parallel Retrieval
```
Dense Search (Semantic):
  • Embed query (160ms)
  • Search Qdrant dense index
  • Top matches: build logs, error messages
  • Results: [jenkins_log_142, error_trace, stack_overflow_link]

BM25 Search (Keyword):
  • Tokenize: ["why", "build", "142", "fail"]
  • Code-aware split: ["build", "142", "fail"]
  • BM25 scoring
  • Top matches: "build #142", "jenkins_log_142"
  • Results: [jenkins_log_142, vwo_issue_26, playwright_error]
```

### Step 3: Fusion
```
RRF Ranking:
  1. jenkins_log_142         (1/1 + 1/1 = 2.0)  ← Best
  2. error_trace             (1/2 + 1/3 = 0.83)
  3. stack_overflow_link     (1/3 + 1/5 = 0.53)
  
Top-40 candidates → Reranker
```

### Step 4: Reranking
```
Cross-encoder scores:
  jenkins_log_142:     0.95  ✓ Most relevant
  error_trace:         0.87
  stack_overflow:      0.45
  
Top-6 for LLM:
  [0] jenkins_log_142      (0.95)
  [1] error_trace          (0.87)
  [2] vwo_issue_26         (0.73)
  [3] playwright_issue     (0.68)
  [4] test_output          (0.61)
  [5] meeting_notes        (0.58)
```

### Step 5: Answer Generation
```
LLM Prompt (simplified):
  "You are a QA assistant. Based on these chunks, answer the question.
   
   CHUNKS:
   [0] Jenkins build #142 failed on 2026-04-15...
   [1] Error: TimeoutException on login test...
   [2] VWO-26: Login timeout due to IP allowlist...
   
   Question: Why did build #142 fail?
   
   Instructions:
   - Cite sources using [0] [1] [2] format
   - Be concise (under 200 words)"

LLM Output:
  "Build #142 failed due to a timeout in the login test [0].
   The root cause was a new IP allowlist on the auth server [2]
   that wasn't updated for the CI environment [1].
   
   The fix: Update the IP allowlist to include the CI runner IP."
```

### Step 6: Response to User
```
UI Display:
┌─────────────────────────────────────────┐
│ Answer:                                  │
│                                          │
│ Build #142 failed due to a timeout in   │
│ the login test [0]. The root cause was  │
│ a new IP allowlist on the auth server   │
│ [2] that wasn't updated for the CI      │
│ environment [1].                         │
│                                          │
│ The fix: Update the IP allowlist to     │
│ include the CI runner IP.                │
│                                          │
├─────────────────────────────────────────┤
│ Sources:                                 │
│ [0] Jenkins: vwo-selenium-regression    │
│     Build #142 log (Apr 15, 2026)       │
│ [1] Meeting Note: CI Login Failure      │
│     Triage (Apr 15, 2026)               │
│ [2] Jira: VWO-26 - Login timeout due    │
│     to IP allowlist                      │
├─────────────────────────────────────────┤
│ Retrieval Trace:                        │
│ Dense rank: #2 | BM25 rank: #1          │
│ Fusion score: 1.89 | Rerank: 0.95       │
└─────────────────────────────────────────┘
```

---

## 📊 Performance Characteristics

| Operation | Latency | Hardware |
|-----------|---------|----------|
| Embed query (1024 tokens) | ~160ms | Ollama on CPU |
| Dense search (100K vectors) | ~15ms | Qdrant |
| BM25 search (10K chunks) | ~5ms | In-memory |
| RRF fusion + reranking | ~1.2s | CPU cross-encoder |
| LLM first token | ~0.8s | Groq API |
| Full answer (2.5K tokens) | 2-5s | Groq API |
| **Total end-to-end** | **~4-7 seconds** | |

---

## 🎯 Quality Metrics

### Retrieval Quality (eval/golden.yaml - 24 questions)

| Metric | Score | Interpretation |
|--------|-------|-----------------|
| Hit@6 | 100% | Answer found in top 6 results |
| Mean Reciprocal Rank | 0.91 | Good ranking (higher is better) |
| Dense only Hit@6 | 100% | Semantic search works alone |
| BM25 only Hit@6 | 100% | Keyword search works alone |
| Hybrid Hit@6 | 100% | Fusion improves MRR |

### Answer Quality

- **18 regression tests** in `tests/test_pipeline.py`
- **Coverage:**
  - Misnamed Jira exports
  - PDF table parsing
  - Secret redaction
  - Citation accuracy
  - Edge cases (word boundaries, Unicode)

---

## 🔐 Security & Privacy

### Built-in Protections

1. **Secret Redaction**
   - Passwords: `password=<redacted>`
   - API keys: `api_key=<redacted>`
   - Tokens: `token=<redacted>`
   - NOT redacted: Locators like `By.id("login-password")`

2. **Demo Data Protection**
   - Non-sensitive data only (sample questions/answers)
   - Real framework code (public GitHub repos)
   - Corpus publicly available at https://qabuddy-ai-nine.vercel.app
   - Redaction verified at ingest time

3. **No External Data Leakage**
   - Embeddings stay local (Ollama)
   - BM25 is in-memory
   - Only questions/answers go to LLM (Groq)
   - LLM responses don't train on your data

---

## 🚀 Deployment Options

### Option 1: Local Development (Recommended First)
- All services run locally
- Ollama + Qdrant + API on same machine
- No cloud costs
- ~30 minutes setup

### Option 2: Qdrant Cloud + Local Compute
- Qdrant hosted in cloud (free tier available)
- Ollama + API on local machine
- Offload vector DB
- ~20 minutes setup

### Option 3: Full Cloud (Docker)
- Deployed to VPS (DigitalOcean, AWS, etc.)
- Ollama + API in containers
- Qdrant external (Cloud or VPS)
- HTTPS + team login via Caddy
- See `deploy/DEPLOY.md`

---

## 📋 Configuration Quick Reference

| Setting | Default | Adjusts |
|---------|---------|---------|
| `EMBED_MODEL` | `qwen3-embedding:0.6b` | Semantic quality vs. speed |
| `EMBED_DIM` | `1024` | Vector size (leave alone) |
| `RERANK_ENABLED` | `true` | Enable reranking (slower but better) |
| `RERANK_CANDIDATES` | `24` | # results to rerank (↑accuracy, ↑latency) |
| `PREFETCH_K` | `40` | # per retriever before fusion |
| `FINAL_K` | `6` | # chunks given to LLM (↑context, ↑cost) |
| `CONTEXT_TOKENS` | `3500` | Prompt source-text budget |
| `PORT` | `8300` | Server port |

---

## ✅ What's Implemented

- [x] Hybrid search (dense + sparse + RRF fusion)
- [x] Configurable chunking per source type
- [x] Secret redaction at ingest
- [x] Retrieval evaluation on golden questions
- [x] Regression test suite
- [x] FastAPI backend
- [x] React frontend with trace viewer
- [x] CLI for batch operations
- [x] Jira integration (REST + JQL)
- [x] Docker deployment configs
- [x] Hosted demo on Vercel

---

## 🔮 Future Phases

- [ ] **Phase 2:** Figma design specs, auto-ingest cron, dashboard
- [ ] **Phase 3:** Advanced modes (gap analysis, test matrix)
- [ ] **Phase 4:** Multi-workspace support, audit logging

---

**Created:** 2026-10-10  
**Last Updated:** 2026-10-10  
**Version:** 1.0
