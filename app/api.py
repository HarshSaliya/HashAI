import uuid

from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded

from app.config import RATE_LIMIT
from app.embedder import Embedder
from app.history import ChatHistory
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
history = ChatHistory()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
@limiter.limit(RATE_LIMIT)
def ask(request: Request, body: Ask):
    log.info("question: %s", body.question)

    session_id = body.session_id or str(uuid.uuid4())

    try:
        rows = embedder.search(body.question)
        if not rows:
            log.warning("no chunks matched")
            return {"answer": "I dont have that information.", "session_id": session_id}

        context = embedder.build_context(rows)
        past_turns = history.get_recent(session_id)
        ans = ai.generate(context, body.question, past_turns)
        history.save(session_id, body.question, ans)

        return {"answer": ans, "session_id": session_id}
    except Exception:
        log.exception("ask failed for session %s", session_id)
        return {"answer": "Something went wrong, please try again.", "session_id": session_id}
