from app.database.connection import get_connection
from psycopg.types.json import Json


class VectorStore:

    def create_tables(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE EXTENSION IF NOT EXISTS vector;

                    CREATE TABLE IF NOT EXISTS document_chunks (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        metadata JSONB,
                        embedding vector(3072)
                    );
                """)

    def clear(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "TRUNCATE TABLE document_chunks RESTART IDENTITY;"
                )

    def add_chunk(self, content, metadata, embedding):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO document_chunks
                        (content, metadata, embedding)
                    VALUES (%s, %s, %s::vector)
                    """,
                    (
                        content,
                        Json(metadata),
                        str(embedding),
                    ),
                )

    def search(self, query_embedding, limit=5):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        content,
                        metadata,
                        embedding <=> %s::vector AS distance
                    FROM document_chunks
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        str(query_embedding),
                        str(query_embedding),
                        limit,
                    ),
                )

                results = cur.fetchall()

        return results