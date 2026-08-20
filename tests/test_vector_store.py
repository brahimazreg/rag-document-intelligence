from app.vectorstore.vector_store import VectorStore
from app.ingestion.embedding import embedding_model


def main():
    store = VectorStore()

    query = "What is Retrieval-Augmented Generation?"

    query_embedding = embedding_model.embed_query(query)

    print(f"✅ Query embedding: {len(query_embedding)} dimensions")

    results = store.search(
        query_embedding=query_embedding,
        limit=5,
    )

    print(f"✅ Results found: {len(results)}")

    for result in results:
        chunk_id, content, metadata, distance = result

        print("\n--- Result ---")
        print(f"ID: {chunk_id}")
        print(f"Distance: {distance:.4f}")
        print(f"Metadata: {metadata}")
        print(f"Content: {content}")


if __name__ == "__main__":
    main()