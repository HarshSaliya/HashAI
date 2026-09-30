from app.models import Ask
from app.embedder import Embedder
from app.llm import Llm

from fastapi import FastAPI

app = FastAPI()
embedder = Embedder()
ai = Llm()

@app.post("/ask")
def ask(body: Ask):
    rows = embedder.search(body.question)
    if not rows:
        return {"answer": "I dont have have that information."}
    context = embedder.build_context(rows)
    ans = ai.generate(context, body.question)
    return {"answer": ans}
