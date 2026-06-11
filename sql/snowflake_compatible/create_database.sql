-- Este arquivo e uma referencia de migracao conceitual para Snowflake.
-- Ele nao e executado no DuckDB local do laboratorio.
-- O objetivo e demonstrar como a estrutura basica do ambiente poderia ser
-- provisionada em uma plataforma Snowflake real.

create database if not exists LOCAL_DATA_PLATFORM_DEMO
    comment = 'Database conceitual para a plataforma local-first migrada para Snowflake';

create warehouse if not exists WH_TRANSFORMING
    warehouse_size = 'XSMALL'
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true
    comment = 'Warehouse conceitual para cargas ELT, dbt e transformacoes';

create warehouse if not exists WH_ANALYTICS
    warehouse_size = 'XSMALL'
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true
    comment = 'Warehouse conceitual para consumo analitico, BI e consultas de negocio';

use database LOCAL_DATA_PLATFORM_DEMO;

-- Os schemas por camada sao criados no arquivo create_schemas.sql.
