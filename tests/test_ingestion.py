from app.ingestion.load_data import load_documents
from app.ingestion.splitter import split_documents
from app.ingestion.embedding import embed_documents
from app.vectorstore.vector_store import VectorStore


def main():
    # 1. Load
    documents = load_documents("data/raw")
    print(f"Documents loaded: {len(documents)}")

    # 2. Split
    chunks = split_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    # 3. Embeddings
    vectors = embed_documents(chunks)
    print(f"Embeddings generated: {len(vectors)}")

    # 4. Store
    store = VectorStore()

    for chunk, vector in zip(chunks, vectors):
        store.add_chunk(
            content=chunk.page_content,
            embedding=vector,
            metadata=chunk.metadata,
        )

    print("✅ Documents inserted into vector store")


if __name__ == "__main__":
    main()