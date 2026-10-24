
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_FILE = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"

# Small sentence-embedding model suitable for a prototype.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    """Load processed document chunks from JSONL."""
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"{CHUNKS_FILE} not found. Run the ingestion pipeline first."
        )

    chunks = []
    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))

    if not chunks:
        raise ValueError("No document chunks found.")

    return chunks


def semantic_search(query: str, top_k: int = 3):
    """Retrieve document chunks by sentence-embedding similarity."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must not be empty.")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 10:
        raise ValueError("top_k must be an integer between 1 and 10.")

    chunks = load_chunks()
    texts = [chunk.get("text", "") for chunk in chunks]

    if any(not text.strip() for text in texts):
        raise ValueError("A document chunk contains empty text.")

    model = SentenceTransformer(MODEL_NAME)
    document_embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )[0]

    scores = document_embeddings @ query_embedding
    ranked_indices = np.argsort(scores)[::-1]

    results = []
    for index in ranked_indices:
        score = float(scores[index])
        if score <= 0:
            continue

        result = dict(chunks[index])
        result["score"] = score
        results.append(result)

        if len(results) >= top_k:
            break

    return results


if __name__ == "__main__":
    question = input("Enter your question: ").strip()
    for result in semantic_search(question):
        print(f"\nSimilarity score: {result['score']:.4f}")
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Text: {result.get('text', '')}")
