"""
labs/08-mlflow-dvc/train.py
Latih model tabular dengan Pipeline (sklearn), log metrik ke MLflow, dan simpan artifact.
- Membaca konfigurasi dari params.yaml (opsional override via argumen CLI)
- Menggunakan dataset processed jika ada; jika tidak, membuat data sintetis
- Menyimpan:
    - models/model.joblib (pipeline terlatih)
    - labs/08-mlflow-dvc/metrics.json (untuk DVC metrics)
- Melakukan MLflow logging jika MLflow tersedia

Jalankan:
  python ai-engineering-roadmap/labs/08-mlflow-dvc/train.py --params ai-engineering-roadmap/labs/08-mlflow-dvc/params.yaml

Catatan:
- MLFLOW_TRACKING_URI dan MLFLOW_EXPERIMENT_NAME bisa diatur via .env
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Model opsional
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def load_params(path: Optional[str]) -> dict:
    default = {
        "train": {
            "random_state": 42,
            "n_samples": 1000,
            "test_size": 0.2,
            "model": "RandomForestRegressor",  # atau "LinearRegression"
            "rf": {"n_estimators": 300, "max_depth": None},
        },
        "data": {
            "input_csv": "",  # jika kosong, akan generate synthetic
            "target": "price",
        },
    }
    if not path:
        return default
    p = Path(path)
    if not p.exists():
        print(f"[WARN] params.yaml tidak ditemukan di: {p}. Menggunakan default.")
        return default
    with p.open("r", encoding="utf-8") as f:
        user = yaml.safe_load(f) or {}
    # merge secara sederhana
    for k, v in user.items():
        if isinstance(v, dict) and k in default:
            default[k].update(v)
        else:
            default[k] = v
    return default


def find_repo_root() -> Path:
    # File ini: ai-engineering-roadmap/labs/08-mlflow-dvc/train.py
    # repo root: parents[2]
    here = Path(__file__).resolve()
    return here.parents[2]


def maybe_load_csv(repo_root: Path, input_csv: str, target_col: str) -> Optional[Tuple[pd.DataFrame, pd.Series]]:
    if not input_csv:
        return None
    csv_path = (repo_root / input_csv).resolve()
    if not csv_path.exists():
        print(f"[WARN] CSV tidak ditemukan: {csv_path}. Menggunakan data sintetis.")
        return None
    df = pd.read_csv(csv_path)
    if target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ada di CSV: {csv_path}")
    y = df[target_col]
    X = df.drop(columns=[target_col])
    return X, y


def make_synthetic_housing(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    area = rng.normal(loc=80, scale=30, size=n_samples).clip(20, 300)
    rooms = rng.integers(low=1, high=7, size=n_samples)
    age = rng.integers(low=0, high=50, size=n_samples)

    cities = np.array(["A", "B", "C"])
    conditions = np.array(["poor", "fair", "good"])
    city = rng.choice(cities, size=n_samples, p=[0.4, 0.4, 0.2])
    condition = rng.choice(conditions, size=n_samples, p=[0.2, 0.5, 0.3])

    base_price = 30000
    price = (
        base_price
        + area * 1500
        + rooms * 10000
        - age * 800
        + np.where(city == "A", 10000, np.where(city == "B", 5000, 0))
        + np.where(condition == "good", 15000, np.where(condition == "fair", 5000, 0))
    )
    noise = rng.normal(0, 15000, size=n_samples)
    price = (price + noise).clip(10000, None)

    df = pd.DataFrame(
        {
            "area": area,
            "rooms": rooms,
            "age": age,
            "city": city,
            "condition": condition,
            "price": price,
        }
    )
    return df


def build_pipeline(X: pd.DataFrame, model_name: str, rf_params: dict, random_state: int) -> Pipeline:
    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()

    numeric_tf = Pipeline(steps=[("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])

    categorical_tf = Pipeline(
        steps=[("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocess = ColumnTransformer(transformers=[("num", numeric_tf, num_cols), ("cat", categorical_tf, cat_cols)])

    if model_name.lower() == "linearregression":
        model = LinearRegression()
    else:
        # Default ke RandomForestRegressor
        model = RandomForestRegressor(
            n_estimators=int(rf_params.get("n_estimators", 300)),
            max_depth=None if rf_params.get("max_depth", None) in (None, "None") else int(rf_params.get("max_depth")),
            random_state=random_state,
            n_jobs=-1,
        )

    pipe = Pipeline(steps=[("prep", preprocess), ("model", model)])
    return pipe


def eval_regression(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {"rmse": float(rmse), "mae": float(mae), "r2": float(r2)}


def mlflow_log(params: dict, metrics: dict, model_obj: Pipeline, model_out_dir: Path) -> None:
    try:
        import mlflow
        import mlflow.sklearn

        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "default")
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

        with mlflow.start_run(run_name="labs-08-mlflow-dvc"):
            for k, v in params.items():
                mlflow.log_param(k, v)
            for k, v in metrics.items():
                mlflow.log_metric(k, float(v))

            # Simpan model sklearn sebagai artifact juga
            mlflow.sklearn.log_model(model_obj, "model")

            # Simpan salinan file model ke disk (untuk konsumsi API/artefak DVC)
            model_out_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(model_obj, model_out_dir / "model.joblib")

    except Exception as e:
        print(f"[INFO] MLflow logging dilewati/gagal: {e}")
        # Tetap simpan model ke disk walaupun MLflow gagal
        model_out_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model_obj, model_out_dir / "model.joblib")


def main():
    parser = argparse.ArgumentParser(description="Train tabular model with sklearn pipeline + MLflow logging.")
    parser.add_argument("--params", type=str, default="", help="Path params.yaml")
    args = parser.parse_args()

    params = load_params(args.params)
    repo_root = find_repo_root()

    # Data
    target_col = params["data"]["target"]
    csv_path = params["data"].get("input_csv", "").strip()

    res = maybe_load_csv(repo_root, csv_path, target_col)
    if res is None:
        print("[INFO] Menggunakan data sintetis.")
        df = make_synthetic_housing(n_samples=int(params["train"]["n_samples"]), random_state=int(params["train"]["random_state"]))
        y = df[target_col]
        X = df.drop(columns=[target_col])
    else:
        X, y = res

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(params["train"]["test_size"]), random_state=int(params["train"]["random_state"])
    )

    # Model
    pipe = build_pipeline(
        X_train,
        model_name=str(params["train"]["model"]),
        rf_params=dict(params["train"].get("rf", {})),
        random_state=int(params["train"]["random_state"]),
    )

    print(f"[INFO] Melatih model: {params['train']['model']}")
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    metrics = eval_regression(np.asarray(y_test), np.asarray(y_pred))
    print(f"[METRICS] RMSE={metrics['rmse']:.2f} MAE={metrics['mae']:.2f} R2={metrics['r2']:.4f}")

    # Output paths
    models_dir = repo_root / "models"
    metrics_path = Path(__file__).resolve().parent / "metrics.json"

    # MLflow log + simpan model ke models/
    flat_params = {
        "model": str(params["train"]["model"]),
        "random_state": int(params["train"]["random_state"]),
        "test_size": float(params["train"]["test_size"]),
        "n_samples": int(params["train"]["n_samples"]),
        "rf_n_estimators": params["train"].get("rf", {}).get("n_estimators", None),
        "rf_max_depth": params["train"].get("rf", {}).get("max_depth", None),
        "input_csv": csv_path or "synthetic",
    }
    mlflow_log(flat_params, metrics, pipe, models_dir)

    # Tulis metrics.json (untuk DVC metrics)
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] Metrics ditulis ke: {metrics_path}")
    print(f"[INFO] Model disimpan ke: {models_dir / 'model.joblib'}")


if __name__ == "__main__":
    main()
