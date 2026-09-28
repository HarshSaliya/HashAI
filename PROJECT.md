# HashAi — Project

## What it is

A RAG chatbot for my portfolio site. Recruiters ask questions about me, the bot
answers from my resume. It only answers from retrieved content — if something
isn't in the resume, it says it doesn't know.

## Flow

```
PDF -> extract -> clean -> chunk -> embed -> Postgres (pgvector)

question -> embed -> cosine search -> top chunks -> LLM -> answer
```

## Steps

**1. Extract** (`main.py`) — pdfplumber reads the resume PDF. Cleans `(cid:127)`
(bullet glyphs) and stray `[]` from empty table output.

**2. Chunk** — `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`.
Produces 6 chunks.

**3. Embed** — `BAAI/bge-m3` via sentence-transformers, runs locally. Outputs
1024 dimensions, so the DB column is `vector(1024)`.

**4. Store** — Neon Postgres with pgvector. `db.py` wraps psycopg with
fetchone / fetchall / insert / update / delete.

**5. Retrieve** (`embed.py`) — embed the question, then:

```sql
SELECT content, embedding <=> %s AS distance
FROM resume_chunks
ORDER BY embedding <=> %s
LIMIT 5
```

`<=>` is cosine distance. Lower = closer in meaning.

**6. Generate** — retrieved chunks + question go to Groq. System prompt limits
the answer to the given context.

## Stack

| Layer | Choice |
|---|---|
| PDF | pdfplumber |
| Chunking | langchain-text-splitters |
| Embeddings | sentence-transformers, BAAI/bge-m3 (local) |
| Vector store | Neon Postgres + pgvector |
| Generation | Groq |
| API | FastAPI (not built yet) |

## Status

Done: ingestion, embedding, storage, retrieval, generation.
Left: FastAPI endpoint.

## Known gaps

- No `source` column. Ingestion does `DELETE FROM resume_chunks` before insert,
  so adding a second document would wipe the first one's chunks.
- `updated_at` column exists but nothing updates it.
- Re-embeds every chunk on each run, even unchanged ones.
- No HNSW index (fine at 6 rows, needed later).
- No rate limiting on the API.
