# 12 — MLOps Dasar: MLflow (Tracking) dan DVC (Versioning Data/Model)

Tujuan modul:
- Mencatat eksperimen (parameter, metrik, artifact) dengan MLflow.
- Mem-versioning data dan model dengan DVC agar reproducible.
- Menjalankan pipeline sederhana end-to-end.

Catatan: Fokus pada praktik dan langkah-langkah mudah. Anda bisa memperluas ke CI/CD dan deployment model registry di tahap lanjut.

------------------------------------------------------------

## 1) MLflow — Tracking Eksperimen

Kenapa penting?
- Mengetahui pengaturan (hyperparameter) apa yang menghasilkan performa paling bagus.
- Membandingkan eksperimen dengan rapi (param → metric → artifact).
- Memudahkan kerja tim (UI untuk melihat hasil).

Instalasi (sudah ada di requirements.txt):
- mlflow

Menjalankan UI lokal:
```
mlflow ui --port 5000
```
Buka http://127.0.0.1:5000 untuk melihat dashboard eksperimen.

Contoh penggunaan (Python):
```python
import mlflow
import mlflow.sklearn

with mlflow.start_run(run_name="contoh-run"):
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_param("n_samples", 1000)
    # ... latih model dan hitung metrik ...
    rmse = 1234.56
    mlflow.log_metric("rmse", rmse)
    # Simpan model sebagai artifact:
    # mlflow.sklearn.log_model(model, "model")
```

Integrasi contoh di repo ini:
- labs/03-ml-pipeline.py sudah punya helper maybe_log_mlflow() supaya Anda bisa melihat run di UI (jika MLflow terpasang dan env `MLFLOW_TRACKING_URI` di-set, mis. http://127.0.0.1:5000)

Tips:
- Tambahkan run_name yang informatif.
- Log parameter kunci (learning rate, arsitektur, dsb.).
- Log metric utama dan mungkin beberapa metric tambahan (mis. waktu training, ukuran model).

------------------------------------------------------------

## 2) DVC — Versioning Data dan Model

Kenapa DVC?
- Git bagus untuk kode, tetapi tidak efisien untuk file besar (dataset/model).
- DVC menyimpan metadata di Git, sementara file besarnya disimpan di remote storage (S3/Drive/minio/SSH/…).
- Mudah mengembalikan ke versi dataset/model tertentu.

Instalasi (sudah ada di requirements.txt):
- dvc

Inisialisasi di root repo:
```
dvc init
```
Ini menambahkan folder `.dvc/` dan konfigurasi dasar.

Menambahkan dataset (contoh):
- Misal Anda punya `datasets/raw/housing.csv`
```
dvc add datasets/raw/housing.csv
git add datasets/raw/housing.csv.dvc .gitignore
git commit -m "Track raw dataset with DVC"
```
Sekarang file besar tidak langsung masuk Git, tapi dilacak via DVC.

Konfigurasi remote (opsional):
- Contoh S3:
```
dvc remote add -d myremote s3://bucket-nama/proyek-ku
dvc push   # kirim data ke remote
```
- Contoh lokal (folder di disk lain):
```
dvc remote add -d localremote /path/ke/folder-penyimpanan
dvc push
```

Menambahkan model hasil training:
- Setelah latihan, simpan model ke `models/model.joblib`
```
dvc add models/model.joblib
git add models/model.joblib.dvc .gitignore
git commit -m "Track trained model with DVC"
dvc push
```

Menarik ulang data/model (di mesin lain):
```
git clone ...
pip install -r requirements.txt
dvc pull  # ambil data/model sesuai versi Git
```

------------------------------------------------------------

## 3) Pipeline dengan DVC (dvc.yaml dan params.yaml)

DVC bisa menjalankan pipeline (tahapan berurutan) dan melacak dependensi/keluaran.

Contoh file `dvc.yaml`:
```yaml
stages:
  prepare:
    cmd: python scripts/prepare_data.py
    deps:
      - scripts/prepare_data.py
      - datasets/raw
    outs:
      - datasets/processed

  train:
    cmd: python train.py --config params.yaml
    deps:
      - datasets/processed
      - train.py
      - params.yaml
    outs:
      - models/model.joblib
    metrics:
      - metrics.json
```

Contoh file `params.yaml`:
```yaml
train:
  random_state: 42
  n_samples: 1000
  model: "LinearRegression"
```

Menjalankan pipeline:
```
dvc repro
```
DVC akan mengeksekusi tahap yang perlu diulang sesuai perubahan dependensi.

Membandingkan hasil dua eksperimen:
```
dvc metrics show
dvc metrics diff
```

Catatan:
- Di repo ini kita belum menyediakan `scripts/prepare_data.py` dan `train.py` terpisah karena data sintetis dibuat langsung di `labs/03-ml-pipeline.py`. Saat Anda punya dataset nyata, pindahkan logika proses ke skrip-skrip terpisah dan susun `dvc.yaml` seperti di atas.

------------------------------------------------------------

## 4) Alur Praktik: MLflow + DVC

- Eksperimen:
  1) Jalankan `mlflow ui`, buka dashboard.
  2) Jalankan eksperimen dari script (mis. labs/03-ml-pipeline.py) beberapa kali dengan parameter berbeda.
  3) Lihat perbandingan metrik di UI MLflow.

- Versioning data/model:
  1) Simpan dataset di `datasets/raw/` dan `dvc add`.
  2) Simpan model di `models/` dan `dvc add`.
  3) Commit Git dan `dvc push` ke remote (opsional).
  4) Di mesin lain, `git pull` + `dvc pull` untuk dapatkan versi sama.

- Pipeline (jika diperlukan):
  1) Buat `scripts/prepare_data.py` untuk cleaning/feature engineering.
  2) Buat `train.py` yang membaca `params.yaml`.
  3) Tulis `dvc.yaml` untuk merangkai `prepare` → `train`.
  4) Jalankan `dvc repro` saat ada perubahan.

------------------------------------------------------------

## 5) Troubleshooting Singkat

- “dvc: command not found”:
  - Pastikan venv aktif dan `pip install dvc` sudah sukses.

- “dvc push error”:
  - Cek konfigurasi remote (akses, kredensial).
  - Coba `dvc remote list` untuk memastikan remote terpasang.

- MLflow run tidak muncul di UI:
  - Pastikan `mlflow ui` berjalan dan environment `MLFLOW_TRACKING_URI` sesuai (default UI lokal: http://127.0.0.1:5000).
  - Pada script, panggil `mlflow.set_tracking_uri()` jika perlu diarahkan ke server tertentu.

- Performance lambat di CI:
  - Hindari menjalankan training berat di CI (cukup lint/test cepat).
  - Gunakan caching dependencies.

------------------------------------------------------------

## 6) Checklist

- [ ] MLflow UI berjalan dan Anda melihat minimal 1 run
- [ ] Beberapa eksperimen tercatat (param + metric)
- [ ] DVC di-inisialisasi dan minimal 1 file besar dilacak
- [ ] (Opsional) DVC remote dikonfigurasi dan `dvc push` sukses
- [ ] (Opsional) dvc.yaml + params.yaml dibuat untuk pipeline proyek nyata

Lanjutkan ke:
- docs/13-ci-cd.md (opsional) untuk menyiapkan CI/CD (GitHub Actions) agar lint/test berjalan otomatis saat push.
