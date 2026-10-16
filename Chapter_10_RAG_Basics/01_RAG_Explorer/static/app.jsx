const { useState, useEffect } = React;

async function api(path, body) {
  const res = await fetch(path, body
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
    : undefined);
  const data = await res.json();
  if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : res.statusText);
  return data;
}

const STAGES = [
  { name: "1. Extract", detail: "pypdf · per page" },
  { name: "2. Normalise", detail: "repair the text" },
  { name: "3. Chunk", detail: (s) => `${s.size}w / ${s.overlap} overlap`, key: "chunk" },
  { name: "4. Embed", detail: (s) => `nomic · ${s.dimension || 768}d · local`, key: "embed" },
  { name: "5. Store", detail: "Chroma · cosine" },
];

function Stages({ size, overlap, dimension }) {
  return (
    <div className="stages">
      {STAGES.map((st, i) => (
        <div className={"stage" + (st.key === "chunk" ? " hot" : "")} key={i}>
          <b>{st.name}</b>
          <code>{typeof st.detail === "function" ? st.detail({ size, overlap, dimension }) : st.detail}</code>
        </div>
      ))}
    </div>
  );
}

function ScoreBar({ score }) {
  const pct = Math.max(0, Math.min(1, score)) * 100;
  return (
    <div>
      <div className="bar"><div style={{ width: pct + "%" }} /></div>
      <span className="score">similarity {score.toFixed(4)}</span>
    </div>
  );
}

// Shows the overlap words (shared with the previous chunk) in a highlight colour.
function ChunkText({ text, overlapWords }) {
  if (!overlapWords) return <p>{text}</p>;
  const words = text.split(" ");
  return (
    <p>
      <span className="shared">{words.slice(0, overlapWords).join(" ")}</span>{" "}
      {words.slice(overlapWords).join(" ")}
    </p>
  );
}

function Chunk({ chunk, rank, score, hit, showOverlap }) {
  return (
    <div className={"chunk" + (hit ? " hit" : "")}>
      <div className="meta">
        {rank && <span className="tag">Rank #{rank}</span>}
        <span className="tag">{chunk.id}</span>
        <span className="tag">page {chunk.page}</span>
        <span className="tag">{chunk.words} words</span>
        {showOverlap && chunk.overlap_words > 0 && (
          <span className="tag">{chunk.overlap_words} shared with previous</span>
        )}
      </div>
      {score !== undefined && <ScoreBar score={score} />}
      <ChunkText text={chunk.text} overlapWords={showOverlap ? chunk.overlap_words : 0} />
    </div>
  );
}

function IngestTab({ status, onStatus }) {
  const saved = status || { chunk_size: 180, chunk_overlap: 40 };
  const [size, setSize] = useState(saved.chunk_size);
  const [overlap, setOverlap] = useState(saved.chunk_overlap);
  const [chunks, setChunks] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const loadChunks = () => api("/api/chunks").then(setChunks).catch(e => setError(e.message));
  useEffect(() => { loadChunks(); }, []);

  // Keep overlap below the chunk size when the size slider moves.
  const changeSize = (value) => {
    setSize(value);
    if (overlap >= value) setOverlap(value - 1);
  };

  const ingest = async () => {
    setBusy(true); setError("");
    try {
      const r = await api("/api/ingest", { chunk_size: size, chunk_overlap: overlap });
      setResult(r);
      await loadChunks();
      onStatus();
    } catch (e) { setError(e.message); }
    setBusy(false);
  };

  const dimension = result?.dimension || saved.dimension;
  const pct = Math.round((overlap / size) * 100);

  return (
    <>
      <h2 className="section">1 · Ingest the PDF</h2>
      <p className="lead">
        Five stages turn a PDF into something searchable. Change the chunk settings and re-run to
        watch the trade-off move.
      </p>

      <Stages size={size} overlap={overlap} dimension={dimension} />

      <div className="card">
        <div className="controls">
          <div className="control">
            <label>Chunk size: <b>{size} words</b></label>
            <input type="range" min="20" max="500" step="10" value={size}
              onChange={e => changeSize(Number(e.target.value))} />
          </div>
          <div className="control">
            <label>Overlap: <b>{overlap} words</b> <span className="pct">({pct}%)</span></label>
            <input type="range" min="0" max={size - 1} step="5" value={Math.min(overlap, size - 1)}
              onChange={e => setOverlap(Number(e.target.value))} />
          </div>
        </div>
        <button className="btn" onClick={ingest} disabled={busy}>
          {busy ? "Ingesting..." : "Ingest PDF"}
        </button>
        {error && <p className="error">{error}</p>}

        {result && (
          <div className="stats">
            <div className="stat"><b>{result.pages}</b><span>pages</span></div>
            <div className="stat"><b>{result.words}</b><span>words extracted</span></div>
            <div className="stat"><b>{result.chunks}</b><span>chunks stored</span></div>
            <div className="stat"><b>{result.dimension}</b><span>dimensions per vector</span></div>
          </div>
        )}
      </div>

      {chunks.length > 0 && (
        <>
          <div className="chunk-list-title">Chunks ({chunks.length}) · highlighted words are shared with the previous chunk</div>
          {chunks.map(c => <Chunk key={c.id} chunk={c} showOverlap />)}
        </>
      )}
    </>
  );
}

function SearchTab() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const run = async () => {
    if (!query.trim()) return;
    setBusy(true); setError("");
    try { setResult(await api("/api/search", { question: query, top_k: 3 })); }
    catch (e) { setError(e.message); }
    setBusy(false);
  };

  return (
    <>
      <h2 className="section">2 · Search the chunks</h2>
      <p className="lead">
        Your question is embedded into a vector, then compared with every chunk vector using cosine
        similarity (closer to 1 = more similar). The three highest scores are returned.
      </p>
      <div className="card">
        <div className="row" style={{ marginTop: 0 }}>
          <input className="text-input" type="text" value={query}
            placeholder="e.g. What is the error recovery flow?"
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === "Enter" && run()} />
          <button className="btn" style={{ marginTop: 0 }} onClick={run} disabled={busy}>
            {busy ? "Searching..." : "Search"}
          </button>
        </div>
        {error && <p className="error">{error}</p>}
      </div>
      {result && (
        <>
          <div className="chunk-list-title">Top 3 results for “{result.query}”</div>
          {result.results.map((hit, i) => (
            <Chunk key={hit.id} chunk={hit} rank={i + 1} score={hit.score} hit />
          ))}
        </>
      )}
    </>
  );
}

