import pytest

from src.ingestion.loader import load_document
from src.ingestion.chunker import chunk_document


def test_load_text_file(tmp_path):
    path = tmp_path / "guide.txt"
    path.write_text(
        "  Python   uses virtual environments.  ",
        encoding="utf-8",
    )

    records = load_document(path)

    assert len(records) == 1
    assert records[0]["text"] == (
        "Python uses virtual environments."
    )
    assert records[0]["source"] == "guide.txt"
    assert records[0]["page"] is None


def test_load_markdown_file(tmp_path):
    path = tmp_path / "guide.md"
    path.write_text("# Setup\n\nInstall Python.", encoding="utf-8")

    records = load_document(path)

    assert len(records) == 1
    assert "Install Python." in records[0]["text"]


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_document("missing_document.txt")


def test_unsupported_extension(tmp_path):
    path = tmp_path / "guide.csv"
    path.write_text("a,b", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(path)


def test_empty_text_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("   ", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_document(path)


def test_chunking_and_metadata():
    words = [f"word{i}" for i in range(250)]
    record = {
        "text": " ".join(words),
        "source": "manual.pdf",
        "page": 2,
    }

    chunks = chunk_document(
        [record],
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) == 3
    assert len(chunks[0]["text"].split()) == 100
    assert len(chunks[1]["text"].split()) == 100
    assert chunks[0]["source"] == "manual.pdf"
    assert chunks[0]["page"] == 2

    # The first chunk's final 20 words overlap
    # with the second chunk's first 20 words.
    first_words = chunks[0]["text"].split()
    second_words = chunks[1]["text"].split()
    assert first_words[-20:] == second_words[:20]


def test_invalid_chunk_settings():
    with pytest.raises(ValueError):
        chunk_document([], chunk_size=0)

    with pytest.raises(ValueError):
        chunk_document([], chunk_size=10, overlap=10)


def test_empty_records_are_skipped():
    chunks = chunk_document(
        [{"text": " ", "source": "empty.txt", "page": None}]
    )

    assert chunks == []
