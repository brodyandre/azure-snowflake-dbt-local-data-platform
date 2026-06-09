from __future__ import annotations

import json

from src.utils.config import DATA_SAMPLES_DIR
from src.utils.io import read_csv_file, read_json_file


CUSTOMERS_COLUMNS = {
    "customer_id",
    "full_name",
    "email",
    "city",
    "state",
    "created_at",
    "customer_segment",
}

ORDERS_COLUMNS = {
    "order_id",
    "customer_id",
    "order_date",
    "sales_channel",
    "order_status",
    "gross_amount",
    "discount_amount",
}

PAYMENTS_FIELDS = {
    "payment_id",
    "order_id",
    "payment_method",
    "payment_status",
    "paid_amount",
    "paid_at",
}

EVENTS_FIELDS = {
    "event_id",
    "customer_id",
    "event_type",
    "event_timestamp",
    "source_system",
}


def test_customers_sample_has_expected_columns() -> None:
    customers_df = read_csv_file(DATA_SAMPLES_DIR / "customers.csv")
    assert CUSTOMERS_COLUMNS.issubset(customers_df.columns)


def test_orders_sample_has_expected_columns() -> None:
    orders_df = read_csv_file(DATA_SAMPLES_DIR / "orders.csv")
    assert ORDERS_COLUMNS.issubset(orders_df.columns)


def test_payments_sample_has_expected_fields() -> None:
    payments_df = read_json_file(DATA_SAMPLES_DIR / "payments.json")
    assert PAYMENTS_FIELDS.issubset(payments_df.columns)


def test_events_sample_has_valid_jsonl_lines() -> None:
    events_path = DATA_SAMPLES_DIR / "events_sample.jsonl"
    with events_path.open("r", encoding="utf-8") as events_file:
        parsed_records = 0
        for line_number, line in enumerate(events_file, start=1):
            raw_line = line.strip()
            if not raw_line:
                continue
            record = json.loads(raw_line)
            assert EVENTS_FIELDS.issubset(record), (
                f"Missing expected event fields on line {line_number}"
            )
            parsed_records += 1

    assert parsed_records > 0


def test_orders_customer_ids_exist_in_customers() -> None:
    customers_df = read_csv_file(DATA_SAMPLES_DIR / "customers.csv")
    orders_df = read_csv_file(DATA_SAMPLES_DIR / "orders.csv")

    customer_ids = set(customers_df["customer_id"].astype(str))
    order_customer_ids = set(orders_df["customer_id"].astype(str))

    assert order_customer_ids.issubset(customer_ids)
