with staged_events as (
    select *
    from {{ ref('stg_events') }}
),

aggregated_events as (
    select
        customer_id,
        count(*) as total_events,
        sum(case when event_type = 'page_view' then 1 else 0 end) as page_view_count,
        sum(case when event_type = 'product_view' then 1 else 0 end) as product_view_count,
        sum(case when event_type = 'add_to_cart' then 1 else 0 end) as add_to_cart_count,
        sum(case when event_type = 'checkout_started' then 1 else 0 end) as checkout_started_count,
        sum(case when event_type = 'purchase_completed' then 1 else 0 end) as purchase_completed_count,
        sum(case when event_type = 'support_contact' then 1 else 0 end) as support_contact_count,
        min(event_timestamp) as first_event_at,
        max(event_timestamp) as last_event_at
    from staged_events
    group by customer_id
)

select
    customer_id,
    total_events,
    page_view_count,
    product_view_count,
    add_to_cart_count,
    checkout_started_count,
    purchase_completed_count,
    support_contact_count,
    first_event_at,
    last_event_at
from aggregated_events
