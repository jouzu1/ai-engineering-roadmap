# 04 — Visualisasi Data Cepat (Matplotlib & Seaborn)

Tujuan:
- Membuat grafik dasar dengan cepat: line, bar, histogram, boxplot, scatter.
- Memahami kapan memakai Matplotlib vs Seaborn.
- Tips praktis agar visual rapi dan mudah dibaca.

Jika ingin interaktif, gunakan notebook (labs/01-numpy-pandas.ipynb) atau jalankan contoh di bawah ini.

------------------------------------------------------------

## 1) Setup Dasar

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Gaya default yang rapi
sns.set_theme(style="whitegrid")
```

Contoh DataFrame sederhana:
```python
df = pd.DataFrame({
    "city": ["A","B","A","C","B","A","C"],
    "area": [80, 120, 60, 100, 95, 70, 130],
    "rooms": [3, 5, 2, 4, 4, 2, 5],
    "price": [200_000, 400_000, 150_000, 300_000, 280_000, 160_000, 420_000],
})
```

Tips umum:
- Selalu beri judul, label sumbu, dan legenda jika perlu.
- Skala angka besar: dibagi 1e6 (juta) agar mudah dibaca.

------------------------------------------------------------

## 2) Line Plot (Tren)

Line cocok untuk data berurutan (waktu/urutan).

```python
plt.figure(figsize=(6,4))
plt.plot(df.index, df["price"]/1e3, marker="o")
plt.title("Harga (ribuan)")
plt.xlabel("Index")
plt.ylabel("Price (k)")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------

## 3) Bar Plot (Perbandingan Kategori)

Perbandingan rata-rata harga per kota:
```python
avg_price = df.groupby("city")["price"].mean().reset_index()

plt.figure(figsize=(6,4))
sns.barplot(data=avg_price, x="city", y="price", palette="Blues_d")
plt.title("Rata-rata Harga per Kota")
plt.ylabel("Price")
plt.tight_layout()
plt.show()
```

Stacked bar (dengan pivot):
```python
pv = df.pivot_table(values="price", index="city", columns="rooms", aggfunc="mean")
pv.plot(kind="bar", stacked=True, figsize=(7,4))
plt.title("Harga Rata-rata (Stacked) per City & Rooms")
plt.ylabel("Price")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------

## 4) Histogram dan KDE (Distribusi)

Lihat sebaran nilai (area):
```python
plt.figure(figsize=(6,4))
sns.histplot(df["area"], bins=8, kde=True, color="teal")
plt.title("Distribusi Area")
plt.xlabel("Area (m^2)")
plt.tight_layout()
plt.show()
```

Kapan dipakai?
- Menilai distribusi (normal/skew), outlier, range.

------------------------------------------------------------

## 5) Boxplot (Sebaran & Outlier)

Bandingkan distribusi harga per kota:
```python
plt.figure(figsize=(6,4))
sns.boxplot(data=df, x="city", y="price", palette="Set2")
plt.title("Sebaran Harga per Kota")
plt.tight_layout()
plt.show()
```

Interpretasi:
- Median (garis tengah), quartile, dan outlier (titik di luar whisker).

------------------------------------------------------------

## 6) Scatter Plot (Hubungan 2 Variabel)

Hubungan area vs price:
```python
plt.figure(figsize=(6,4))
sns.scatterplot(data=df, x="area", y="price", hue="city", style="rooms", palette="deep")
plt.title("Area vs Price")
plt.tight_layout()
plt.show()
```

Tambahkan garis regresi cepat:
```python
plt.figure(figsize=(6,4))
sns.regplot(data=df, x="area", y="price", scatter_kws={"alpha":0.7}, line_kws={"color":"red"})
plt.title("Area vs Price (dengan garis tren)")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------

## 7) Pairplot (Eksplorasi Cepat Banyak Variabel)

Eksplor hubungan beberapa kolom numerik:
```python
sns.pairplot(df[["area","rooms","price"]], corner=True)
plt.show()
```

Catatan:
- Untuk dataset besar, pairplot bisa lambat. Sampling dulu jika perlu.

------------------------------------------------------------

## 8) Korelasi (Heatmap)

```python
import numpy as np

num_cols = df.select_dtypes(include=np.number).columns
corr = df[num_cols].corr()

plt.figure(figsize=(5,4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Korelasi Numerik")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------

## 9) Tips Praktis

- Ukuran figur: `plt.figure(figsize=(w,h))` sebelum plot.
- Rotasi label: `plt.xticks(rotation=45)` untuk label kategori panjang.
- Format sumbu: gunakan fungsi bantu (mis. matplotlib.ticker) untuk format ribuan.
- Simpan gambar: `plt.savefig("plots/plot1.png", dpi=150, bbox_inches="tight")`.

------------------------------------------------------------

Checklist:
- [ ] Membuat line/bar/hist/box/scatter dengan label yang jelas
- [ ] Menilai distribusi dan outlier dengan hist/box
- [ ] Membuat pairplot dan heatmap korelasi untuk eksplorasi awal
- [ ] Menyimpan plot ke file untuk laporan

Lanjut ke:
- docs/05-ml-dasar.md untuk mulai membangun model ML.
