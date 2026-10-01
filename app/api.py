from fastapi import FastAPI

from app.embedder import Embedder
from app.llm import Llm
from app.logger import get_logger
from app.models import Ask

log = get_logger(__name__)

app = FastAPI()
embedder = Embedder()
ai = Llm()


@app.post("/ask")
def ask(body: Ask):
    log.info("question: %s", body.question)

    rows = embedder.search(body.question)
    if not rows:
        log.warning("no chunks matched")
        return {"answer": "I dont have that information."}

    context = embedder.build_context(rows)
    ans = ai.generate(context, body.question)
    return {"answer": ans}
