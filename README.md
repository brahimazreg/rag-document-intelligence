# RAG Document Intelligence

A production-oriented **Retrieval-Augmented Generation (RAG) backend** that allows users to ask questions about indexed documents.

The application combines **document processing, embeddings, PostgreSQL + pgvector, semantic vector search, FastAPI, LangChain, and Google Gemini** to retrieve relevant document chunks and generate answers grounded in the indexed documents.

---

## Project Links

* **GitHub:** https://github.com/brahimazreg/rag-document-intelligence
* **Live API:** Add your Render URL after deployment
* **API Documentation:** Add your Render `/docs` URL after deployment

---

## Overview

Large Language Models (LLMs) do not automatically have access to an organization's private documents.

This project implements a complete RAG pipeline that:

1. Loads PDF and text documents.
2. Splits documents into smaller chunks.
3. Generates embeddings for each chunk.
4. Stores chunks and embeddings in PostgreSQL using pgvector.
5. Converts user questions into embeddings.
6. Performs vector similarity search.
7. Retrieves the most relevant document chunks.
8. Builds a context from the retrieved chunks.
9. Sends the context and question to Google Gemini.
10. Generates an answer based only on the retrieved context.

The goal is to reduce unsupported answers by grounding the LLM response in information retrieved from the indexed documents.

---

## Architecture

```text
                         DOCUMENT INGESTION
                                │
                                ▼
                       PDF / TXT Documents
                                │
                                ▼
                         Document Loading
                                │
                                ▼
                            Chunking
                                │
                                ▼
                       Embedding Generation
                                │
                                ▼
                     PostgreSQL + pgvector
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
                         Query Embedding
                                │
                                ▼
                     PostgreSQL + pgvector
                                │
                                ▼
                    Relevant Document Chunks
                                │
                                ▼
                         Context Builder
                                │
                                ▼
                        Prompt Construction
                                │
                                ▼
                         Google Gemini
                                │
                                ▼
                         Generated Answer
```

---

## RAG Pipeline

The core retrieval and generation flow is:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Context Construction
      │
      ▼
LLM Prompt
      │
      ▼
Google Gemini
      │
      ▼
Generated Answer
```

### Example

```text
Question:
"What is Retrieval-Augmented Generation?"

        ↓

Query embedding

        ↓

pgvector similarity search

        ↓

Relevant document chunks

        ↓

Context construction

        ↓

Google Gemini

        ↓

Answer grounded in the retrieved documents
```

The retrieval layer has been tested successfully and returns relevant document chunks from PostgreSQL.

The complete RAG chain has also been tested successfully with Gemini.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### AI / LLM

* Google Gemini
* LangChain
* `langchain-google-genai`
* Embedding model

### Vector Storage

* PostgreSQL
* pgvector
* Psycopg

### Document Processing

* PDF documents
* TXT documents
* Document chunking
* Metadata extraction
* Embedding generation

### Development / Deployment

* `uv`
* Docker
* GitHub
* Render

---

## Project Structure

```text
rag-document-intelligence/
│
├── app/
│   ├── __init__.py
│   │
│   ├── api.py
│   ├── config.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── embedding.py
│   │   ├── load_data.py
│   │   ├── pipeline.py
│   │   └── splitter.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   └── chain.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retriever.py
│   │
│   └── vectorstore/
│       ├── __init__.py
│       └── vector_store.py
│
├── scripts/
│   ├── __init__.py
│   └── ingest.py
│
├── data/
│   └── raw/
│       ├── pdf/
│       └── txt/
│
├── .env
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

> `.env`, `.venv`, Python cache files, and other local/generated files should not be committed to GitHub.

---

## Main Components

### 1. Document Ingestion

The ingestion pipeline is responsible for loading, splitting, embedding, and storing documents.

The main flow is:

```text
Documents
    ↓
load_documents()
    ↓
split_documents()
    ↓
embed_documents()
    ↓
PostgreSQL + pgvector
```

The ingestion script can be executed with:

```powershell
uv run python -m scripts.ingest
```

A successful ingestion reports the number of processed chunks.

