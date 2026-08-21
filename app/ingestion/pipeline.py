from app.ingestion.load_data import load_documents
from app.ingestion.splitter import split_documents
from app.ingestion.embedding import embed_documents
from app.vectorstore.vector_store import VectorStore


def ingest_documents():
    """Load, split, embed, and store documents."""

    # 1. Load documents
    documents = load_documents()

    # 2. Split documents into chunks
    chunks = split_documents(documents)

    # 3. Generate embeddings
    vectors = embed_documents(chunks)

    # 4. Store chunks + embeddings in PostgreSQL
    vector_store = VectorStore()

    vector_store.clear()

    for chunk, vector in zip(chunks, vectors):
        vector_store.add_chunk(
        content=chunk.page_content,
        metadata=chunk.metadata,
        embedding=vector,
    )

    return len(chunks)

