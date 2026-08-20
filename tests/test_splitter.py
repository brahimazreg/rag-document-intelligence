from app.config.settings import DATA_FILE_PATH
from app.ingestion.load_data import load_documents
from app.ingestion.splitter import split_documents


def main():
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    chunks = split_documents(documents)

    print(f"✅ Chunks created: {len(chunks)}")

    print("=" * 60)

    for i, chunk in enumerate(chunks[:5]):
        print(f"\n--- Chunk {i + 1} ---")
        print("Source:", chunk.metadata.get("source"))
        print("Characters:", len(chunk.page_content))
        print("Content:")
        print(chunk.page_content[:500])


if __name__ == "__main__":
    main()