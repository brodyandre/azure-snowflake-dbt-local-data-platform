-- Resumo de engajamento digital por segmento cadastral.

select
    customers.customer_segment,
    count(*) as customers_with_events,
    avg(events.total_events) as average_events_per_customer,
    sum(events.page_view_count) as total_page_views,
    sum(events.product_view_count) as total_product_views,
    sum(events.add_to_cart_count) as total_add_to_cart,
    sum(events.checkout_started_count) as total_checkout_started,
    sum(events.purchase_completed_count) as total_purchase_completed,
    sum(events.support_contact_count) as total_support_contacts,
    max(events.last_event_at) as most_recent_event_at
from INTERMEDIATE.INT_CUSTOMER_EVENTS as events
inner join MARTS.DIM_CUSTOMERS as customers
    on events.customer_id = customers.customer_id
group by customers.customer_segment
order by average_events_per_customer desc, total_purchase_completed desc;
