select
    customer_id,
    full_name,
    email,
    city,
    state,
    customer_segment,
    created_at
from {{ ref('stg_customers') }}
