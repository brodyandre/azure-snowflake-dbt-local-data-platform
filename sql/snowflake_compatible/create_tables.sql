-- Estruturas simplificadas para mostrar como as fontes e as camadas analiticas
-- do laboratorio poderiam ser representadas em Snowflake.

use database LOCAL_DATA_PLATFORM;

create table if not exists RAW.CUSTOMERS_RAW (
    customer_id varchar,
    full_name varchar,
    email varchar,
    city varchar,
    state varchar,
    created_at timestamp_ntz,
    customer_segment varchar,
    ingestion_ts timestamp_ntz default current_timestamp()
);

create table if not exists RAW.ORDERS_RAW (
    order_id varchar,
    customer_id varchar,
    order_date date,
    sales_channel varchar,
    order_status varchar,
    gross_amount number(12, 2),
    discount_amount number(12, 2),
    ingestion_ts timestamp_ntz default current_timestamp()
);

create table if not exists RAW.PAYMENTS_RAW (
    payment_id varchar,
    order_id varchar,
    payment_method varchar,
    payment_status varchar,
    paid_amount number(12, 2),
    paid_at timestamp_ntz,
    ingestion_ts timestamp_ntz default current_timestamp()
);

create table if not exists RAW.EVENTS_RAW (
    event_id varchar,
    customer_id varchar,
    event_type varchar,
    event_timestamp timestamp_ntz,
    source_system varchar,
    ingestion_ts timestamp_ntz default current_timestamp()
);

create table if not exists CONTROL.PIPELINE_RUN_LOG (
    run_id number autoincrement start 1 increment 1,
    pipeline_name varchar,
    run_status varchar,
    rows_loaded number,
    started_at timestamp_ntz default current_timestamp(),
    finished_at timestamp_ntz,
    execution_note varchar
);

create table if not exists MARTS.DIM_CUSTOMERS (
    customer_id varchar,
    full_name varchar,
    email varchar,
    city varchar,
    state varchar,
    customer_segment varchar,
    created_at timestamp_ntz
);

create table if not exists INTERMEDIATE.INT_ORDERS_ENRICHED (
    order_id varchar,
    customer_id varchar,
    order_date date,
    sales_channel varchar,
    order_status varchar,
    gross_amount number(12, 2),
    discount_amount number(12, 2),
    net_amount number(12, 2),
    payment_id varchar,
    payment_method varchar,
    payment_status varchar,
    payment_quality_status varchar,
    paid_amount number(12, 2),
    paid_at timestamp_ntz,
    is_completed_order boolean
);

create table if not exists INTERMEDIATE.INT_CUSTOMER_EVENTS (
    customer_id varchar,
    total_events number,
    page_view_count number,
    product_view_count number,
    add_to_cart_count number,
    checkout_started_count number,
    purchase_completed_count number,
    support_contact_count number,
    first_event_at timestamp_ntz,
    last_event_at timestamp_ntz
);

create table if not exists MARTS.FCT_ORDERS (
    order_id varchar,
    customer_id varchar,
    order_date date,
    sales_channel varchar,
    order_status varchar,
    gross_amount number(12, 2),
    discount_amount number(12, 2),
    net_amount number(12, 2),
    payment_id varchar,
    payment_method varchar,
    payment_status varchar,
    payment_quality_status varchar,
    paid_amount number(12, 2),
    paid_at timestamp_ntz,
    is_completed_order boolean
);

create table if not exists MARTS.MART_CUSTOMER_360 (
    customer_id varchar,
    full_name varchar,
    email varchar,
    city varchar,
    state varchar,
    customer_segment varchar,
    created_at timestamp_ntz,
    total_orders number,
    completed_orders number,
    canceled_orders number,
    pending_orders number,
    total_gross_amount number(12, 2),
    total_discount_amount number(12, 2),
    total_net_amount number(12, 2),
    total_paid_amount number(12, 2),
    total_events number,
    last_event_at timestamp_ntz,
    customer_lifecycle_status varchar
);
