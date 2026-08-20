# RAG Document Intelligence

A production-oriented **Retrieval-Augmented Generation (RAG)** API that allows users to ask questions about indexed documents.

The application combines **document embeddings**, **PostgreSQL + pgvector**, **vector similarity search**, **FastAPI**, and **Google Gemini** to retrieve relevant document chunks and generate grounded answers.

---

## Project Links

- **GitHub:** https://github.com/brahimazreg/rag-document-intelligence
- **Live API:** https://your-service.onrender.com
- **API Documentation:** https://your-service.onrender.com/docs

## Overview

Large Language Models (LLMs) do not automatically have access to an organization's private documents.

This project implements a RAG pipeline that:

1. Loads documents.
2. Splits documents into chunks.
3. Generates embeddings for the chunks.
4. Stores the chunks and embeddings in PostgreSQL using pgvector.
5. Converts a user's question into an embedding.
6. Retrieves the most relevant document chunks.
7. Adds the retrieved chunks to the LLM prompt.
8. Generates an answer using the retrieved context.

The system is designed to reduce unsupported answers by instructing the LLM to answer only from the retrieved documents.

---

## Architecture

```text
                    DOCUMENT INGESTION
                           │
                           ▼
                    Documents (PDF/TXT)
                           │
                           ▼
                       Chunking
                           │
                           ▼
                  Embedding Model
                  embed_documents()
                           │
                           ▼
              PostgreSQL + pgvector
                           │
                           │
                           │
                           ▼
                    USER QUESTION
                           │
                           ▼
                        FastAPI
                           │
                           ▼
                       RAGChain
                           │
                           ▼
                       Retriever
                           │
                           ▼
                    embed_query()
                           │
                           ▼
              PostgreSQL + pgvector
                           │
                           ▼
                Relevant document chunks
                           │
                           ▼
                     Context
                           │
                           ▼
                   Prompt construction
                           │
                           ▼
                     Google Gemini
                           │
                           ▼
                    Generated Answer
```

---

## RAG Pipeline

The core retrieval flow is:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
      ↓
Context Construction
      ↓
LLM Prompt
      ↓
Generated Answer
```

For example:

```text
Question:
"What is Retrieval-Augmented Generation?"

        ↓

Embedding Model

        ↓

Query Vector

        ↓

pgvector similarity search

        ↓

Relevant document chunks

        ↓

Gemini

        ↓

Answer based on retrieved context
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### AI / LLM

* Google Gemini
* LangChain integration
* Embedding model

### Vector Storage

* PostgreSQL
* pgvector

### Document Processing

* PDF documents
* TXT documents
* Document chunking
* Embedding generation

### Deployment

* Render
* GitHub

---

## Project Structure

```text
rag-document-intelligence/
│
├── app/
│   ├── __init__.py
│   │
│   ├── api.py
│   │
│   └── rag/
│       ├── __init__.py
│       ├── chain.py
│       ├── retriever.py
│       ├── vector_store.py
│       ├── embedding.py
│       └── ...
│
├── data/
│   └── raw/
│       ├── pdf/
│       └── txt/
│
├── README.md
├── requirements.txt
├── .gitignore
└── ...
```

---

## Main Components

### 1. Embedding Model

The embedding model converts text into numerical vectors.

During document ingestion:

```python
embed_documents(chunks)
```

is used to create embeddings for document chunks.

During retrieval:

```python
embed_query(query)
```

is used to create an embedding for the user's question.

Conceptually:

```text
Document chunk
      ↓
Embedding
      ↓
Vector

User question
      ↓
Embedding
      ↓
Query vector
```

---

### 2. VectorStore

The `VectorStore` class handles interaction with PostgreSQL and pgvector.

Its responsibilities include:

* Creating database tables.
* Storing document chunks.
* Storing embeddings.
* Searching for similar vectors.

The search operation uses pgvector's vector distance operators to find the closest document chunks to a query embedding.

Conceptually:

```text
Query Vector
     │
     ├───────────────┐
     │               │
     ▼               ▼
Document Vector  Document Vector
     │               │
     └──── similarity ────┘
             │
             ▼
       Ranked results
```

---

### 3. Retriever

The `Retriever` coordinates query embedding and vector search.

Its main responsibility is:

```text
Question
   ↓
embed_query()
   ↓
query embedding
   ↓
VectorStore.search()
   ↓
relevant chunks
```

The Retriever does not generate the final answer.

It only finds the information that can be used to answer the question.

---

### 4. RAGChain

`RAGChain` connects the Retriever with the LLM.

Its responsibilities are:

1. Retrieve relevant document chunks.
2. Build the context.
3. Construct the prompt.
4. Send the prompt to Gemini.
5. Return the generated answer.

