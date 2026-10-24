import json
from pathlib import Path

from src.ingestion.loader import load_document
from src.ingestion.chunker import chunk_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}


def run_ingestion() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(
        path
        for path in RAW_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not files:
        raise RuntimeError(
            f"No supported documents found in {RAW_DIR}"
        )

    all_chunks = []
    errors = []

    for path in files:
        try:
            records = load_document(path)
            chunks = chunk_document(records)
            all_chunks.extend(chunks)

            print(f"OK: {path.name} -> {len(chunks)} chunks")

        except (ValueError, OSError) as exc:
            errors.append((path.name, str(exc)))
            print(f"ERROR: {path.name}: {exc}")

    if not all_chunks:
        raise RuntimeError(
            "No chunks were generated. Check the document errors above."
        )

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for chunk in all_chunks:
            output.write(
                json.dumps(chunk, ensure_ascii=False) + "\n"
            )

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Output: {OUTPUT_FILE}")

    if errors:
        print(f"Documents with errors: {len(errors)}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run_ingestion())
