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

## Principios arquiteturais

- Evolucao incremental do repositorio.
- Separar dados brutos, dados em processamento e artefatos analiticos.
- Privilegiar componentes locais simples, reproduziveis e de baixo custo.
- Documentar decisoes desde o inicio para facilitar migracao futura.

## Observacao importante

Este projeto nao executa Azure nem Snowflake reais. O objetivo e simular conceitos arquiteturais, padroes operacionais e fluxos de desenvolvimento usando alternativas locais.
