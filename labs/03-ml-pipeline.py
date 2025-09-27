"""
03-ml-pipeline.py — Contoh pipeline tabular end-to-end (sklearn)
- Membuat dataset sintetis (regresi)
- Split train/test
- Pipeline: preprocess numeric/categorical + model
- Evaluasi RMSE
- Simpan model.joblib (untuk konsumsi API)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression


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


def build_pipeline(X: pd.DataFrame) -> Pipeline:
    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()

    numeric_tf = Pipeline(steps=[("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical_tf = Pipeline(steps=[("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])

    preprocess = ColumnTransformer(transformers=[("num", numeric_tf, num_cols), ("cat", categorical_tf, cat_cols)])
    model = LinearRegression()
    pipe = Pipeline(steps=[("prep", preprocess), ("model", model)])
    return pipe


def main():
    parser = argparse.ArgumentParser(description="Train simple tabular pipeline and save model.joblib")
    parser.add_argument("--n-samples", type=int, default=1000)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    df = make_synthetic_housing(n_samples=args.n_samples, random_state=args.random_state)
    y = df["price"]
    X = df.drop(columns=["price"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=args.random_state)
    pipe = build_pipeline(X_train)
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    print(f"RMSE: {rmse:.2f}")

    # Simpan model untuk API
    out_dir = Path(__file__).resolve().parent.parent / "07-fastapi-ml"
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_dir / "model.joblib")
    print(f"Model saved to: {out_dir / 'model.joblib'}")


if __name__ == "__main__":
    main()
