
from pathlib import Path
import re

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}



def clean_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph and heading breaks."""
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in text.split("\n")
    ]

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()



def load_document(file_path: str | Path) -> list[dict]:
    """Load a PDF, Markdown, or TXT document."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, received: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension or '[no extension]'}. "
            "Supported types: PDF, Markdown, TXT."
        )

    records = []

    if extension == ".pdf":
        try:
            reader = PdfReader(str(path))

            if reader.is_encrypted:
                raise ValueError(
                    f"Encrypted PDFs are not supported: {path.name}"
                )

            for page_number, page in enumerate(reader.pages, start=1):
                text = clean_text(page.extract_text() or "")

                if text:
                    records.append({
                        "text": text,
                        "source": path.name,
                        "page": page_number,
                    })

        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(
                f"Could not read PDF '{path.name}': {exc}"
            ) from exc

        if not records:
            raise ValueError(
                f"No extractable text found in '{path.name}'. "
                "It may be scanned or image-only. OCR is not implemented."
            )

    else:
        try:
            text = clean_text(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError as exc:
            raise ValueError(
                f"'{path.name}' is not valid UTF-8 text."
            ) from exc

        if not text:
            raise ValueError(f"Document is empty: {path.name}")

        records.append({
            "text": text,
            "source": path.name,
            "page": None,
        })

    return records
