from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.retrieval.retriever import Retriever


class RAGChain:

    def __init__(self):
        self.retriever = Retriever()

        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
        )

    def answer(self, question, limit=5):
        """Retrieve relevant context and generate an answer."""

        results = self.retriever.retrieve(
            question,
            limit=limit,
        )

        

        context = "\n\n".join(
            result[1]
            for result in results
        )

        

        prompt = f"""
            You are a helpful AI assistant.

            Answer the question using only the provided context.

            Context:
            {context}

            Question:
            {question}

            If the answer cannot be found in the context, say:
            "I don't have enough information in the provided documents."

            Answer:
            """

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, list):
            return "".join(
                item.get("text", "")
                for item in content
            if isinstance(item, dict)
        )

        return content