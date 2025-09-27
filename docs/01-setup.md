# 01 — Setup Lingkungan Kerja (Windows/macOS/Linux)

Tujuan: menyiapkan komputer Anda agar bisa menjalankan seluruh contoh di roadmap ini dengan mudah. Kita pakai Python, venv, pip, Jupyter, dan alat pendukung lain.

Ringkas:
- Install Python 3.10+ (disarankan 3.11)
- Buat virtual environment (venv)
- Install requirements
- Siapkan Jupyter kernel
- Buat file .env (opsional)
- Verifikasi instalasi (cek paket + tes GPU opsional)

Jika mengalami error, baca bagian Troubleshooting di akhir.

------------------------------------------------------------

## 1) Install Python 3.11 dan VSCode

- Windows:
  1. Unduh Python 3.11 dari https://www.python.org/downloads/windows/
  2. Jalankan installer, centang “Add Python to PATH”, lanjutkan sampai selesai.
  3. Install VSCode: https://code.visualstudio.com/
  4. Install ekstensi VSCode: “Python”, “Jupyter”, “Pylance”, “Docker” (opsional).
  5. Buka Terminal VSCode: Terminal → New Terminal (PowerShell).

- macOS:
  - Install via Homebrew:
    - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    - brew install python@3.11
  - Install VSCode + ekstensi seperti di atas.

- Linux (Debian/Ubuntu):
  - sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip
  - Install VSCode + ekstensi seperti di atas.

Cek versi:
- python --version
- pip --version

Jika Python tidak dikenali, restart terminal/komputer lalu coba lagi.

------------------------------------------------------------

## 2) Clone/Siapkan Repo dan Masuk Folder

Letakkan repositori “ai-engineering-roadmap” di lokasi kerja Anda dan masuk ke dalamnya.

Contoh (Windows PowerShell):
- cd "c:\Users\Jouzu\Documents\Development\Vibe Coding\ai-engineering-roadmap"

Contoh (macOS/Linux):
- cd ~/Documents/ai-engineering-roadmap

------------------------------------------------------------

## 3) Buat Virtual Environment (venv)

Pisahkan paket proyek agar tidak bentrok dengan sistem.

- Windows (PowerShell):
  - python -m venv .venv
  - .venv\Scripts\Activate
- macOS/Linux:
  - python -m venv .venv
  - source .venv/bin/activate

Tips:
- Untuk keluar venv: deactivate
- Pastikan prompt terminal menunjukkan (.venv)

Upgrade alat dasar:
- python -m pip install --upgrade pip setuptools wheel

------------------------------------------------------------

## 4) Install Dependensi

Di dalam venv dan di root repo (folder yang berisi requirements.txt):

- pip install -r requirements.txt

Ini akan memasang:
- NumPy, Pandas, Matplotlib/Seaborn (data/visualisasi)
- scikit-learn (ML)
- PyTorch (CPU), torchvision, torchaudio
- Transformers, datasets, accelerate, sentencepiece (NLP/LLM)
- LangChain, FAISS CPU (RAG)
- FastAPI + Uvicorn (API)
- MLflow, DVC (MLOps)
- JupyterLab, ipykernel, dan utilitas lainnya

Catatan: Instalasi bisa memakan waktu, tergantung koneksi dan spek komputer.

------------------------------------------------------------

## 5) (OPSIONAL) Install PyTorch GPU (NVIDIA)

Default requirements memasang PyTorch CPU. Jika Anda punya GPU NVIDIA dan ingin akselerasi:

1) Pastikan driver NVIDIA terbaru terpasang (cek dengan nvidia-smi di Command Prompt/PowerShell). CUDA Toolkit TIDAK wajib jika memakai wheel PyTorch resmi (cukup driver modern).

2) Hapus paket torch/torchvision/torchaudio CPU (opsional, jika ingin bersih):
- pip uninstall -y torch torchvision torchaudio

3) Pasang PyTorch GPU sesuai CUDA yang didukung wheel resmi (contoh CUDA 12.1):
- pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio

4) Verifikasi:
```bash
python -c "import torch; print('Torch:', torch.__version__, 'CUDA:', torch.cuda.is_available())"
```
Jika “CUDA: True”, berarti GPU terbaca.

