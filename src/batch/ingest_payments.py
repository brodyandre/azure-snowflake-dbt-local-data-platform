from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.audit import write_pipeline_audit
from src.utils.config import DATA_LANDING_DIR, DATA_SAMPLES_DIR, ensure_project_directories
from src.utils.io import read_json_file, save_dataframe_as_parquet
from src.utils.logger import get_logger


logger = get_logger(__name__)

PIPELINE_NAME = "ingest_payments"
SOURCE_PATH = DATA_SAMPLES_DIR / "payments.json"
TARGET_PATH = DATA_LANDING_DIR / "payments" / "payments.parquet"
REQUIRED_COLUMNS = [
    "payment_id",
    "order_id",
    "payment_method",
    "payment_status",
    "paid_amount",
    "paid_at",
]
TEXT_COLUMNS = ["payment_id", "order_id", "payment_method", "payment_status"]


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in payments dataset: {missing_columns}")


def _strip_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = df[column].apply(lambda value: value.strip() if isinstance(value, str) else value)
    return df


def _validate_required_identifier(df: pd.DataFrame, column_name: str) -> None:
    invalid_mask = df[column_name].isna() | df[column_name].eq("")
    if invalid_mask.any():
        raise ValueError(f"Column '{column_name}' contains null or empty values")


def _convert_paid_amount(df: pd.DataFrame) -> pd.DataFrame:
    df["paid_amount"] = pd.to_numeric(df["paid_amount"], errors="raise")
    return df


def _convert_paid_at(df: pd.DataFrame) -> pd.DataFrame:
    original_values = df["paid_at"]
    converted_values = pd.to_datetime(original_values, errors="coerce")
    invalid_mask = original_values.notna() & converted_values.isna()
    if invalid_mask.any():
        raise ValueError("Column 'paid_at' contains invalid datetime values")
    df["paid_at"] = converted_values
    return df


def run() -> Path:
    started_at = datetime.now(timezone.utc)
    records_processed = 0

    ensure_project_directories()
    logger.info("Starting payments ingestion from %s", SOURCE_PATH)

    try:
        payments_df = read_json_file(SOURCE_PATH)
        _validate_required_columns(payments_df)
        payments_df = _strip_text_columns(payments_df, TEXT_COLUMNS)
        _validate_required_identifier(payments_df, "payment_id")
        payments_df = _convert_paid_amount(payments_df)
        payments_df = _convert_paid_at(payments_df)

        records_processed = len(payments_df)
        save_dataframe_as_parquet(payments_df, TARGET_PATH)

        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="success",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=f"Payments data written to {TARGET_PATH}",
        )
        logger.info("Payments ingestion completed with %s records", records_processed)
        return TARGET_PATH
    except Exception as exc:
        logger.exception("Payments ingestion failed")
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
