# 14 — Monitoring, Logging, dan Healthcheck (Bahasa Sederhana)

Tujuan:
- Menerapkan logging yang rapi pada aplikasi (FastAPI).
- Menyediakan healthcheck, readiness, dan basic metrics.
- Praktik sederhana untuk observability (log, metrics, traces ringan).

Fokus: langkah praktis, mudah diterapkan di project kecil-menengah.

------------------------------------------------------------

## 1) Konsep Singkat

- Logging: jejak kejadian aplikasi (info/warning/error), bahan debugging dan audit.
- Monitoring: mengamati performa (latensi, error rate, throughput).
- Healthcheck:
  - Liveness: “apakah proses masih hidup?”
  - Readiness: “apakah siap melayani (dependensi siap, model termuat)?”

Hasil akhir yang diinginkan:
- Log yang konsisten (format, level).
- Endpoint /health yang jelas statusnya.
- (Opsional) Metrics dasar (request count, latensi) untuk grafik/alert.

------------------------------------------------------------

## 2) Logging Praktis di FastAPI

Contoh pola logging memakai loguru (sudah di requirements.txt):
```python
# contoh_snippet_logging.py
from loguru import logger
from fastapi import FastAPI, Request
import time

app = FastAPI()

# Middleware sederhana: catat waktu proses setiap request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} {response.status_code} {duration_ms:.2f}ms")
    return response

@app.get("/health")

def health():
    return {"status": "ok"}
```

Tips:
- Simpan log ke stdout (container-friendly) dan/atau file (rotasi harian).
- Gunakan level:
  - debug: detail pengembangan
  - info: kejadian biasa
  - warning: ada hal aneh tapi belum error
  - error: kegagalan yang perlu tindakan
- Jangan log data sensitif (PII, API key).

Konfigurasi Uvicorn supaya akses log aktif:
- Jalankan dengan `--log-level info` (default) dan `--proxy-headers` jika di belakang reverse proxy.

------------------------------------------------------------

## 3) Healthcheck, Readiness, dan Model Status

Di layanan model (labs/07-fastapi-ml/main.py) sudah ada /health dengan field:
- status: “ok”
- model_loaded: True/False
- error: pesan jika load gagal

Readiness (opsional):
- Tambahkan endpoint /ready yang mengembalikan ok hanya jika model dan dependensi lain siap.
- Gunakan untuk orchestrator (Kubernetes) agar tidak mengirim trafik sebelum siap.

Contoh:
```python
@app.get("/ready")

def ready():
    is_ready = _model is not None  # tambahkan cek dependensi lain bila ada
    return {"ready": is_ready}
```

------------------------------------------------------------

## 4) Metrics Dasar (Opsional)

Jika ingin kumpulkan metrics Prometheus:
- Tambah paket: prometheus-client
- Expose endpoint /metrics

Contoh ringkas:
```python
# pip install prometheus-client
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

REQUEST_COUNT = Counter("app_requests_total", "Total request", ["method","endpoint","http_status"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    import time
    start = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(time.time() - start)
    return response

@app.get("/metrics")

def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

Dengan ini, Anda bisa scrape metrics dengan Prometheus dan menampilkannya di Grafana.

------------------------------------------------------------

## 5) Penanganan Error

- Tangani error yang mungkin dipicu oleh input user (validasi dengan Pydantic).
- Tangkap exception tak terduga dan log errornya.
- Kembalikan HTTP status code yang sesuai (400 untuk input invalid, 500 untuk internal error).
- Jangan bocorkan stack trace di produksi; log di server, balas pesan ringkas ke user.

Contoh handler global:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```

------------------------------------------------------------

## 6) Rotasi Log (Jika Simpan ke File)

- Gunakan loguru/sistem logging untuk rotasi file per ukuran/tanggal.
- Contoh loguru:
```python
from loguru import logger
logger.add("logs/app_{time}.log", rotation="1 day", retention="7 days")
```

Di container, lebih umum menulis ke stdout dan serahkan rotasi ke platform logging (Docker/K8s/Cloud).

------------------------------------------------------------

## 7) Observability Checklist

- [ ] /health mengembalikan status ok + info singkat
- [ ] (Opsional) /ready untuk readiness check
- [ ] Logging request (method, path, status, durasi)
- [ ] Tangkap dan log error tak terduga
- [ ] (Opsional) Ekspos /metrics Prometheus (request count/latency)
- [ ] Hindari log data sensitif dan batasi ukuran payload

Lanjut ke:
- docs/15-etika-keamanan.md untuk praktik etika, privasi, dan keamanan model/aplikasi AI.
