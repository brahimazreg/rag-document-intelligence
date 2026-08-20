from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.chain import RAGChain

app = FastAPI()

rag = RAGChain()


class QuestionRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "RAG document project"}


@app.get("/healthy")
def health():
    return {"status": "ok"}


@app.post("/document")
def get_info(request: QuestionRequest):
    response = rag.answer(request.query, limit=3)
    return {"answer": response}