from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
def ask():
    # return("First Fastapi")
    return("First Fastapi.....", {"greet": "welcome"})
    