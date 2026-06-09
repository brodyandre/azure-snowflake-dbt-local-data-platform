from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.batch.run_batch_pipeline import run_batch_pipeline
from src.utils.config import DATA_LANDING_DIR


DATASET_SPECS = [
    (
        "customers",
        DATA_LANDING_DIR / "customers" / "customers.parquet",
        [
            "customer_id",
            "full_name",
            "email",
            "city",
            "state",
            "created_at",
            "customer_segment",
        ],
    ),
    (
        "orders",
        DATA_LANDING_DIR / "orders" / "orders.parquet",
        [
            "order_id",
            "customer_id",
            "order_date",
            "sales_channel",
            "order_status",
            "gross_amount",
            "discount_amount",
            "net_amount",
        ],
    ),
    (
        "payments",
        DATA_LANDING_DIR / "payments" / "payments.parquet",
        [
            "payment_id",
            "order_id",
            "payment_method",
            "payment_status",
            "paid_amount",
            "paid_at",
        ],
    ),
]


@pytest.fixture(scope="module")
def batch_ready() -> bool:
    run_batch_pipeline()
    return True


@pytest.mark.parametrize(
    ("dataset_name", "path", "required_columns"),
    DATASET_SPECS,
)
def test_batch_generates_parquet_files(
    batch_ready: bool,
    dataset_name: str,
    path: Path,
    required_columns: list[str],
) -> None:
    assert batch_ready is True
    assert path.exists(), f"Expected parquet file for {dataset_name} at {path}"

    dataframe = pd.read_parquet(path)

    assert not dataframe.empty, f"Expected records in {path}"
    assert set(required_columns).issubset(dataframe.columns), (
        f"Missing required columns for {dataset_name}: "
        f"{set(required_columns) - set(dataframe.columns)}"
    )
