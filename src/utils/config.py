from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


def _resolve_project_path(env_var_name: str, default_relative_path: str) -> Path:
    raw_value = os.getenv(env_var_name, default_relative_path)
    candidate_path = Path(raw_value)
    if candidate_path.is_absolute():
        return candidate_path
    return PROJECT_ROOT / candidate_path


DATA_RAW_DIR = _resolve_project_path("DATA_RAW_DIR", "data/raw")
DATA_LANDING_DIR = _resolve_project_path("DATA_LANDING_DIR", "data/landing")
DATA_SAMPLES_DIR = _resolve_project_path("DATA_SAMPLES_DIR", "data/samples")
EVIDENCE_LOGS_DIR = _resolve_project_path("EVIDENCE_LOGS_DIR", "evidence/execution-logs")
WAREHOUSE_DIR = _resolve_project_path("DATA_WAREHOUSE_DIR", "data/warehouse")

DUCKDB_PATH = _resolve_project_path("DUCKDB_PATH", "data/warehouse/local_warehouse.duckdb")

REDPANDA_BROKER = os.getenv("REDPANDA_BROKER", "localhost:9092")
REDPANDA_TOPIC_CUSTOMER_EVENTS = os.getenv(
    "REDPANDA_TOPIC_CUSTOMER_EVENTS",
    "customer-events",
)

AZURITE_ACCOUNT_NAME = os.getenv("AZURITE_ACCOUNT_NAME", "devstoreaccount1")
AZURITE_BLOB_ENDPOINT = os.getenv(
    "AZURITE_BLOB_ENDPOINT",
    "http://127.0.0.1:10000/devstoreaccount1",
)


def ensure_project_directories() -> None:
    directories = (
        DATA_RAW_DIR,
        DATA_LANDING_DIR,
        DATA_SAMPLES_DIR,
        EVIDENCE_LOGS_DIR,
        WAREHOUSE_DIR,
    )
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
