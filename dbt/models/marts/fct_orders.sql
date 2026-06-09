select
    order_id,
    customer_id,
    order_date,
    sales_channel,
    order_status,
    gross_amount,
    discount_amount,
    net_amount,
    payment_id,
    payment_method,
    payment_status,
    payment_quality_status,
    paid_amount,
    paid_at,
    is_completed_order
from {{ ref('int_orders_enriched') }}
