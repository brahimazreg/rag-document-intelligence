from app.ingestion.pipeline import ingest_documents

if __name__ == "__main__":
    count = ingest_documents()
    print(f"Successfully ingested {count} chunks.")