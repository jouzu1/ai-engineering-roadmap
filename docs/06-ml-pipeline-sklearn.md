# 06 — Pipeline scikit-learn untuk Data Tabular (Bahasa Sederhana)

Tujuan:
- Memahami kenapa perlu Pipeline (rapi, aman dari data leakage, mudah deploy).
- Membangun preprocessing numerik dan kategori dengan ColumnTransformer.
- Menggabungkan preprocessing + model (Linear/Tree/Forest) dalam satu Pipeline.
- Melakukan tuning sederhana (GridSearchCV) dan menyimpan model (joblib).

Untuk praktik runnable, lihat labs/03-ml-pipeline.py.

------------------------------------------------------------

## 1) Kenapa Pipeline?

Tanpa pipeline:
- Anda melakukan imputasi/scaling/encoding manual → berisiko bocor (fit di seluruh data).
- Susah mengulang langkah yang sama di data baru (val/test/produksi).

Dengan Pipeline:
- Semua langkah (preprocessing → model) “terikat” jadi satu objek.
- Fit hanya pada data training (aman), transform otomatis pada val/test.
- Mudah disimpan dan dipakai ulang (joblib).

------------------------------------------------------------

## 2) Preprocessing Numerik vs Kategori

- Numerik: tangani missing (impute), scaling (StandardScaler/MinMaxScaler).
- Kategori: impute most_frequent, OneHotEncoder(handle_unknown="ignore").

Contoh template:
```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

df = pd.read_csv("datasets/housing.csv")  # contoh
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

------------------------------------------------------------

## 3) Split Data dan Evaluasi

Selalu bagi data agar evaluasi jujur.
```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)
pred = model.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared=False)
print("RMSE:", rmse)
```

Untuk klasifikasi, gunakan metrik sesuai (accuracy/f1/roc-auc).

------------------------------------------------------------

## 4) Tuning Sederhana (GridSearchCV)

Tuning hyperparameter di dalam pipeline aman dan rapi. Nama langkah dipakai sebagai prefix.

Contoh: ganti model ke RandomForestRegressor lalu grid search jumlah pohon dan kedalaman.
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

rf_model = Pipeline(steps=[
    ("prep", preprocess),
    ("rf", RandomForestRegressor(random_state=42))
])

param_grid = {
    "rf__n_estimators": [100, 300],
    "rf__max_depth": [None, 10, 20]
}

grid = GridSearchCV(
    rf_model,
    param_grid=param_grid,
    scoring="neg_root_mean_squared_error",
    cv=3,
    n_jobs=-1
)
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
print("Best CV RMSE:", -grid.best_score_)

best = grid.best_estimator_
test_rmse = mean_squared_error(y_test, best.predict(X_test), squared=False)
print("Test RMSE:", test_rmse)
```

Tips:
- Gunakan prefix langkah (“rf__”) untuk mengakses hyperparameter model di pipeline.
- Pilih scoring sesuai tugas (regresi/klasifikasi).
- CV 3–5 cukup untuk awal; perbesar jika data kecil.

------------------------------------------------------------

## 5) Simpan dan Muat Model (joblib)

```python
import joblib

joblib.dump(best, "models/housing_rf.joblib")

# Muat ulang
model2 = joblib.load("models/housing_rf.joblib")
yhat = model2.predict(X_test)  # langsung bisa dipakai
```

Keuntungan:
- Pipeline menyimpan seluruh preprocessing + model → tidak perlu ulang encoding/scaling.
- Cocok untuk dipakai di FastAPI (lihat modul 11).

------------------------------------------------------------

## 6) Avoiding Data Leakage

Data leakage = informasi dari val/test “bocor” saat training.
- Contoh: menghitung mean untuk imputasi di seluruh data sebelum split.
- Hindari dengan pipeline fit di train saja; transform otomatis di val/test.

Checklist anti-leak:
- [ ] Selalu split sebelum fit preprocessing
- [ ] Semua transform dimasukkan ke Pipeline/ColumnTransformer
- [ ] Gunakan GridSearchCV pada pipeline, bukan pada data yang sudah transform manual

------------------------------------------------------------

## 7) Monitoring dan Reproducibility

- Set random_state pada model yang mendukung (untuk hasil konsisten).
- Log semua eksperimen dengan MLflow (lihat modul 12).
- Simpan versi dataset dan model (DVC).

Cuplikan MLflow (ringkas):
```python
import mlflow
with mlflow.start_run():
    mlflow.log_param("model", "RandomForestRegressor")
    mlflow.log_param("n_estimators", 300)
    mlflow.log_metric("rmse_test", float(test_rmse))
```

------------------------------------------------------------

## 8) Kesalahan Umum

- “ValueError: columns mismatch” saat predict:
  - Struktur kolom input beda (nama/urutan/tipe). Pastikan format sama seperti training.
- OneHotEncoder error pada kategori baru:
  - Pastikan handle_unknown="ignore".
- Skewed target:
  - Coba transform target (log1p) dan balikkan prediksi dengan expm1. Atau pakai model yang robust.

------------------------------------------------------------

## 9) Checklist

- [ ] Tentukan num_cols dan cat_cols dengan benar
- [ ] Gunakan SimpleImputer + scaler untuk numerik
- [ ] Gunakan OneHotEncoder(handle_unknown="ignore") untuk kategori
- [ ] Bungkus dengan Pipeline
- [ ] Split train/test sebelum fit
- [ ] Tuning sederhana dengan GridSearchCV di atas pipeline
- [ ] Simpan pipeline terlatih (joblib) untuk deploy

Lanjut ke:
- docs/07-deep-learning-pytorch.md untuk masuk ke DL, atau
- docs/11-deploy-fastapi-docker.md untuk konsumsi pipeline di API.
