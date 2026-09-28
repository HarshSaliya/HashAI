from app.models import Ask
from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
def ask(body:Ask):
    return(body.question)