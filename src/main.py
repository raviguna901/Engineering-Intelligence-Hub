
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.retrieval.search import search_documents
from src.retrieval.semantic_search import semantic_search
from src.retrieval.hybrid_search import hybrid_search

app = FastAPI(
    title="Engineering Intelligence Hub API",
    description="Search engineering troubleshooting documents using TF-IDF, semantic, or hybrid retrieval.",
    version="1.1.0",
)


class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Question to search for",
    )
    top_k: int = Field(default=3, ge=1, le=10)
    search_mode: Literal["tfidf", "semantic", "hybrid"] = Field(
        default="hybrid",
        description="Retrieval method to use",
    )


@app.get("/")
def home():
    return {
        "message": "Engineering Intelligence Hub API is running",
        "version": app.version,
        "search_modes": ["tfidf", "semantic", "hybrid"],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/search")
def search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    search_functions = {
        "tfidf": search_documents,
        "semantic": semantic_search,
        "hybrid": hybrid_search,
    }

    try:
        results = search_functions[request.search_mode](
            request.query.strip(),
            top_k=request.top_k,
        )

        return {
            "query": request.query,
            "search_mode": request.search_mode,
            "count": len(results),
            "results": results,
        }

    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
