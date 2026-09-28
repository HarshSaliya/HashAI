-- HashAi database schema. Run once against the Neon database.
-- Requires pgvector (Neon ships it; just enable the extension).

CREATE EXTENSION IF NOT EXISTS vector;

-- vector(1024) matches BAAI/bge-m3 output. Changing the embedding model
-- changes this number, and every stored row becomes invalid.
CREATE TABLE IF NOT EXISTS resume_chunks (
    id         bigserial PRIMARY KEY,
    content    text NOT NULL,
    embedding  vector(1024) NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);
