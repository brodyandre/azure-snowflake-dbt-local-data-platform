from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.audit import write_pipeline_audit
from src.utils.config import DATA_LANDING_DIR, DATA_SAMPLES_DIR, ensure_project_directories
from src.utils.io import read_csv_file, save_dataframe_as_parquet
from src.utils.logger import get_logger


logger = get_logger(__name__)

PIPELINE_NAME = "ingest_customers"
SOURCE_PATH = DATA_SAMPLES_DIR / "customers.csv"
TARGET_PATH = DATA_LANDING_DIR / "customers" / "customers.parquet"
REQUIRED_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "city",
    "state",
    "created_at",
    "customer_segment",
]
TEXT_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "city",
    "state",
    "customer_segment",
]


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in customers dataset: {missing_columns}")


def _strip_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = df[column].apply(lambda value: value.strip() if isinstance(value, str) else value)
    return df


def _validate_required_identifier(df: pd.DataFrame, column_name: str) -> None:
    invalid_mask = df[column_name].isna() | df[column_name].eq("")
    if invalid_mask.any():
        raise ValueError(f"Column '{column_name}' contains null or empty values")


def _convert_created_at(df: pd.DataFrame) -> pd.DataFrame:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="raise")
    return df


def run() -> Path:
    started_at = datetime.now(timezone.utc)
    records_processed = 0

    ensure_project_directories()
    logger.info("Starting customers ingestion from %s", SOURCE_PATH)

    try:
        customers_df = read_csv_file(SOURCE_PATH)
        _validate_required_columns(customers_df)
        customers_df = _strip_text_columns(customers_df, TEXT_COLUMNS)
        _validate_required_identifier(customers_df, "customer_id")
        customers_df = _convert_created_at(customers_df)

        records_processed = len(customers_df)
        save_dataframe_as_parquet(customers_df, TARGET_PATH)

        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="success",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=f"Customers data written to {TARGET_PATH}",
        )
        logger.info("Customers ingestion completed with %s records", records_processed)
        return TARGET_PATH
    except Exception as exc:
        logger.exception("Customers ingestion failed")
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
