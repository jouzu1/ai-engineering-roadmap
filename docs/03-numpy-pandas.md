# 03 — NumPy dan Pandas Dasar (Bahasa Sederhana)

Tujuan:
- Paham apa itu NumPy (untuk operasi numerik) dan Pandas (untuk data tabular).
- Bisa memuat CSV, melihat ringkasan data, memilih kolom/baris, filter, agregasi.
- Praktik cepat cleaning data: missing values, duplikat, tipe data.

Jika ingin praktik interaktif, gunakan notebook labs/01-numpy-pandas.ipynb (akan disediakan) atau jalankan potongan kode ini di Python REPL.

------------------------------------------------------------

## 1) NumPy Singkat
NumPy menyediakan array cepat (ndarray) untuk komputasi numerik.

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)       # [11 22 33]
print(a * 2)       # [2 4 6]
print(a.mean())    # 2.0

# Matriks 2D
M = np.array([[1,2],[3,4]])
print(M.shape)    # (2, 2)
print(M @ M)       # perkalian matriks
```

Kapan pakai NumPy?
- Operasi numerik intensif, vectorization, linear algebra, pembuatan data sintetis.

------------------------------------------------------------

## 2) Pandas: Memuat Data dan Melihat Ringkasan
Pandas menggunakan DataFrame untuk data tabular (baris-kolom).

```python
import pandas as pd

# Contoh membuat DataFrame sederhana
df = pd.DataFrame({
    "city": ["A","B","A","C"],
    "area": [80, 120, 60, 100],
    "rooms": [3, 5, 2, 4],
    "price": [200_000, 400_000, 150_000, 300_000],
})

print(df.head())       # lihat 5 baris pertama
print(df.info())       # tipe data per kolom
print(df.describe())   # statistik ringkas kolom numerik
```

Memuat CSV:
```python
df = pd.read_csv("datasets/raw/housing.csv")  # ganti path sesuai file Anda
```

Menyimpan ke CSV:
```python
df.to_csv("datasets/processed/housing_clean.csv", index=False)
```


------------------------------------------------------------

## 3) Seleksi Kolom/Baris dan Filter
```python
# Kolom
areas = df["area"]                # Series
sub = df[["area", "rooms"]]       # DataFrame

# Baris
row0 = df.iloc[0]                 # baris ke-0 (berdasarkan posisi)
row_mask = df["city"] == "A"
dfa = df[row_mask]  # filter baris city == "A"

# Kondisi gabungan
df_big = df[(df["area"] > 90) & (df["rooms"] >= 4)]
```

------------------------------------------------------------

## 4) Agregasi dan GroupBy
```python
# Rata-rata harga per kota
avg_price = df.groupby("city")["price"].mean().reset_index()
print(avg_price)

# Banyaknya baris per kota
counts = df["city"].value_counts()
print(counts)
```

Pivot table (ringkas):
```python
# Rata-rata harga per kota dan jumlah kamar
pivot = df.pivot_table(values="price", index="city", columns="rooms", aggfunc="mean")
print(pivot)
```

------------------------------------------------------------

## 5) Handling Missing Values dan Duplikat
```python
# Cek missing
print(df.isna().sum())

# Isi missing dengan rata-rata (kolom numerik)
df["area"] = df["area"].fillna(df["area"].mean())

# Hapus baris yang masih memiliki missing di kolom penting
df = df.dropna(subset=["price"])

# Hapus duplikat baris
df = df.drop_duplicates()
```

Ubah tipe data:
```python
df["rooms"] = df["rooms"].astype(int)
```

------------------------------------------------------------

## 6) Feature Engineering Ringkas
```python
# Buat fitur baru: price_per_m2
df["price_per_m2"] = df["price"] / df["area"]

# Binning area (kecil/sedang/besar)
bins = [0, 70, 100, float("inf")]
labels = ["small", "medium", "large"]
df["area_bin"] = pd.cut(df["area"], bins=bins, labels=labels)
```

Encoding kategori (untuk ML pipeline lengkap, lihat modul 06):
```python
# One-hot encoding cepat (untuk eksplorasi)
df_enc = pd.get_dummies(df, columns=["city"], drop_first=True)
```

------------------------------------------------------------

## 7) Join/Merge DataFrame
```python
cities = pd.DataFrame({
    "city": ["A","B","C"],
    "region": ["North","East","West"]
})

merged = df.merge(cities, on="city", how="left")
print(merged.head())
```

------------------------------------------------------------

## 8) Alur Praktik Cepat
1) Muat CSV → df = pd.read_csv(...)
2) Inspeksi (head, info, describe)
3) Tangani missing/duplikat/tipe data
4) Buat fitur baru seperlunya
5) GroupBy/pivot untuk insight awal
6) Simpan ke datasets/processed/... untuk tahap ML

------------------------------------------------------------

## 9) Troubleshooting Singkat
- UnicodeDecodeError saat read_csv: coba `encoding="utf-8"` atau `errors="ignore"`.
- Memori habis: gunakan `usecols=...` atau `chunksize=...` untuk baca bertahap.
- Tanggal: parsing dengan `parse_dates=[...]` dan `pd.to_datetime(...)`.

------------------------------------------------------------

Checklist:
- [ ] Bisa memuat, melihat ringkasan, dan menyimpan CSV
- [ ] Bisa seleksi kolom/baris dan filter kondisi
- [ ] Bisa agregasi (groupby/pivot) untuk insight
- [ ] Bisa cleaning dasar (missing, duplikat, dtype)
- [ ] Bisa feature engineering sederhana

Lanjut ke:
- docs/04-visualisasi.md untuk plotting cepat (Matplotlib/Seaborn).
