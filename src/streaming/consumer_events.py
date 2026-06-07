from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from confluent_kafka import Consumer, KafkaException
from confluent_kafka.admin import AdminClient

from src.utils.audit import write_pipeline_audit
from src.utils.config import DATA_LANDING_DIR, REDPANDA_BROKER, REDPANDA_TOPIC_CUSTOMER_EVENTS
from src.utils.logger import get_logger


logger = get_logger(__name__)

PIPELINE_NAME = "streaming_consumer_events"
TARGET_PATH = DATA_LANDING_DIR / "events" / "events.jsonl"
DEFAULT_MAX_EVENTS = 20
POLL_TIMEOUT_SECONDS = 2.0
MAX_EMPTY_POLLS = 3


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consume customer events from Redpanda.")
    parser.add_argument(
        "--max-events",
        type=int,
        default=DEFAULT_MAX_EVENTS,
        help="Maximum number of events to consume before exiting.",
    )
    return parser.parse_args()


def _ensure_broker_available() -> None:
    admin_client = AdminClient({"bootstrap.servers": REDPANDA_BROKER})
    try:
        admin_client.list_topics(timeout=5)
    except KafkaException as exc:
        raise ConnectionError(
            f"Unable to connect to Redpanda broker at {REDPANDA_BROKER}"
        ) from exc


def _write_events_jsonl(events: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for event in events:
            output_file.write(json.dumps(event, ensure_ascii=True) + "\n")


def run(max_events: int) -> Path:
    if max_events <= 0:
        raise ValueError("--max-events must be greater than zero")

    started_at = datetime.now(timezone.utc)
    records_processed = 0
    consumed_events: list[dict[str, object]] = []
    consecutive_timeouts = 0

    logger.info(
        "Starting streaming consumer for topic %s with max-events=%s",
        REDPANDA_TOPIC_CUSTOMER_EVENTS,
        max_events,
    )

    consumer = Consumer(
        {
            "bootstrap.servers": REDPANDA_BROKER,
            "group.id": "local-data-platform-events-consumer",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    )

    try:
        _ensure_broker_available()
        consumer.subscribe([REDPANDA_TOPIC_CUSTOMER_EVENTS])

        while records_processed < max_events and consecutive_timeouts < MAX_EMPTY_POLLS:
            message = consumer.poll(POLL_TIMEOUT_SECONDS)
            if message is None:
                consecutive_timeouts += 1
                logger.info(
                    "No message received from topic %s (timeout %s/%s)",
                    REDPANDA_TOPIC_CUSTOMER_EVENTS,
                    consecutive_timeouts,
                    MAX_EMPTY_POLLS,
                )
                continue

            if message.error():
                raise RuntimeError(f"Kafka consumer error: {message.error()}")

            consecutive_timeouts = 0
            event = json.loads(message.value().decode("utf-8"))
            consumed_events.append(event)
            records_processed += 1

        _write_events_jsonl(consumed_events, TARGET_PATH)
        status_message = (
            f"Consumed {records_processed} event(s) from topic "
            f"{REDPANDA_TOPIC_CUSTOMER_EVENTS}"
        )
        if records_processed < max_events:
            status_message += " before reaching timeout threshold"

        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="success",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=status_message,
        )
        logger.info(status_message)
        logger.info("Events written to %s", TARGET_PATH)
        return TARGET_PATH
    except Exception as exc:
        logger.exception("Streaming consumer failed")
        write_pipeline_audit(
            pipeline_name=PIPELINE_NAME,
            status="failed",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            records_processed=records_processed,
            message=str(exc),
        )
        raise
    finally:
        consumer.close()


def main() -> int:
    args = _parse_args()
    try:
        run(max_events=args.max_events)
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
