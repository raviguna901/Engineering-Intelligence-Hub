
import pytest

from src.retrieval.search import search_documents


def test_python_question_returns_python_document():
    results = search_documents(
        "Why can't Python find an imported module?"
    )

    assert results[0]["source"] == "python_troubleshooting.md"
    assert results[0]["score"] > 0


def test_http_404_question_returns_api_document():
    results = search_documents("What does HTTP 404 mean?")

    assert results[0]["source"] == "api_troubleshooting.txt"
    assert results[0]["score"] > 0


def test_empty_query_is_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        search_documents("   ")


def test_invalid_top_k_is_rejected():
    with pytest.raises(ValueError, match="greater than zero"):
        search_documents("Python error", top_k=0)
