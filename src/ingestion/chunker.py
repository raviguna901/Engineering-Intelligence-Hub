
import re

from src.ingestion.loader import clean_text


def chunk_document(
    records: list[dict],
    chunk_size: int = 120,
    overlap: int = 30,
) -> list[dict]:
    """
    Split document records into overlapping, sentence-aware word chunks.

    Chunks prefer sentence boundaries and preserve source/page metadata.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    if not isinstance(records, list):
        raise TypeError("records must be a list of dictionaries.")

    chunks = []
    step = chunk_size - overlap

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Each record must be a dictionary.")

        text = clean_text(record.get("text", ""))

        if not text:
            continue

        source = record.get("source")
        page = record.get("page")

        # Split at likely sentence-ending punctuation.
        sentences = re.split(r"(?<=[.!?])\s+", text)
        word_chunks = []
        current_words = []

        for sentence in sentences:
            sentence_words = sentence.split()

            if not sentence_words:
                continue

            # Handle a sentence larger than the target chunk size.
            if len(sentence_words) > chunk_size:
                if current_words:
                    word_chunks.append(current_words)
                    current_words = []

                for start in range(0, len(sentence_words), step):
                    part = sentence_words[start:start + chunk_size]
                    word_chunks.append(part)

                    if start + chunk_size >= len(sentence_words):
                        break
                continue

            if (
                current_words
                and len(current_words) + len(sentence_words) > chunk_size
            ):
                word_chunks.append(current_words)

                # Retain trailing words as overlapping context.
                current_words = current_words[-overlap:] if overlap else []

            current_words.extend(sentence_words)

        if current_words:
            word_chunks.append(current_words)

        for words in word_chunks:
            if not words:
                continue

            chunks.append(
                {
                    "chunk_id": f"chunk_{len(chunks) + 1:05d}",
                    "text": " ".join(words),
                    "source": source,
                    "page": page,
                }
            )

    return chunks
