-- Objetivo:
-- Consultar a visao customer 360 com foco em cliente, receita liquida,
-- total de pedidos, total de eventos e status de ciclo de vida.

with customer_summary as (
    select
        customer_id,
        full_name,
        email,
        city,
        state,
        customer_segment,
        total_orders,
        total_net_amount,
        total_paid_amount,
        total_events,
        customer_lifecycle_status,
        last_event_at
    from MARTS.MART_CUSTOMER_360
)

select
    customer_id,
    full_name,
    email,
    city,
    state,
    customer_segment,
    total_orders,
    total_net_amount,
    total_paid_amount,
    total_events,
    customer_lifecycle_status,
    last_event_at
from customer_summary
order by total_net_amount desc, total_orders desc, total_events desc;
