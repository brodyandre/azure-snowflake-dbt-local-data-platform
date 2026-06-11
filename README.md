# azure-snowflake-dbt-local-data-platform

[![CI - Python Validation](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/ci.yml)
[![CI - dbt Validation](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/dbt-validation.yml/badge.svg)](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/dbt-validation.yml)
[![CI - Documentation Validation](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/docs-validation.yml/badge.svg)](https://github.com/brodyandre/azure-snowflake-dbt-local-data-platform/actions/workflows/docs-validation.yml)

## Visao geral

Este repositorio e um laboratorio local-first de Engenharia de Dados criado para simular, com ferramentas gratuitas e executaveis localmente, uma arquitetura inspirada em Azure + Snowflake. O projeto cobre ingestao batch, ingestao streaming, transformacoes com dbt, consumo analitico em DuckDB, dashboard com Streamlit, qualidade de dados, SQL analitico e validacoes com GitHub Actions.

O foco nao e reproduzir a nuvem produto a produto. O foco e demonstrar organizacao tecnica, boas praticas de engenharia, clareza de arquitetura e disciplina de validacao em um ambiente simples de subir no WSL2.

Documentacao complementar:

- [Arquitetura](docs/architecture.md)
- [Requisitos de negocio](docs/business_requirements.md)
- [Contratos de dados](docs/data_contracts.md)
- [Governanca de dados](docs/data_governance.md)
- [Migracao para Azure + Snowflake](docs/migration_to_azure_snowflake.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Status do projeto](docs/project_status.md)

## Objetivo do projeto

Construir um ambiente tecnico reproduzivel para demonstrar praticas de Engenharia de Dados local-first com desenho cloud-compatible. Isso inclui:

- ingestao e preparo de dados por pipelines Python
- simulacao de eventos em streaming
- organizacao da camada analitica com dbt
- uso do DuckDB como warehouse local
- consultas SQL e modelos analiticos com foco em negocio
- testes automatizados, relatorio de qualidade e CI/CD
- camada simples de consumo com Streamlit

## Responsabilidades da vaga demonstradas pelo projeto

| Requisito da vaga | Como o projeto demonstra | Arquivos ou componentes relacionados |
| --- | --- | --- |
| Engenharia de dados em ambiente cloud | Simula desenho de dados inspirado em Azure + Snowflake, mas com execucao local e sem credenciais reais | `docs/architecture.md`, `docs/migration_to_azure_snowflake.md`, `docker-compose.yml` |
| Pipelines batch | Processa fontes CSV e JSON, valida colunas obrigatorias e publica parquet na landing | `src/batch/`, `Makefile`, `data/samples/` |
| Pipelines streaming | Publica e consome eventos sinteticos para demonstrar ingestao orientada a eventos | `src/streaming/`, `make streaming-demo`, `data/landing/events/events.jsonl` |
| ETL/ELT | Separa ingestao Python da transformacao analitica com dbt sobre DuckDB | `src/batch/`, `dbt/models/`, `data/warehouse/local_warehouse.duckdb` |
| Azure-inspired architecture | Usa Azurite, Redpanda, DuckDB e dbt para representar conceitos equivalentes de storage, streaming e analytics | `docker-compose.yml`, `docs/architecture.md` |
| Snowflake-compatible SQL | Mantem exemplos de DDL, schemas, procedures e queries analiticas em sintaxe orientada a Snowflake | `sql/snowflake_compatible/`, `sql/analytical_queries/` |
| dbt | Organiza a camada analitica em `staging`, `intermediate` e `marts`, com testes e materializacoes controladas | `dbt/dbt_project.yml`, `dbt/models/` |
| Qualidade de dados | Usa testes dbt, testes Python e relatorio operacional consolidado | `tests/`, `dbt/models/*/schema.yml`, `src/quality/data_quality_report.py` |
| Governanca | Documenta contratos, rastreabilidade, auditoria e controles locais de evolucao | `docs/data_contracts.md`, `docs/data_governance.md`, `evidence/execution-logs/` |
| SQL analitico | Responde perguntas de receita, segmentacao, pagamento e customer 360 | `sql/analytical_queries/`, `dbt/models/marts/` |
| CI/CD | Valida Python, dbt e documentacao com workflows simples e reproduziveis | `.github/workflows/`, `Makefile` |
| DevOps | Padroniza comandos locais, automacao e validacoes sem depender de cloud real | `Makefile`, `.github/workflows/`, `docs/troubleshooting.md` |
| Dashboard analitico | Consome o DuckDB local em uma interface objetiva para leitura de KPIs e tabelas analiticas | `dashboard/app.py` |
| POC local | Reune infraestrutura, dados sinteticos, testes, SQL e dashboard em um laboratorio unico e demonstravel | repositorio completo |

## Arquitetura local

Fluxo principal do laboratorio:

```text
Fontes simuladas
→ data/samples
→ pipelines Python
→ data/landing
→ dbt staging tables
→ dbt intermediate
→ dbt marts
→ DuckDB local
→ Streamlit dashboard
→ GitHub Actions
```

Esse desenho ajuda a explicar a separacao entre ingestao, transformacao, consumo e validacao continua, mesmo sem usar Azure real nem Snowflake real nesta fase.

## Tecnologias utilizadas

- Python para pipelines, validacoes e utilitarios
- DuckDB como warehouse analitico local
- dbt Core com adapter DuckDB para modelagem e testes
- Streamlit para camada de consumo analitico local
- Redpanda para demonstracao de fluxo streaming local
- Azurite para simular padroes de object storage
- SQL para modelagem, analise e compatibilidade conceitual com Snowflake
- pytest para testes Python
- GitHub Actions para CI/CD
- Docker Compose para subir servicos locais

## Como este projeto simula Azure + Snowflake localmente

| Componente local | Equivalente conceitual | Papel no laboratorio |
| --- | --- | --- |
| Azurite | Azure Blob Storage / ADLS Gen2 | Representar landing zone e armazenamento de artefatos |
| Redpanda | Azure Event Hubs / Kafka | Representar publicacao e consumo de eventos |
| DuckDB | Snowflake | Representar a camada analitica local |
| dbt + DuckDB | dbt + Snowflake | Representar modelagem em camadas, testes e promocao de modelos |
| GitHub Actions | GitHub Actions / Azure DevOps | Representar automacao de validacao e esteira CI/CD |

## Limitacoes conhecidas

- O projeto nao executa Azure real nem Snowflake real localmente.
- O fluxo streaming em CI nao sobe broker; usa preparo de arquivos para manter a validacao simples.
- O ambiente local nao replica elasticidade, seguranca gerenciada, custo e operacao de uma plataforma cloud real.
- As evidencias visuais precisam ser capturadas manualmente pelo mantenedor e versionadas quando fizer sentido.

## Como executar localmente

Fluxo recomendado para demonstracao completa:

```bash
make up
make batch
make streaming-demo
make dbt-build
make test
make quality-report
make dashboard
```

Outros comandos uteis:

```bash
make ci-python
make ci-dbt
make ci-docs
make down
```

## Ambiente Python no WSL2

Em WSL2, o interpretador mais comum e `python3`. O preparo recomendado do ambiente local e:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m compileall src dashboard
```

Quando a `.venv` existe, o `Makefile` passa a preferir automaticamente `.venv/bin/python`, o que ajuda a manter o fluxo local consistente.

## Servicos locais com Docker Compose

Os servicos locais suportam a demonstracao de armazenamento, streaming e observabilidade operacional.

| Servico | Funcao | Portas |
| --- | --- | --- |
| Azurite | Simula object storage e landing zone | `10000`, `10001`, `10002` |
| Redpanda | Broker Kafka-compatible para eventos | `9092`, `29092`, `9644` |
| Redpanda Console | Inspecao visual do broker e topicos | `8080` |

Comandos:

```bash
make up
make ps
make logs
make down
```

## Fontes de dados simuladas

| Fonte | Formato | Papel no laboratorio |
| --- | --- | --- |
| `data/samples/customers.csv` | CSV | Cadastro sintetico de clientes |
| `data/samples/orders.csv` | CSV | Pedidos multicanal e metricas comerciais |
| `data/samples/payments.json` | JSON | Status de pagamento, falha, pendencia e estorno |
| `data/samples/events_sample.jsonl` | JSON Lines | Eventos digitais para navegacao, conversao e suporte |

## Pipeline batch

O pipeline batch le as fontes estruturadas, aplica validacoes minimas e grava a camada `landing` em parquet.

Entradas:

- `customers.csv`
- `orders.csv`
- `payments.json`

Saidas:

- `data/landing/customers/customers.parquet`
- `data/landing/orders/orders.parquet`
- `data/landing/payments/payments.parquet`

Comando:

```bash
make batch
```

Validacoes principais:

- colunas obrigatorias
- IDs obrigatorios
- tipagem de datas
- tipagem de valores monetarios
- remocao de espacos em campos textuais
- geracao de `net_amount`
- auditoria em `evidence/execution-logs/pipeline_audit.jsonl`

## Pipeline streaming

O pipeline streaming demonstra publicacao e consumo de eventos locais com Redpanda, sem dependencia de cloud real.

Fluxo:

`events_sample.jsonl` -> producer -> topic `customer-events` -> consumer -> `data/landing/events/events.jsonl`

Comandos:

```bash
make streaming-producer
make streaming-consumer
make streaming-demo
```

## Transformacoes com dbt

O dbt organiza a camada analitica sobre o DuckDB local.

Camadas:

- `staging`: limpeza, padronizacao e tipagem inicial
- `intermediate`: combinacoes e regras reutilizaveis
- `marts`: tabelas finais para consumo analitico

Comandos:

```bash
make dbt-debug
make dbt-run
make dbt-test
make dbt-build
```

Observacao importante: os modelos `staging` que leem arquivos da landing foram materializados como `table` para evitar problemas de resolucao de caminhos relativos quando o DuckDB e consultado por ferramentas externas, como o dashboard Streamlit.

## Modelagem analitica

| Modelo | Camada | Tipo | Finalidade |
| --- | --- | --- | --- |
| `stg_customers` | staging | table | Padronizar atributos cadastrais |
| `stg_orders` | staging | table | Padronizar pedidos e valores comerciais |
| `stg_payments` | staging | table | Padronizar pagamentos e seus status |
| `stg_events` | staging | table | Padronizar eventos digitais |
| `int_orders_enriched` | intermediate | view | Enriquecer pedidos com sinais de pagamento |
| `int_customer_events` | intermediate | view | Agregar eventos por cliente |
| `dim_customers` | marts | table | Publicar dimensao de clientes |
| `fct_orders` | marts | table | Publicar fato de pedidos |
| `mart_customer_360` | marts | table | Consolidar relacionamento, receita e engajamento |

## Qualidade de dados

O projeto combina validacoes em dois niveis:

- testes dbt para integridade analitica
- testes Python para contratos, landing e auditoria

O relatorio de qualidade fica em:

- `evidence/execution-logs/data_quality_report.md`

Comandos:

```bash
make test
make quality-report
```

## SQL e compatibilidade com Snowflake

Os arquivos em `sql/snowflake_compatible/` mostram como a camada analitica atual poderia ser descrita em um ambiente Snowflake, sem afirmar que Snowflake roda localmente.

Arquivos principais:

- `create_database.sql`
- `create_schemas.sql`
- `create_tables.sql`
- `procedures_examples.sql`

Consultas analiticas:

- `customer_360.sql`
- `revenue_by_channel.sql`
- `payment_quality_summary.sql`
- `customer_engagement_summary.sql`

## Dashboard local

O dashboard em Streamlit fecha o ciclo de consumo do laboratorio usando o DuckDB local como fonte analitica.

Modelos consultados:

- `mart_customer_360`
- `fct_orders`
- `dim_customers`
- `int_customer_events`

Comandos:

```bash
make batch
make streaming-demo
make dbt-build
make dashboard
```

URL esperada:

- `http://localhost:8501`

## CI/CD com GitHub Actions

Os workflows validam o projeto automaticamente sem depender de Azure real, Snowflake real, secrets ou servicos obrigatorios de infraestrutura no runner.

Workflows:

- `CI - Python Validation`: `compileall`, batch, testes Python e relatorio de qualidade
- `CI - dbt Validation`: batch, `prepare-dbt-inputs`, `dbt debug` e `dbt build`
- `CI - Documentation Validation`: presenca da documentacao e dos arquivos centrais do repositorio

Diferenca entre validacao local e validacao em CI:

- localmente, o fluxo completo pode usar `make streaming-demo` com Redpanda
- em CI, o projeto evita Docker e broker para manter a validacao simples e estavel

Por que o CI usa `prepare-dbt-inputs`:

- o `dbt build` precisa de `data/landing/events/events.jsonl`
- em CI, esse arquivo e preparado a partir de `data/samples/events_sample.jsonl`
- isso reduz dependencias externas e mantem a validacao reprodutivel

Comandos locais equivalentes:

```bash
make ci-python
make ci-dbt
make ci-docs
```

## Governanca de dados

O laboratorio documenta contratos, regras minimas de qualidade, auditoria e rastreabilidade para manter a evolucao tecnica controlada.

Leituras principais:

- [Contratos de dados](docs/data_contracts.md)
- [Governanca de dados](docs/data_governance.md)

Elementos praticos ja presentes:

- contratos das fontes sinteticas
- testes automatizados dbt e pytest
- relatorio de qualidade
- log de auditoria do pipeline
- validacao continua com GitHub Actions

## Evidencias de execucao

Os caminhos abaixo representam os prints esperados para publicacao no GitHub. Eles nao devem ser tratados como evidencias existentes ate que sejam capturados e versionados manualmente.

| Print esperado | Comando relacionado | Objetivo da evidencia | Status esperado |
| --- | --- | --- | --- |
| `evidence/screenshots/docker-compose-running.png` | `make up` / `make ps` | Mostrar servicos locais ativos | A capturar manualmente |
| `evidence/screenshots/batch-pipeline-success.png` | `make batch` | Registrar ingestao batch concluida | A capturar manualmente |
| `evidence/screenshots/streaming-demo-success.png` | `make streaming-demo` | Registrar publicacao e consumo de eventos | A capturar manualmente |
| `evidence/screenshots/dbt-build-success.png` | `make dbt-build` | Mostrar build e testes dbt aprovados | A capturar manualmente |
| `evidence/screenshots/pytest-success.png` | `make test` | Mostrar suite Python aprovada | A capturar manualmente |
| `evidence/screenshots/quality-report-generated.png` | `make quality-report` | Mostrar geracao do relatorio de qualidade | A capturar manualmente |
| `evidence/screenshots/streamlit-dashboard.png` | `make dashboard` | Mostrar camada de consumo analitico local | A capturar manualmente |
| `evidence/screenshots/github-actions-success.png` | workflows do GitHub Actions | Mostrar validacoes em CI aprovadas | A capturar manualmente |

## Troubleshooting

Problemas comuns e solucoes praticas foram organizados em:

- [docs/troubleshooting.md](docs/troubleshooting.md)

Esse guia cobre desde `python3` no WSL2 ate problemas de `events.jsonl`, Redpanda, Docker, Streamlit e resolucao de caminhos relativos no DuckDB.

## Proximos passos

- adicionar capturas reais de execucao na pasta `evidence/screenshots/`
- publicar evidencias do dashboard e dos workflows
- testar cenarios incrementais no dbt
- incluir cobertura de testes Python
- explorar uma versao de deploy controlado em ambiente cloud ou local mais proximo de producao

## Autor

- GitHub: [brodyandre](https://github.com/brodyandre)
