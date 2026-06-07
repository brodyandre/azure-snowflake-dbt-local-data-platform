from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from .config import EVIDENCE_LOGS_DIR


AuditStatus = Literal["success", "failed"]


def _format_timestamp(value: datetime | str) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def write_pipeline_audit(
    pipeline_name: str,
    status: AuditStatus,
    started_at: datetime | str,
    finished_at: datetime | str,
    records_processed: int,
    message: str,
) -> Path:
    normalized_status = status.lower()
    if normalized_status not in {"success", "failed"}:
        raise ValueError("status must be either 'success' or 'failed'")
    if records_processed < 0:
        raise ValueError("records_processed must be greater than or equal to zero")

    audit_file_path = EVIDENCE_LOGS_DIR / "pipeline_audit.jsonl"
    audit_file_path.parent.mkdir(parents=True, exist_ok=True)

    audit_record = {
        "pipeline_name": pipeline_name,
        "status": normalized_status,
        "started_at": _format_timestamp(started_at),
        "finished_at": _format_timestamp(finished_at),
        "records_processed": records_processed,
        "message": message,
    }

    with audit_file_path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(audit_record, ensure_ascii=True) + "\n")

    return audit_file_path
