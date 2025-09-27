# 13 — CI/CD Sederhana dengan GitHub Actions (Lint, Test, Build)

Tujuan:
- Menjalankan pengecekan otomatis saat push/PR: linting, format check, dan cek sintaks.
- Menjaga kualitas kode agar stabil dan konsisten.
- Menyediakan pijakan untuk pipeline build/deploy yang lebih lanjut.

Repo ini sudah menyertakan workflow minimal di:
- .github/workflows/ci.yml

------------------------------------------------------------

## 1) Konsep Singkat CI/CD

- CI (Continuous Integration): setiap perubahan kode akan di-cek otomatis (lint, test, build) di server (GitHub Actions).
- CD (Continuous Delivery/Deployment): melanjutkan hasil CI untuk otomatis rilis/publish/deploy (opsional, tidak dibahas penuh di sini).

Manfaat:
- Menghindari kode “rusak” masuk ke main branch.
- Konsistensi format dan standar kualitas.
- Memudahkan kolaborasi tim (PR dilengkapi status check).

------------------------------------------------------------

## 2) Isi Workflow yang Disediakan (Ringkas)

File: .github/workflows/ci.yml (sudah ada di repo)
- Menjalankan di ubuntu-latest setiap push dan pull_request.
- Memasang Python 3.11.
- Menginstall dev tools ringan: ruff, black, isort (tanpa Torch/Faiss yang berat).
- Menjalankan:
  - ruff check ai-engineering-roadmap
  - black --check ai-engineering-roadmap
  - isort --check-only ai-engineering-roadmap
  - python -m compileall -q ai-engineering-roadmap (cek sintaks)

Kenapa tidak install semua requirements?
- Banyak paket berat (torch, faiss) yang memperlambat CI dan sering tidak diperlukan untuk lint/syntax check.
- Untuk test yang benar-benar butuh dependensi berat, buat job terpisah.

------------------------------------------------------------

## 3) Menambahkan Unit Test (Opsional)

Struktur sederhana:
```
ai-engineering-roadmap/
├─ tests/
│  ├─ test_example.py
```

Contoh test:
```python
# ai-engineering-roadmap/tests/test_example.py
def test_math():
    assert 1 + 1 == 2
```

Ubah workflow agar install pytest dan menjalankannya (kalau belum terpasang di requirements):
- Pastikan dev tools sudah termasuk pytest (requirements.txt sudah menyediakan).
- Tambahkan langkah:
```yaml
- name: Run pytest
  run: pytest -q ai-engineering-roadmap/tests
```

Catatan:
- Untuk test yang melibatkan model besar/unduhan data, gunakan mocking atau dataset kecil.
- Pisahkan job “quick tests” dan “heavy tests” (kendalikan via path filter atau label PR).

------------------------------------------------------------

## 4) Rilis Docker Image (Opsional)

Jika ingin push Docker image ke registry (mis. GHCR/Docker Hub) setelah CI sukses:

Contoh langkah tambahan (garis besar):
```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    file: ai-engineering-roadmap/labs/07-fastapi-ml/Dockerfile
    push: true
    tags: yourname/fastapi-ml:latest
```

Catatan:
- Simpan kredensial sebagai GitHub Secrets, jangan di-commit.
- Pastikan ukuran image tidak membengkak (gunakan base image slim dan cache).

------------------------------------------------------------

## 5) Good Practices

- Jalankan format otomatis lokal sebelum commit:
  - black ai-engineering-roadmap
  - isort ai-engineering-roadmap
  - ruff check ai-engineering-roadmap (atau ruff --fix untuk perbaiki otomatis)
- Gunakan pre-commit hooks (opsional) agar lint/format berjalan sebelum commit:
  - pip install pre-commit
  - Buat .pre-commit-config.yaml, lalu pre-commit install
- Kelola secrets di Settings → Secrets and variables → Actions
- Pisahkan job cepat vs berat:
  - lint/syntax → cepat
  - test berat (GPU/torch) → opsional, jalankan saat rilis/cabang tertentu

------------------------------------------------------------

## 6) Checklist

- [ ] CI lint + syntax check jalan saat push/PR
- [ ] (Opsional) Unit test dasar berjalan
- [ ] (Opsional) Build/push Docker image dengan secrets
- [ ] Standar format konsisten (black/isort/ruff)

Lanjut ke:
- docs/14-monitoring-logging.md untuk menambah logging, healthcheck, dan monitoring dasar pada layanan Anda.
