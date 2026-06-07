from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .logger import get_logger


logger = get_logger(__name__)


def _ensure_input_file_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Input path is not a file: {path}")


def _ensure_output_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv_file(path: Path) -> pd.DataFrame:
    _ensure_input_file_exists(path)
    try:
        return pd.read_csv(path)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV file '{path}': {exc}") from exc


def read_json_file(path: Path) -> pd.DataFrame:
    _ensure_input_file_exists(path)
    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON content in '{path}': {exc.msg}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to open JSON file '{path}': {exc}") from exc

    if isinstance(payload, list):
        return pd.json_normalize(payload)
    if isinstance(payload, dict):
        return pd.json_normalize(payload)
    raise ValueError(f"Unsupported JSON structure in '{path}'. Expected object or array.")


def read_jsonl_file(path: Path) -> pd.DataFrame:
    _ensure_input_file_exists(path)

    records: list[dict[str, object]] = []
    try:
        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                try:
                    records.append(json.loads(stripped_line))
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON on line {line_number} in '{path}': {exc.msg}"
                    ) from exc
    except OSError as exc:
        raise ValueError(f"Failed to open JSONL file '{path}': {exc}") from exc

    return pd.json_normalize(records)


def save_dataframe_as_parquet(df: pd.DataFrame, path: Path) -> None:
    _ensure_output_directory(path)
    try:
        df.to_parquet(path, index=False)
        logger.info("DataFrame saved as Parquet at %s", path)
    except Exception as exc:
        raise ValueError(f"Failed to save DataFrame as Parquet to '{path}': {exc}") from exc


def save_dataframe_as_csv(df: pd.DataFrame, path: Path) -> None:
    _ensure_output_directory(path)
    try:
        df.to_csv(path, index=False)
        logger.info("DataFrame saved as CSV at %s", path)
    except Exception as exc:
        raise ValueError(f"Failed to save DataFrame as CSV to '{path}': {exc}") from exc
