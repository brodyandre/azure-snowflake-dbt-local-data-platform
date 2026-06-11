# Arquitetura do Laboratorio

## Proposito

Definir a arquitetura inicial de um laboratorio local de Engenharia de Dados inspirado em padroes Azure + Snowflake, sem depender de servicos pagos.

## Camadas propostas

1. `data/raw`: recepcao de dados brutos vindos de cargas locais ou simuladas.
2. `data/landing`: zona intermediaria para dados preparados para processamento.
3. `src/batch`: pipelines batch e rotinas de carga.
4. `src/streaming`: produtores, consumidores e adaptadores de eventos.
5. `src/quality`: regras de validacao, contratos e checks de qualidade.
6. `dbt`: projeto analitico e transformacoes orientadas a modelo.
7. `sql`: consultas compativeis com a proposta analitica do projeto.
8. `dashboard`: camada futura para visualizacao de resultados.
9. `.github/workflows`: automacao CI/CD do repositorio.

## Componentes locais planejados

- Azurite para simular padroes de Azure Blob Storage.
- DuckDB para representar conceitos de warehouse analitico inspirados em Snowflake.
- Redpanda ou Apache Kafka para representar padroes de streaming inspirados em Azure Event Hubs.
- dbt para modelagem, testes e organizacao das transformacoes.

## Fluxo streaming local

O fluxo streaming proposto para este laboratorio segue o caminho abaixo:

`events_sample.jsonl`
-> producer Python
-> Redpanda topic `customer-events`
-> consumer Python
-> `data/landing/events/events.jsonl`

Esse fluxo permite demonstrar publicacao e consumo de eventos em ambiente local, sem depender de Azure real, mantendo o desenho compativel com padroes de event streaming usados em arquiteturas cloud.

## Camada ELT com dbt

O fluxo ELT planejado para a camada analitica local segue o caminho abaixo:

`data/landing`
-> `dbt staging tables`
-> `dbt intermediate`
-> `dbt marts`
-> `data/warehouse/local_warehouse.duckdb`

Nessa abordagem, o dbt organiza as transformacoes em camadas e o DuckDB funciona como warehouse analitico local. A materializacao da `staging` como `table` ajuda a desacoplar o consumo analitico dos caminhos relativos usados pelas fontes locais. Em um ambiente cloud, o profile do dbt poderia apontar para Snowflake, preservando os conceitos de modelagem sem afirmar que Snowflake roda localmente.

## Fluxo de modelagem dbt

O fluxo de modelagem analitica implementado no dbt segue a sequencia abaixo:

`landing files`
-> `staging`
-> `intermediate`
-> `marts`
-> `analytics/dashboard`

Nesse desenho, os arquivos tratados na landing servem como base para a padronizacao inicial, as regras reutilizaveis ficam concentradas na camada intermediate e os datasets finais ficam publicados na camada marts para consumo analitico.

## Camada de consumo analitico

O fluxo de consumo analitico deste laboratorio segue um desenho direto e facil de explicar:

`landing files`
-> `dbt staging tables`
-> `dbt intermediate e marts`
-> `DuckDB local`
-> `Streamlit dashboard`

Com isso, o projeto mostra nao apenas ingestao e transformacao, mas tambem a etapa final de consumo dos dados curados em uma interface local, sem depender de cloud real.

## Principios arquiteturais

- Evolucao incremental do repositorio.
- Separar dados brutos, dados em processamento e artefatos analiticos.
- Privilegiar componentes locais simples, reproduziveis e de baixo custo.
- Documentar decisoes desde o inicio para facilitar migracao futura.

## Compatibilidade conceitual com Snowflake

O laboratorio usa DuckDB para execucao local, mas tenta manter nomenclatura, separacao de camadas e contratos de dados proximos do que seria esperado em uma esteira com Snowflake. Isso reduz retrabalho na migracao futura porque os modelos dbt, as regras de qualidade e as consultas analiticas continuam organizados por responsabilidade, nao por ferramenta.

Os scripts em `sql/snowflake_compatible` nao afirmam que Snowflake roda localmente. Eles existem para mostrar como database, schemas, tabelas de controle, tabelas analiticas e procedures poderiam ser descritos em um ambiente gerenciado, preservando a mesma logica de negocio usada hoje no DuckDB.

## Observacao importante

Este projeto nao executa Azure nem Snowflake reais. O objetivo e simular conceitos arquiteturais, padroes operacionais e fluxos de desenvolvimento usando alternativas locais.
