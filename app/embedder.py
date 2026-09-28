from sentence_transformers import SentenceTransformer

from app.db import DB

EMBED_MODEL = "BAAI/bge-m3"

SEARCH_SQL = """SELECT content, embedding <=> %s AS distance
                FROM resume_chunks
                ORDER BY embedding <=> %s
                LIMIT %s"""


class Embedder:
    def __init__(self, model_name=EMBED_MODEL):
        self.model = SentenceTransformer(model_name)
        self.db = DB()

    def encode(self, text):
        """Turn a string into its vector."""
        return self.model.encode(text)

    def encode_many(self, texts):
        """Turn a list of strings into a list of vectors."""
        return self.model.encode(texts)

    def search(self, question, limit=5):
        """Return the chunks closest in meaning to the question."""
        qvec = self.encode(question)
        return self.db.fetchall(SEARCH_SQL, (qvec, qvec, limit))

    def build_context(self, rows):
        """Turn retrieved rows into the plain text block the LLM reads."""
        return "\n\n".join(row["content"] for row in rows)


if __name__ == "__main__":
    embedder = Embedder()
    for row in embedder.search("How many Database he know ?"):
        print(f"  [{row['distance']:.4f}] {row['content'][:60]}...")
