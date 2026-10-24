
from src.retrieval.search import search_documents


EVALUATION_CASES = [
    # HTTP and API troubleshooting
    {
        "query": "What does HTTP 404 mean?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "What does HTTP 500 indicate?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "Why does an API return a not found error?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "How can I troubleshoot an internal server error?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "What should I check when an API request fails?",
        "expected_source": "api_troubleshooting.txt",
    },
    {
        "query": "How do I troubleshoot an HTTP error response?",
        "expected_source": "api_troubleshooting.txt",
    },

    # Python troubleshooting
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
        "query": "How can I resolve a ModuleNotFoundError?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "Why does Python report that a package is missing?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How do I install a missing Python dependency?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "Why is my Python virtual environment not working?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How can I troubleshoot a Python import error?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "What should I check when Python cannot connect to a database?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How do I run Python with the correct environment?",
        "expected_source": "python_troubleshooting.md",
    },
    {
    "query": "How do I install packages using the active Python interpreter?",
    "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "Why does Python fail to import a module installed with pip?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "How do I troubleshoot Python environment configuration?",
        "expected_source": "python_troubleshooting.md",
    },
    {
        "query": "What can cause Python database connection failures?",
        "expected_source": "python_troubleshooting.md",
    },
]


def evaluate_retrieval():
    top1_correct = 0
    recall_at_3_hits = 0
    reciprocal_ranks = []

    for case in EVALUATION_CASES:
        results = search_documents(case["query"], top_k=3)
        expected_source = case["expected_source"]

        matching_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if result.get("source") == expected_source
        ]

        first_rank = matching_ranks[0] if matching_ranks else None

        if first_rank == 1:
            top1_correct += 1

        if first_rank is not None and first_rank <= 3:
            recall_at_3_hits += 1

        reciprocal_ranks.append(
            1 / first_rank if first_rank is not None else 0
        )

        status = "PASS" if first_rank is not None else "FAIL"
        print(f"[{status}] {case['query']}")
        print(f"  Expected: {expected_source}")
        print(f"  Rank: {first_rank if first_rank else 'Not found'}")

    total = len(EVALUATION_CASES)

    if total == 0:
        print("No evaluation cases available.")
        return

    print("\n--- Retrieval Evaluation Summary ---")
    print(f"Evaluation queries: {total}")
    print(f"Top-1 Accuracy: {top1_correct / total:.1%}")
    print(f"Recall@3: {recall_at_3_hits / total:.1%}")
    print(f"Mean Reciprocal Rank (MRR): {sum(reciprocal_ranks) / total:.4f}")


if __name__ == "__main__":
    evaluate_retrieval()
