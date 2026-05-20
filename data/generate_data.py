from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_transactions(output_path: str | Path, rows: int = 5000, seed: int = 42) -> Path:
    rng = np.random.default_rng(seed)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    amount = rng.gamma(shape=2.2, scale=45.0, size=rows).round(2)
    hour = rng.integers(0, 24, size=rows)
    merchant_risk = rng.beta(a=2.0, b=8.0, size=rows)
    user_age_days = rng.integers(1, 2500, size=rows)
    country_risk = rng.choice([0.05, 0.15, 0.35, 0.65], size=rows, p=[0.55, 0.25, 0.15, 0.05])

    fraud_score = (
        (amount > 180).astype(float) * 0.25
        + ((hour < 5) | (hour > 22)).astype(float) * 0.2
        + merchant_risk * 0.55
        + country_risk * 0.45
        + (user_age_days < 30).astype(float) * 0.25
        + rng.normal(0, 0.08, size=rows)
    )
    label = (fraud_score > 0.55).astype(int)

    frame = pd.DataFrame(
        {
            "transaction_id": np.arange(1, rows + 1),
            "amount": amount,
            "hour": hour,
            "merchant_risk": merchant_risk.round(4),
            "user_age_days": user_age_days,
            "country_risk": country_risk,
            "is_fraud": label,
        }
    )
    frame.to_csv(output, index=False)
    return output


if __name__ == "__main__":
    path = generate_transactions("data/raw/transactions.csv")
    print(f"generated={path}")

