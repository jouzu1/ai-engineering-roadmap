# 10 — Membangun RAG (Retrieval-Augmented Generation) dengan LangChain + FAISS

Tujuan modul:
- Memahami konsep RAG: menggabungkan LLM dengan pencarian dokumen.
- Mempersiapkan pipeline “ingest → index → retrieve → generate”.
- Menjalankan contoh RAG lokal yang sederhana namun praktis.

Kita akan membuat dua skrip:
- labs/06-rag-chatbot/ingest.py — memecah dokumen → buat embedding → simpan index FAISS
- labs/06-rag-chatbot/app.py — tanya jawab (CLI) memakai index + LLM

Anda bisa memilih:
- OpenAI (butuh OPENAI_API_KEY) atau
- Lokal: Sentence Transformers + Ollama (gratis, privat)

------------------------------------------------------------

## 1) Konsep Singkat RAG
- Masalah LLM: bisa “halusinasi” karena tidak punya pengetahuan baru/terkini.
- RAG solusi: sebelum menjawab, LLM mengambil (retrieve) potongan dokumen yang relevan sebagai konteks.
- Alur:
  1) Ingest: ambil dokumen → potong jadi chunk → hitung embedding → simpan ke vector store (FAISS)
  2) Query: embed pertanyaan → cari chunk terdekat (similarity search)
  3) Generate: panggil LLM dengan konteks chunk terpilih → hasil jawaban yang lebih akurat

------------------------------------------------------------

## 2) Persiapan
- Pastikan requirements sudah terpasang (lihat docs/01-setup.md).
- Siapkan .env:
  - Untuk OpenAI: isi OPENAI_API_KEY
  - Untuk lokal: install dan jalankan Ollama (OLLAMA_BASE_URL, OLLAMA_MODEL), dan kita akan pakai Sentence Transformers untuk embedding lokal.
- Siapkan bahan dokumen:
  - Kita akan gunakan file markdown di folder docs/ sebagai contoh (mis. 00-overview.md, 09-llm-dasar.md).
  - Anda bisa menambahkan dokumen sendiri (.md, .txt, .pdf yang bisa dibaca) nanti.

------------------------------------------------------------

## 3) Ingest: Membuat Index FAISS
Skrip ingest akan:
- Membaca file .md di folder docs/
- Memecah teks menjadi potongan (chunk) ukuran ~800 karakter
- Menghitung embedding:
  - Jika ada OPENAI_API_KEY → pakai OpenAIEmbeddings
  - Jika tidak → pakai Sentence Transformers lokal (all-MiniLM-L6-v2)
- Menyimpan index FAISS ke folder cache (default .cache/vectorstore atau sesuai .env)

Perintah (setelah file tersedia):
```
python labs/06-rag-chatbot/ingest.py --glob "docs/*.md"
```

Parameter opsional:
- --glob pola file (default: docs/*.md)
- --chunk-size 800
- --chunk-overlap 100

Output:
- Folder index FAISS di lokasi VECTORSTORE_PATH (lihat .env) atau default lokal.

------------------------------------------------------------

## 4) App: Tanya Jawab Berbasis RAG (CLI)
Skrip app akan:
- Memuat index FAISS
- Menerima pertanyaan dari terminal
- Melakukan similarity search untuk mengambil konteks
- Memanggil LLM (OpenAI atau Ollama) untuk menghasilkan jawaban berbasis konteks

Perintah:
```
python labs/06-rag-chatbot/app.py
```

Contoh pertanyaan:
- “Apa itu AI Engineering?”
- “Apa langkah utama dalam siklus hidup AI?”
- “Bagaimana cara deploy model dengan FastAPI dan Docker?”

Keluar dari aplikasi: ketik “exit” atau “quit”.

------------------------------------------------------------

## 5) Catatan Model dan Biaya
- OpenAI: kualitas bagus, berbayar (per token).
- Ollama (lokal): gratis, kualitas bervariasi, butuh unduh model (mis. mistral, llama3).
- Embedding:
  - OpenAI: text-embedding-3-small (default di .env)
  - Lokal: Sentence Transformers all-MiniLM-L6-v2 (gratis, cepat)
- Vector store: FAISS (in-memory + file). Cepat dan mudah untuk lokal.

------------------------------------------------------------

## 6) Troubleshooting
- “ModuleNotFoundError”: pastikan pip install -r requirements.txt sudah dilakukan di venv aktif.
- FAISS error di Windows lama: pastikan Python 64-bit, gunakan versi faiss-cpu terbaru.
- Kunci API OpenAI tidak terbaca: cek file .env dan jalankan terminal dari root repo, atau panggil dotenv di skrip.
- Ollama lambat/tidak merespon: pastikan server berjalan (default http://localhost:11434) dan model sudah di-pull.
- Index tidak ketemu: jalankan ingest.py dulu untuk menghasilkan vector store.

------------------------------------------------------------

## 7) Checklist
- [ ] Menjalankan ingest untuk membuat index
- [ ] Menanyakan 2–3 pertanyaan via app CLI
- [ ] Mencoba dua mode: OpenAI dan Lokal (Ollama + Sentence Transformers)
- [ ] Mengevaluasi apakah jawaban “berdasarkan” dokumen yang diindeks

Lanjutkan ke:
- docs/11-deploy-fastapi-docker.md untuk membungkus model ke API dan Docker.
- labs/07-fastapi-ml untuk men-deploy model sklearn (dari modul ML) sebagai layanan.
