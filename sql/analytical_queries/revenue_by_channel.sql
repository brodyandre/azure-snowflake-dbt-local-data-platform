-- Objetivo:
-- Resumir receita bruta, descontos, receita liquida e quantidade de pedidos
-- agrupados por canal de venda.

with channel_metrics as (
    select
        sales_channel,
        count(*) as total_orders,
        sum(gross_amount) as gross_revenue,
        sum(discount_amount) as total_discount,
        sum(net_amount) as net_revenue,
        sum(case when is_completed_order then 1 else 0 end) as completed_orders
    from MARTS.FCT_ORDERS
    group by sales_channel
)

select
    sales_channel,
    total_orders,
    completed_orders,
    gross_revenue,
    total_discount,
    net_revenue
from channel_metrics
order by net_revenue desc, total_orders desc;
