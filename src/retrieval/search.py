
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_FILE = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"


def load_chunks() -> list[dict]:
    """Load document chunks from the JSONL file."""
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}. "
            "Run the ingestion pipeline first."
        )

    chunks = []

    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))

    if not chunks:
        raise ValueError("No document chunks were found.")

    return chunks



def search_documents(query: str, top_k: int = 3) -> list[dict]:
    """Return the most relevant chunks for a search query."""
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    chunks = load_chunks()
    documents = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector, document_vectors
    ).flatten()

    ranked_indices = scores.argsort()[::-1]
    ranked_indices = [
        index for index in ranked_indices
        if scores[index] > 0
    ][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            **chunks[index],
            "score": float(scores[index]),
        })

    return results




if __name__ == "__main__":
    question = input("Enter your question: ")
    results = search_documents(question)

    for result in results:
        print(f"\nRelevance score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Text: {result['text']}")
