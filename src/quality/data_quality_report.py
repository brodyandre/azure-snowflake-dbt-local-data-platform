from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.config import (
    DATA_LANDING_DIR,
    EVIDENCE_LOGS_DIR,
    PROJECT_ROOT,
    ensure_project_directories,
)
from src.utils.io import read_jsonl_file
from src.utils.logger import get_logger


logger = get_logger(__name__)

REPORT_PATH = EVIDENCE_LOGS_DIR / "data_quality_report.md"

REQUIRED_COLUMNS_BY_DATASET = {
    "customers": [
        "customer_id",
        "full_name",
        "email",
        "city",
        "state",
        "created_at",
        "customer_segment",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_date",
        "sales_channel",
        "order_status",
        "gross_amount",
        "discount_amount",
        "net_amount",
    ],
    "payments": [
        "payment_id",
        "order_id",
        "payment_method",
        "payment_status",
        "paid_amount",
        "paid_at",
    ],
    "events": [
        "event_id",
        "customer_id",
        "event_type",
        "event_timestamp",
        "source_system",
    ],
}

PRIMARY_KEYS_BY_DATASET = {
    "customers": "customer_id",
    "orders": "order_id",
    "payments": "payment_id",
    "events": "event_id",
}


def _read_parquet_file(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_parquet(path)


def _get_dataset_specs() -> list[dict[str, object]]:
    return [
        {
            "name": "customers",
            "path": DATA_LANDING_DIR / "customers" / "customers.parquet",
            "loader": _read_parquet_file,
        },
        {
            "name": "orders",
            "path": DATA_LANDING_DIR / "orders" / "orders.parquet",
            "loader": _read_parquet_file,
        },
        {
            "name": "payments",
            "path": DATA_LANDING_DIR / "payments" / "payments.parquet",
            "loader": _read_parquet_file,
        },
        {
            "name": "events",
            "path": DATA_LANDING_DIR / "events" / "events.jsonl",
            "loader": read_jsonl_file,
        },
    ]


def _relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def _missing_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    return [column for column in required_columns if column not in df.columns]


def _null_counts(df: pd.DataFrame) -> dict[str, int]:
    return {column: int(count) for column, count in df.isna().sum().items()}


def _duplicate_primary_key_count(df: pd.DataFrame, primary_key: str) -> int | None:
    if primary_key not in df.columns:
        return None
    return int(df.duplicated(subset=[primary_key]).sum())


def _build_observations(
    record_count: int,
    missing_columns: list[str],
    null_counts: dict[str, int],
    duplicate_count: int | None,
) -> list[str]:
    observations: list[str] = []
    populated_null_counts = {column: count for column, count in null_counts.items() if count > 0}

    if record_count == 0:
        observations.append("Dataset carregado sem registros.")
    if missing_columns:
        observations.append(
            "Colunas obrigatorias ausentes: " + ", ".join(sorted(missing_columns))
        )
    if duplicate_count is None:
        observations.append("Chave primaria nao encontrada no dataset.")
    elif duplicate_count > 0:
        observations.append(f"Foram encontradas {duplicate_count} duplicidades na chave primaria.")
    if populated_null_counts:
        formatted_nulls = ", ".join(
            f"{column}={count}" for column, count in sorted(populated_null_counts.items())
        )
        observations.append("Colunas com nulos: " + formatted_nulls)

    if not observations:
        observations.append("Nenhum problema critico identificado nas verificacoes locais.")

    return observations


def _render_null_counts_table(null_counts: dict[str, int]) -> list[str]:
    rows = [
        "| Coluna | Nulos |",
        "| --- | ---: |",
    ]
    for column, count in sorted(null_counts.items()):
        rows.append(f"| `{column}` | {count} |")
    return rows


def _build_dataset_section(spec: dict[str, object]) -> tuple[list[str], dict[str, str]]:
    name = str(spec["name"])
    path = Path(spec["path"])
    loader = spec["loader"]
    required_columns = REQUIRED_COLUMNS_BY_DATASET[name]
    primary_key = PRIMARY_KEYS_BY_DATASET[name]

    section_lines = [f"## Dataset `{name}`", f"- Arquivo: `{_relative_path(path)}`"]

    try:
        dataframe = loader(path)
    except FileNotFoundError:
        logger.warning("Dataset %s not found at %s", name, path)
        section_lines.extend(
            [
                "- Status: nao encontrado",
                "- Observacao: dataset ainda nao foi gerado nesta estacao local.",
                "",
            ]
        )
        return section_lines, {
            "dataset": name,
            "status": "nao encontrado",
            "records": "0",
            "columns": "0",
            "missing": ", ".join(required_columns),
            "duplicates": "n/a",
        }
    except Exception as exc:
        logger.warning("Failed to load dataset %s from %s: %s", name, path, exc)
        section_lines.extend(
            [
                "- Status: erro na leitura",
                f"- Observacao: {exc}",
                "",
            ]
        )
        return section_lines, {
            "dataset": name,
            "status": "erro",
            "records": "0",
            "columns": "0",
            "missing": "n/a",
            "duplicates": "n/a",
        }

    record_count = len(dataframe)
    column_count = len(dataframe.columns)
    missing_columns = _missing_required_columns(dataframe, required_columns)
    null_counts = _null_counts(dataframe)
    duplicate_count = _duplicate_primary_key_count(dataframe, primary_key)
    observations = _build_observations(record_count, missing_columns, null_counts, duplicate_count)

    section_lines.extend(
        [
            "- Status: carregado com sucesso",
            f"- Quantidade de registros: {record_count}",
            f"- Quantidade de colunas: {column_count}",
            "- Colunas obrigatorias ausentes: "
            + (", ".join(sorted(missing_columns)) if missing_columns else "nenhuma"),
            "- Duplicidade na chave primaria `"
            + primary_key
            + "`: "
            + (str(duplicate_count) if duplicate_count is not None else "n/a"),
            "",
            "### Nulos por coluna",
            *_render_null_counts_table(null_counts),
            "",
            "### Observacoes de qualidade",
        ]
    )
    section_lines.extend(f"- {observation}" for observation in observations)
    section_lines.append("")

    return section_lines, {
        "dataset": name,
        "status": "ok",
        "records": str(record_count),
        "columns": str(column_count),
        "missing": ", ".join(sorted(missing_columns)) if missing_columns else "nenhuma",
        "duplicates": str(duplicate_count) if duplicate_count is not None else "n/a",
    }


def generate_quality_report() -> Path:
    ensure_project_directories()
    report_generated_at = datetime.now(timezone.utc).isoformat()

    report_lines = [
        "# Relatorio Local de Qualidade de Dados",
        "",
        f"Gerado em: `{report_generated_at}`",
        "",
        "## Resumo por dataset",
        "",
        "| Dataset | Status | Registros | Colunas | Colunas obrigatorias ausentes | Duplicidades na chave primaria |",
        "| --- | --- | ---: | ---: | --- | ---: |",
    ]

    for spec in _get_dataset_specs():
        section_lines, summary_row = _build_dataset_section(spec)
        report_lines.append(
            "| `{dataset}` | {status} | {records} | {columns} | {missing} | {duplicates} |".format(
                **summary_row
            )
        )
        report_lines.append("")
        report_lines.extend(section_lines)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines).strip() + "\n", encoding="utf-8")

    logger.info("Data quality report generated at %s", REPORT_PATH)
    return REPORT_PATH


def main() -> int:
    try:
        generate_quality_report()
        return 0
    except Exception:
        logger.exception("Failed to generate data quality report")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
