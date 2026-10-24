
import re

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def clean_markdown(text: str) -> str:
    """Clean common Markdown heading and spacing artifacts."""
    text = text.strip()
    text = re.sub(r"(?m)^\s*#{1,6}\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


st.set_page_config(
    page_title="Engineering Intelligence Hub",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Engineering Intelligence Hub")
st.caption("Engineering documentation retrieval powered by hybrid search")

with st.sidebar:
    st.header("Search settings")

    search_modes = {
        "Hybrid Search": "hybrid",
        "TF-IDF Keyword Search": "tfidf",
        "Semantic Search": "semantic",
    }

    selected_mode = st.selectbox(
        "Retrieval method",
        options=list(search_modes.keys()),
        index=0,
    )

    top_k = st.select_slider(
        "Number of results",
        options=[1, 2, 3, 5],
        value=3,
    )

    st.divider()
    st.caption("Hybrid search combines keyword and semantic rankings.")

with st.form("search_form"):
    question = st.text_input(
        "What would you like to troubleshoot?",
        placeholder="e.g. How do I fix ModuleNotFoundError?",
    )
    submitted = st.form_submit_button("Search documents", type="primary")

if submitted:
    if not question.strip():
        st.warning("Enter a question before searching.")
    else:
        mode = search_modes[selected_mode]

        try:
            with st.spinner(f"Searching with {selected_mode}..."):
                response = requests.post(
                    f"{API_URL}/search",
                    json={
                        "query": question.strip(),
                        "top_k": top_k,
                        "search_mode": mode,
                    },
                    timeout=90,
                )
                response.raise_for_status()
                data = response.json()

            results = data.get("results", [])

            st.subheader("Search results")
            st.caption(
                f"{len(results)} result(s) · {selected_mode}"
            )

            if not results:
                st.info(
                    "No relevant documents found. Try using different "
                    "keywords or rephrasing your question."
                )

            for rank, result in enumerate(results, start=1):
                with st.container(border=True):
                    st.markdown(f"### {rank}. {result.get('source') or 'Unknown source'}")

                    page = result.get("page")
                    if page is not None and str(page).strip():
                        st.caption(f"Page: {page}")

                    if mode == "hybrid":
                        st.metric(
                            "RRF score",
                            f"{result.get('rrf_score', 0.0):.4f}",
                        )

                        col1, col2 = st.columns(2)
                        keyword_rank = result.get("keyword_rank")
                        semantic_rank = result.get("semantic_rank")

                        col1.metric(
                            "Keyword rank",
                            keyword_rank if keyword_rank is not None else "Not ranked",
                        )
                        col2.metric(
                            "Semantic rank",
                            semantic_rank if semantic_rank is not None else "Not ranked",
                        )
                    else:
                        st.metric(
                            "Relevance score",
                            f"{result.get('score', 0.0):.4f}",
                        )

                    document_text = clean_markdown(
                        result.get("text", "")
                    )
                    st.markdown(document_text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. Start the backend on port 8000."
            )
        except requests.exceptions.Timeout:
            st.error(
                "The search timed out. The first semantic search may "
                "take longer while the model loads."
            )
        except requests.exceptions.HTTPError as exc:
            st.error(f"API error: {exc}")
        except (ValueError, KeyError) as exc:
            st.error(f"Unexpected response: {exc}")
