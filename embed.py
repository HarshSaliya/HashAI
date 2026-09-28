from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector
from groq import Groq
from db import DB
import os

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("BAAI/bge-m3")

# # The sentences to encode
# sentences = [
#     "The weather is lovely today.",
#     "It's so sunny outside!",
#     "He drove to the stadium.",
# ]

# # 2. Calculate embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print(embeddings.shape)

db = DB()

result = db.fetchone(query="SELECT content from resume_chunks;")
print(result)

# question = "Does he know Django?"
question = "How many Database he know ?"

qvec = model.encode(question)

print("query return ans:::",qvec)

rows = db.fetchall(
    """SELECT content, embedding <=> %s AS distance
       FROM resume_chunks
       ORDER BY embedding <=> %s
       LIMIT 5""",
    (qvec, qvec),
)

print("************", rows)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "Answer only from the context given. If the answer is not in it, say you don't know."},
        {"role": "user", "content": f"Context:\n{rows}\n\nQuestion: {question}"},
    ],
)
# print([m.id for m in client.models.list().data])

answer = resp.choices[0].message.content

print("GROQ Ans :::",answer)