Catatan:
- Lihat panduan resmi: https://pytorch.org/get-started/locally/
- Wheel GPU hanya untuk NVIDIA. Untuk AMD/Apple Silicon, lihat dokumentasi PyTorch khusus.

------------------------------------------------------------

## 6) Siapkan Jupyter Kernel

Agar notebook di labs/ bisa memilih kernel venv ini:

- python -m ipykernel install --user --name ai-roadmap --display-name "Python (ai-roadmap)"

Buka JupyterLab:
- jupyter lab

Pilih kernel “Python (ai-roadmap)” saat membuka notebook.

------------------------------------------------------------

## 7) Buat File .env (Variabel Lingkungan)

Salin template:
- Windows PowerShell: copy .env.example .env
- macOS/Linux: cp .env.example .env

Isi nilai seperlunya:
- OPENAI_API_KEY jika ingin pakai OpenAI untuk RAG/LLM
- OLLAMA_BASE_URL dan OLLAMA_MODEL jika pakai model lokal (Ollama)
- MLFLOW_TRACKING_URI jika ingin UI MLflow (default lokal: http://127.0.0.1:5000)

VSCode akan otomatis memuat variabel saat menjalankan proses dari terminal jika Anda memakai python-dotenv di kode terkait.

------------------------------------------------------------

## 8) Verifikasi Instalasi (Tes Cepat)

Jalankan perintah-perintah ini di terminal (dalam venv):

1) Paket data/ML:
```bash
python -c "import numpy, pandas, sklearn; print('OK data/ML')"
```

2) PyTorch:
```bash
python -c "import torch; print('Torch', torch.__version__, 'CUDA', torch.cuda.is_available())"
```

3) NLP/LLM:
```bash
python -c "import transformers, datasets; print('OK NLP')"
```

4) RAG/Vector store:
```bash
python -c "import faiss; print('OK FAISS')"
```

5) FastAPI/Uvicorn:
```bash
python -c "import fastapi, uvicorn; print('OK API')"
```

Jika semua “OK”, Anda siap lanjut.

------------------------------------------------------------

## 9) Menjalankan Contoh Pertama

- Script pipeline ML:
  - python labs/03-ml-pipeline.py
- RAG (setelah isi .env):
  - python labs/06-rag-chatbot/ingest.py
  - python labs/06-rag-chatbot/app.py
- API model:
  - uvicorn labs.07-fastapi-ml.main:app --reload
- MLflow UI:
  - mlflow ui --port 5000

Detail tiap langkah ada di modul docs/ lainnya.

------------------------------------------------------------

## 10) Troubleshooting (Masalah Umum)

- “python: command not found” / tidak dikenali:
  - Pastikan saat install Python centang “Add to PATH” (Windows), atau buka terminal baru.
  - macOS/Linux: gunakan python3 dan pip3 jika perlu.

- Gagal install paket (timeout/SSL):
  - Coba ulang, pastikan koneksi internet stabil.
  - Upgrade pip/setuptools/wheel:
    - python -m pip install --upgrade pip setuptools wheel

- FAISS error di Windows lama:
  - Pastikan versi Python 64-bit dan paket “faiss-cpu” terbaru.
  - Alternatif: gunakan vector store lain (mis. ChromaDB). Modul RAG akan kami buat fleksibel.

- PyTorch GPU tidak terdeteksi:
  - Cek nvidia-smi
  - Pastikan memasang wheel yang sesuai (cu121 atau yang direkomendasikan situs PyTorch).
  - Gunakan driver NVIDIA terbaru.

- Permission error saat ipykernel install:
  - Tambahkan --user (sudah ada di perintah di atas), atau jalankan terminal sebagai user biasa (bukan admin) dan pastikan venv aktif.

- Konflik versi paket:
  - Buat venv baru dari nol, lalu pip install -r requirements.txt kembali.

------------------------------------------------------------

Selesai. Lanjutkan ke:
- docs/05-ml-dasar.md (konsep ML inti dan evaluasi)
- labs/03-ml-pipeline.py (praktik cepat pipeline tabular)

Selamat belajar dan bereksperimen!
