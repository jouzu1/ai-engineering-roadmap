# Dockerfile untuk layanan FastAPI (model sklearn)
# Build context: root repo (ai-engineering-roadmap berada di bawah /app setelah COPY . .)
# Build image:
#   docker build -f labs/07-fastapi-ml/Dockerfile -t fastapi-ml .
# Run container:
#   docker run --rm -p 8000:8000 --env-file .env fastapi-ml

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Salin requirements lalu install (cache layer lebih efisien)
COPY ai-engineering-roadmap/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh repo agar model.joblib dan kode tersedia
COPY . /app

# Konfigurasi default (bisa diubah via --env-file .env)
ENV APP_ENV=production \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    LOG_LEVEL=info

EXPOSE 8000

# Jalankan layanan langsung via Python (menghindari isu modul dengan nama folder ber-hyphen)
CMD ["python", "ai-engineering-roadmap/labs/07-fastapi-ml/main.py"]
