from __future__ import annotations

from collections.abc import Callable

from src.batch.ingest_customers import run as run_customers_ingestion
from src.batch.ingest_orders import run as run_orders_ingestion
from src.batch.ingest_payments import run as run_payments_ingestion
from src.utils.logger import get_logger


logger = get_logger(__name__)

PipelineStep = tuple[str, Callable[[], object]]


def run_batch_pipeline() -> None:
    pipeline_steps: list[PipelineStep] = [
        ("customers", run_customers_ingestion),
        ("orders", run_orders_ingestion),
        ("payments", run_payments_ingestion),
    ]

    logger.info("Starting local batch pipeline")
    for pipeline_name, pipeline_function in pipeline_steps:
        logger.info("Running batch step: %s", pipeline_name)
        pipeline_function()
        logger.info("Finished batch step: %s", pipeline_name)
    logger.info("Local batch pipeline completed successfully")


def main() -> int:
    try:
        run_batch_pipeline()
        return 0
    except Exception:
        logger.exception("Local batch pipeline failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
