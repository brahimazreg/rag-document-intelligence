from app.config import settings
from app.ingestion.load_data import load_documents
from app.ingestion.splitter import split_into_chunks
from app.ingestion.embedding import embed_documents


def main():
    documents = load_documents(settings.DATA_FILE_PATH)
    print(f"Documents loaded: {len(documents)}")

    chunks = split_into_chunks(documents)
    print(f"Chunks created: {len(chunks)}")

    vectors = embed_documents(chunks)
    print(f"Vectors created: {len(vectors)}")
    print(f"Vector dimensions: {len(vectors[0])}")

    print("\nChecking chunks and embeddings:\n")

    for i in range(min(5, len(chunks))):
        print("=" * 60)
        print(f"Chunk {i}")
        print("Source:", chunks[i].metadata.get("source"))
        print("Chunk length:", len(chunks[i].page_content))
        print("Embedding dimensions:", len(vectors[i]))
        print("Text:", chunks[i].page_content[:150])


if __name__ == "__main__":
    main()