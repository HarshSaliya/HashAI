from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

from db import DB

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

db = DB()

result = db.fetchone(query="SELECT content from resume_chunks;")
print(result)


qvec = model.encode("Does he know Django?")

print("query return ans:::",qvec)

rows = db.fetchall(
    """SELECT content, embedding <=> %s AS distance
       FROM resume_chunks
       ORDER BY embedding <=> %s
       LIMIT 3""",
    (qvec, qvec),
)

print("************", rows)