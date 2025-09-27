# 05 — Dasar Machine Learning (sklearn) — Bahasa Sederhana

Tujuan modul:
- Paham konsep inti ML: fitur, label, train/val/test, overfitting.
- Paham metrik evaluasi yang tepat (regresi vs klasifikasi).
- Paham preprocessing data tabular (numerik vs kategori).
- Paham cara membuat Pipeline yang rapi di scikit-learn.

Jika ingin langsung praktik, lihat file labs/03-ml-pipeline.py (runnable).

------------------------------------------------------------

## 1) Inti Machine Learning

- Fitur (features): kolom-kolom yang menjelaskan data (mis. luas bangunan, jumlah kamar).
- Label/Target: hal yang ingin diprediksi (mis. harga rumah).
- Supervised Learning: ada label (regresi/klasifikasi).
- Unsupervised Learning: tidak ada label (clustering, reduksi dimensi).

Hati-hati “data leakage”: jangan sampai informasi dari data uji (test) bocor saat melatih model.

------------------------------------------------------------

## 2) Split Data: Train / Validation / Test

Kenapa split?
- Train: dipakai untuk melatih model.
- Validation: untuk mencoba berbagai setting (hyperparameter) dan memilih yang terbaik.
- Test: untuk mengukur performa akhir secara jujur (tidak pernah disentuh saat training/tuning).

Contoh (sklearn):
```python
from sklearn.model_selection import train_test_split

# X: fitur (DataFrame/array), y: label/target (Series/array)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test   = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
# Hasil: 70% train, 15% val, 15% test
```

Catatan:
- Untuk klasifikasi tak seimbang, gunakan stratify=y agar proporsi kelas seimbang di setiap split.

------------------------------------------------------------

## 3) Metrik Evaluasi (Pilih yang Tepat)

Regresi (prediksi angka):
- MAE (Mean Absolute Error): rata-rata selisih absolut.
- MSE (Mean Squared Error): penalti lebih besar untuk error besar.
- RMSE: akar dari MSE, satuannya sama dengan target.
- R²: seberapa banyak variasi target yang dijelaskan model (0–1, makin tinggi makin baik).

Klasifikasi:
- Accuracy: persentase benar. Mudah, tapi bisa menipu pada data tidak seimbang.
- Precision: dari semua prediksi positif, berapa yang benar positif?
- Recall: dari semua positif sebenarnya, berapa yang berhasil ditangkap?
- F1: rata-rata harmonik precision dan recall (bagus untuk data imbang maupun tidak imbang).
- ROC-AUC / PR-AUC: menilai kualitas probabilitas pada berbagai threshold.

Tip:
- Untuk data tidak seimbang (mis. fraud 1%), gunakan F1, ROC-AUC, atau PR-AUC; jangan hanya accuracy.

------------------------------------------------------------

## 4) Preprocessing: Numerik vs Kategori

- Numerik: scaling (StandardScaler/MinMaxScaler), imputasi nilai hilang (SimpleImputer).
- Kategori: One-Hot Encoding (OneHotEncoder) untuk ubah teks → kolom biner.
- Lakukan preprocessing di dalam Pipeline agar tidak “bocor” dan mudah diulang.

Contoh ColumnTransformer + Pipeline:
```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

df = pd.read_csv("datasets/housing.csv")  # contoh; lihat labs/03-ml-pipeline.py untuk versi runnable
y = df["price"]
X = df.drop(columns=["price"])

num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()

numeric_tf = Pipeline(steps=[
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler())
])

categorical_tf = Pipeline(steps=[
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_tf, num_cols),
        ("cat", categorical_tf, cat_cols),
    ]
)

model = Pipeline(steps=[
    ("prep", preprocess),
    ("reg", LinearRegression())
])
```

Keuntungan Pipeline:
- Mengikat preprocessing dan model dalam satu objek.
- Menghindari kebocoran data (fit hanya di data train).
- Memudahkan deploy (satu objek untuk predict).

------------------------------------------------------------

## 5) Overfitting vs Underfitting

- Overfitting: Model “menghafal” data train, performa turun pada val/test.
- Underfitting: Model terlalu sederhana dan gagal menangkap pola.
- Ciri:
  - Overfitting: train score tinggi, val/test score rendah
  - Underfitting: train dan val/test sama-sama buruk
- Solusi:
  - Tambah data/pembersihan fitur
  - Regularisasi (Ridge/Lasso), dropout (untuk DL)
  - Simpler model atau tuning hyperparameter
  - Early stopping (untuk DL)

------------------------------------------------------------

## 6) Cross-Validation (CV)

Gunakan K-Fold CV untuk estimasi performa yang lebih stabil.
```python
from sklearn.model_selection import cross_val_score, KFold
import numpy as np

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring="neg_root_mean_squared_error")
rmse_scores = -scores
print("RMSE per fold:", rmse_scores)
print("RMSE rata-rata:", np.mean(rmse_scores))
```

Catatan:
- Pilih scoring sesuai tugas (regresi/klasifikasi).
- Untuk klasifikasi tak seimbang, pertimbangkan StratifiedKFold.

------------------------------------------------------------

## 7) Baseline Dulu, Baru Tuning

- Mulai dari baseline (model sederhana): LinearRegression/LogisticRegression.
- Catat metrik, lalu bandingkan dengan model yang lebih kompleks (RandomForest, XGBoost, dll.).
- Hindari tuning berlebihan sebelum baseline yang kuat.

------------------------------------------------------------

## 8) Reproducibility dan Tracking

- Tetapkan random_state agar hasil bisa diulang.
- Simpan eksperimen (param, metrik, artifact) dengan MLflow.

Cuplikan MLflow:
```python
import mlflow
with mlflow.start_run():
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_metric("rmse", 1234.56)
    # mlflow.sklearn.log_model(model, "model")
```

------------------------------------------------------------

## 9) Alur Praktik Cepat (Tabular)

1) Muat data → cek missing/duplikat.
2) Bagi data → train/val/test (ingat stratify jika klasifikasi).
3) Definisikan kolom numerik/kategori.
4) Buat ColumnTransformer + Pipeline.
5) Latih di train → evaluasi di val (atau CV).
6) Cek overfitting/underfitting → perbaiki.
7) Final fit pada gabungan train+val → uji di test.
8) Simpan model (joblib) + catat hasil (MLflow).

------------------------------------------------------------

## 10) Checklist

- [ ] Pahami fitur, label, dan hindari data leakage
- [ ] Gunakan train/val/test yang benar
- [ ] Pilih metrik sesuai tugas
- [ ] Gunakan preprocessing terpisah untuk numerik/kategori
- [ ] Bungkus semua dalam Pipeline
- [ ] Mulai dari baseline, lalu tingkatkan
- [ ] Catat eksperimen dengan MLflow

Lanjutkan ke:
- labs/03-ml-pipeline.py untuk praktik lengkap dan runnable.
- docs/07-deep-learning-pytorch.md untuk masuk ke Deep Learning.
