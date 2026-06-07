from __future__ import annotations

import json
from datetime import datetime, timezone

from confluent_kafka import KafkaException, Producer
from confluent_kafka.admin import AdminClient

from src.utils.audit import write_pipeline_audit
from src.utils.config import (
    DATA_SAMPLES_DIR,
    REDPANDA_BROKER,
    REDPANDA_TOPIC_CUSTOMER_EVENTS,
)
from src.utils.io import read_jsonl_file
from src.utils.logger import get_logger


logger = get_logger(__name__)

PIPELINE_NAME = "streaming_producer_events"
SOURCE_PATH = DATA_SAMPLES_DIR / "events_sample.jsonl"


def _ensure_broker_available() -> None:
    admin_client = AdminClient({"bootstrap.servers": REDPANDA_BROKER})
    try:
        admin_client.list_topics(timeout=5)
    except KafkaException as exc:
        raise ConnectionError(
            f"Unable to connect to Redpanda broker at {REDPANDA_BROKER}"
        ) from exc


def run() -> int:
    started_at = datetime.now(timezone.utc)
    records_processed = 0

    logger.info("Starting streaming producer from %s", SOURCE_PATH)

    try:
        _ensure_broker_available()
        events_df = read_jsonl_file(SOURCE_PATH)
        producer = Producer({"bootstrap.servers": REDPANDA_BROKER})

        for event in events_df.to_dict(orient="records"):
            event_payload = json.dumps(event, ensure_ascii=True, default=str)
            producer.produce(
                REDPANDA_TOPIC_CUSTOMER_EVENTS,
                value=event_payload.encode("utf-8"),
            )
            records_processed += 1

        remaining_messages = producer.flush(10)
        if remaining_messages != 0:
            raise RuntimeError(
                f"Failed to deliver {remaining_messages} event(s) to topic "
                f"{REDPANDA_TOPIC_CUSTOMER_EVENTS}"
            )

        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="success",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=(
                f"Published {records_processed} event(s) to topic "
                f"{REDPANDA_TOPIC_CUSTOMER_EVENTS}"
            ),
        )
        logger.info(
            "Published %s event(s) to topic %s",
            records_processed,
            REDPANDA_TOPIC_CUSTOMER_EVENTS,
        )
        return records_processed
    except Exception as exc:
        logger.exception("Streaming producer failed")
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
