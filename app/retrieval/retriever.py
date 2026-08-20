from app.vectorstore.vector_store import VectorStore
from app.ingestion.embedding import embedding_model


class Retriever:

    def __init__(self):
        self.store = VectorStore()

    def retrieve(self, query, limit=5):
        """Retrieve the most relevant document chunks."""

        query_embedding = embedding_model.embed_query(query)

        results = self.store.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        return results