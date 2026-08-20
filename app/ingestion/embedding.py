from app.config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key =os.getenv("GEMINI_API_KEY")

embedding_model = GoogleGenerativeAIEmbeddings(
    model=settings.EMBEDDING_MODEL_NAME,
    google_api_key=gemini_api_key
)

def embed_documents(chunks):
    """Generate embeddings for document chunks."""
    #  vectors variable is not the vector database.
    # It's simply an in-memory Python list
    vectors = embedding_model.embed_documents(
        [chunk.page_content for chunk in chunks]
    )

    return vectors