# RAG – Indexing & Retrieval Only

This repository contains a partial implementation of an undergraduate thesis project focusing on the indexing and retrieval module of a Retrieval-Augmented Generation (RAG) system for legal documents (Peraturan Rektor Universitas Brawijaya).

This project does not include the generation module and is intended only to demonstrate the document indexing, vector storage, and retrieval process.

---

Repository ini berisi **implementasi sebagian (partial)** dari project skripsi ssaya yang berfokus pada **tahap indexing dan retrieval** pada sistem *Retrieval-Augmented Generation (RAG)* untuk dokumen hukum (Peraturan Rektor Universitas Brawijaya).

Repository ini **tidak mencakup modul generation (LLM answering)** dan hanya bertujuan untuk mendemonstrasikan proses:

- pemrosesan dokumen,
- penyimpanan vektor,
- serta pengambilan (retrieval) dokumen berbasis kemiripan.

---

Dokumen hukum yang digunakan dalam eksperimen pada repository ini adalah (**./document folder**):

- **Per-55-2023-Penyelenggaraan-Pendidikan-Universitas-Brawijaya-Tahun-Akademik-2023–2024.pdf**  
  (Peraturan Rektor UB tentang Penyelenggaraan Pendidikan Tahun Akademik 2023/2024)

- **Per-59-2025-Yudisium, Penerbitan Ijazah, Transkrip Nilai, Surat Keterangan Pendamping Ijazah, dan Sertifikat Profesi.pdf**

- **Peraturan Rektor Universitas Brawijaya Nomor 89 Tahun 2023 tentang Tata Naskah Dinas.pdf**

- **Per-1-2025-Perubahan Ketiga atas Peraturan Rektor Nomor 12 Tahun 2023 tentang Organisasi dan Tata Kerja Unsur yang Berada di Bawah Rektor.pdf**

Catatan:  
File PDF tidak disertakan di dalam repository ini. Dokumen hanya digunakan pada tahap eksperimen dan pengujian sistem indexing dan retrieval.

---

## 📌 Ruang Lingkup Project

Cakupan pada repository ini:

- embedding dokumen
- fixed-size chunking
- indexing ke vector database (Chroma)
- similarity-based retrieval
- antarmuka sederhana untuk inspeksi hasil retrieval

Di luar cakupan:

- prompt engineering
- answer generation menggunakan LLM
- end-to-end RAG pipeline

---

## 📁 Struktur Folder
## Project Structure

```text
db_pertor_for_legal-bert/
├── app.py                   # Main Flask/Streamlit application
├── RAG_Fixed-Chunking.ipynb # Notebook for RAG experimentation
├── RAG_Fixed-Chunking.py    # Python script for RAG processing
└── README.md                # Project documentation
```

---

## 📄 Deskripsi File

### 1. `app.py`

Merupakan aplikasi berbasis **Streamlit** untuk melakukan pencarian similarity terhadap database vektor yang sudah tersedia.

Fitur utama:

- memuat database Chroma secara persisten
- menggunakan HuggingFace embedding
- pengaturan Top-K retrieval
- menampilkan potongan dokumen (chunk) beserta metadata

File ini digunakan untuk inspeksi hasil retrieval secara interaktif.

---

### 2. `RAG_Fixed-Chunking.ipynb`

Notebook utama eksperimen.

Berisi seluruh alur proses, mulai dari:

- pemuatan dokumen hukum,
- pembersihan dokumen,
- proses fixed chunking,
- pembuatan embedding,
- penyimpanan vektor ke Chroma,
- hingga pengujian retrieval.

Notebook ini merepresentasikan workflow eksperimen yang digunakan dalam skripsi.

---

### 3. `RAG_Fixed-Chunking.py`

Script versi ringkas untuk langsung memuat database vektor yang sudah ada dan melakukan retrieval melalui terminal.

Digunakan untuk pengujian cepat tanpa menjalankan notebook.

---

## ⚙️ Teknologi yang Digunakan

- Python
- Streamlit
- ChromaDB
- LangChain
- HuggingFace Embeddings

Model embedding:
# Qwen/Qwen3-Embedding-0.6B


---

## ▶️ Cara Menjalankan

### 1. Install dependensi

Disarankan menggunakan virtual environment.


```bash
python -m venv venv
venv\Scripts\activate
```

Install dependensi:

``` bash
pip install streamlit chromadb langchain langchain-chroma langchain-huggingface
```


---

### 2. Menjalankan aplikasi UI
``` bash
streamlit run app.py
```


---

### 3. Menjalankan retrieval via terminal
``` bash
python RAG_Fixed-Chunking.py
```


Kemudian masukkan pertanyaan pada prompt yang tersedia.

---

## 📝 Catatan

- Repository ini hanya berisi **tahap indexing dan retrieval**.
- Database vektor harus sudah tersedia sebelum menjalankan `app.py` atau `RAG_Fixed-Chunking.py`.
- Proses preprocessing dokumen, chunking, dan indexing dapat dilihat pada file notebook.

---

## 🎓 Pernyataan Akademik

Repository ini merupakan **rilis sebagian (partial code release)** dari project skripsi.

Beberapa komponen, eksperimen, dan detail implementasi tidak disertakan secara penuh demi kepentingan akademik dan institusional.

Repository ini ditujukan untuk:

- pembelajaran,
- demonstrasi teknis sistem retrieval dokumen hukum,
- serta replikasi penelitian pada level modul (indexing & retrieval) saja.