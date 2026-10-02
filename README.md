# HashAi

RAG chatbot for my portfolio site. Instead of a static About page, recruiters can just ask - "does he know AWS Lambda?", "what databases has he used?" - and get answers from my resume.

Answers come only from the resume. If something is not in it, the bot says it doesn't know instead of making things up.

## Stack

- pdfplumber - read the PDF
- langchain-text-splitters - chunking
- sentence-transformers - embeddings, runs locally
- Neon Postgres + pgvector - vector storage
- Groq - answer generation
- FastAPI - the API
- Streamlit - the chat UI

```
resume.pdf -> chunks -> embeddings -> postgres

question -> embedding -> cosine search -> chunks + question -> llm -> answer
```

See PROJECT.md for how it works and why it is built this way.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

Copy `.env.template` to `.env` and fill in `DATABASE_URL` (Neon, needs `?sslmode=require`) and `GROQ_API_KEY`.

Run `schema.sql` on the database once.

## Running it

Load the resume into the database:

```bash
python -m scripts.resume_to_db media/Harsh_Saliya_Portfolio.pdf
```

Start the API:

```bash
uvicorn app.api:app --reload
```

Start the UI in another terminal:

```bash
streamlit run ui.py
```

`localhost:8501` for the chat, `localhost:8000/docs` for the API.

## Two setups

The embedding model decides the vector column width, so the model and table go together.

| | model | dimensions | table |
|---|---|---|---|
| local | BAAI/bge-m3 | 1024 | `resume_chunks` |
| deploy | all-MiniLM-L6-v2 | 384 | `resume_chunks_mini` |

bge-m3 needs ~2GB RAM, MiniLM fits a 512MB free tier. Switch with env vars:

```bash
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2 TABLE_NAME=resume_chunks_mini uvicorn app.api:app
```

## Tests

```bash
pytest
```

## Layout

```
app/
  api.py        fastapi routes
  config.py     env vars
  db.py         psycopg wrapper
  embedder.py   model + vector search
  llm.py        groq
  logger.py     logging setup
  models.py     request schemas
scripts/
  resume_to_db.py
tests/
ui.py           streamlit chat
schema.sql
```
