# HashAi

RAG chatbot for my portfolio site. Instead of a static About page, recruiters can just ask — "does he know AWS Lambda?", "what databases has he used?" — and get answers from my actual resume.

Answers come only from the resume. If something is not there, it says it doesn't know instead of making things up.

## Stack

- pdfplumber - read the PDF
- langchain-text-splitters - chunking
- sentence-transformers, BAAI/bge-m3 - embeddings, runs locally
- Neon Postgres + pgvector - vector storage
- Groq - answer generation
- FastAPI - the API

## Flow

```
resume.pdf -> chunks -> embeddings -> postgres

question -> embedding -> cosine search -> chunks + question -> llm -> answer
```

Embeddings run on my machine so there is no API cost for them. Only the final answer call goes out.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

Copy `.env.template` to `.env` and fill in:

- `DATABASE_URL` - Neon connection string, needs `?sslmode=require`
- `GROQ_API_KEY` - from console.groq.com/keys

Run `schema.sql` on the database once. It enables pgvector and creates the table.

## Usage

Load the resume into the database:

```bash
python -m scripts.resume_to_db media/Harsh_Saliya_Portfolio.pdf
```

Start the API:

```bash
uvicorn app.api:app --reload
```

Open `localhost:8000/docs` to try it.

## Layout

```
app/
  api.py        fastapi routes
  config.py     env vars
  db.py         psycopg wrapper
  embedder.py   model + vector search
  llm.py        groq
  models.py     request schemas
scripts/
  resume_to_db.py
media/          the resume pdf
schema.sql
```

## Notes

The `vector(1024)` column is tied to bge-m3. Switching the embedding model means a different dimension, so the table has to be recreated and everything re-embedded.

Re-running the ingest script clears the table first, so updating the resume just works. It also means a second document would wipe the first one - see PROJECT.md.
