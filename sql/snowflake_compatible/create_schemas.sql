-- Este arquivo documenta a organizacao conceitual de schemas para uma
-- implementacao futura em Snowflake. O laboratorio continua executando
-- localmente com DuckDB e dbt.

use database LOCAL_DATA_PLATFORM_DEMO;

create schema if not exists RAW
    comment = 'Camada de recepcao inicial de dados brutos vindos de batch e streaming';

create schema if not exists STAGING
    comment = 'Camada de padronizacao basica e tipagem inicial das fontes';

create schema if not exists INTERMEDIATE
    comment = 'Camada de regras reutilizaveis e combinacoes entre entidades';

create schema if not exists MARTS
    comment = 'Camada final para dimensoes, fatos e visoes analiticas';

create schema if not exists GOVERNANCE
    comment = 'Camada de auditoria, qualidade de dados e controles operacionais';

-- Exemplos conceituais de grants para um ambiente corporativo:
-- grant usage on database LOCAL_DATA_PLATFORM_DEMO to role ROLE_TRANSFORMER;
-- grant usage on schema STAGING to role ROLE_TRANSFORMER;
-- grant usage on schema INTERMEDIATE to role ROLE_TRANSFORMER;
-- grant usage on schema MARTS to role ROLE_ANALYST;
-- grant select on all tables in schema MARTS to role ROLE_ANALYST;
-- grant usage on schema GOVERNANCE to role ROLE_GOVERNANCE;
