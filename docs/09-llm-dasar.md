# 09 — Dasar LLM (Large Language Model) dan Prompting (Bahasa Sederhana)

Tujuan modul:
- Mengerti apa itu LLM dan cara “berkomunikasi” lewat prompt.
- Mengerti token, context window, dan parameter penting (temperature, max tokens).
- Mencoba panggilan LLM dengan 2 opsi: OpenAI (cloud) dan Ollama (lokal).
- Mengerti embedding: mengubah teks jadi angka untuk pencarian/kemiripan.

Jika ingin langsung praktik RAG, lanjut ke docs/10-langchain-rag.md setelah memahami dasar ini.

------------------------------------------------------------

## 1) Apa itu LLM?
- LLM (Large Language Model) adalah model yang dilatih untuk memahami dan menghasilkan teks.
- LLM bisa:
  - Menjawab pertanyaan
  - Merangkum dokumen
  - Menulis kode
  - Membuat rencana langkah, dsb.
- LLM tidak “tahu segalanya” dan bisa salah (halusinasi). Kita perlu memberi konteks yang benar (lihat RAG pada modul berikutnya).

------------------------------------------------------------

## 2) Token dan Context Window
- Token: potongan teks (bisa beberapa huruf/karakter). Model menghitung “biaya” dan batas berdasarkan token, bukan kata.
- Context window: jumlah token maksimum yang bisa diproses sekali jalan (mis. 8k, 32k, 128k token tergantung model).
- Implikasi:
  - Prompt + dokumen + jawaban harus muat di context window.
  - Jika terlalu panjang, potong/dilakukan chunking.

------------------------------------------------------------

## 3) Prompting 101 (Bahasa Sederhana)
- Prompt = instruksi ke model. Ibarat “brief” ke asisten.
- Format peran (role) pada banyak API:
  - system: nada/aturan umum
  - user: pertanyaan/perintah
  - assistant: jawaban (hasil)
- Teknik dasar:
  - Jelaskan tujuan dengan jelas (“Tuliskan ringkasan 3 poin…”) 
  - Beri batasan (“Gunakan bahasa Indonesia, maksimal 100 kata”) 
  - Contoh (few-shot) jika perlu (“Contoh input-output seperti ini…”) 
  - Format keluaran (“Kembalikan dalam JSON dengan field: title, summary”)
- Parameter penting:
  - temperature (0.0–1.0): kreativitas. Lebih rendah = lebih deterministik.
  - top_p: alternatif pengaturan sampling (umumnya biarkan default).
  - max_tokens: batas panjang jawaban.
  - stop: string tempat model berhenti.
- Best practice:
  - Mulai dari prompt sederhana → uji → perbaiki
  - Simpan prompt yang efektif

Contoh kerangka prompt:
```
Anda adalah asisten AI yang membantu ringkasan dokumen.
Instruksi:
- Gunakan bahasa Indonesia formal.
- Maksimal 120 kata.
- Beri 3 poin utamanya.

Teks sumber:
{{teks}}

Tugas:
Ringkas teks sumber sesuai aturan di atas.
```

------------------------------------------------------------

## 4) Memanggil LLM: OpenAI (Cloud) vs Ollama (Lokal)

A) OpenAI (butuh API key)
- Isi OPENAI_API_KEY di file .env
- Install dependensi sudah ada di requirements.txt (langchain-openai)

Contoh (LangChain, chat):
```python
# file: examples/openai_chat.py (opsional)
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

messages = [
    SystemMessage(content="Anda adalah asisten AI yang ringkas dan jelas."),
    HumanMessage(content="Jelaskan singkat apa itu AI Engineering."),
]
resp = llm.invoke(messages)
print(resp.content)
```

B) Ollama (lokal, gratis)
- Install Ollama: https://ollama.ai
- Jalankan: `ollama pull mistral` (atau `llama3`, dsb.)
- Pastikan .env:
  - OLLAMA_BASE_URL=http://localhost:11434
  - OLLAMA_MODEL=mistral

Contoh (LangChain, chat):
```python
# file: examples/ollama_chat.py (opsional)
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()
llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    model=os.getenv("OLLAMA_MODEL", "mistral"),
    temperature=0.2,
)

messages = [
    SystemMessage(content="Anda adalah asisten AI yang ringkas dan jelas."),
    HumanMessage(content="Apa manfaat membuat API untuk model ML?"),
]
resp = llm.invoke(messages)
print(resp.content)
```

Catatan:
- Model lokal lebih lambat dan kualitas bervariasi, tetapi murah dan privat.
- Model cloud umumnya lebih kuat, tapi berbayar.

------------------------------------------------------------

## 5) Embedding: Teks → Vektor Angka
- Embedding mengubah teks menjadi vector (mis. 768-dim), sehingga kita bisa:
  - Mengukur kemiripan (cosine similarity)
  - Mencari dokumen mirip untuk RAG

A) OpenAI Embedding (butuh API key):
```python
# pip install langchain-openai
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()
emb = OpenAIEmbeddings(model="text-embedding-3-small")
vec = emb.embed_query("Apa itu AI Engineering?")
print(len(vec), vec[:5])  # panjang vektor dan contoh isi
```

B) Lokal (Sentence Transformers):
```python
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = ["AI Engineering fokus deploy model", "Memasak rendang butuh waktu lama"]
vectors = model.encode(texts, normalize_embeddings=True)  # shape: (2, 384)

# cosine similarity
sim = float(np.dot(vectors[0], vectors[1]))  # karena sudah dinormalisasi
print("Kemiripan:", sim)  # antara -1 dan 1
```

Catatan:
- Untuk RAG, kita akan menyimpan embedding ke vector store (mis. FAISS) agar pencarian cepat.

------------------------------------------------------------

## 6) Tantangan Umum dan Tips
- Halusinasi: Model bisa yakin tapi salah. Solusi: beri konteks akurat (RAG), minta sumber.
- Batas token: Potong teks panjang menjadi beberapa “chunk”.
- Biaya: Batasi panjang prompt, gunakan model yang lebih murah jika cukup.
- Privasi: Jangan kirim PII/data sensitif ke layanan cloud (kecuali ada izin dan proteksi).
- Evaluasi: Cek apakah jawaban benar dan konsisten. Gunakan test set Q&A untuk penilaian.

------------------------------------------------------------

## 7) Checklist
- [ ] Mengerti token dan context window
- [ ] Bisa memanggil LLM (OpenAI atau Ollama)
- [ ] Mengerti parameter prompting (temperature, max_tokens)
- [ ] Bisa menghasilkan embedding (OpenAI atau lokal)
- [ ] Paham risiko halusinasi dan cara mitigasi dasar

Lanjutkan ke:
- docs/10-langchain-rag.md untuk membangun RAG: memecah dokumen, membuat embedding, menyimpan di FAISS, dan melakukan retrieval + generasi jawaban.
