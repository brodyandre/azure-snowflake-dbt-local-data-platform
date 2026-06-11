-- Estes exemplos sao referencia arquitetural para Snowflake SQL/Scripting.
-- Eles nao precisam ser executados no laboratorio local em DuckDB.

use database LOCAL_DATA_PLATFORM_DEMO;

create or replace procedure GOVERNANCE.SP_REGISTER_PIPELINE_AUDIT(
    pipeline_name varchar,
    pipeline_status varchar,
    started_at timestamp_ntz,
    finished_at timestamp_ntz,
    records_processed number,
    message varchar
)
returns varchar
language sql
execute as caller
as
$$
begin
    insert into GOVERNANCE.PIPELINE_AUDIT (
        pipeline_name,
        status,
        started_at,
        finished_at,
        records_processed,
        message
    )
    values (
        :pipeline_name,
        :pipeline_status,
        :started_at,
        :finished_at,
        :records_processed,
        :message
    );

    return 'Pipeline audit registered successfully';
end;
$$;

create or replace procedure GOVERNANCE.SP_REGISTER_DATA_QUALITY_RESULT(
    dataset_name varchar,
    check_name varchar,
    check_status varchar,
    affected_records number,
    details varchar
)
returns varchar
language sql
execute as caller
as
$$
begin
    insert into GOVERNANCE.DATA_QUALITY_RESULTS (
        dataset_name,
        check_name,
        check_status,
        checked_at,
        affected_records,
        details
    )
    values (
        :dataset_name,
        :check_name,
        :check_status,
        current_timestamp(),
        :affected_records,
        :details
    );

    return 'Data quality result registered successfully';
end;
$$;

create or replace procedure MARTS.SP_REFRESH_CUSTOMER_360()
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
    ),
    customer_events as (
        select
            customer_id,
            total_events,
            last_event_at
        from INTERMEDIATE.INT_CUSTOMER_EVENTS
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
    from MARTS.DIM_CUSTOMERS as customers
    left join order_metrics
        on customers.customer_id = order_metrics.customer_id
    left join customer_events
        on customers.customer_id = customer_events.customer_id;

    return 'MARTS.MART_CUSTOMER_360 refreshed successfully';
end;
$$;

-- Task conceitual para agendar a atualizacao do mart em Snowflake.
create or replace task MARTS.TASK_REFRESH_CUSTOMER_360
    warehouse = WH_TRANSFORMING
    schedule = 'USING CRON 0 * * * * UTC'
    comment = 'Task conceitual para atualizar a visao customer 360 a cada hora'
as
    call MARTS.SP_REFRESH_CUSTOMER_360();

alter task MARTS.TASK_REFRESH_CUSTOMER_360 suspend;

-- Stream conceitual para captura de mudancas incrementais em eventos.
create or replace stream RAW.EVENTS_CHANGES
    on table RAW.EVENTS
    append_only = true
    comment = 'Stream conceitual para CDC/logica incremental sobre eventos';
