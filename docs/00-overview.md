# 00 — Gambaran Umum AI Engineering (Bahasa Sederhana)

Dokumen ini menjelaskan apa itu AI Engineering, kenapa penting, alur kerja dari data sampai jadi aplikasi, dan apa saja yang akan Anda pelajari di roadmap ini.

## Apa itu AI Engineering?
- AI Engineering adalah pekerjaan merancang, membangun, dan menjalankan sistem AI di dunia nyata.
- Bukan hanya “melatih model”, tetapi:
  - Mengelola data
  - Melatih dan mengevaluasi model (ML/DL/LLM)
  - Membuat API/aplikasi supaya bisa dipakai user
  - Mendeploy ke server/Cloud
  - Memantau performa dan memperbaiki saat kualitas turun
- Intinya: Mengubah riset AI menjadi produk yang berguna dan aman dipakai.

## Kenapa Penting?
- Banyak model bagus di lab, tapi sulit dipakai di bisnis kalau tidak di-engineer dengan benar.
- AI Engineering memastikan sistem:
  - Konsisten, bisa diulang (reproducible), gampang di-maintain
  - Aman, memperhatikan privasi, etika, dan biaya
  - Skalabel, bisa menangani lebih banyak user/data

## Alur Kerja End-to-End (Siklus Hidup AI)
1) Kumpulkan & paham data
   - Ambil data (file CSV, database, dokumen PDF, log)
   - Bersihkan data (missing values, duplikat, anomali)
   - Bagi data: train / validation / test
2) Bangun model
   - Pilih pendekatan: Machine Learning (sklearn) atau Deep Learning (PyTorch) atau LLM
   - Latih model, catat parameter dan hasil (MLflow)
3) Evaluasi
   - Hitung metrik (RMSE, Accuracy, F1, dll.)
   - Bandingkan beberapa eksperimen (model/setting berbeda)
4) Kemas jadi layanan
   - Buat API (FastAPI) agar model bisa diakses aplikasi lain
   - Tambah logging, healthcheck, konfigurasi .env
5) Deploy
   - Bungkus dengan Docker
   - Jalankan di server/Cloud
6) Monitoring & Iterasi
   - Pantau metrik, error, biaya
   - Perbarui model jika performa turun atau data berubah

Gambaran sederhana:
Data → Model → Evaluasi → API → Docker → Deploy → Monitoring → Ulangi

## Apa yang Akan Anda Buat di Roadmap Ini?

- Proyek mini bertahap:
  - ML tabular sederhana (regresi harga rumah)
  - NLP sentimen (pakai model Transformers)
  - CV sederhana (PyTorch CNN)
  - RAG Chatbot (LLM + pencarian dokumen)
  - API FastAPI untuk model + Docker
  - MLOps dasar: MLflow, DVC, CI/CD
- Semua dengan bahasa sederhana dan file contoh yang bisa langsung dijalankan.

## Peta Jalan Belajar (Ringkas)
- Fondasi (Python, NumPy, Pandas, Visualisasi)
- ML dengan scikit-learn (split data, pipeline, metrik)
- Deep Learning dengan PyTorch (dataset, DataLoader, training loop)
- LLM & RAG (prompt, embedding, indexing, retrieval)
- Deploy (FastAPI, Docker)
- MLOps (MLflow, DVC, CI/CD)
- Etika & Keamanan (privasi, bias, PII)

Detail lengkap ada di folder docs/ (modul 01–15).

## Pilar Skill yang Anda Bangun
- Skill teknis:
  - Python untuk data
  - ML/DL/LLM dasar
  - API & Docker
  - MLOps (tracking, versioning, CI/CD)
- Skill non-teknis:
  - Problem framing (memahami masalah bisnis)
  - Eksperimen terstruktur dan dokumentasi
  - Etika & privasi data
  - Komunikasi hasil (membuat laporan yang jelas)

## Tool Utama yang Dipakai
- Python, pip/venv
- NumPy, Pandas, Matplotlib/Seaborn
- scikit-learn, PyTorch
- Transformers (HuggingFace), LangChain, FAISS
- FastAPI, Uvicorn
- Docker
- MLflow (tracking), DVC (versioning)
- Git & GitHub Actions (CI/CD)
- Optional: OpenAI API atau model lokal (Ollama)

## Istilah Kunci (Bahasa Sederhana)
- Dataset: Kumpulan data untuk melatih/menguji model
- Fitur (feature): Kolom/karakteristik yang dipakai model
- Label/Target: Nilai yang ingin diprediksi
- Overfitting: Model “terlalu hafal” data latihan, jelek di data baru
- Pipeline: Rangkaian langkah otomatis (preprocessing → model)
- API: Cara aplikasi lain memanggil model lewat HTTP
- Docker: “Kotak” berisi aplikasi + dependensi agar mudah dipindah
- RAG: Retrieval-Augmented Generation (LLM + pencarian dokumen)
- Tracking: Mencatat eksperimen agar mudah dibandingkan

## Cara Memakai Roadmap Ini
1) Buka README.md dan ikuti “Cara Mulai Cepat”
2) Mulai dari docs/01-setup.md → siapkan environment
3) Coba contoh di labs/ secara bertahap (mulai dari yang paling mudah)
4) Catat hasil eksperimen (pakai MLflow)
5) Lanjutkan ke modul LLM/RAG dan Deploy
6) Akhiri dengan MLOps dasar dan capstone

## Checklist “Mulai Hari Ini”
- [ ] Instal Python 3.10+ dan VSCode
- [ ] Buat virtual environment dan install requirements.txt
- [ ] Jalankan satu contoh sederhana (labs/03-ml-pipeline.py)
- [ ] Baca docs/01-setup.md lalu lanjut docs/05-ml-dasar.md
- [ ] Buat catatan eksperimen pertama Anda (MLflow)

Selamat belajar! Fokus pada langkah kecil, jalankan kode, lihat output, dan ulangi. Anda akan membangun fondasi kuat untuk menjadi AI Engineer yang siap produksi.
