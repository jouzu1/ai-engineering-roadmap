# 11 — Deploy Model dengan FastAPI + Docker (Bahasa Sederhana)

Tujuan modul:
- Bungkus model ML jadi layanan web (API) menggunakan FastAPI.
- Jalankan API secara lokal.
- Bungkus API ke dalam Docker image sehingga mudah dipindah/deploy.

Kita akan menggunakan model dari labs/03-ml-pipeline.py yang menyimpan file model di:
- labs/07-fastapi-ml/model.joblib

Endpoint yang disediakan:
- GET /health → cek status
- POST /predict → prediksi 1 data
- POST /predict_batch → prediksi banyak data sekaligus

------------------------------------------------------------

## 1) Siapkan Model
Jalankan script untuk membuat model terlebih dahulu (jika belum):

```
python labs/03-ml-pipeline.py --n-samples 1500 --random-state 42
```

Output:
- File model tersimpan di labs/07-fastapi-ml/model.joblib

------------------------------------------------------------

## 2) Jalankan API Secara Lokal (tanpa Docker)

Jalankan server:
```
python labs/07-fastapi-ml/main.py
```

Default port: 8000 (bisa diatur via .env: APP_PORT=8000)

Cek health:
```
curl http://127.0.0.1:8000/health
```

Respons contoh:
```json
{"status":"ok","model_loaded":true}
```

Coba prediksi satu data (contoh fitur sesuai dataset sintetis):
```
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 90.5,
    "rooms": 4,
    "age": 10,
    "city": "A",
    "condition": "good"
  }'
```

Respons contoh:
```json
{"prediction":[345678.12]}
```

Coba prediksi batch:
```
curl -X POST http://127.0.0.1:8000/predict_batch \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"area": 80, "rooms": 3, "age": 15, "city": "B", "condition": "fair"},
      {"area": 120, "rooms": 5, "age": 5, "city": "A", "condition": "good"}
    ]
  }'
```

Dokumentasi interaktif (Swagger UI):
- Buka di browser: http://127.0.0.1:8000/docs

------------------------------------------------------------

## 3) Bungkus ke Docker

Pastikan Docker terpasang (Docker Desktop untuk Windows/macOS).

Bangun image dari root repo (ai-engineering-roadmap):
```
docker build -f labs/07-fastapi-ml/Dockerfile -t fastapi-ml .
```

Jalankan container:
```
docker run --rm -p 8000:8000 --env-file .env fastapi-ml
```

Tes health:
```
curl http://127.0.0.1:8000/health
```

Jika Anda belum punya file .env, salin dari template:
```
copy .env.example .env           # Windows PowerShell
# cp .env.example .env          # macOS/Linux
```

Catatan:
- Secara default, file model sudah dibundel karena kita menyalin seluruh repo ke dalam image (lihat Dockerfile). Jika Anda menyimpan model di lokasi lain, sesuaikan COPY di Dockerfile.
- Untuk mengurangi ukuran image, Anda bisa menambahkan .dockerignore dan menyalin file seperlunya saja.

------------------------------------------------------------

## 4) Strukur File Terkait
- labs/03-ml-pipeline.py → membuat model.joblib
- labs/07-fastapi-ml/main.py → kode FastAPI (API)
- labs/07-fastapi-ml/Dockerfile → definisi image Docker

------------------------------------------------------------

## 5) Tips Produksi (Ringkas)
- Logging & Monitoring: catat request/response ringkas dan error. Tambahkan tools monitoring bila perlu.
- Konfigurasi via environment (.env) — jangan hardcode kunci/API key.
- Versi model: simpan checksum/versi model di response /health untuk audit.
- Keamanan:
  - Batasi CORS (asal domain yang diizinkan) pada produksi.
  - Validasi input dan batasi ukuran payload.
  - Jangan memaparkan file model mentah ke publik.
- Skala: gunakan server produksi (gunicorn/uvicorn workers) + autoscaling di cloud jika trafik tinggi.
- CI/CD: otomatisasi build/push image dan deployment (lihat modul 13 CI/CD ringkas).

------------------------------------------------------------

Checklist:
- [ ] Model dibuat (model.joblib)
- [ ] API FastAPI berjalan lokal
- [ ] Image Docker berhasil dibangun
- [ ] Container berjalan dan endpoint /health → ok
- [ ] Coba prediksi satu data dan batch

Lanjutkan ke:
- docs/12-mlops-mlflow-dvc.md untuk tracking eksperimen (MLflow) dan versioning data/model (DVC).
