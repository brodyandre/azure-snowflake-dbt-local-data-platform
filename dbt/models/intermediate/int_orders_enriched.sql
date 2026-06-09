with orders as (
    select *
    from {{ ref('stg_orders') }}
),

payments as (
    select *
    from {{ ref('stg_payments') }}
),

orders_with_payments as (
    select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        orders.sales_channel,
        orders.order_status,
        orders.gross_amount,
        orders.discount_amount,
        orders.net_amount,
        payments.payment_id,
        payments.payment_method,
        payments.payment_status,
        payments.paid_amount,
        payments.paid_at
    from orders
    left join payments
        on orders.order_id = payments.order_id
)

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
    paid_amount,
    paid_at,
    case
        when payment_id is null then 'missing_payment'
        when payment_status = 'paid' then 'paid'
        when payment_status = 'pending' then 'pending'
        when payment_status = 'failed' then 'failed'
        when payment_status = 'refunded' then 'refunded'
        else 'unknown'
    end as payment_quality_status,
    case
        when order_status = 'completed' then true
        else false
    end as is_completed_order
from orders_with_payments
