
from __future__ import annotations

from src.retrieval.search import search_documents
from src.retrieval.semantic_search import semantic_search


def hybrid_search(
    query: str,
    top_k: int = 3,
    candidate_k: int = 10,
    rrf_k: int = 60,
) -> list[dict]:
    """Combine keyword and semantic rankings using Reciprocal Rank Fusion."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be greater than zero.")

    if (
        not isinstance(candidate_k, int)
        or isinstance(candidate_k, bool)
        or candidate_k < top_k
        or candidate_k > 100
    ):
        raise ValueError("candidate_k must be between top_k and 100.")

    if not isinstance(rrf_k, int) or isinstance(rrf_k, bool) or rrf_k < 1:
        raise ValueError("rrf_k must be a positive integer.")

    keyword_results = search_documents(query, top_k=candidate_k)
    semantic_results = semantic_search(query, top_k=min(candidate_k, 10))

    fused: dict[str, dict] = {}

    def add_ranked_results(results: list[dict]) -> None:
        for rank, result in enumerate(results, start=1):
            # A chunk's source, page, and text identify it without relying
            # on a potentially absent chunk ID.
            key = (
                str(result.get("source", "")),
                str(result.get("page", "")),
                str(result.get("text", "")),
            )

            if key not in fused:
                fused[key] = {
                    **result,
                    "rrf_score": 0.0,
                    "keyword_rank": None,
                    "semantic_rank": None,
                }

            fused[key]["rrf_score"] += 1.0 / (rrf_k + rank)

            if results is keyword_results:
                fused[key]["keyword_rank"] = rank
            else:
                fused[key]["semantic_rank"] = rank

    add_ranked_results(keyword_results)
    add_ranked_results(semantic_results)

    ranked = sorted(
        fused.values(),
        key=lambda result: result["rrf_score"],
        reverse=True,
    )

    return ranked[:top_k]
