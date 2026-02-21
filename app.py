import streamlit as st
import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import LlamaCppEmbeddings
import os
from pathlib import Path
import base64

os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(
    page_title="Pertor UB Retrieval",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistem Retrieval Peraturan Rektor UB")

# Helper to display PDF
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="700"
            style="border:none;">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


# Load embedding (.GGUF / .bin - llama.cpp)
@st.cache_resource
def load_embeddings():
    return LlamaCppEmbeddings(
        # model_path="./models/Qwen3-Embedding-0.6B-f16.gguf",
        model_path="./models/Qwen3-Embedding-0.6B-q8_0.bin",
        n_ctx=4096,
        n_threads=os.cpu_count(),
        verbose=False
    )

embeddings = load_embeddings()


# Load vector store
@st.cache_resource
def load_vectorstore():
    client = chromadb.PersistentClient(
        path="./db_pertor_for_legal-bert"
    )

    collection = client.get_or_create_collection(
        name="fixed_chunk_cosine",
        configuration={
            "hnsw": {"space": "cosine"}
        }
    )

    vector_store = Chroma(
        client=client,
        collection_name="fixed_chunk_cosine",
        embedding_function=embeddings,
    )

    return vector_store, collection


vector_store, collection = load_vectorstore()


# Sidebar
with st.sidebar:
    st.header("ℹ️ Informasi Database")
    st.write(f"Jumlah chunk tersimpan: **{collection.count()}**")
    st.markdown("---")
    st.write("**Top-K Retrieval**")
    k = st.slider("Jumlah dokumen", 1, 10, 5)


# Query
st.subheader("🔎 Masukkan Pertanyaan")

question = st.text_input(
    "Pertanyaan",
    placeholder="Contoh: Apa pengertian dari kurikulum?"
)

if "results" not in st.session_state:
    st.session_state.results = None

if "selected_pdf" not in st.session_state:
    st.session_state.selected_pdf = None


# Retrieval
if st.button("Submit", type="primary"):

    if question.strip() == "":
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
    else:
        with st.spinner("Melakukan similarity search..."):
            st.session_state.results = vector_store.similarity_search(
                question, k=k
            )

        st.success(
            f"Top-{len(st.session_state.results)} chunk relevan"
        )


# Hasil retrieval
if st.session_state.results is not None:

    st.markdown("## 📄 Hasil Retrieval")

    for i, doc in enumerate(st.session_state.results, 1):
        with st.expander(f"📄 Chunk {i}", expanded=(i == 1)):
            st.write(doc.page_content)

            if doc.metadata:
                st.markdown("**Metadata:**")
                st.json(doc.metadata)


# Manual document viewer
st.markdown("---")

with st.expander("Help?", expanded=False):
    st.subheader("📂 Buka dokumen peraturan (manual)")

    docs_dir = Path("./document")

    if not docs_dir.exists():
        st.warning("Folder ./document tidak ditemukan.")
    else:
        pdf_files = sorted([p.name for p in docs_dir.glob("*.pdf")])

        if len(pdf_files) == 0:
            st.info("Tidak ada file PDF di folder document.")
        else:
            selected = st.selectbox(
                "Pilih dokumen peraturan untuk ditampilkan",
                options=["-- Pilih dokumen --"] + pdf_files,
                index=0,
                key="manual_pdf_select"
            )

            if selected != "-- Pilih dokumen --":
                st.session_state.selected_pdf = selected

            if st.session_state.selected_pdf:
                st.markdown(f"### 📘 {st.session_state.selected_pdf}")
                show_pdf(docs_dir / st.session_state.selected_pdf)