function ChatTab() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const ask = async () => {
    if (!question.trim()) return;
    setBusy(true); setError(""); setResponse(null);
    try { setResponse(await api("/api/chat", { question, top_k: 3 })); }
    catch (e) { setError(e.message); }
    setBusy(false);
  };

  return (
    <>
      <h2 className="section">3 · Chat with the PDF</h2>
      <p className="lead">
        Steps: question → vector search (top 3 chunks, with scores) → chunks sent to{" "}
        <code>openai/gpt-oss-120b</code> on Groq → an answer that cites chunk ids.
      </p>
      <div className="card">
        <div className="row" style={{ marginTop: 0 }}>
          <input className="text-input" type="text" value={question}
            placeholder="Ask a question about the PRD"
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === "Enter" && ask()} />
          <button className="btn" style={{ marginTop: 0 }} onClick={ask} disabled={busy}>
            {busy ? "Thinking..." : "Ask"}
          </button>
        </div>
        {error && <p className="error">{error}</p>}
      </div>
      {response && (
        <>
          <div className="card">
            <div className="chunk-list-title" style={{ marginTop: 0 }}>Answer</div>
            <div className="answer">{response.answer}</div>
          </div>
          <div className="chunk-list-title">Top chunks used as context</div>
          {response.sources.map((hit, i) => (
            <Chunk key={hit.id} chunk={hit} rank={i + 1} score={hit.score} hit />
          ))}
        </>
      )}
    </>
  );
}

function App() {
  const [tab, setTab] = useState("ingest");
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  const loadStatus = () => api("/api/status").then(setStatus).catch(e => setError(e.message));
  useEffect(() => { loadStatus(); }, []);

  const tabs = [
    { id: "ingest", label: "1 · Ingest & Chunks" },
    { id: "search", label: "2 · Search" },
    { id: "chat", label: "3 · Chat" },
  ];

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="logo">R</div>
          <div>
            <h1>RAG Explorer</h1>
            <small>PDF → chunks → vectors → answers</small>
          </div>
        </div>
        <div className="badges">
          <span className="badge"><span className="dot" />nomic-embed-text</span>
          <span className="badge llm">openai/gpt-oss-120b</span>
          <span className="badge">chroma</span>
        </div>
      </header>

      <nav className="tabs">
        {tabs.map(t => (
          <button key={t.id} className={tab === t.id ? "active" : ""} onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </nav>

      {error && <p className="error">{error}</p>}
      {tab === "ingest" && <IngestTab status={status} onStatus={loadStatus} />}
      {tab === "search" && <SearchTab />}
      {tab === "chat" && <ChatTab />}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
