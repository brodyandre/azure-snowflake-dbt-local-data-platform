-- Receita, pedidos concluidos e ticket medio por canal e mes de pedido.

select
    date_trunc('month', order_date) as order_month,
    sales_channel,
    count(*) as total_orders,
    sum(case when is_completed_order then 1 else 0 end) as completed_orders,
    sum(gross_amount) as gross_revenue,
    sum(discount_amount) as total_discount,
    sum(net_amount) as net_revenue,
    sum(case when payment_quality_status = 'paid' then paid_amount else 0 end) as settled_revenue,
    round(avg(net_amount), 2) as average_ticket
from MARTS.FCT_ORDERS
group by 1, 2
order by order_month, net_revenue desc;
