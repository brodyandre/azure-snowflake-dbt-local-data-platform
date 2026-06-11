-- Procedures simples para ilustrar controle operacional e publicacao analitica em Snowflake.

use database LOCAL_DATA_PLATFORM;

create or replace procedure CONTROL.REGISTER_PIPELINE_RUN(
    pipeline_name varchar,
    run_status varchar,
    rows_loaded number,
    execution_note varchar
)
returns varchar
language sql
execute as caller
as
$$
begin
    insert into CONTROL.PIPELINE_RUN_LOG (
        pipeline_name,
        run_status,
        rows_loaded,
        started_at,
        finished_at,
        execution_note
    )
    values (
        :pipeline_name,
        :run_status,
        :rows_loaded,
        current_timestamp(),
        current_timestamp(),
        :execution_note
    );

    return 'Pipeline run registered successfully';
end;
$$;

create or replace procedure MARTS.REFRESH_CUSTOMER_360()
returns varchar
language sql
execute as caller
as
$$
begin
    create or replace table MARTS.MART_CUSTOMER_360 as
    with order_metrics as (
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
        from MARTS.FCT_ORDERS
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
        coalesce(events.total_events, 0) as total_events,
        events.last_event_at,
        case
            when coalesce(order_metrics.total_net_amount, 0) >= 1000
                and coalesce(order_metrics.total_orders, 0) >= 3
                then 'high_value'
            when coalesce(order_metrics.completed_orders, 0) >= 1
                then 'active'
            when coalesce(events.total_events, 0) > 0
                and coalesce(order_metrics.completed_orders, 0) = 0
                then 'browsing'
            when coalesce(order_metrics.total_orders, 0) = 0
                and coalesce(events.total_events, 0) = 0
                then 'inactive'
            else 'review_needed'
        end as customer_lifecycle_status
    from MARTS.DIM_CUSTOMERS as customers
    left join order_metrics
        on customers.customer_id = order_metrics.customer_id
    left join INTERMEDIATE.INT_CUSTOMER_EVENTS as events
        on customers.customer_id = events.customer_id;

    return 'MARTS.MART_CUSTOMER_360 refreshed successfully';
end;
$$;
