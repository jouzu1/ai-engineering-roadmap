"""
Ingest dokumen untuk RAG (LangChain + FAISS)
- Membaca file teks/markdown sesuai pola glob (default: docs/*.md)
- Memecah teks menjadi chunk
- Membuat embedding (OpenAI jika API key tersedia, atau lokal SentenceTransformers)
- Menyimpan index FAISS ke folder (default: .cache/vectorstore, bisa diatur via .env atau argumen)

Cara pakai:
  python labs/06-rag-chatbot/ingest.py --glob "docs/*.md" --chunk-size 800 --chunk-overlap 100

Catatan:
- Jika ingin OpenAI Embeddings, isi OPENAI_API_KEY di .env
- Jika ingin lokal: akan pakai model "sentence-transformers/all-MiniLM-L6-v2"
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv

# LangChain core
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Embeddings (dua opsi)
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def read_files_by_glob(pattern: str) -> List[Tuple[str, str]]:
    """
    Membaca file dengan pola glob. Mengembalikan list (path, content).
    Hanya mengambil file teks umum (.md, .txt) agar aman.
    """
    out: List[Tuple[str, str]] = []
    for p in Path().glob(pattern):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            # fallback encoding
            text = p.read_text(encoding="utf-8", errors="ignore")
        out.append((str(p), text))
    return out


def build_embeddings() -> Tuple[object, dict]:
    """
    Membangun embedding:
    - Jika ada OPENAI_API_KEY => OpenAIEmbeddings
    - Jika tidak => HuggingFaceEmbeddings (sentence-transformers/all-MiniLM-L6-v2)
    Mengembalikan (embeddings, info_dict) untuk disimpan sebagai metadata.
    """
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        emb = OpenAIEmbeddings(model=model)
        info = {"type": "openai", "model": model}
    else:
        model = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        # Normalisasi embedding memudahkan cosine similarity yang stabil
        emb = HuggingFaceEmbeddings(
            model_name=model,
            encode_kwargs={"normalize_embeddings": True},
        )
        info = {"type": "huggingface", "model": model}
    return emb, info


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Ingest dokumen menjadi vectorstore FAISS untuk RAG.")
    parser.add_argument("--glob", default="docs/*.md", help="Pola glob file (default: docs/*.md)")
    parser.add_argument("--chunk-size", type=int, default=800, help="Ukuran chunk karakter")
    parser.add_argument("--chunk-overlap", type=int, default=100, help="Overlap karakter antar chunk")
    parser.add_argument(
        "--vs-path",
        default=os.getenv("VECTORSTORE_PATH", ".cache/vectorstore"),
        help="Lokasi simpan vectorstore FAISS",
    )
    args = parser.parse_args()

    files = read_files_by_glob(args.glob)
    if not files:
        print(f"Tidak ditemukan file untuk pola: {args.glob}")
        return

    print(f"Memuat {len(files)} file...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    texts: List[str] = []
    metadatas = []
    for path, content in files:
        chunks = splitter.split_text(content)
        for i, ch in enumerate(chunks):
            texts.append(ch)
            metadatas.append({"source": path, "chunk": i})

    print(f"Total chunk: {len(texts)}")

    emb, emb_info = build_embeddings()
    print(f"Menggunakan embeddings: {emb_info}")

    vs = FAISS.from_texts(texts=texts, embedding=emb, metadatas=metadatas)

    vs_path = Path(args.vs_path)
    vs_path.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(vs_path))
    # Simpan metadata embeddings agar app.py bisa memuat tipe yang sama
    (vs_path / "embeddings.json").write_text(json.dumps(emb_info, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Vectorstore tersimpan ke: {vs_path.resolve()}")
    print("Selesai. Jalankan app: python labs/06-rag-chatbot/app.py")


if __name__ == "__main__":
    main()
