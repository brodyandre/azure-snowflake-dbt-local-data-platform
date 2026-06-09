with customers as (
    select *
    from {{ ref('dim_customers') }}
),

orders as (
    select *
    from {{ ref('fct_orders') }}
),

customer_events as (
    select *
    from {{ ref('int_customer_events') }}
),

order_metrics as (
    select
        customer_id,
        count(order_id) as total_orders,
        sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
        sum(case when order_status = 'canceled' then 1 else 0 end) as canceled_orders,
        sum(case when order_status = 'pending' then 1 else 0 end) as pending_orders,
        sum(gross_amount) as total_gross_amount,
        sum(discount_amount) as total_discount_amount,
        sum(net_amount) as total_net_amount,
        sum(case when payment_quality_status = 'paid' then paid_amount else 0 end) as total_paid_amount
    from orders
    group by customer_id
)

select
    customers.customer_id,
    customers.full_name,
    customers.email,
    customers.city,
    customers.state,
    customers.customer_segment,
    customers.created_at,
    coalesce(order_metrics.total_orders, 0) as total_orders,
    coalesce(order_metrics.completed_orders, 0) as completed_orders,
    coalesce(order_metrics.canceled_orders, 0) as canceled_orders,
    coalesce(order_metrics.pending_orders, 0) as pending_orders,
    coalesce(order_metrics.total_gross_amount, 0) as total_gross_amount,
    coalesce(order_metrics.total_discount_amount, 0) as total_discount_amount,
    coalesce(order_metrics.total_net_amount, 0) as total_net_amount,
    coalesce(order_metrics.total_paid_amount, 0) as total_paid_amount,
    coalesce(customer_events.total_events, 0) as total_events,
    customer_events.last_event_at,
    case
        when coalesce(order_metrics.total_net_amount, 0) >= 1000
            and coalesce(order_metrics.total_orders, 0) >= 3
            then 'high_value'
        when coalesce(order_metrics.completed_orders, 0) >= 1
            then 'active'
        when coalesce(customer_events.total_events, 0) > 0
            and coalesce(order_metrics.completed_orders, 0) = 0
            then 'browsing'
        when coalesce(order_metrics.total_orders, 0) = 0
            and coalesce(customer_events.total_events, 0) = 0
            then 'inactive'
        else 'review_needed'
    end as customer_lifecycle_status
from customers
left join order_metrics
    on customers.customer_id = order_metrics.customer_id
left join customer_events
    on customers.customer_id = customer_events.customer_id
