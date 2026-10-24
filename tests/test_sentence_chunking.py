
from src.ingestion.chunker import chunk_document


def test_long_document_creates_multiple_chunks():
    sentences = [
        f"Sentence number {i} explains an engineering problem."
        for i in range(1, 31)
    ]
    text = " ".join(sentences)

    records = [{"text": text, "source": "test.txt", "page": 1}]
    chunks = chunk_document(records, chunk_size=30, overlap=5)

    assert len(chunks) > 1
    assert all(len(chunk["text"].split()) <= 30 for chunk in chunks)
    assert all(chunk["source"] == "test.txt" for chunk in chunks)
    assert all(chunk["page"] == 1 for chunk in chunks)


def test_chunk_ids_are_sequential():
    records = [
        {
            "text": " ".join(
                f"word{i}" for i in range(100)
            ),
            "source": "test.txt",
            "page": None,
        }
    ]

    chunks = chunk_document(records, chunk_size=20, overlap=5)

    assert chunks[0]["chunk_id"] == "chunk_00001"
    assert chunks[1]["chunk_id"] == "chunk_00002"
