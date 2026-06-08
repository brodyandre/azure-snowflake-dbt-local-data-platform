select
    cast(trim(event_id) as varchar) as event_id,
    cast(trim(customer_id) as varchar) as customer_id,
    lower(trim(event_type)) as event_type,
    cast(event_timestamp as timestamp) as event_timestamp,
    lower(trim(source_system)) as source_system
from {{ source('landing', 'events') }}
