# Engineering Intelligence Hub

An AI-powered technical knowledge retrieval system that helps users find relevant information from engineering and troubleshooting documents. The project supports traditional TF-IDF retrieval and semantic search using sentence embeddings.

## Features

- **Document ingestion:** Processes technical documents into searchable text chunks.
- **Sentence-aware chunking:** Splits documents into manageable chunks while preserving sentence boundaries.
- **TF-IDF search:** Retrieves relevant chunks using keyword-based similarity.
- **Semantic search:** Uses Sentence Transformers to identify documents with similar meanings, even when the wording differs.
- **REST API:** FastAPI endpoints for health checks and document search.
- **Interactive UI:** Streamlit-based interface.
- **Automated tests:** Pytest coverage for core project functionality.

## Technology Stack

- Python 3.12
- FastAPI and Uvicorn
- Streamlit
- Scikit-learn and TF-IDF
- Sentence Transformers
- NumPy
- Pytest

## Project Structure

```text
Engineering-Intelligence-Hub/
├── app.py
├── src/
│   ├── main.py
│   ├── ingestion/
│   │   └── pipeline.py
│   └── retrieval/
│       ├── search.py
│       └── semantic_search.py
├── data/
│   ├── raw/
│   └── processed/
│       └── chunks.jsonl
├── tests/
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Engineering-Intelligence-Hub
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Process the documents

```bash
python -m src.ingestion.pipeline
```

This generates the processed document chunks used by the retrieval system.

## Running the Application

### Streamlit interface

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, typically `http://localhost:8501`.

### FastAPI backend

```bash
uvicorn src.main:app --reload
```

- API base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Running Search

### TF-IDF retrieval

```bash
python -m src.retrieval.search
```

### Semantic retrieval

```bash
python -m src.retrieval.semantic_search
```

### Compare both methods

```bash
python compare_search.py
```

The comparison script evaluates both retrieval methods on the same five sample queries and displays the top three unique source documents for each method.

## Evaluation

The current project has **19 passing automated tests**.

A manual comparison was conducted using five queries covering Python troubleshooting, HTTP status codes, data pipelines, machine learning model evaluation, and SQL errors.

Observed results:

- TF-IDF retrieved `python_troubleshooting.md` first for the Python import question.
- Semantic search retrieved `http_status_codes.md` first for the HTTP 404 question.
- Both methods retrieved `data_pipeline_troubleshooting.md` first for the data pipeline question.
- Semantic search retrieved `model_evaluation.md` first for the model evaluation question.
- Both methods retrieved `sql_troubleshooting.md` first for the SQL troubleshooting question.

These are qualitative observations from a small sample, not a formal benchmark. Similarity scores from TF-IDF and semantic search are not directly comparable, and a larger labeled evaluation set is needed to establish which method performs better overall.

## Limitations

- Search quality depends on the source documents and their chunking.
- Semantic search requires downloading a pretrained model on first use if it is not already cached.
- The current comparison uses only five queries.
- Search similarity scores do not guarantee factual correctness.
- The system retrieves relevant document passages; retrieval alone does not guarantee that a generated answer is available.

## Future Improvements

- Expand the technical document collection.
- Build a larger, labeled retrieval evaluation dataset.
- Measure Precision@K, Recall@K, and Mean Reciprocal Rank.
- Add document metadata filters and source citations in the UI.
- Optimize model loading and embedding reuse.
- Add answer generation grounded in retrieved passages.

## License

Add your chosen open-source license here before publishing the repository.
