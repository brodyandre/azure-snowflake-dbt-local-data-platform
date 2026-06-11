-- Objetivo:
-- Consolidar status de pagamento, quantidade de pedidos, valor pago e
-- indicadores de pendencia operacional.

with payment_summary as (
    select
        payment_quality_status,
        count(*) as total_orders,
        sum(paid_amount) as total_paid_amount,
        sum(case when payment_quality_status in ('pending', 'failed', 'missing_payment') then 1 else 0 end)
            as pending_or_problem_orders,
        sum(case when payment_quality_status = 'pending' then paid_amount else 0 end) as pending_amount
    from MARTS.FCT_ORDERS
    group by payment_quality_status
)

select
    payment_quality_status,
    total_orders,
    total_paid_amount,
    pending_or_problem_orders,
    pending_amount
from payment_summary
order by total_orders desc, total_paid_amount desc;
