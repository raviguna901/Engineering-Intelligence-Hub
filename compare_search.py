
from src.retrieval.search import search_documents
from src.retrieval.semantic_search import semantic_search

queries = [
    "Why can't Python find an imported module?",
    "What does HTTP 404 mean?",
    "How do I troubleshoot a failed data pipeline?",
    "How can I evaluate a machine learning model?",
    "How do I fix SQL query errors?",
]


def unique_sources(results):
    seen = set()
    unique = []

    for result in results:
        source = result["source"]
        if source not in seen:
            seen.add(source)
            unique.append(result)

    return unique


for query in queries:
    print("\n" + "=" * 75)
    print(f"QUERY: {query}")

    for method_name, search_function in [
        ("TF-IDF", search_documents),
        ("SEMANTIC SEARCH", semantic_search),
    ]:
        results = unique_sources(search_function(query, top_k=10))
        print(f"\n{method_name}")

        for result in results[:3]:
            print(f"  {result['source']} | Score: {result['score']:.4f}")
