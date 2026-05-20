from pathlib import Path

import pandas as pd

from data.generate_data import generate_transactions


def test_generate_transactions_creates_expected_columns(tmp_path: Path) -> None:
    output = generate_transactions(tmp_path / "transactions.csv", rows=100, seed=7)
    frame = pd.read_csv(output)

    assert len(frame) == 100
    assert set(frame.columns) == {
        "transaction_id",
        "amount",
        "hour",
        "merchant_risk",
        "user_age_days",
        "country_risk",
        "is_fraud",
    }
    assert frame["is_fraud"].isin([0, 1]).all()

