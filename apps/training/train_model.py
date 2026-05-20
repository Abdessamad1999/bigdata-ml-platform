from __future__ import annotations

import argparse
import os
from pathlib import Path

import mlflow
import mlflow.pytorch
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from spark.jobs.etl_features import FEATURE_COLUMNS


class FraudNet(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x).squeeze(1)


def load_feature_frame(path: str) -> pd.DataFrame:
    frame = pd.read_parquet(path)
    missing = set(FEATURE_COLUMNS + ["label"]) - set(frame.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    return frame


def train(features_path: str, model_dir: str, epochs: int = 8) -> dict[str, float]:
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "fraud-deep-learning-demo"))

    frame = load_feature_frame(features_path)
    x = frame[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
    y = frame["label"].to_numpy(dtype=np.float32)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train).astype(np.float32)
    x_test = scaler.transform(x_test).astype(np.float32)

    train_ds = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
    loader = DataLoader(train_ds, batch_size=128, shuffle=True)

    model = FraudNet(input_dim=x_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    loss_fn = nn.BCEWithLogitsLoss()

    with mlflow.start_run() as run:
        mlflow.log_params({"epochs": epochs, "batch_size": 128, "lr": 0.002})
        for epoch in range(epochs):
            model.train()
            total_loss = 0.0
            for xb, yb in loader:
                optimizer.zero_grad()
                loss = loss_fn(model(xb), yb)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            mlflow.log_metric("train_loss", total_loss / len(loader), step=epoch)

        model.eval()
        with torch.no_grad():
            logits = model(torch.from_numpy(x_test))
            probs = torch.sigmoid(logits).numpy()
            preds = (probs >= 0.5).astype(int)

        metrics = {
            "accuracy": float(accuracy_score(y_test, preds)),
            "f1": float(f1_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, probs)),
        }
        mlflow.log_metrics(metrics)
        mlflow.pytorch.log_model(model, "model")

        output_dir = Path(model_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "model_state": model.state_dict(),
                "feature_columns": FEATURE_COLUMNS,
                "scaler_mean": scaler.mean_,
                "scaler_scale": scaler.scale_,
                "run_id": run.info.run_id,
            },
            output_dir / "fraud_net.pt",
        )
        return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="data/processed/features.parquet")
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--epochs", type=int, default=8)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(train(args.features, args.model_dir, args.epochs))

