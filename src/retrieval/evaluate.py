
EVALUATION_CASES = [
    # HTTP and API troubleshooting
    {
        "query": "What does HTTP 404 mean?",
        "relevant_sources": ["api_troubleshooting.txt", "http_status_codes.md"],
    },
    {
        "query": "What does HTTP 500 indicate?",
        "relevant_sources": ["api_troubleshooting.txt", "http_status_codes.md"],
    },
    {
        "query": "Why does an API return a not found error?",
        "relevant_sources": ["api_troubleshooting.txt", "http_status_codes.md"],
    },
    {
        "query": "How can I troubleshoot an internal server error?",
        "relevant_sources": ["api_troubleshooting.txt", "http_status_codes.md"],
    },
    {
        "query": "What should I check when an API request fails?",
        "relevant_sources": ["api_troubleshooting.txt"],
    },
    {
        "query": "How do I troubleshoot an HTTP error response?",
        "relevant_sources": ["api_troubleshooting.txt", "http_status_codes.md"],
    },

    # Python troubleshooting
    {
        "query": "Why can't Python find an imported module?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I fix a database connection error?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I activate a virtual environment?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How can I resolve a ModuleNotFoundError?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "Why does Python report that a package is missing?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I install a missing Python dependency?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "Why is my Python virtual environment not working?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How can I troubleshoot a Python import error?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "What should I check when Python cannot connect to a database?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I run Python with the correct environment?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I install packages using the active Python interpreter?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "Why does Python fail to import a module installed with pip?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "How do I troubleshoot Python environment configuration?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
    {
        "query": "What can cause Python database connection failures?",
        "relevant_sources": ["python_troubleshooting.md"],
    },
]


def evaluate_retrieval(search_function, top_k=3):
    """Evaluate retrieval using one or more relevant source files per query."""
    if not EVALUATION_CASES:
        raise ValueError("EVALUATION_CASES must contain at least one case.")

    top1_correct = 0
    recall_at_k_hits = 0
    reciprocal_ranks = []

    for case in EVALUATION_CASES:
        results = search_function(case["query"], top_k=top_k)
        relevant_sources = set(case["relevant_sources"])

        matching_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if result.get("source") in relevant_sources
        ]

        first_rank = matching_ranks[0] if matching_ranks else None

        if first_rank == 1:
            top1_correct += 1

        if first_rank is not None:
            recall_at_k_hits += 1

        reciprocal_ranks.append(
            1 / first_rank if first_rank is not None else 0
        )

        status = "PASS" if first_rank is not None else "FAIL"
        print(f"[{status}] {case['query']}")
        print(f"  Relevant sources: {sorted(relevant_sources)}")
        print(f"  First relevant rank: {first_rank or 'Not found'}")

    total = len(EVALUATION_CASES)

    metrics = {
        "top1_accuracy": top1_correct / total,
        "recall_at_k": recall_at_k_hits / total,
        "mrr": sum(reciprocal_ranks) / total,
    }

    print("\n--- Retrieval Evaluation Summary ---")
    print(f"Evaluation queries: {total}")
    print(f"Top-1 Accuracy: {metrics['top1_accuracy']:.1%}")
    print(f"Recall@{top_k}: {metrics['recall_at_k']:.1%}")
    print(f"MRR: {metrics['mrr']:.4f}")

    return metrics


if __name__ == "__main__":
    from src.retrieval.search import search_documents

    evaluate_retrieval(search_documents)
