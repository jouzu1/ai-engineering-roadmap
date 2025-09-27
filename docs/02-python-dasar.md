# 02 — Python Dasar (Bahasa Sederhana)

Tujuan:
- Memahami tipe data dasar, variabel, operator, kondisi, perulangan.
- Memahami fungsi dan modul (import/package).
- Praktik cepat membaca/menulis file dan struktur data umum (list, dict).
- Tips pengelolaan environment (venv) dan paket (pip).

Jika baru mulai, cukup jalankan contoh-contoh kecil di sini dalam Python REPL atau file .py.

------------------------------------------------------------

## 1) Tipe Data dan Variabel

Tipe umum:
- int (bilangan bulat): `x = 10`
- float (pecahan): `pi = 3.14`
- bool (benar/salah): `is_ok = True`
- str (teks): `name = "Budi"`
- list (daftar): `nums = [1, 2, 3]`
- dict (kamus): `user = {"name": "Ana", "age": 20}`
- None (kosong): `val = None`

Konversi tipe:
```python
x = "42"
n = int(x)   # 42
s = str(123) # "123"
```

Operator dasar:
```python
a = 5 + 2      # tambah
b = 5 * 2      # kali
c = 5 / 2      # 2.5 (float)
d = 5 // 2     # 2   (pembagian bulat)
e = 5 % 2      # 1   (modulus)
f = 2 ** 3     # 8   (pangkat)
```

------------------------------------------------------------

## 2) Kondisi dan Perulangan

Kondisi:
```python
age = 18
if age >= 18:
    print("Dewasa")
elif age >= 13:
    print("Remaja")
else:
    print("Anak")
```

For dan while:
```python
for i in range(3):
    print(i)  # 0,1,2

nums = [10, 20, 30]
for n in nums:
    print(n)

count = 0
while count < 3:
    print(count)
    count += 1
```

List comprehension:
```python
squares = [i*i for i in range(5)]  # [0,1,4,9,16]
```

------------------------------------------------------------

## 3) Fungsi

```python
def add(a, b=0):
    """Menjumlahkan dua angka."""
    return a + b

print(add(2, 3))   # 5
print(add(10))     # 10 (b memakai default 0)
```

Fungsi anonim (lambda) singkat:
```python
double = lambda x: x * 2
print(double(5))  # 10
```

------------------------------------------------------------

## 4) Struktur Data Umum

List (terurut, bisa diubah):
```python
fruits = ["apel", "pisang", "jeruk"]
fruits.append("mangga")
print(fruits[0])   # "apel"
```

Tuple (terurut, tidak bisa diubah):
```python
point = (10, 20)
```

Dict (kunci-nilai):
```python
user = {"name": "Ana", "age": 20}
print(user["name"])
user["age"] = 21
```

Set (unik, tidak terurut):
```python
langs = {"py", "js", "py"}
print(langs)  # {"py","js"}
```

Unpacking:
```python
x, y = (1, 2)
name, age = user["name"], user["age"]
```

------------------------------------------------------------

## 5) File I/O Sederhana

```python
# Tulis file
with open("contoh.txt", "w", encoding="utf-8") as f:
    f.write("Halo dunia\n")

# Baca file
with open("contoh.txt", "r", encoding="utf-8") as f:
    text = f.read()
print(text)
```

------------------------------------------------------------

## 6) Modul, Package, dan Import

Buat file `utils.py`:
```python
def greet(name: str) -> str:
    return f"Halo, {name}!"
```

Gunakan di file lain:
```python
import utils
print(utils.greet("Sinta"))
```

Atau:
```python
from utils import greet
print(greet("Sinta"))
```

Instal paket pihak ketiga:
- Pastikan venv aktif
- `pip install requests`
- Lalu:
```python
import requests
print(requests.get("https://httpbin.org/get").status_code)
```

------------------------------------------------------------

## 7) Tips venv dan pip (ringkas)

- Buat venv: `python -m venv .venv`
- Aktifkan:
  - Windows: `.venv\Scripts\Activate`
  - macOS/Linux: `source .venv/bin/activate`
- Instal: `pip install -r requirements.txt`
- Bekukan versi (opsional): `pip freeze > pinned-requirements.txt`

Lihat docs/01-setup.md untuk panduan lengkap.

------------------------------------------------------------

## 8) Latihan Singkat

1) Buat fungsi `is_even(n)` yang mengembalikan True jika n genap.
2) Dari list `[1,2,3,4,5,6]`, buat list baru berisi kuadrat hanya untuk bilangan genap (pakai list comprehension).
3) Buat dict `person = {"name":"Ani","city":"Bandung"}`, ubah city menjadi "Jakarta".
4) Buat file `hello.txt` berisi “Halo AI Engineering”, lalu baca kembali dan cetak.

Checklist:
- [ ] Paham tipe data dasar dan operator
- [ ] Paham if/for/while dan list comprehension
- [ ] Paham fungsi, import modul sederhana
- [ ] Bisa baca/tulis file

Lanjut ke:
- docs/03-numpy-pandas.md untuk olah data tabular modern.
