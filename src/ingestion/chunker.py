
import re

from src.ingestion.loader import clean_text


HEADING_PATTERN = re.compile(
    r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$"
)

def chunk_document(
    records: list[dict],
    chunk_size: int = 120,
    overlap: int = 30,
) -> list[dict]:
    """Create overlapping chunks while preserving Markdown section context."""
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

        raw_text = record.get("text", "")
        if not isinstance(raw_text, str):
            raise TypeError("Record text must be a string.")

        text = clean_text(raw_text)
        if not text:
            continue

        source = record.get("source")
        page = record.get("page")
        current_heading = None
        section_lines = []

        def flush_section():
            if not section_lines:
                return

            section_text = "\n".join(section_lines).strip()
            if not section_text:
                return

            prefix = f"{current_heading}\n" if current_heading else ""
            words = section_text.split()
            word_chunks = []
            current_words = []

            # Preserve sentence boundaries where possible.
            sentences = re.split(r"(?<=[.!?])\s+", section_text)

            for sentence in sentences:
                sentence_words = sentence.split()
                if not sentence_words:
                    continue

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
                    current_words = (
                        current_words[-overlap:] if overlap else []
                    )

                current_words.extend(sentence_words)

            if current_words:
                word_chunks.append(current_words)

            for chunk_words in word_chunks:
                body = " ".join(chunk_words).strip()
                if not body:
                    continue

                # Include the heading as searchable context, but do not
                # count it toward the body chunk's word limit.
                chunk_text = f"{prefix}{body}".strip()

                chunks.append({
                    "chunk_id": f"chunk_{len(chunks) + 1:05d}",
                    "text": chunk_text,
                    "source": source,
                    "page": page,
                    "heading": current_heading,
                })

        for line in text.splitlines():
            match = HEADING_PATTERN.match(line)

            if match:
                flush_section()
                current_heading = match.group(1).strip()
                section_lines = []
            else:
                section_lines.append(line)

        flush_section()

    return chunks
