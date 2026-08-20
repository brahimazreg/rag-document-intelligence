from app.rag.chain import RAGChain


def main():

    rag = RAGChain()

    questions = [
        "How can AI help teachers and students?",
        "What are the main applications of AI in education?",
        "What is supervised learning?",
        "What is Retrieval-Augmented Generation?",
        "What is prompt engineering?",
        "What is personalized learning?",
        "What is curriculum design?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print(f"QUESTION: {question}")
        print("=" * 70)

        answer = rag.answer(question)

        print("\nANSWER:")
        print(answer)


if __name__ == "__main__":
    main()