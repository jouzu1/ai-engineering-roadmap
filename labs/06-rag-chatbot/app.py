"""
RAG Chatbot (CLI) — LangChain + FAISS
- Memuat vectorstore FAISS hasil dari ingest.py
- Menggunakan LLM: OpenAI (jika OPENAI_API_KEY ada) atau Ollama (lokal)
- Menjawab pertanyaan dengan konteks dari dokumen yang diindeks

Cara pakai:
  1) Pastikan sudah menjalankan:
       python labs/06-rag-chatbot/ingest.py --glob "docs/*.md"
  2) Jalankan aplikasi:
       python labs/06-rag-chatbot/app.py
  3) Ketik pertanyaan, lalu Enter. Ketik "exit" untuk keluar.

Konfigurasi via .env:
  - VECTORSTORE_PATH (default: .cache/vectorstore)
  - OPENAI_API_KEY (opsional, untuk OpenAI)
  - OLLAMA_BASE_URL, OLLAMA_MODEL (opsional, untuk Ollama lokal)
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter  # hanya jika perlu split tambahan
from langchain.schema import SystemMessage, HumanMessage

# Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# LLMs
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama


def build_embeddings_from_meta(vs_dir: Path):
    """
    Membangun embeddings sesuai metadata yang disimpan saat ingest.
    Jika metadata tidak ada, fallback ke aturan environment:
      - jika OPENAI_API_KEY tersedia -> OpenAIEmbeddings (model dari env EMBEDDING_MODEL)
      - jika tidak -> HuggingFaceEmbeddings (LOCAL_EMBEDDING_MODEL)
    """
    meta_path = vs_dir / "embeddings.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("type") == "openai":
                model = meta.get("model", "text-embedding-3-small")
                return OpenAIEmbeddings(model=model)
            else:
                model = meta.get("model", "sentence-transformers/all-MiniLM-L6-v2")
                return HuggingFaceEmbeddings(
                    model_name=model,
                    encode_kwargs={"normalize_embeddings": True},
                )
        except Exception as e:
            print(f"[INFO] Gagal memuat metadata embeddings, fallback env. Detail: {e}")

    # Fallback by env
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model)
    else:
        model = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        return HuggingFaceEmbeddings(
            model_name=model,
            encode_kwargs={"normalize_embeddings": True},
        )


def build_llm():
    """
    Bangun LLM:
      - Jika OPENAI_API_KEY tersedia -> ChatOpenAI (model dari env OPENAI_CHAT_MODEL atau default)
      - Jika tidak -> ChatOllama lokal (base_url + model dari env)
    """
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        return ChatOpenAI(model=model, temperature=temperature)
    else:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "mistral")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        return ChatOllama(base_url=base_url, model=model, temperature=temperature)


def format_context(docs) -> str:
    parts: List[str] = []
    for d in docs:
        meta = d.metadata or {}
        src = meta.get("source", "unknown")
        ch = meta.get("chunk", "?")
        parts.append(f"[{src}#chunk-{ch}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


def main():
    load_dotenv()

    vs_path = Path(os.getenv("VECTORSTORE_PATH", ".cache/vectorstore"))
    if not vs_path.exists():
        print(f"Vectorstore tidak ditemukan di: {vs_path.resolve()}")
        print('Jalankan dulu: python labs/06-rag-chatbot/ingest.py --glob "docs/*.md"')
        return

    # Build embeddings dan load FAISS index
    embeddings = build_embeddings_from_meta(vs_path)
    try:
        # allow_dangerous_deserialization diperlukan untuk beberapa versi langchain/faiss
        vs = FAISS.load_local(str(vs_path), embeddings, allow_dangerous_deserialization=True)
    except TypeError:
        # Kompatibilitas versi lama yang tidak punya argumen allow_dangerous_deserialization
        vs = FAISS.load_local(str(vs_path), embeddings)

    retriever_k = int(os.getenv("RETRIEVER_TOP_K", "4"))

    llm = build_llm()
    print("RAG Chatbot siap. Ketik pertanyaan Anda. Ketik 'exit' untuk keluar.\n")

    system_preamble = (
        "Anda adalah asisten AI yang menjawab singkat, jelas, dan berbasis konteks dokumen."
        " Gunakan Bahasa Indonesia yang mudah dipahami. Jika informasi tidak ditemukan di konteks,"
        " katakan tidak yakin dan sarankan sumber relevan."
    )

    while True:
        try:
            q = input("> ")
        except KeyboardInterrupt:
            print("\nKeluar.")
            break

        if not q.strip():
            continue
        if q.strip().lower() in {"exit", "quit"}:
            print("Selesai.")
            break

        # Retrieve dokumen relevan
        docs = vs.similarity_search(q, k=retriever_k)
        context = format_context(docs)

        prompt = (
            f"Pertanyaan: {q}\n"
            "Jawab berdasarkan konteks berikut. Jika tidak cukup, katakan tidak yakin.\n\n"
            f"Konteks:\n{context}\n\n"
            "Jawaban:"
        )

        try:
            resp = llm.invoke([SystemMessage(content=system_preamble), HumanMessage(content=prompt)])
            answer = getattr(resp, "content", str(resp))
            print("\n" + answer.strip() + "\n")

            # Tampilkan sumber
            if docs:
                unique_src = []
                for d in docs:
                    src = (d.metadata or {}).get("source", "unknown")
                    if src not in unique_src:
                        unique_src.append(src)
                print("Sumber:", "; ".join(unique_src))
            print("-" * 60)
        except Exception as e:
            print(f"[ERROR] Gagal memanggil LLM: {e}")
            print("Periksa koneksi, kunci API, atau server Ollama Anda.")
            print("-" * 60)


if __name__ == "__main__":
    main()
