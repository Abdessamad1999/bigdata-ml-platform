import pandas as pd
import pytest

from apps.training.train_model import load_feature_frame
from spark.jobs.etl_features import FEATURE_COLUMNS


def test_load_feature_frame_rejects_missing_columns(tmp_path):
    path = tmp_path / "features.parquet"
    pd.DataFrame({"label": [0, 1]}).to_parquet(path)

    with pytest.raises(ValueError, match="missing columns"):
        load_feature_frame(str(path))


def test_load_feature_frame_accepts_expected_schema(tmp_path):
    path = tmp_path / "features.parquet"
    data = {column: [0.1, 0.2] for column in FEATURE_COLUMNS}
    data["label"] = [0, 1]
    pd.DataFrame(data).to_parquet(path)

    frame = load_feature_frame(str(path))

    assert list(frame.columns) == FEATURE_COLUMNS + ["label"]

