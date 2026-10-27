from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded

from app.config import RATE_LIMIT
from app.embedder import Embedder
from app.llm import Llm
from app.logger import get_logger
from app.models import Ask
from app.rate_limiting import limiter, rate_limit_handler

log = get_logger(__name__)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

embedder = Embedder()
ai = Llm()


@app.post("/ask")
@limiter.limit(RATE_LIMIT)
def ask(request: Request, body: Ask):
    log.info("question: %s", body.question)

    rows = embedder.search(body.question)
    if not rows:
        log.warning("no chunks matched")
        return {"answer": "I dont have that information."}

    context = embedder.build_context(rows)
    ans = ai.generate(context, body.question)
    return {"answer": ans}