---

### 2. Embedding Model

The embedding model converts text into numerical vectors.

During document ingestion:

```python
embed_documents(chunks)
```

generates embeddings for document chunks.

During retrieval:

```python
embed_query(query)
```

generates an embedding for the user's question.

Conceptually:

```text
Document Chunk
      ↓
Embedding Model
      ↓
Document Vector


User Question
      ↓
Embedding Model
      ↓
Query Vector
```

The document and query vectors can then be compared using vector similarity.

---

### 3. VectorStore

The `VectorStore` class handles interaction with PostgreSQL and pgvector.

Its responsibilities include:

* Creating the vector database table.
* Storing document chunks.
* Storing document metadata.
* Storing embeddings.
* Performing vector similarity searches.

The database table currently used by the application is:

```text
document_chunks
```

with the following main fields:

```text
id
content
metadata
embedding
```

The embedding column stores the numerical representation of each document chunk.

---

### 4. Retriever

The `Retriever` coordinates query embedding and vector search.

Its flow is:

```text
Question
    ↓
embed_query()
    ↓
Query Vector
    ↓
VectorStore.search()
    ↓
Top-K Relevant Chunks
```

The Retriever is responsible for **finding relevant information**.

It does not generate the final answer.

---

### 5. RAGChain

`RAGChain` connects retrieval with the LLM.

Its responsibilities are:

1. Receive the user's question.
2. Retrieve relevant document chunks.
3. Build the context.
4. Construct the prompt.
5. Send the prompt to Google Gemini.
6. Return the generated answer.

The simplified flow is:

```text
Question
    ↓
Retriever
    ↓
Relevant Chunks
    ↓
Context
    ↓
Prompt
    ↓
Gemini
    ↓
Answer
```

The prompt explicitly instructs the model to use the provided context and to state that there is insufficient information when the answer cannot be found in the retrieved documents.

---

## FastAPI

FastAPI exposes the RAG functionality through an HTTP API.

### Available Endpoints

| Method | Endpoint    | Description                            |
| ------ | ----------- | -------------------------------------- |
| GET    | `/`         | Basic application information          |
| GET    | `/healthy`  | Health check                           |
| POST   | `/document` | Ask a question about indexed documents |

---

## API Usage

### Health Check

```http
GET /healthy
```

Example response:

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

Example response:

```json
{
  "answer": "Retrieval-Augmented Generation, commonly called RAG, combines information retrieval with text generation..."
}
```

---

## Swagger Documentation

FastAPI automatically provides interactive API documentation.

When running locally:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test the API without requiring a separate frontend.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/brahimazreg/rag-document-intelligence.git
cd rag-document-intelligence
```

### Create the Virtual Environment

Using `uv`:

```bash
uv sync
```

Or using standard Python:

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

Install dependencies if using the standard Python workflow:

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

Recommended `.gitignore` entries:

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

The application stores:

```text
document_chunks
│
├── id
├── content
├── metadata
└── embedding
```

Conceptually:

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector
      ↓
PostgreSQL + pgvector
```

During retrieval:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Relevant Document Chunks
```

The vector search uses pgvector's distance operator to rank chunks by similarity to the query embedding.

---

## Running Locally

### Start PostgreSQL

If PostgreSQL is running through Docker Compose, start the database with:

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker ps
```

### Ingest Documents

From the project root:

```bash
uv run python -m scripts.ingest
```

The ingestion pipeline loads the documents, creates chunks, generates embeddings, and stores them in PostgreSQL.

### Start FastAPI

```bash
uvicorn app.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Testing the RAG Pipeline

The retrieval layer can be tested directly:

```powershell
uv run python -c "from app.retrieval.retriever import Retriever; r=Retriever(); results=r.retrieve('What is this document about?'); print('RESULTS:', len(results)); [print(x) for x in results]"
```

The RAG generation chain can be tested with:

```powershell
uv run python -c "from app.rag.chain import RAGChain; chain=RAGChain(); print(chain.answer('What is Retrieval-Augmented Generation?'))"
```

A successful test retrieves relevant chunks and generates an answer using Gemini.

Example:

```text
Retrieval-Augmented Generation, commonly called RAG,
combines information retrieval with text generation.
Instead of relying only on information stored in an LLM's
parameters, a RAG system first retrieves relevant documents
or document chunks and then gives that context to a language model.
```

---

## Example RAG Behavior

### Question With Available Information

```text
Question:

