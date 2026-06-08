select
    cast(trim(payment_id) as varchar) as payment_id,
    cast(trim(order_id) as varchar) as order_id,
    lower(trim(payment_method)) as payment_method,
    lower(trim(payment_status)) as payment_status,
    cast(paid_amount as decimal(18, 2)) as paid_amount,
    cast(paid_at as timestamp) as paid_at
from {{ source('landing', 'payments') }}
