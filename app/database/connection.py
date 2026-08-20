import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Create and return a PostgreSQL connection."""

    if not DATABASE_URL:
        raise ValueError(
            "Missing DATABASE_URL. "
            "Please add it to your .env file."
        )

    return psycopg.connect(DATABASE_URL)