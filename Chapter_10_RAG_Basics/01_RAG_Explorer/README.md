# RAG Explorer

A small RAG app that shows how a PDF is ingested (chunked, embedded, stored) and how questions are answered from its chunks.

- **Embeddings:** `nomic-ai/nomic-embed-text-v1.5` via fastembed (local, no GPU or PyTorch needed)
- **Vector DB:** ChromaDB (persistent, stored in `chroma_db/`)
- **Search:** cosine similarity, top 3 chunks with scores
- **LLM:** `openai/gpt-oss-120b` on Groq (uses `GROQ_API_KEY` from `.env`)
- **UI:** React page (no build step) served by FastAPI

## Setup (Windows PowerShell)

```powershell
cd C:\Users\mamta\AITESTER4XBATCH\Chapter_10_RAG_Basics\01_RAG_Explorer
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If you create the venv again from scratch: `python -m venv .venv`, then run the steps above.

## Run

```powershell
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

On the first start, the app reads `data/*.pdf`, builds the chunks and stores them in ChromaDB. The first start also downloads the embedding model (about 2 minutes).

## Tabs

1. **Ingestion & chunks:** the pipeline steps, chunk stats, and every chunk with its page and character range. "Re-ingest PDF" rebuilds everything.
2. **Search:** type a question to see the top 3 chunks with cosine similarity scores.
3. **Chat:** the answer from `gpt-oss-120b`, plus the top 3 chunks it was given.

## Privacy note

Embeddings and search run locally. In Chat mode, the question and the retrieved chunks are sent to Groq's API to generate the answer. Don't use this with a confidential PDF unless your organization allows sending that content to Groq.

## Key files

| File | Purpose |
|---|---|
| `rag.py` | PDF extraction, chunking, embeddings, ChromaDB, search, Groq call |
| `main.py` | FastAPI routes (`/api/status`, `/api/ingest`, `/api/chunks`, `/api/search`, `/api/chat`) |
| `static/index.html`, `static/app.jsx` | React UI |
| `.env` | `GROQ_API_KEY` (git-ignored, never commit it) |
