from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import rag

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="RAG Explorer")


def pdf_path() -> Path:
    pdfs = sorted(rag.DATA_DIR.glob("*.pdf"))
    if not pdfs:
        raise HTTPException(status_code=404, detail="No PDF found in data/")
    return pdfs[0]


@app.on_event("startup")
def startup():
    # Ingest the PDF once at startup if the vector store is empty.
    if rag.get_collection().count() == 0:
        rag.ingest_pdf(pdf_path())


class Question(BaseModel):
    question: str
    top_k: int = 3


class IngestSettings(BaseModel):
    chunk_size: int = Field(default=rag.DEFAULT_CHUNK_SIZE, ge=20, le=500)
    chunk_overlap: int = Field(default=rag.DEFAULT_OVERLAP, ge=0, le=200)


@app.get("/api/status")
def status():
    return {
        **rag.load_config(),
        "file": pdf_path().name,
        "chunks_stored": rag.get_collection().count(),
        "embedding_model": rag.EMBED_MODEL,
        "llm_model": rag.GROQ_MODEL,
    }


@app.post("/api/ingest")
def ingest(settings: IngestSettings):
    """Re-read the PDF and rebuild the chunks and embeddings with the given settings."""
    try:
        return rag.ingest_pdf(pdf_path(), settings.chunk_size, settings.chunk_overlap)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/chunks")
def chunks():
    return rag.list_chunks()


@app.post("/api/search")
def search(body: Question):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")
    return {"query": body.question, "results": rag.search(body.question, body.top_k)}


@app.post("/api/chat")
def chat(body: Question):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")
    hits = rag.search(body.question, body.top_k)
    try:
        answer = rag.ask_llm(body.question, hits)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}")
    return {"question": body.question, "answer": answer, "sources": hits}


STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
