from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.chain import RAGChain
from app.vectorstore.vector_store import VectorStore

app = FastAPI()

vector_store = VectorStore()
vector_store.create_tables()

rag = RAGChain()


class QuestionRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "RAG document project"}


@app.get("/healthy")
def health():
    return {"status": "ok"}



@app.post("/query")
def query(request: QuestionRequest):
    response = rag.answer(request.query, limit=3)
    return {"answer": response}