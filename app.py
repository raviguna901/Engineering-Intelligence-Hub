
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Engineering Intelligence Hub",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Engineering Intelligence Hub")
st.write(
    "Search engineering troubleshooting documents "
    "using TF-IDF and cosine similarity."
)

st.info(
    "Ask about Python errors, virtual environments, "
    "database connections, or HTTP errors."
)

with st.form("search_form"):
    question = st.text_input(
        "Enter your question",
        placeholder="Example: What does HTTP 404 mean?",
    )
    top_k = st.selectbox(
        "Number of results",
        options=[1, 2, 3, 5],
        index=1,
    )
    submitted = st.form_submit_button("Search")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/search",
                json={
                    "query": question,
                    "top_k": top_k,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            results = data["results"]

            if not results:
                st.warning(
                    "No relevant documents found. "
                    "Try different keywords."
                )
            else:
                st.subheader("Search results")
                st.caption(f"Results found: {data['count']}")

                for rank, result in enumerate(results, start=1):
                    with st.container(border=True):
                        st.markdown(f"### Result {rank}")
                        st.write(f"**Source:** {result['source']}")
                        st.write(f"**Page:** {result['page']}")
                        st.metric(
                            "Relevance score",
                            f"{result['score']:.4f}",
                        )
                        st.write(result["text"])

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running on port 8000."
            )
        except requests.exceptions.Timeout:
            st.error("The API request timed out. Please try again.")
        except requests.exceptions.HTTPError as exc:
            st.error(f"API error: {exc}")
        except (ValueError, KeyError) as exc:
            st.error(f"Invalid API response: {exc}")
