
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.retrieval.search import search_documents

app = FastAPI(
    title="Engineering Intelligence Hub API",
    description="Search engineering troubleshooting documents.",
    version="1.0.0",
)


class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Question to search for",
    )
    top_k: int = Field(default=3, ge=1, le=10)


@app.get("/")
def home():
    return {
        "message": "Engineering Intelligence Hub API is running"
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

    try:
        results = search_documents(
            request.query,
            top_k=request.top_k,
        )
        return {
            "query": request.query,
            "count": len(results),
            "results": results,
        }

    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