The simplified flow is:

```text
Question
   ↓
Retriever
   ↓
Relevant chunks
   ↓
Context
   ↓
Prompt
   ↓
Gemini
   ↓
Answer
```

---

### 5. FastAPI

FastAPI exposes the RAG functionality through an HTTP API.

Available endpoints:

| Method | Endpoint    | Description                                |
| ------ | ----------- | ------------------------------------------ |
| GET    | `/`         | Basic application information              |
| GET    | `/healthy`  | Health check                               |
| POST   | `/document` | Ask a question about the indexed documents |

---

## API Usage

### Health Check

```http
GET /healthy
```

Response:

```json
{
  "status": "ok"
}
```

---

### Ask a Question

```http
POST /document
```

Request:

```json
{
  "query": "What is Retrieval-Augmented Generation?"
}
```

Response:

```json
{
  "answer": "Based on the provided context, Retrieval-Augmented Generation (commonly called RAG) combines information retrieval with text generation..."
}
```

---

## Swagger Documentation

FastAPI automatically provides interactive API documentation.

When running locally, open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test the API without needing a separate frontend.

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd rag-document-intelligence
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
LLM_MODEL_NAME=your_model_name
DATABASE_URL=your_postgresql_connection_string
```

Do **not** commit `.env` to GitHub.

The `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## Database

This project uses PostgreSQL with the **pgvector** extension.

pgvector adds vector storage and similarity search capabilities to PostgreSQL.

The database stores information such as:

```text
id
content
metadata
embedding
```

The embedding column contains the numerical representation of each document chunk.

Example:

```text
Document chunk
      ↓
Embedding model
      ↓
[0.12, -0.45, 0.78, ...]
      ↓
PostgreSQL + pgvector
```

During retrieval, the query embedding is compared against the stored document embeddings.

---

## Running Locally

Start the FastAPI server:

```bash
uvicorn app.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Example RAG Behavior

### Question with available information

If the indexed documents contain information about RAG:

```text
Question:
What is Retrieval-Augmented Generation?
```

The Retriever finds relevant RAG documents and provides them to the LLM.

The LLM generates an answer using that context.

---

### Question without available information

If the indexed documents do not contain information about refunds:

```text
Question:
What is the refund policy?
```

The system may return:

```json
{
  "answer": "I don't have enough information in the provided documents."
}
```

This behavior is intentional.

The prompt instructs the LLM not to invent an answer when the required information cannot be found in the retrieved context.

---

## Design Principles

### Separation of Responsibilities

Each component has a specific responsibility:

```text
Embedding Model
    ↓
Text → Vector

VectorStore
    ↓
Store and search vectors

Retriever
    ↓
Find relevant document chunks

RAGChain
    ↓
Build context and orchestrate retrieval + generation

LLM
    ↓
Generate the final answer

FastAPI
    ↓
Expose the system through an HTTP API
```

This separation makes the system easier to test, maintain, and extend.

---

## Retrieval vs Generation

An important characteristic of this architecture is the separation between **retrieval quality** and **answer quality**.

Retrieval asks:

> Did we find the right documents?

Generation asks:

> Did the LLM produce a good answer using those documents?

For example:

```text
Question
   ↓
Retriever
   ↓
Wrong chunks
   ↓
LLM
   ↓
Poor answer
```

Even a powerful LLM cannot reliably answer a question using context that does not contain the required information.

Therefore, retrieval quality is a critical part of a RAG system.

---

## Future Improvements

Potential improvements include:

* Add a Streamlit or React frontend.
* Add document upload through the API.
* Add authentication and authorization.
* Add metadata filtering.
* Improve chunking strategies.
* Add hybrid keyword + vector search.
* Add reranking.
* Add retrieval evaluation metrics.
* Add automated tests.
* Add structured logging.
* Add monitoring and observability.
* Add conversation history.
* Add citation/source references in responses.
* Improve production database configuration.
* Add CI/CD with GitHub Actions.

---

## Deployment

The FastAPI application can be deployed as a web service on Render.

Production start command:

```bash
uvicorn app.api:app --host 0.0.0.0 --port $PORT
```

Required environment variables should be configured in the Render dashboard rather than committed to the repository.

After deployment, the FastAPI Swagger documentation can be accessed through:

```text
https://<your-render-service>.onrender.com/docs
```

---

## Project Status

**Status: Working prototype / production-oriented RAG backend**

The current implementation demonstrates:

* Document ingestion
* Text chunking
* Embedding generation
* Vector storage
* PostgreSQL + pgvector
* Semantic retrieval
* Context construction
* Gemini LLM generation
* FastAPI API
* Health checks
* Interactive Swagger documentation

---

## AUTHOR

AZREG BRAHIM

```text
MIT License
```


