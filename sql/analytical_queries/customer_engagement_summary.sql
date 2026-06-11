-- Objetivo:
-- Resumir engajamento digital por cliente, destacando ultima interacao e
-- clientes com navegacao, mas sem compra concluida.

with completed_orders as (
    select
        customer_id,
        sum(case when is_completed_order then 1 else 0 end) as completed_orders
    from MARTS.FCT_ORDERS
    group by customer_id
),

customer_engagement as (
    select
        customers.customer_id,
        customers.full_name,
        customers.customer_segment,
        events.total_events,
        events.page_view_count,
        events.product_view_count,
        events.add_to_cart_count,
        events.checkout_started_count,
        events.purchase_completed_count,
        events.support_contact_count,
        events.last_event_at,
        coalesce(completed_orders.completed_orders, 0) as completed_orders
    from INTERMEDIATE.INT_CUSTOMER_EVENTS as events
    inner join MARTS.DIM_CUSTOMERS as customers
        on events.customer_id = customers.customer_id
    left join completed_orders
        on events.customer_id = completed_orders.customer_id
)

select
    customer_id,
    full_name,
    customer_segment,
    total_events,
    page_view_count,
    product_view_count,
    add_to_cart_count,
    checkout_started_count,
    purchase_completed_count,
    support_contact_count,
    last_event_at,
    case
        when total_events > 0 and completed_orders = 0 then true
        else false
    end as has_browsing_without_completed_purchase
from customer_engagement
order by has_browsing_without_completed_purchase desc, total_events desc, last_event_at desc;
