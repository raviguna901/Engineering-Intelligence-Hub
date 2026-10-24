
from src.retrieval.evaluate import evaluate_retrieval
from src.retrieval.search import search_documents
from src.retrieval.semantic_search import semantic_search
from src.retrieval.hybrid_search import hybrid_search


METHODS = {
    "TF-IDF": search_documents,
    "Semantic": semantic_search,
    "Hybrid": hybrid_search,
}


def main():
    for method_name, search_function in METHODS.items():
        print(f"\n--- {method_name} ---")
        evaluate_retrieval(search_function, top_k=3)


if __name__ == "__main__":
    main()
