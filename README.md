# AI Engineering Roadmap (Bahasa Indonesia, dari nol)

Dokumentasi dan contoh kode untuk belajar AI Engineering secara bertahap, dari dasar sampai bisa membangun dan mendistribusikan (deploy) aplikasi AI di dunia nyata. Bahasa sederhana, fokus praktik.

## Kenapa AI Engineering?
- Mengubah model AI/ML menjadi produk siap pakai (API, aplikasi, automasi).
- Mengelola siklus hidup model: data, eksperimen, versi, deploy, monitoring.
- Menjembatani riset (ML/DL/LLM) dengan kebutuhan bisnis dan pengguna.

## Hasil Akhir yang Diharapkan
- Paham dasar ML dan Deep Learning.
- Bisa melatih model, mengevaluasi, dan memperbaiki performa.
- Bisa membuat API (FastAPI), membungkus dengan Docker, dan deploy.
- Paham MLOps dasar: MLflow (tracking), DVC (versioning data/model), CI/CD.
- Bisa membangun aplikasi modern seperti RAG chatbot (LLM + pencarian dokumen).

## Prasyarat Ringan
- Python 3.10+ (direkomendasikan 3.11), VSCode, Git, pip.
- Internet untuk unduh paket dan dataset.
- GPU opsional (lebih cepat untuk deep learning, tapi tidak wajib).
- Akun GitHub untuk CI/CD (opsional).
- Kunci API LLM opsional (mis. OpenAI). Alternatif: model lokal (Ollama).

## Struktur Repo (akan diisi bertahap)
```
ai-engineering-roadmap/
├─ README.md
├─ requirements.txt                 # dependensi Python (akan ditambahkan)
├─ .env.example                     # template kunci API/konfigurasi (akan ditambahkan)
├─ docs/                            # materi belajar langkah demi langkah
│  ├─ 00-overview.md               # apa itu AI Engineering, alur end-to-end
│  ├─ 01-setup.md                  # instalasi Python, venv, VSCode, Git
│  ├─ 02-python-dasar.md
│  ├─ 03-numpy-pandas.md
│  ├─ 04-visualisasi.md
│  ├─ 05-ml-dasar.md               # train/val/test, metric, overfitting
│  ├─ 06-ml-pipeline-sklearn.md    # ColumnTransformer + Pipeline
│  ├─ 07-deep-learning-pytorch.md  # dataset, dataloader, training loop
│  ├─ 08-nlp-cv-dasar.md
│  ├─ 09-llm-dasar.md              # prompt, embedding, RAG konsep
│  ├─ 10-langchain-rag.md          # bangun RAG chatbot
│  ├─ 11-deploy-fastapi-docker.md  # API, Dockerfile, healthcheck
│  ├─ 12-mlops-mlflow-dvc.md       # tracking, versioning, pipeline
│  ├─ 13-ci-cd.md                  # GitHub Actions
│  ├─ 14-monitoring-logging.md
│  └─ 15-etika-keamanan.md
├─ labs/                            # proyek mini (praktik)
│  ├─ 01-numpy-pandas.ipynb        # eksplorasi data
│  ├─ 02-ml-regression-sklearn.ipynb
│  ├─ 03-ml-pipeline.py            # pipeline tabular lengkap
│  ├─ 04-pytorch-cnn.ipynb
│  ├─ 05-nlp-sentiment-transformers.ipynb
│  ├─ 06-rag-chatbot/
│  │  ├─ ingest.py                 # buat embedding + index FAISS
│  │  └─ app.py                    # aplikasi Q&A (CLI/Streamlit)
│  └─ 07-fastapi-ml/
│     ├─ main.py                   # API prediksi
│     └─ Dockerfile
├─ .github/workflows/ci.yml         # CI sederhana (lint/test/build)
├─ datasets/
│  └─ README.md                    # panduan dataset
└─ Makefile atau tasks.ps1         # perintah ringkas (setup/run/test)
```

Catatan: Di awal, sebagian file belum ada. File-file akan ditambahkan bertahap di commit selanjutnya.

## Cara Mulai Cepat
1) Clone repo ini (atau salin folder ke komputer Anda).
2) Buat virtual environment:
   - Windows PowerShell:
     - python -m venv .venv
     - .venv\Scripts\Activate
   - macOS/Linux:
     - python -m venv .venv
     - source .venv/bin/activate
3) Install dependensi:
   - pip install -r requirements.txt
4) Jalankan contoh:
   - Jupyter: jupyter lab lalu buka notebooks di folder labs/
   - Script: python labs/03-ml-pipeline.py
5) RAG chatbot:
   - Isi OPENAI_API_KEY di file .env (atau gunakan Ollama untuk lokal)
   - python labs/06-rag-chatbot/ingest.py
   - python labs/06-rag-chatbot/app.py
6) API model:
   - uvicorn labs.07-fastapi-ml.main:app --reload
7) MLflow UI:
   - mlflow ui --port 5000

Instruksi rinci ada di folder docs. Mulailah dari:
- docs/00-overview.md
- docs/01-setup.md

## Modul Pembelajaran (ringkas)
- Fondasi: Python dasar, NumPy, Pandas, Visualisasi.
- ML: split data, metrik (RMSE/Accuracy/Precision-Recall), pipeline sklearn.
- DL: PyTorch (Dataset, DataLoader, model sederhana, training loop).
- LLM: dasar prompt, embedding, RAG (LangChain + FAISS).
- Deploy: FastAPI, Docker, logging, healthcheck.
- MLOps: MLflow, DVC, CI/CD (GitHub Actions), monitoring ringan.
- Etika & keamanan: PII, bias, keamanan API.

## Proyek Mini (bertahap)
1) Regresi harga rumah (scikit-learn) — data tabular, evaluasi RMSE.
2) Sentimen teks (Transformers) — evaluasi F1/Accuracy.
3) Klasifikasi gambar (PyTorch) — CNN sederhana di CIFAR-10.
4) RAG Chatbot (LangChain + FAISS) — tanya jawab dokumen lokal.
5) API + Docker (FastAPI) — endpoint /predict dan /health.
6) MLOps (MLflow + DVC) — tracking eksperimen, versioning data/model.

## Tips Belajar
- Mulai dari contoh terkecil, jalankan, amati output, catat temuan.
- Ulangi eksperimen kecil (ubah learning rate, arsitektur, metrik).
- Versikan eksperimen dan data (MLflow + DVC) supaya rapi.
- Fokuskan pada kasus dunia nyata: data kotor, metrik realistis, logging.

## Lisensi
MIT License. Gunakan dengan bijak. Perhatikan privasi data dan etika penggunaan AI.

---

Roadmap ini disusun agar Anda bisa belajar mandiri, cepat mendapat hasil, dan paham konsep inti tanpa matematika berat di awal. Selamat belajar!
