
from src.retrieval.search import search_documents


def test_http_404_retrieves_api_document():
    results = search_documents("What does HTTP 404 mean?")

    assert len(results) > 0
    assert results[0]["source"] == "api_troubleshooting.txt"
    assert results[0]["score"] > 0


def test_python_import_error_retrieves_python_document():
    results = search_documents(
        "Why can't Python find an imported module?"
    )

    assert len(results) > 0
    assert results[0]["source"] == "python_troubleshooting.md"
    assert results[0]["score"] > 0


def test_database_error_retrieves_python_document():
    results = search_documents(
        "How do I fix a database connection error?"
    )

    assert len(results) > 0
    assert results[0]["source"] == "python_troubleshooting.md"


def test_unrelated_query_returns_no_results():
    results = search_documents("How do I bake a cake?")

    assert results == []


def test_empty_query_is_rejected():
    try:
        search_documents("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for an empty query")
