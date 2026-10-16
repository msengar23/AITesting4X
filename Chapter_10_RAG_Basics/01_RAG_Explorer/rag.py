"""
Minimal RAG pipeline for the RAG Explorer.

Pipeline:
  PDF -> page text -> chunks (with overlap) -> embeddings (Nomic, local)
      -> ChromaDB (local vector store)
  Question -> embedding -> cosine similarity search -> top-k chunks
      -> Groq LLM (openai/gpt-oss-120b) -> answer grounded in those chunks
"""
import json
import os
import re
from pathlib import Path

import chromadb
import httpx
from dotenv import load_dotenv
from fastembed import TextEmbedding
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "prd_chunks"

EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"
CONFIG_PATH = CHROMA_DIR / "ingest_config.json"
DEFAULT_CHUNK_SIZE = 180   # words per chunk
DEFAULT_OVERLAP = 40       # words shared between neighbouring chunks

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"

_embedder = None
_collection = None


def get_embedder():
    global _embedder
    if _embedder is None:
        # First call downloads the model (once), then it runs locally on CPU.
        _embedder = TextEmbedding(model_name=EMBED_MODEL)
    return _embedder


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},  # rank by cosine similarity
        )
    return _collection


def embed(texts, kind="document"):
    # Nomic models expect a task prefix: "search_document: " for stored text,
    # "search_query: " for questions.
    prefix = "search_document: " if kind == "document" else "search_query: "
    vectors = list(get_embedder().embed([prefix + t for t in texts]))
    return [v.tolist() for v in vectors]


def extract_pages(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        # PDFs often come out one word per line. Collapse every run of whitespace
        # (including Unicode spaces and newlines) into a single space.
        text = re.sub(r"\s+", " ", text).strip()
        pages.append({"page": number, "text": text})
    return pages


def chunk_words(text: str, size: int, overlap: int):
    """Split text into windows of `size` words; each window repeats the last `overlap` words of the previous one."""
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        window = words[start:start + size]
        chunks.append({
            "text": " ".join(window),
            # The first `overlap` words of every chunk except the first are shared with the previous chunk.
            "overlap_words": overlap if start else 0,
        })
        if start + size >= len(words):
            break
    return chunks


def load_config():
    """Settings used by the last ingest, or the defaults if nothing has been ingested yet."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"chunk_size": DEFAULT_CHUNK_SIZE, "chunk_overlap": DEFAULT_OVERLAP}


def ingest_pdf(pdf_path: Path, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_OVERLAP):
    """Read the PDF, chunk it by words, embed it and store it in ChromaDB. Replaces old data."""
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("overlap must be at least 0 and smaller than the chunk size")

    pages = extract_pages(pdf_path)
    records = []
    for page in pages:
        for i, c in enumerate(chunk_words(page["text"], chunk_size, chunk_overlap)):
            records.append({
                "id": f"p{page['page']}-c{i}",
                "text": c["text"],
                "page": page["page"],
                "words": len(c["text"].split()),
                "overlap_words": c["overlap_words"],
            })

    collection = get_collection()
    if collection.count():
        collection.delete(ids=collection.get()["ids"])

    dimension = None
    if records:
        vectors = embed([r["text"] for r in records], kind="document")
        dimension = len(vectors[0])
        collection.add(
            ids=[r["id"] for r in records],
            documents=[r["text"] for r in records],
            embeddings=vectors,
            metadatas=[{k: r[k] for k in ("page", "words", "overlap_words")} for r in records],
        )

    config = {
        "file": pdf_path.name,
        "pages": len(pages),
        "words": sum(len(p["text"].split()) for p in pages),
        "chunks": len(records),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "dimension": dimension,
    }
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config), encoding="utf-8")
    return config


def list_chunks():
    data = get_collection().get()
    chunks = []
    for cid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        chunks.append({"id": cid, "text": doc, **meta})
    # ids look like "p3-c12": sort by page, then by chunk number.
    chunks.sort(key=lambda c: (c["page"], int(c["id"].split("-c")[1])))
    return chunks


def search(query: str, top_k: int = 3):
    """Embed the query and return the top_k most similar chunks with scores."""
    query_vector = embed([query], kind="query")[0]
    result = get_collection().query(query_embeddings=[query_vector], n_results=top_k)
    hits = []
    for cid, doc, meta, dist in zip(
        result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append({
            "id": cid,
            "text": doc,
            "page": meta["page"],
            # Chroma returns cosine distance (1 - similarity); convert back to similarity.
            "score": round(1 - dist, 4),
        })
    return hits


def ask_llm(question: str, hits):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from .env")

    context = "\n\n".join(f"[Chunk {h['id']} | page {h['page']}]\n{h['text']}" for h in hits)
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions about a Product Requirements Document. "
                "Use only the provided context. If the answer is not in the context, say so. "
                "Cite the chunk ids you used, for example (p2-c1)."
            ),
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    response = httpx.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.2},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
