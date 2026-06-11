-- Visao de qualidade de pagamentos para apoiar acompanhamento operacional e financeiro.

select
    payment_quality_status,
    payment_method,
    count(*) as total_transactions,
    sum(net_amount) as total_net_amount,
    sum(case when payment_quality_status = 'paid' then paid_amount else 0 end) as settled_amount,
    count_if(payment_quality_status = 'paid') as paid_transactions,
    round(
        100 * count_if(payment_quality_status = 'paid') / nullif(count(*), 0),
        2
    ) as settlement_rate_pct
from MARTS.FCT_ORDERS
group by 1, 2
order by total_transactions desc, settlement_rate_pct desc;
