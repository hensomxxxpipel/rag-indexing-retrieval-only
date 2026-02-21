import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddingss = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")

# Buat client manual dulu
client = chromadb.PersistentClient(path="./db_pertor_for_legal-bert")

# Buat collection dengan cosine similarity
collection = client.get_or_create_collection(
    name="fixed_chunk_cosine",
    configuration={
        "hnsw": {
            "space": "cosine",         # <- metric similarity
        }
    }
)

# Hubungkan ke LangChain
vector_store = Chroma(
    client=client,
    collection_name="fixed_chunk_cosine",
    embedding_function=embeddingss,
)

# Apa pengertian dari kurikulum?
# Apa saja syarat yudisium?
question = input("Masukkan pertanyaan: ")

retrieved_docs = vector_store.similarity_search(question, k=5)
# retrieved_docs = vector_store.similarity_search_by_vector(embedding=embeddings.embed_query(question), k=5)

for i, doc in enumerate(retrieved_docs, 1):
    print(f"\n--- Chunk {i} ---\n {doc.page_content} [{doc.metadata}]")

