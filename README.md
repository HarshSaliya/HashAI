# HashAi

A personal RAG chatbot for my portfolio site. Instead of a static "About Me" page, recruiters can ask questions — *"What's his experience with PostgreSQL?"*, *"Has he worked with AWS Lambda?"* — and get answers grounded in my actual resume.

Answers come only from retrieved resume content. If something isn't in the resume, the bot says it doesn't know rather than inventing it.

## Stack

| Layer | Choice |
|---|---|
| PDF extraction | pdfplumber |
| Chunking | langchain-text-splitters |
| Embeddings | sentence-transformers · BAAI/bge-m3 (1024-d, runs locally) |
| Vector store | Neon Postgres + pgvector |
| Generation | Groq |
| API | FastAPI *(in progress)* |

## How it works

```
PDF ─► extract ─► clean ─► chunk ─► embed ─► Postgres (pgvector)
                                                   │
question ─► embed ─► cosine search ◄───────────────┘
                          │
                    top-k chunks + question ─► LLM ─► answer
```

Embeddings run on your machine — no API cost, no data leaving it. Only the final generation step is a remote call.

See [PROJECT.md](PROJECT.md) for design decisions and trade-offs.

## Setup

**1. Virtualenv and dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

**2. Environment**

```bash
cp .env.template .env
```

Fill in `DATABASE_URL` (Neon → Connect → psycopg) and `GROQ_API_KEY` ([console.groq.com/keys](https://console.groq.com/keys)).

**3. Database**

Run [schema.sql](schema.sql) against your Neon database — it enables pgvector and creates `resume_chunks`.

**4. Ingest the resume**

```bash
python main.py
```

Extracts the PDF, chunks it, embeds each chunk, writes to Postgres. First run downloads bge-m3 (~2GB) into the HuggingFace cache.

**5. Ask a question**

```bash
python embed.py
```

## Project layout

```
HashAi/
├── main.py          # ingestion: PDF → chunks → embeddings → Postgres
├── embed.py         # retrieval + generation
├── db.py            # psycopg wrapper (fetchone/fetchall/insert/update/delete)
├── schema.sql       # database schema
├── media/           # source resume PDF
├── .env.template    # required environment variables
└── requirement.txt
```

## Notes

- **`vector(1024)` is tied to bge-m3.** Switching embedding models changes the dimension and invalidates every stored row — the table has to be recreated.
- **Re-running `main.py` clears the table first**, so edits to the resume just work. It also means ingesting a second document would wipe the first. See *Known gaps* in [PROJECT.md](PROJECT.md).
