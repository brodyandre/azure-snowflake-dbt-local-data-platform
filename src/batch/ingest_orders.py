from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.audit import write_pipeline_audit
from src.utils.config import DATA_LANDING_DIR, DATA_SAMPLES_DIR, ensure_project_directories
from src.utils.io import read_csv_file, save_dataframe_as_parquet
from src.utils.logger import get_logger


logger = get_logger(__name__)

PIPELINE_NAME = "ingest_orders"
SOURCE_PATH = DATA_SAMPLES_DIR / "orders.csv"
TARGET_PATH = DATA_LANDING_DIR / "orders" / "orders.parquet"
REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "order_date",
    "sales_channel",
    "order_status",
    "gross_amount",
    "discount_amount",
]
TEXT_COLUMNS = ["order_id", "customer_id", "sales_channel", "order_status"]


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in orders dataset: {missing_columns}")


def _strip_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = df[column].apply(lambda value: value.strip() if isinstance(value, str) else value)
    return df


def _validate_required_identifier(df: pd.DataFrame, column_name: str) -> None:
    invalid_mask = df[column_name].isna() | df[column_name].eq("")
    if invalid_mask.any():
        raise ValueError(f"Column '{column_name}' contains null or empty values")


def _convert_order_date(df: pd.DataFrame) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="raise")
    return df


def _convert_numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="raise")
    return df


def _add_net_amount(df: pd.DataFrame) -> pd.DataFrame:
    df["net_amount"] = df["gross_amount"] - df["discount_amount"]
    return df


def run() -> Path:
    started_at = datetime.now(timezone.utc)
    records_processed = 0

    ensure_project_directories()
    logger.info("Starting orders ingestion from %s", SOURCE_PATH)

    try:
        orders_df = read_csv_file(SOURCE_PATH)
        _validate_required_columns(orders_df)
        orders_df = _strip_text_columns(orders_df, TEXT_COLUMNS)
        _validate_required_identifier(orders_df, "order_id")
        orders_df = _convert_order_date(orders_df)
        orders_df = _convert_numeric_columns(orders_df, ["gross_amount", "discount_amount"])
        orders_df = _add_net_amount(orders_df)

        records_processed = len(orders_df)
        save_dataframe_as_parquet(orders_df, TARGET_PATH)

        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="success",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=f"Orders data written to {TARGET_PATH}",
        )
        logger.info("Orders ingestion completed with %s records", records_processed)
        return TARGET_PATH
    except Exception as exc:
        logger.exception("Orders ingestion failed")
        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="failed",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=str(exc),
        )
        raise


def main() -> int:
    try:
        run()
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
