# HashAi - notes

## Why

Portfolio About page is static. If someone wants to know whether I have used AWS Glue, they have to read the whole thing and hope. This turns the same content into something they can ask.

The main requirement is that it should not make things up. A bot that invents job history is worse than no bot.

## How it works

PDF text goes in, gets split into chunks, each chunk becomes a vector, vectors sit in Postgres. A question becomes a vector too, Postgres finds the closest chunks, and those chunks get sent to the LLM as context.

The LLM never answers from its own knowledge. It only rewrites what came back from the database.

## Steps

**Read** - pdfplumber pulls text from both pages. Two things need cleaning: `(cid:127)` which is the bullet character it cannot map, and stray `[]` from empty table output. If they stay, they end up inside the embeddings.

**Chunk** - RecursiveCharacterTextSplitter, 500 size, 50 overlap. Gives 6 chunks. It splits on `\n\n` first, then `\n`, then space, and only falls to the weaker ones when a piece is still too big.

**Embed** - bge-m3 through sentence-transformers, running locally. 1024 dimensions, which is why the column is `vector(1024)`. Same model has to embed both chunks and questions, otherwise the vectors are not comparable.

**Store** - Neon Postgres with pgvector. `DB` class wraps psycopg with fetchone / fetchall / insert / update / delete.

**Search** -

```sql
SELECT content, embedding <=> %s AS distance
FROM resume_chunks
ORDER BY embedding <=> %s
LIMIT 5
```

`<=>` is cosine distance, lower means closer in meaning. Postgres does the math.

**Answer** - chunks get joined into one string and sent to Groq with the question. System prompt tells it to stay inside that context.

## Choices

Used pgvector instead of Qdrant because there are only 6 vectors. One database is simpler than two. At millions of vectors Qdrant would win.

Wrote the SQL directly instead of using langchain-postgres. The queries are four lines and the operator is the whole point, so hiding it behind a wrapper did not help.

No reranker. It matters when you pull 50 candidates and squeeze to 5. With 6 chunks the LLM sees almost all of them anyway.

Embeddings local, LLM remote. Embeddings run on every ingest and every question, so keeping them local avoids cost. Generation needs a big model.

## Left to do

- Delete and insert run on separate connections, so if the insert fails after the delete commits, the table is left empty. Low risk since the script is run by hand and watched.
- `updated_at` column exists but nothing sets it.
- Re-embeds everything on every run even if nothing changed.
- No HNSW index. Fine at 6 rows, needed once it grows.
- No rate limiting on the API.
- No conversation memory. The UI shows chat history but each question is sent on its own, so follow-ups like "what about AWS?" have no reference to resolve.

## Version 2 - someday, not now

Right now this is single tenant. One resume, one table, ingested by hand.

The idea for v2 is auth and multi-tenancy: anyone signs up, uploads their own
resume, and gets a link to their own chatbot. Same bot, their content.

That turns a few shortcuts into real work:

- Auth and a users table.
- `user_id` on the chunks, and every search filtered by it. Right now the search has no `WHERE` at all because there is only one person's data in there.
- Upload as an API endpoint instead of a script.
- The ingest `DELETE` scoped per user. Today it clears the whole table.
- A per-user link, so each person gets their own chat page.

Not building this yet. v1 is for my own portfolio, and multi-tenancy would be building for users who do not exist.

## Status

Ingest, embedding, storage, search, generation, API, UI and tests all work. Left: deploy.
