# Arquitetura do Laboratorio

## Visao geral da arquitetura

Este projeto foi desenhado como um laboratorio local-first de Engenharia de Dados. A proposta e mostrar como uma esteira moderna de ingestao, transformacao, validacao e consumo pode ser organizada de forma clara, reproduzivel e pronta para explicacao tecnica, mesmo sem depender de Azure real ou Snowflake real.

O repositorio separa responsabilidades entre:

- fontes simuladas
- pipelines Python
- camada `landing`
- modelagem com dbt
- warehouse local em DuckDB
- dashboard em Streamlit
- validacoes automatizadas em CI/CD

## Decisao local-first

A decisao local-first foi adotada para manter o projeto:

- simples de executar no WSL2
- barato de manter
- facil de validar em entrevista ou demonstracao
- proximo de boas praticas reais de Engenharia de Dados

Em vez de simular a nuvem com excesso de complexidade, o laboratorio prioriza separacao de camadas, contratos, validacoes e rastreabilidade.

## Simulacao de servicos cloud

O projeto usa componentes locais para representar conceitos de uma arquitetura corporativa:

| Componente local | Equivalente conceitual | Papel arquitetural |
| --- | --- | --- |
| Azurite | Azure Blob Storage / ADLS Gen2 | Landing zone, armazenamento de arquivos e artefatos |
| Redpanda | Azure Event Hubs / Kafka | Publicacao e consumo de eventos |
| DuckDB | Snowflake | Camada analitica local |
| dbt + DuckDB | dbt + Snowflake | Transformacao em camadas, testes e documentacao |
| GitHub Actions | GitHub Actions / Azure DevOps | Validacao continua e automacao |

## Fluxo batch

O pipeline batch le arquivos sinteticos de `data/samples`, valida a estrutura minima e grava a camada `landing` em parquet.

Fluxo:

`customers.csv`, `orders.csv`, `payments.json`
-> `src/batch`
-> `data/landing`

Objetivos do fluxo batch:

- padronizar ingestao de dados estruturados
- aplicar validacoes simples e reutilizaveis
- preparar a camada de entrada para dbt
- registrar auditoria de execucao

## Fluxo streaming

O pipeline streaming usa Redpanda localmente para demonstrar uma esteira de eventos sem depender de servico cloud real.

Fluxo:

`events_sample.jsonl`
-> producer Python
-> topic `customer-events`
-> consumer Python
-> `data/landing/events/events.jsonl`

Esse fluxo existe para demonstrar integracao, consumo e persistencia de eventos em ambiente local.

## dbt e DuckDB

O dbt organiza a camada analitica sobre o DuckDB local em tres niveis:

- `staging`
- `intermediate`
- `marts`

Fluxo principal:

`landing files`
-> `dbt staging tables`
-> `dbt intermediate`
-> `dbt marts`
-> `data/warehouse/local_warehouse.duckdb`

O DuckDB funciona como warehouse analitico local e permite validar SQL, testes dbt e consumo do dashboard sem infraestrutura adicional.

## Staging como table para estabilidade de consumo

Os modelos `staging` que leem diretamente a camada `landing` foram materializados como `table`. Essa decisao foi importante para estabilizar o consumo do DuckDB por ferramentas externas, como o Streamlit.

Sem essa materializacao, views que apontavam para arquivos externos podiam depender de caminhos relativos e falhar quando o banco era consultado fora do contexto do dbt. Ao materializar `staging` como `table`, o consumo do dashboard ficou desacoplado desses caminhos.

## Camada marts

A camada `marts` concentra os datasets finais para consumo analitico:

- `dim_customers`
- `fct_orders`
- `mart_customer_360`

Esses modelos representam a parte mais proxima das perguntas de negocio do laboratorio, como receita, valor de cliente, canal de venda, status de pagamento e comportamento digital.

## Dashboard

O dashboard em Streamlit consome o DuckDB local e fecha o ciclo do laboratorio:

`dbt marts`
-> `DuckDB local`
-> `dashboard/app.py`

Ele foi mantido simples de proposito: o objetivo e demonstrar a camada de consumo analitico, nao construir um front-end complexo.

## Automacao e validacao continua

O repositorio usa GitHub Actions para validar:

- sintaxe Python
- testes Python
- `dbt debug`
- `dbt build`
- presenca da documentacao essencial

O CI nao usa Azure real, Snowflake real, secrets ou Redpanda obrigatorio no runner. Para manter a esteira previsivel, a validacao do dbt usa `prepare-dbt-inputs` para criar o arquivo de eventos necessario sem depender do broker.

Isso mostra uma pratica relevante de DevOps aplicada a Engenharia de Dados: automatizar o que importa sem tornar o pipeline fragil demais.

## Pontos de migracao para Azure + Snowflake

O desenho atual foi organizado para facilitar uma migracao futura, se desejado:

- `data/landing` pode evoluir para Blob Storage ou ADLS
- DuckDB pode ser substituido por Snowflake
- Redpanda pode ser substituido por Azure Event Hubs
- o profile do dbt pode apontar para um ambiente gerenciado
- GitHub Actions pode evoluir para uma esteira com ambientes, aprovacoes e controles mais fortes

## Resumo arquitetural

Fluxo completo do laboratorio:

```text
Fontes simuladas
-> data/samples
-> pipelines Python
-> data/landing
-> dbt staging tables
-> dbt intermediate
-> dbt marts
-> DuckDB local
-> Streamlit dashboard
-> GitHub Actions
```

## Observacao importante

Este projeto nao executa Azure nem Snowflake reais. O objetivo e demonstrar desenho de solucao, disciplina de engenharia e capacidade de validacao em um ambiente local e reproduzivel.
