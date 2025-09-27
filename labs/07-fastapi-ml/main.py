"""
FastAPI untuk menyajikan model ML (regresi tabular) dari labs/03-ml-pipeline.py

Menjalankan:
  - python labs/07-fastapi-ml/main.py
  - atau gunakan Dockerfile di folder yang sama

Endpoint:
  - GET  /health
  - POST /predict        -> 1 data
  - POST /predict_batch  -> banyak data

Catatan:
  - Pastikan model.joblib sudah ada (buat dengan menjalankan labs/03-ml-pipeline.py)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Muat .env (APP_ENV, APP_HOST, APP_PORT, dll.)
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

app = FastAPI(title="FastAPI ML Service", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

# CORS longgar saat development
if APP_ENV.lower() == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # sesuaikan pada produksi
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Lokasi model: bersebelahan dengan file ini
MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
_model = None
_model_loaded_error: Optional[str] = None


def load_model():
    global _model, _model_loaded_error
    try:
        _model = joblib.load(MODEL_PATH)
        _model_loaded_error = None
    except Exception as e:
        _model = None
        _model_loaded_error = str(e)


load_model()


class Item(BaseModel):
    area: float = Field(..., description="Luas bangunan (m^2)")
    rooms: int = Field(..., ge=0, description="Jumlah kamar")
    age: int = Field(..., ge=0, description="Umur bangunan (tahun)")
    city: str = Field(..., description="Kota: A/B/C")
    condition: str = Field(..., description="Kondisi: poor/fair/good")


class Items(BaseModel):
    items: List[Item]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None,
        "model_path": str(MODEL_PATH),
        "error": _model_loaded_error,
        "env": APP_ENV,
    }


def _ensure_model_loaded():
    if _model is None:
        raise HTTPException(status_code=500, detail=f"Model belum siap: {_model_loaded_error or 'unknown error'}")


def _predict_df(df: pd.DataFrame):
    # Pipeline sklearn yang disimpan menerima DataFrame kolom nama aslinya
    preds = _model.predict(df)  # type: ignore[attr-defined]
    return preds.tolist()


@app.post("/predict")
def predict(item: Item):
    _ensure_model_loaded()
    # Susun DataFrame 1 baris sesuai kolom training
    df = pd.DataFrame([item.model_dump()])
    try:
        y = _predict_df(df)
        return {"prediction": y}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal memprediksi: {e}")


@app.post("/predict_batch")
def predict_batch(payload: Items):
    _ensure_model_loaded()
    if not payload.items:
        raise HTTPException(status_code=400, detail="Items tidak boleh kosong")
    df = pd.DataFrame([it.model_dump() for it in payload.items])
    try:
        y = _predict_df(df)
        return {"prediction": y}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal memprediksi batch: {e}")


if __name__ == "__main__":
    # Jalankan langsung tanpa masalah nama modul (hindari 'uvicorn module:app' yang gagal karena nama folder ber-hyphen)
    uvicorn.run(app, host=APP_HOST, port=APP_PORT, log_level=LOG_LEVEL)
