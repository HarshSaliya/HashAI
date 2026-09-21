# HashAi

A personal RAG chatbot embedded in my portfolio website. Instead of a static "About Me" page, HR and recruiters can ask questions directly — "What's his experience with PostgreSQL?", "Has he worked with AWS Lambda?" — and get answers grounded in my actual resume/portfolio content.

## Goal

Replace the passive portfolio page with something interactive: a chat widget that answers questions about me, backed by retrieval over my real background instead of a hardcoded FAQ.

## Stack

- **FastAPI** — HTTP API serving the chat endpoint, consumed by the portfolio frontend
- **LangChain** — text splitting, embedding pipeline, and retrieval/generation orchestration
- **PGVector** — vector store for chunked portfolio/resume content, backed by Postgres

## How it works (planned flow)

1. **Ingest** — portfolio/resume content (`media/`) is loaded and split into chunks (`langchain_text_splitters`)
2. **Embed** — chunks are embedded and stored in PGVector
3. **Serve** — FastAPI exposes an endpoint that takes a user question
4. **Retrieve** — the question is embedded and matched against stored chunks via similarity search
5. **Generate** — matched chunks + question are passed to an LLM to produce a grounded answer
6. **Respond** — answer is returned to the portfolio site's chat widget
