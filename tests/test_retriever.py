from app.retrieval.retriever import Retriever


def main():
    retriever = Retriever()

    results = retriever.retrieve(
        "What is Retrieval-Augmented Generation?",
        limit=3,
    )

    print(f"✅ Results found: {len(results)}")

    for result in results:
        print("\n--- Result ---")
        print(f"ID: {result[0]}")
        print(f"Content: {result[1]}")
        print(f"Metadata: {result[2]}")
        print(f"Distance: {result[3]:.4f}")


if __name__ == "__main__":
    main()