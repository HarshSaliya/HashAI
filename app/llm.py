from groq import Groq

from app.config import GROQ_API

GROQ_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "Answer only from the context given. "
    "If the answer is not in it, say you don't know."
)


class Llm:
    def __init__(self, model=GROQ_MODEL):
        self.client = Groq(api_key=GROQ_API)
        self.model = model

    def generate(self, context, question):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
        )

        answer = response.choices[0].message.content
        return answer


if __name__ == "__main__":
    ai = Llm()
    print(ai.generate(
        context="Databases: PostgreSQL, MongoDB, SQLite3, Qdrant, pgvector",
        question="How many databases does he know?",
    ))
