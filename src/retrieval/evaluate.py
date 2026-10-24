
from src.retrieval.search import search_documents


EVALUATION_CASES = [
    {
        "query": "What does HTTP 404 mean?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "Why can't Python find an imported module?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How do I fix a database connection error?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How do I activate a virtual environment?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "What does HTTP 500 indicate?",
        "expected_source": "api_troubleshooting.txt",
    },
]


def evaluate_retrieval():
    top1_correct = 0
    recall_at_3_hits = 0
    reciprocal_ranks = []

    for case in EVALUATION_CASES:
        results = search_documents(case["query"], top_k=3)
        expected_source = case["expected_source"]

        # Find the rank of the first expected document.
        matching_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if result["source"] == expected_source
        ]

        first_rank = matching_ranks[0] if matching_ranks else None

        # Top-1 accuracy
        if first_rank == 1:
            top1_correct += 1

        # Recall@3: expected source appears in the top three.
        if first_rank is not None and first_rank <= 3:
            recall_at_3_hits += 1

        # Reciprocal rank: 1/rank, or 0 if not retrieved.
        reciprocal_rank = 1 / first_rank if first_rank else 0
        reciprocal_ranks.append(reciprocal_rank)

        status = "PASS" if first_rank is not None else "FAIL"
        print(f"[{status}] {case['query']}")
        print(f"  Expected: {expected_source}")
        print(f"  Rank: {first_rank if first_rank else 'Not found'}")

    total = len(EVALUATION_CASES)

    if total == 0:
        print("No evaluation cases available.")
        return

    top1_accuracy = top1_correct / total
    recall_at_3 = recall_at_3_hits / total
    mrr = sum(reciprocal_ranks) / total

    print("\n--- Retrieval Evaluation Summary ---")
    print(f"Evaluation queries: {total}")
    print(f"Top-1 Accuracy: {top1_accuracy:.1%}")
    print(f"Recall@3: {recall_at_3:.1%}")
    print(f"Mean Reciprocal Rank (MRR): {mrr:.4f}")


if __name__ == "__main__":
    evaluate_retrieval()
