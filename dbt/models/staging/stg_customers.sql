select
    cast(trim(customer_id) as varchar) as customer_id,
    trim(full_name) as full_name,
    lower(trim(email)) as email,
    trim(city) as city,
    upper(trim(state)) as state,
    cast(created_at as timestamp) as created_at,
    lower(trim(customer_segment)) as customer_segment
from {{ source('landing', 'customers') }}
