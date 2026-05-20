from __future__ import annotations

from apps.training.train_model import train
from data.generate_data import generate_transactions
from spark.jobs.etl_features import build_features


def main() -> None:
    raw_path = generate_transactions("data/raw/transactions.csv", rows=5000)
    print(f"raw_data={raw_path}")
    build_features(str(raw_path), "data/processed/features.parquet")
    print("features=data/processed/features.parquet")
    metrics = train("data/processed/features.parquet", "models", epochs=8)
    print(f"metrics={metrics}")


if __name__ == "__main__":
    main()
