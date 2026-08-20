from app.ingestion.load_data import load_documents
from app.config.settings import DATA_FILE_PATH
from dotenv import load_dotenv

load_dotenv()

def main():
    documents = load_documents(DATA_FILE_PATH)

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print("=" * 60)
        print("Source:", document.metadata.get("source"))
        print("Content:", document.page_content[:200])


if __name__=="__main__":
    main()