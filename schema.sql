CREATE EXTENSION IF NOT EXISTS vector;

-- local: bge-m3, 1024 dimensions
CREATE TABLE IF NOT EXISTS resume_chunks (
    id         bigserial PRIMARY KEY,
    content    text NOT NULL,
    embedding  vector(1024) NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- deploy: all-MiniLM-L6-v2, 384 dimensions, fits in 512MB RAM
CREATE TABLE IF NOT EXISTS resume_chunks_mini (
    id         bigserial PRIMARY KEY,
    content    text NOT NULL,
    embedding  vector(384) NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);
