-- DDL conceitual em sintaxe proxima de Snowflake.
-- O objetivo e demonstrar como as principais entidades do laboratorio local
-- poderiam ser mapeadas para uma arquitetura analitica gerenciada.

use database LOCAL_DATA_PLATFORM_DEMO;

create table if not exists RAW.CUSTOMERS (
    customer_id varchar comment 'Identificador unico do cliente',
    full_name varchar comment 'Nome completo do cliente',
    email varchar comment 'Endereco de email padronizado',
    city varchar comment 'Cidade declarada no cadastro',
    state varchar comment 'Unidade federativa do cliente',
    created_at timestamp_ntz comment 'Timestamp de criacao do cadastro',
    customer_segment varchar comment 'Segmento comercial do cliente',
    ingestion_ts timestamp_ntz default current_timestamp() comment 'Momento de aterrissagem do registro'
)
comment = 'Tabela raw para clientes vindos do CRM ou cadastro mestre';

create table if not exists RAW.ORDERS (
    order_id varchar comment 'Identificador unico do pedido',
    customer_id varchar comment 'Cliente associado ao pedido',
    order_date date comment 'Data operacional do pedido',
    sales_channel varchar comment 'Canal de venda utilizado',
    order_status varchar comment 'Status do pedido',
    gross_amount number(18, 2) comment 'Valor bruto do pedido',
    discount_amount number(18, 2) comment 'Valor total de descontos',
    ingestion_ts timestamp_ntz default current_timestamp() comment 'Momento de aterrissagem do registro'
)
comment = 'Tabela raw para pedidos multicanal';

create table if not exists RAW.PAYMENTS (
    payment_id varchar comment 'Identificador unico do pagamento',
    order_id varchar comment 'Pedido relacionado ao pagamento',
    payment_method varchar comment 'Metodo de pagamento',
    payment_status varchar comment 'Status do processamento do pagamento',
    paid_amount number(18, 2) comment 'Valor pago ou esperado',
    paid_at timestamp_ntz comment 'Timestamp do pagamento quando aplicavel',
    ingestion_ts timestamp_ntz default current_timestamp() comment 'Momento de aterrissagem do registro'
)
comment = 'Tabela raw para eventos financeiros de pagamento';

create table if not exists RAW.EVENTS (
    event_id varchar comment 'Identificador unico do evento',
    customer_id varchar comment 'Cliente associado ao evento',
    event_type varchar comment 'Tipo do evento digital',
    event_timestamp timestamp_ntz comment 'Momento em que o evento ocorreu',
    source_system varchar comment 'Sistema de origem do evento',
    ingestion_ts timestamp_ntz default current_timestamp() comment 'Momento de aterrissagem do evento'
)
comment = 'Tabela raw para eventos digitais vindos de streaming';

create table if not exists MARTS.DIM_CUSTOMERS (
    customer_id varchar comment 'Chave de negocio do cliente',
    full_name varchar comment 'Nome tratado do cliente',
    email varchar comment 'Email padronizado',
    city varchar comment 'Cidade tratada',
    state varchar comment 'UF tratada',
    customer_segment varchar comment 'Segmento comercial padronizado',
    created_at timestamp_ntz comment 'Data de criacao do cliente'
)
comment = 'Dimensao analitica de clientes';

create table if not exists MARTS.FCT_ORDERS (
    order_id varchar comment 'Chave do pedido',
    customer_id varchar comment 'Cliente relacionado ao pedido',
    order_date date comment 'Data do pedido',
    sales_channel varchar comment 'Canal comercial do pedido',
    order_status varchar comment 'Status operacional do pedido',
    gross_amount number(18, 2) comment 'Valor bruto',
    discount_amount number(18, 2) comment 'Valor de desconto',
    net_amount number(18, 2) comment 'Valor liquido do pedido',
    payment_id varchar comment 'Pagamento associado ao pedido',
    payment_method varchar comment 'Metodo de pagamento',
    payment_status varchar comment 'Status original do pagamento',
    payment_quality_status varchar comment 'Classificacao simplificada da qualidade do pagamento',
    paid_amount number(18, 2) comment 'Valor efetivamente pago',
    paid_at timestamp_ntz comment 'Momento do pagamento',
    is_completed_order boolean comment 'Indicador se o pedido foi concluido'
)
comment = 'Fato analitica de pedidos enriquecidos com informacoes de pagamento';

create table if not exists MARTS.MART_CUSTOMER_360 (
    customer_id varchar comment 'Cliente consolidado na visao 360',
    full_name varchar comment 'Nome do cliente',
    email varchar comment 'Email do cliente',
    city varchar comment 'Cidade do cliente',
    state varchar comment 'UF do cliente',
    customer_segment varchar comment 'Segmento comercial',
    created_at timestamp_ntz comment 'Data de criacao do cadastro',
    total_orders number comment 'Quantidade total de pedidos',
    completed_orders number comment 'Quantidade de pedidos concluidos',
    canceled_orders number comment 'Quantidade de pedidos cancelados',
    pending_orders number comment 'Quantidade de pedidos pendentes',
    total_gross_amount number(18, 2) comment 'Receita bruta acumulada',
    total_discount_amount number(18, 2) comment 'Descontos acumulados',
    total_net_amount number(18, 2) comment 'Receita liquida acumulada',
    total_paid_amount number(18, 2) comment 'Valor total liquidado',
    total_events number comment 'Quantidade de eventos digitais',
    last_event_at timestamp_ntz comment 'Ultimo evento conhecido',
    customer_lifecycle_status varchar comment 'Classificacao de lifecycle do cliente'
)
comment = 'Visao analitica consolidada de clientes, pedidos e eventos';

create table if not exists GOVERNANCE.PIPELINE_AUDIT (
    audit_id number autoincrement start 1 increment 1 comment 'Chave tecnica da auditoria',
    pipeline_name varchar comment 'Nome do pipeline ou processo',
    status varchar comment 'Status da execucao',
    started_at timestamp_ntz comment 'Inicio da execucao',
    finished_at timestamp_ntz comment 'Fim da execucao',
    records_processed number comment 'Quantidade de registros processados',
    message varchar comment 'Mensagem operacional resumida'
)
comment = 'Tabela de auditoria operacional de pipelines';

create table if not exists GOVERNANCE.DATA_QUALITY_RESULTS (
    quality_result_id number autoincrement start 1 increment 1 comment 'Chave tecnica do resultado de qualidade',
    dataset_name varchar comment 'Dataset analisado',
    check_name varchar comment 'Nome da regra ou verificacao',
    check_status varchar comment 'Resultado da verificacao',
    checked_at timestamp_ntz default current_timestamp() comment 'Momento da avaliacao',
    affected_records number comment 'Quantidade de registros afetados',
    details varchar comment 'Detalhes resumidos da verificacao'
)
comment = 'Tabela para registrar resultados de testes e verificacoes de qualidade';