What is Retrieval-Augmented Generation?
```

The Retriever searches the indexed documents and returns relevant chunks.

Those chunks are then provided to Gemini as context.

The model generates an answer based on that context.

---

### Question Without Available Information

For example:

```text
Question:

What is the refund policy?
```

If the indexed documents do not contain information about refunds, the system is instructed to return:

```json
{
  "answer": "I don't have enough information in the provided documents."
}
```

This behavior is intentional.

The goal is to reduce hallucinations by grounding the answer in retrieved document context.

---

## Retrieval vs Generation

A key characteristic of this architecture is the separation between **retrieval quality** and **generation quality**.

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
Wrong Chunks
    ↓
LLM
    ↓
Poor Answer
```

Even a powerful LLM cannot reliably answer a question if the required information was not retrieved.

Therefore, retrieval quality is a critical part of a RAG system.

---

## Design Principles

### Separation of Responsibilities

Each component has a specific responsibility:

```text
Document Loader
      ↓
Load documents

Splitter
      ↓
Create document chunks

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

Gemini
      ↓
Generate final answer

FastAPI
      ↓
Expose the RAG system through HTTP
```

This separation makes the system easier to test, maintain, and extend.

---

## Current Validation

The core pipeline has been manually validated end-to-end.

### Ingestion

Successfully processed document chunks and stored embeddings in PostgreSQL.

### Vector Retrieval

A test query successfully returned the top 5 relevant document chunks.

### RAG Generation

A test question successfully produced a Gemini-generated answer grounded in the retrieved document context.

Example test:

```text
Question:
What is Retrieval-Augmented Generation?

Result:
RAG combines information retrieval with text generation...
```

---

## Known Limitations

The current implementation is a **working production-oriented prototype**, rather than a fully production-hardened system.

Current limitations include:

* Re-running ingestion can create duplicate document chunks unless the ingestion strategy is reset/upsert-based.
* Source citations are not yet included in generated answers.
* Retrieval evaluation metrics are not yet implemented.
* Authentication is not currently implemented.
* Conversation history is not currently implemented.
* Observability and structured logging are limited.
* The deployment configuration still requires production hardening.

---

## Future Improvements

Potential next improvements include:

* Make ingestion idempotent using document IDs/hashes and upserts.
* Add source and page citations to generated answers.
* Add document upload through the API.
* Add metadata filtering.
* Improve chunking strategies.
* Add hybrid keyword + vector search.
* Add reranking.
* Add retrieval evaluation metrics.
* Add automated unit and integration tests.
* Add structured logging.
* Add monitoring and observability.
* Add authentication and authorization.
* Add conversation history.
* Add a React or Streamlit frontend.
* Add CI/CD with GitHub Actions.
* Improve production database configuration.

---

## Deployment

The FastAPI application can be deployed as a web service on Render.

Production start command:

```bash
uvicorn app.api:app --host 0.0.0.0 --port $PORT
```

Required environment variables should be configured through the Render dashboard rather than committed to the repository.

After deployment:

```text
https://<your-render-service>.onrender.com
```

Swagger:

```text
https://<your-render-service>.onrender.com/docs
```

---

## Project Status

**Status: Working prototype / production-oriented RAG backend**

The current implementation demonstrates:

* Document ingestion
* PDF/TXT processing
* Text chunking
* Embedding generation
* PostgreSQL + pgvector
* Vector storage
* Semantic retrieval
* Context construction
* Gemini LLM generation
* RAG orchestration
* FastAPI API
* Health checks
* Interactive Swagger documentation

The core pipeline has been tested successfully from document ingestion through retrieval and final LLM generation.

---

## Author

**AZREG BRAHIM**

---

## License

MIT License

