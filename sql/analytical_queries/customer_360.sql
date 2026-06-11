-- Consulta orientada a relacionamento, receita e sinais de engajamento por cliente.

select
    customer_id,
    full_name,
    city,
    state,
    customer_segment,
    customer_lifecycle_status,
    total_orders,
    total_net_amount,
    total_paid_amount,
    total_events,
    last_event_at,
    case
        when total_events >= 4 then 'high_engagement'
        when total_events >= 2 then 'medium_engagement'
        when total_events = 1 then 'low_engagement'
        else 'no_recent_engagement'
    end as engagement_band
from MARTS.MART_CUSTOMER_360
order by total_net_amount desc, total_events desc;
