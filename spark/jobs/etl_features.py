from __future__ import annotations

import argparse
import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

FEATURE_COLUMNS = [
    "amount_log",
    "hour_sin",
    "hour_cos",
    "merchant_risk",
    "account_age_score",
    "country_risk",
]


def build_features(input_path: str, output_path: str) -> None:
    builder = SparkSession.builder.appName("bigdata-ml-feature-engineering").config(
        "spark.sql.shuffle.partitions", "4"
    )
    if spark_master := os.getenv("SPARK_MASTER_URL"):
        builder = builder.master(spark_master)
    spark = builder.getOrCreate()

    raw = spark.read.option("header", True).option("inferSchema", True).csv(input_path)
    features = (
        raw.withColumn("amount_log", F.log1p(F.col("amount")))
        .withColumn("hour_sin", F.sin(2 * F.lit(3.141592653589793) * F.col("hour") / 24))
        .withColumn("hour_cos", F.cos(2 * F.lit(3.141592653589793) * F.col("hour") / 24))
        .withColumn(
            "account_age_score",
            F.when(F.col("user_age_days") < 30, F.lit(1.0))
            .when(F.col("user_age_days") < 180, F.lit(0.5))
            .otherwise(F.lit(0.0)),
        )
        .select(*FEATURE_COLUMNS, F.col("is_fraud").alias("label"))
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    features.coalesce(1).write.mode("overwrite").parquet(output_path)
    spark.stop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/transactions.csv")
    parser.add_argument("--output", default="data/processed/features.parquet")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_features(args.input, args.output)
