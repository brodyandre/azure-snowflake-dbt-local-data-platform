select
    cast(trim(order_id) as varchar) as order_id,
    cast(trim(customer_id) as varchar) as customer_id,
    cast(order_date as date) as order_date,
    lower(trim(sales_channel)) as sales_channel,
    lower(trim(order_status)) as order_status,
    cast(gross_amount as decimal(18, 2)) as gross_amount,
    cast(discount_amount as decimal(18, 2)) as discount_amount,
    cast(net_amount as decimal(18, 2)) as net_amount
from {{ source('landing', 'orders') }}
