# 07 — Deep Learning dengan PyTorch (Bahasa Sederhana)

Tujuan modul:
- Paham konsep dasar PyTorch: Tensor, Autograd, Module (model), dan Training Loop.
- Paham Dataset/DataLoader untuk memuat data dalam batch.
- Bisa melatih model sederhana (CNN untuk MNIST) di CPU/GPU.
- Bisa menyimpan dan memuat ulang model.

Jika ingin langsung praktik, salin kode contoh di bawah ke file baru atau notebook Anda.

------------------------------------------------------------

## 1) Konsep Inti PyTorch (ringkas)
- Tensor: “array” mirip NumPy, tapi bisa berjalan di GPU.
- Autograd: PyTorch otomatis menghitung turunan/gradien untuk optimisasi.
- Module (nn.Module): cara mendefinisikan model (lapisan, forward).
- Training loop: langkah berulang (forward → hitung loss → backward → step optimizer).

Gambaran alur:
1) Siapkan dataset → DataLoader (batch)
2) Definisikan model (nn.Module)
3) Tentukan loss function dan optimizer
4) Loop epoch: train → evaluasi → simpan model

------------------------------------------------------------

## 2) Cek Device (CPU/GPU)
```python
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)  # cuda jika GPU NVIDIA tersedia, selain itu cpu
```

Jika ingin GPU, lihat panduan instalasi PyTorch GPU di docs/01-setup.md.

------------------------------------------------------------

## 3) Dataset & DataLoader (Contoh: MNIST)
Kita pakai dataset MNIST (angka tulisan tangan 28x28). torchvision akan mengunduh otomatis.

```python
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Transformasi: ubah ke Tensor dan normalisasi ringan
transform = transforms.Compose([
    transforms.ToTensor(),                     # [0,1]
    transforms.Normalize((0.1307,), (0.3081,)) # mean/std MNIST
])

train_ds = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_ds  = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True, num_workers=2)
test_loader  = DataLoader(test_ds, batch_size=256, shuffle=False, num_workers=2)
```

Catatan:
- batch_size: jumlah sampel per iterasi (atur sesuai RAM/VRAM).
- shuffle=True pada data train untuk acak urutan.

------------------------------------------------------------

## 4) Definisikan Model (CNN sederhana)
```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)  # 1x28x28 -> 16x28x28
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1) # 16x14x14 -> 32x14x14
        self.pool  = nn.MaxPool2d(2,2)                           # downsample 2x
        self.fc1   = nn.Linear(32*7*7, 128)
        self.fc2   = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x))) # 1x28x28 -> 16x14x14
        x = self.pool(F.relu(self.conv2(x))) # 16x14x14 -> 32x7x7
        x = x.view(x.size(0), -1)            # flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)                      # logits 10 kelas
        return x
```

------------------------------------------------------------

## 5) Training Loop (lengkap dan sederhana)
```python
import torch
from torch import optim
from tqdm import tqdm  # opsional: pip install tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for xb, yb in tqdm(loader, desc="Train", leave=False):
        xb, yb = xb.to(device), yb.to(device)

        optimizer.zero_grad()
        logits = model(xb)                    # forward
        loss = criterion(logits, yb)         # hitung loss
        loss.backward()                      # backward (autograd)
        optimizer.step()                     # update bobot

        total_loss += loss.item() * xb.size(0)
        pred = logits.argmax(dim=1)
        correct += (pred == yb).sum().item()
        total += xb.size(0)

    return total_loss/total, correct/total

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        loss = criterion(logits, yb)
        total_loss += loss.item() * xb.size(0)
        pred = logits.argmax(dim=1)
        correct += (pred == yb).sum().item()
        total += xb.size(0)

    return total_loss/total, correct/total

EPOCHS = 3
for epoch in range(1, EPOCHS+1):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
    te_loss, te_acc = evaluate(model, test_loader, criterion, device)
    print(f"Epoch {epoch}: train loss {tr_loss:.4f} acc {tr_acc:.4f} | test loss {te_loss:.4f} acc {te_acc:.4f}")
```

Hasil tipikal:
- CPU 3 epoch bisa mencapai akurasi test ~0.97 (tergantung mesin).
- GPU akan lebih cepat.

Tips:
- Jika loss tidak turun, coba turunkan lr (mis. 5e-4) atau tambah epoch.

------------------------------------------------------------

## 6) Early Stopping (opsional)
Early stopping menghentikan training ketika validasi tidak membaik. Contoh sederhana:

```python
best_te_acc = 0.0
patience = 2
bad_epochs = 0

for epoch in range(1, 50):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
    te_loss, te_acc = evaluate(model, test_loader, criterion, device)
    print(f"Epoch {epoch}: train {tr_loss:.4f}/{tr_acc:.4f} | test {te_loss:.4f}/{te_acc:.4f}")

    if te_acc > best_te_acc + 1e-4:
        best_te_acc = te_acc
        bad_epochs = 0
        torch.save(model.state_dict(), "best-mnist-cnn.pt")
    else:
        bad_epochs += 1
        if bad_epochs >= patience:
            print("Early stopping.")
            break
```

------------------------------------------------------------

## 7) Simpan dan Muat Ulang Model
- Simpan bobot:
```python
torch.save(model.state_dict(), "mnist-cnn.pt")
```

- Muat ulang:
```python
model = SimpleCNN().to(device)
model.load_state_dict(torch.load("mnist-cnn.pt", map_location=device))
model.eval()
```

- Simpan seluruh model (kurang direkomendasikan untuk jangka panjang):
```python
torch.save(model, "mnist-cnn-full.pt")
# Muat: model = torch.load("mnist-cnn-full.pt", map_location=device)
```

Rekomendasi: gunakan state_dict agar fleksibel terhadap perubahan lingkungan.

------------------------------------------------------------

## 8) Debugging Umum
- Loss NaN/Inf:
  - Cek learning rate terlalu besar
  - Cek input tidak ternormalisasi/ada nilai aneh
- Memori habis (CPU/GPU):
  - Kecilkan batch_size
  - Gunakan num_workers lebih kecil
- Training lambat:
  - Gunakan pin_memory=True di DataLoader saat pakai GPU
  - Periksa apakah benar-benar berjalan di device “cuda”
- Akurasi stagnan:
  - Tambah epoch
  - Coba arsitektur sedikit lebih besar
  - Coba optim berbeda (SGD dengan momentum, AdamW)

------------------------------------------------------------

## 9) Hubungan ke Modul Lain
- Setelah paham training loop, Anda bisa:
  - Mengganti dataset (CIFAR-10) atau tugas (klasifikasi vs regresi).
  - Mengekspor model untuk dipakai FastAPI (lihat labs/07-fastapi-ml).
  - Mencatat hasil eksperimen ke MLflow (parameter, metrik, artifact).

Checklist:
- [ ] Paham Tensor, Autograd, Module, dan Training Loop
- [ ] Bisa memuat data dengan Dataset/DataLoader
- [ ] Bisa melatih CNN sederhana dan mengukur akurasi
- [ ] Bisa menyimpan/memuat model

Lanjutkan ke:
- docs/09-llm-dasar.md untuk konsep LLM/prompting.
- docs/10-langchain-rag.md untuk membangun RAG chatbot.
