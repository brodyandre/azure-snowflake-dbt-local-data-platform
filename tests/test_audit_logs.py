from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.batch.run_batch_pipeline import run_batch_pipeline
from src.utils.config import EVIDENCE_LOGS_DIR


AUDIT_LOG_PATH = EVIDENCE_LOGS_DIR / "pipeline_audit.jsonl"
REQUIRED_AUDIT_FIELDS = {
    "pipeline_name",
    "status",
    "started_at",
    "finished_at",
    "records_processed",
    "message",
}


@pytest.fixture(scope="module")
def audit_log_path() -> Path:
    if not AUDIT_LOG_PATH.exists():
        run_batch_pipeline()
    return AUDIT_LOG_PATH


def test_audit_log_exists_after_pipeline_execution(audit_log_path: Path) -> None:
    assert audit_log_path.exists()


def test_audit_log_lines_are_valid_json(audit_log_path: Path) -> None:
    valid_records = 0

    with audit_log_path.open("r", encoding="utf-8") as audit_file:
        for line in audit_file:
            raw_line = line.strip()
            if not raw_line:
                continue

            record = json.loads(raw_line)
            assert REQUIRED_AUDIT_FIELDS.issubset(record)
            valid_records += 1

    assert valid_records > 0


def test_audit_log_status_values_are_expected(audit_log_path: Path) -> None:
    allowed_statuses = {"success", "failed"}

    with audit_log_path.open("r", encoding="utf-8") as audit_file:
        for line in audit_file:
            raw_line = line.strip()
            if not raw_line:
                continue

            record = json.loads(raw_line)
            assert record["status"] in allowed_statuses
