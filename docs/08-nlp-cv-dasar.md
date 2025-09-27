# 08 — Dasar NLP dan CV (Bahasa Sederhana)

Tujuan:
- Memahami alur kerja dasar NLP (teks) dan CV (gambar).
- Melakukan pra-pemrosesan sederhana untuk teks dan gambar.
- Menjalankan contoh tugas umum:
  - NLP: klasifikasi sentimen dengan HuggingFace Transformers
  - CV: klasifikasi gambar sederhana dengan PyTorch + torchvision

Fokus bahasa awam dan praktik cepat.

------------------------------------------------------------

## 1) NLP (Natural Language Processing) Singkat

Alur umum NLP modern:
1) Persiapan data (teks + label)
2) Tokenisasi (ubah teks → token id sesuai vocab model)
3) Model (mis. BERT/DistilBERT) menghasilkan representasi dan prediksi
4) Evaluasi (Accuracy/F1)
5) Prediksi (inference)

Dua pendekatan:
- Zero-shot/few-shot (pakai model siap pakai tanpa/nyaris tanpa training)
- Fine-tuning (latih ulang sedikit pada dataset tugas Anda)

Pra-pemrosesan ringan:
- Lowercase, hapus karakter non-alfanumerik (opsional tergantung model)
- Tokenisasi ditangani oleh tokenizer bawaan model

Contoh cepat (Transformers — inference sentimen):
```python
# pip install transformers torch
from transformers import pipeline

clf = pipeline("sentiment-analysis")  # default model kecil
print(clf("Produk ini bagus sekali, saya suka!"))
# [{'label': 'POSITIVE', 'score': 0.999...}]
print(clf("Pengiriman lambat dan barang rusak."))
# [{'label': 'NEGATIVE', 'score': ...}]
```

Contoh evaluasi sederhana (dataset kecil):
```python
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# Dataset contoh: imdb (besar). Untuk demo cepat gunakan subset kecil.
ds = load_dataset("imdb")
small_train = ds["train"].shuffle(seed=42).select(range(1000))
small_test  = ds["test"].shuffle(seed=42).select(range(1000))

model_name = "distilbert-base-uncased"
tok = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tok(batch["text"], truncation=True, padding="max_length", max_length=128)

train_tok = small_train.map(tokenize, batched=True)
test_tok  = small_test.map(tokenize, batched=True)

train_tok = train_tok.remove_columns(["text"])
test_tok  = test_tok.remove_columns(["text"])
train_tok = train_tok.rename_column("label", "labels")
test_tok  = test_tok.rename_column("label", "labels")
train_tok.set_format("torch")
test_tok.set_format("torch")

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    acc = accuracy_score(p.label_ids, preds)
    f1 = f1_score(p.label_ids, preds)
    return {"accuracy": acc, "f1": f1}

args = TrainingArguments(
    output_dir="./tmp-imdb",
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    num_train_epochs=1,
    logging_steps=50,
    save_strategy="no"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_tok,
    eval_dataset=test_tok,
    tokenizer=tok,
    compute_metrics=compute_metrics
)

trainer.train()
print(trainer.evaluate())
```

Catatan:
- Untuk eksperimen lebih besar, gunakan GPU agar cepat.
- Untuk produksi, pertimbangkan distil/quantization agar ringan.

------------------------------------------------------------

## 2) CV (Computer Vision) Singkat

Alur umum CV:
1) Dataset (gambar + label)
2) Transformasi/augmentasi (resize, crop, normalize, flip)
3) Model CNN (atau Vision Transformer), training loop
4) Evaluasi (Accuracy/Top-k)
5) Prediksi (inference)

Pra-pemrosesan:
- Normalisasi nilai piksel (mean/std dataset)
- Augmentasi (flip, rotate) untuk robust terhadap variasi

Contoh cepat (CIFAR-10 dengan torchvision — training ringkas):
```python
# pip install torch torchvision
import torch, torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tf_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914,0.4822,0.4465), (0.2470,0.2435,0.2616)),
])
tf_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914,0.4822,0.4465), (0.2470,0.2435,0.2616)),
])

train_ds = datasets.CIFAR10(root="./data", train=True, download=True, transform=tf_train)
test_ds  = datasets.CIFAR10(root="./data", train=False, download=True, transform=tf_test)

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True, num_workers=2)
test_loader  = DataLoader(test_ds, batch_size=256, shuffle=False, num_workers=2)

class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                 # 32x16x16
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                 # 64x8x8
            nn.Flatten(),
            nn.Linear(64*8*8, 128), nn.ReLU(),
            nn.Linear(128, 10),
        )
    def forward(self, x): return self.net(x)

model = TinyCNN().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.CrossEntropyLoss()

def run_epoch(loader, train=True):
    model.train(train)
    total, correct, loss_sum = 0, 0, 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        if train: opt.zero_grad()
        logits = model(xb)
        loss = crit(logits, yb)
        if train:
            loss.backward()
            opt.step()
        loss_sum += loss.item() * xb.size(0)
        pred = logits.argmax(1)
        correct += (pred == yb).sum().item()
        total += xb.size(0)
    return loss_sum/total, correct/total

for epoch in range(2):
    tr_loss, tr_acc = run_epoch(train_loader, train=True)
    te_loss, te_acc = run_epoch(test_loader, train=False)
    print(f"Epoch {epoch+1}: train {tr_loss:.4f}/{tr_acc:.4f} | test {te_loss:.4f}/{te_acc:.4f}")
```

Catatan:
- Ini model kecil untuk demo. Untuk kualitas lebih baik, gunakan arsitektur standar (ResNet, EfficientNet, dll.) atau pretrained.

------------------------------------------------------------

## 3) Perbandingan Singkat: NLP vs CV

- Data:
  - NLP: teks; perhatian pada bahasa, token, panjang konteks (token limit)
  - CV: gambar; perhatian pada ukuran, augmentasi, normalisasi channel
- Model:
  - NLP: Transformer-based (BERT, GPT, LLaMA)
  - CV: CNN/Vision Transformer
- Metrik:
  - NLP: Accuracy/F1, BLEU/ROUGE (untuk generatif)
  - CV: Accuracy/Top-1/Top-5, mAP (deteksi)
- Performa:
  - Keduanya lebih cepat dengan GPU
  - Fine-tuning sering lebih hemat biaya dibanding training dari nol

------------------------------------------------------------

## 4) Tips Praktis

- Mulai dengan model/pretrained pipeline agar cepat melihat hasil.
- Gunakan subset kecil dulu untuk uji alur, lalu skala ke dataset penuh.
- Catat metrik/parameter (MLflow) agar eksperimen rapi.
- Jaga data pribadi (PII) dan bias dataset (lihat modul 15).

------------------------------------------------------------

Checklist:
- [ ] Menjalankan inference NLP sederhana (pipeline sentiment)
- [ ] Memahami tokenisasi dan fine-tuning dasar
- [ ] Melatih CNN kecil untuk klasifikasi gambar
- [ ] Memahami perbedaan alur NLP vs CV dan metriknya

Lanjut ke:
- docs/09-llm-dasar.md dan docs/10-langchain-rag.md untuk LLM/RAG, atau
- docs/11-deploy-fastapi-docker.md untuk deploy model sebagai API.
