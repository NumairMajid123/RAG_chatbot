import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Load and cache the embedding model only once
@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small",
        encode_kwargs={"normalize_embeddings": True}
    )

# Load and cache the FAISS index only once
@st.cache_resource
def load_faiss_index(_embedding_model):  # <-- notice underscore here
    return FAISS.load_local(
        folder_path="faiss_index_new",
        embeddings=_embedding_model,
        allow_dangerous_deserialization=True
    )

# Main App
st.title("📚 RAG-KB: An Intelligent Chatbot for Contextual Information Retrieval ")

query = st.text_input("Enter your query:")

if query:
    with st.spinner("Searching..."):
        embedding_model = load_embedding_model()
        db = load_faiss_index(embedding_model)  # <-- no change here
        query_with_prefix = f"query: {query}"
        results = db.similarity_search(query_with_prefix, k=3)

        if results:
            for i, doc in enumerate(results):
                st.markdown(f"### 🔍 Result {i+1}")
                st.markdown(f"**Header:** {doc.metadata.get('header', 'N/A')}")
                st.markdown(f"**URL:** {doc.metadata.get('url', 'N/A')}")
                st.markdown("**Matched Content:**")
                st.write(doc.page_content)
                with st.expander("📄 Original JSON Metadata"):
                    st.json(doc.metadata.get("raw", {}))
        else:
            st.info("No results found.")
