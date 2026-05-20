from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field

from apps.training.train_model import FraudNet

PREDICTIONS = Counter("fraud_predictions_total", "Total prediction requests")
LATENCY = Histogram("fraud_prediction_latency_seconds", "Prediction latency in seconds")


class Transaction(BaseModel):
    amount_log: float = Field(..., ge=0)
    hour_sin: float = Field(..., ge=-1, le=1)
    hour_cos: float = Field(..., ge=-1, le=1)
    merchant_risk: float = Field(..., ge=0, le=1)
    account_age_score: float = Field(..., ge=0, le=1)
    country_risk: float = Field(..., ge=0, le=1)


class Prediction(BaseModel):
    fraud_probability: float
    is_fraud: bool


def load_model(model_path: str) -> tuple[FraudNet, np.ndarray, np.ndarray]:
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"model artifact not found: {path}")
    artifact = torch.load(path, map_location="cpu", weights_only=False)
    feature_columns = artifact["feature_columns"]
    model = FraudNet(input_dim=len(feature_columns))
    model.load_state_dict(artifact["model_state"])
    model.eval()
    return model, np.asarray(artifact["scaler_mean"]), np.asarray(artifact["scaler_scale"])


app = FastAPI(title="Fraud Deep Learning API", version="1.0.0")
app.mount("/metrics", make_asgi_app())

MODEL_PATH = os.getenv("MODEL_PATH", "models/fraud_net.pt")
try:
    MODEL, SCALER_MEAN, SCALER_SCALE = load_model(MODEL_PATH)
except FileNotFoundError:
    MODEL, SCALER_MEAN, SCALER_SCALE = None, None, None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model_loaded": str(MODEL is not None).lower()}


@app.post("/predict", response_model=Prediction)
def predict(transaction: Transaction) -> Prediction:
    if MODEL is None or SCALER_MEAN is None or SCALER_SCALE is None:
        raise HTTPException(status_code=503, detail="model is not loaded")

    values = np.array([list(transaction.model_dump().values())], dtype=np.float32)
    scaled = (values - SCALER_MEAN) / SCALER_SCALE
    with LATENCY.time():
        with torch.no_grad():
            probability = torch.sigmoid(MODEL(torch.from_numpy(scaled.astype(np.float32)))).item()
    PREDICTIONS.inc()
    return Prediction(fraud_probability=probability, is_fraud=probability >= 0.5)
