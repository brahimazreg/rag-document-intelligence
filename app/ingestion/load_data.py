from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from app.config.settings import DATA_FILE_PATH
from dotenv import load_dotenv

load_dotenv()

def load_documents(path=DATA_FILE_PATH):
    """Load PDF, TXT, and DOCX files from a directory."""

    documents = []

    # Load PDF files
    pdf_loader = DirectoryLoader(
        path=path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    documents.extend(pdf_loader.load())

    # Load TXT files
    txt_loader = DirectoryLoader(
        path=path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    documents.extend(txt_loader.load())

    # Load DOCX files
    docx_loader = DirectoryLoader(
        path=path,
        glob="**/*.docx",
        loader_cls=Docx2txtLoader,
        show_progress=True,
    )
    documents.extend(docx_loader.load())

    return documents