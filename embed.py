from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
import os
import psycopg
# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("BAAI/bge-m3")

# The sentences to encode
sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]

# 2. Calculate embeddings by calling model.encode()
embeddings = model.encode(sentences)
print(embeddings.shape)


with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
    register_vector(conn)

    conn.execute("DELETE FROM resume_chunks")

    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO resume_chunks (content, embedding) VALUES (%s, %s)",
            list(zip(chunks, data)),
        )

    count = conn.execute("SELECT count(*) FROM resume_chunks").fetchone()[0]

print("SAVED ::: rows in table =", count)