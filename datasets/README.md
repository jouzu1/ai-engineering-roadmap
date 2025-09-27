# datasets/ — Panduan Dataset (Bahasa Sederhana)

Folder ini berisi panduan menggunakan dataset untuk latihan di roadmap AI Engineering. Anda bisa:
- Memakai data sintetis (sudah disediakan oleh script) — cepat dan tanpa unduhan.
- Mengunduh dataset publik kecil untuk praktik nyata.
- Memakai loader bawaan library (HuggingFace datasets, torchvision).

Catatan penting:
- Hati-hati lisensi dataset publik (baca terms masing-masing).
- Jangan commit data besar ke Git. Gunakan DVC (lihat docs/12-mlops-mlflow-dvc.md).

------------------------------------------------------------

## 1) Data Sintetis (Paling Mudah, Langsung Jalan)

- labs/03-ml-pipeline.py otomatis membuat data tabular sintetis dan menyimpan model:
  - Output model: labs/07-fastapi-ml/model.joblib
- Tidak perlu file dataset eksternal.

Jalankan:
```
python labs/03-ml-pipeline.py --n-samples 1500 --random-state 42
```

------------------------------------------------------------

## 2) Dataset Publik Kecil (Contoh Direkomendasikan)

Pilih salah satu (atau beberapa) berikut untuk latihan:

A) Tabular
- California Housing (sklearn fetch) — tugas regresi:
  - Referensi: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html
  - Cara muat (contoh singkat):
    ```python
    from sklearn.datasets import fetch_california_housing
    data = fetch_california_housing(as_frame=True)
    df = data.frame  # kolom numerik
    ```
  - Simpan ke CSV jika perlu:
    ```python
    df.to_csv("datasets/raw/california_housing.csv", index=False)
    ```

- Titanic (Kaggle) — tugas klasifikasi:
  - https://www.kaggle.com/c/titanic
  - Perlu akun Kaggle dan unduh manual. Simpan di datasets/raw/titanic/.

B) NLP
- IMDB Sentiment (HuggingFace datasets):
  - https://huggingface.co/datasets/imdb
  - Cara muat:
    ```python
    from datasets import load_dataset
    ds = load_dataset("imdb")
    print(ds["train"][0])
    ```

C) CV (Computer Vision)
- CIFAR-10 (torchvision auto-download):
  - https://pytorch.org/vision/stable/datasets.html#cifar
  - Cara muat (contoh ringkas):
    ```python
    from torchvision import datasets, transforms
    tf = transforms.ToTensor()
    train_ds = datasets.CIFAR10(root="./data", train=True, download=True, transform=tf)
    ```

Tips:
- Simpan dataset mentah di datasets/raw/
- Setelah preprocessing, simpan di datasets/processed/
- Track dengan DVC:
  ```
  dvc add datasets/raw/namafile.csv
  git add datasets/raw/namafile.csv.dvc .gitignore
  git commit -m "Track dataset"
  dvc push  # jika sudah set remote
  ```

------------------------------------------------------------

## 3) Struktur Folder yang Disarankan

```
datasets/
├─ README.md
├─ raw/        # data mentah (jangan diubah)
└─ processed/  # hasil preprocessing/cleaning/feature engineering
```

- raw/ berisi file hasil unduhan asli (CSV/JSON/…)
- processed/ berisi data siap training (setelah cleaning dan split)

------------------------------------------------------------

## 4) Rekomendasi Praktik Baik

- Dokumentasikan sumber data (URL, tanggal unduh, lisensi).
- Simpan skrip pengolahan data di scripts/ (mis. scripts/prepare_data.py).
- Versikan data/model pakai DVC (lihat docs/12-mlops-mlflow-dvc.md).
- Hindari commit file besar ke Git. Gunakan .gitignore (DVC akan menambahkan otomatis).

------------------------------------------------------------

## 5) Catatan Lisensi

- Pastikan penggunaan dataset mematuhi lisensi/ketentuan sumber.
- Jangan unggah dataset berlisensi terbatas ke repo publik tanpa izin.
- Anonimkan data yang mengandung PII (data pribadi) sebelum dibagikan.

------------------------------------------------------------

## 6) Quick Checklist

- [ ] Pilih dataset (atau pakai data sintetis)
- [ ] Simpan di datasets/raw/ (atau gunakan loader bawaan)
- [ ] (Opsional) Proses ke datasets/processed/
- [ ] (Opsional) Track dengan DVC
- [ ] Dokumentasikan sumber dan langkah pembersihan
