
from src.retrieval.evaluate import EVALUATION_CASES
from src.retrieval.search import search_documents
from src.retrieval.semantic_search import semantic_search
from src.retrieval.hybrid_search import hybrid_search


METHODS = {
    "TF-IDF": search_documents,
    "Semantic": semantic_search,
    "Hybrid": hybrid_search,
}


def evaluate_method(search_function):
    """Run retrieval once per query and calculate evaluation metrics."""
    top1_correct = 0
    recall_at_3 = 0
    reciprocal_ranks = []

    for case in EVALUATION_CASES:
        results = search_function(case["query"], top_k=3)
        expected_source = case["expected_source"]

        matching_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if result.get("source") == expected_source
        ]

        rank = matching_ranks[0] if matching_ranks else None

        if rank == 1:
            top1_correct += 1

        if rank is not None:
            recall_at_3 += 1

        reciprocal_ranks.append(1 / rank if rank else 0)

    total = len(EVALUATION_CASES)

    if total == 0:
        raise ValueError("EVALUATION_CASES must contain at least one case.")

    return {
        "top1_accuracy": top1_correct / total,
        "recall_at_3": recall_at_3 / total,
        "mrr": sum(reciprocal_ranks) / total,
    }


def main():
    for method_name, search_function in METHODS.items():
        metrics = evaluate_method(search_function)

        print(f"\n--- {method_name} ---")
        print(f"Top-1 Accuracy: {metrics['top1_accuracy']:.1%}")
        print(f"Recall@3: {metrics['recall_at_3']:.1%}")
        print(f"MRR: {metrics['mrr']:.4f}")


if __name__ == "__main__":
    main()
