# azure-snowflake-dbt-local-data-platform

## Objetivo

Construir um laboratorio local de Engenharia de Dados para demonstrar, de forma profissional e evolutiva, padroes inspirados em uma arquitetura Azure + Snowflake usando somente ferramentas gratuitas e executadas localmente.

## Visao geral

Este repositorio servira como ambiente pratico para estudar e demonstrar ingestao batch, streaming, modelagem analitica com dbt, qualidade de dados, governanca, consultas SQL, automacao CI/CD e documentacao tecnica.

Nesta fase atual, o projeto ja conta com a base estrutural do repositorio, servicos locais via Docker Compose e fontes sinteticas pequenas para apoiar as proximas etapas de pipeline, modelagem e validacao.

## Tecnologias planejadas

- Python para orquestracao, ingestao e utilitarios.
- DuckDB como warehouse analitico local para simular conceitos de armazenamento e processamento inspirados no Snowflake.
- dbt para transformacao, testes e organizacao das camadas analiticas.
- Azurite para simular conceitos de Azure Blob Storage em ambiente local.
- Redpanda ou Apache Kafka para demonstrar padroes de streaming inspirados em Azure Event Hubs.
- SQL para modelagem analitica e consultas exploratorias.
- GitHub Actions para CI/CD local ao repositorio.
- Documentacao em Markdown para registrar requisitos, arquitetura e governanca.

## Servicos locais

Os servicos abaixo sao executados com Docker Compose para manter o laboratorio local-first, simples de subir e compativel com uma futura migracao para cloud.

| Servico | Funcao no projeto | Porta local | Tecnologia cloud simulada |
| --- | --- | --- | --- |
| Azurite | Simula armazenamento de objetos e zonas de aterrissagem para ingestao de dados | `10000`, `10001`, `10002` | Azure Blob Storage |
| Redpanda | Broker Kafka-compatible para eventos, streaming e integracao entre produtores e consumidores | `9092`, `29092`, `9644` | Padrao de streaming inspirado em Azure Event Hubs / Kafka |
| Redpanda Console | Interface web local para visualizar topicos, mensagens e estado operacional do broker | `8080` | Console local de observacao para streaming |

Comandos operacionais:

```bash
make up
make down
make logs
make ps
docker compose ps
```

## Fontes de dados simuladas

As fontes abaixo sao sinteticas, pequenas e consistentes entre si. Elas existem para apoiar testes de pipeline, modelagem, SQL, qualidade de dados e cenarios de streaming, sem depender de dados reais.

| Fonte | Formato | Sistema simulado | Finalidade no projeto |
| --- | --- | --- | --- |
| `customers.csv` | CSV | CRM / cadastro mestre de clientes | Base de referencia para relacionamento de entidades e segmentacao |
| `orders.csv` | CSV | Plataforma de vendas multicanal | Simular pedidos, status comerciais e metricas de receita |
| `payments.json` | JSON | Gateway de pagamentos | Simular liquidacao, falha, pendencia e estorno de pagamentos |
| `events_sample.jsonl` | JSON Lines | Telemetria digital e canais de atendimento | Simular navegacao, conversao e sinais comportamentais para analytics |

## Padroes de codigo Python

Os utilitarios Python deste projeto seguem algumas convencoes simples para manter o laboratorio legivel, testavel e facil de evoluir.

- `pathlib` e usado para construir caminhos de forma portavel e evitar caminhos absolutos fixos.
- Logs estruturados com `logging` padrao ajudam na observabilidade local sem espalhar `print` pelos modulos.
- Funcoes reutilizaveis concentram leituras, escritas, configuracao e auditoria para reduzir duplicacao.
- A separacao entre `config`, `io`, `logger` e `audit` facilita manutencao, testes e extensao incremental.
- O foco e manter codigo simples, local-first, cloud-compatible e facil de entender por outras pessoas do time.

## Ambiente Python no WSL2

Em ambientes WSL2 com Ubuntu, o interpretador disponivel por padrao pode ser `python3`. O fluxo recomendado para preparar o ambiente local e:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m compileall src
```

O `Makefile` tambem usa a variavel `PYTHON` com valor padrao `python3`, o que ajuda a manter os comandos portaveis nesse contexto.

Quando a `.venv` existe, o `Makefile` passa a preferir automaticamente `.venv/bin/python`, o que simplifica a execucao dos targets locais sem depender do Python global do sistema.

## Pipeline batch

O pipeline batch local tem como objetivo ler os arquivos sinteticos em `data/samples`, aplicar validacoes minimas e gravar uma versao tratada em `data/landing` no formato Parquet.

Arquivos de origem:

- `data/samples/customers.csv`
- `data/samples/orders.csv`
- `data/samples/payments.json`

Arquivos de destino:

- `data/landing/customers/customers.parquet`
- `data/landing/orders/orders.parquet`
- `data/landing/payments/payments.parquet`

Validacoes realizadas:

- Presenca das colunas obrigatorias em cada fonte.
- Validacao de identificadores obrigatorios sem nulos ou valores vazios.
- Conversao de campos de data para datetime.
- Conversao de valores monetarios para tipo numerico.
- Remocao de espacos extras em campos textuais relevantes.
- Criacao da coluna `net_amount` na ingestao de pedidos.
- Registro de auditoria em caso de sucesso e falha.

Comando para executar:

```bash
make batch
```

Saida esperada:

- Logs claros indicando inicio e fim de cada etapa.
- Arquivos Parquet gerados em `data/landing`.
- Registro de auditoria por pipeline executado.
- Codigo de saida diferente de zero se alguma etapa falhar.

Localizacao dos arquivos gerados:

- `data/landing/customers/customers.parquet`
- `data/landing/orders/orders.parquet`
- `data/landing/payments/payments.parquet`

Localizacao do log de auditoria:

- `evidence/execution-logs/pipeline_audit.jsonl`

## Pipeline streaming

O pipeline streaming local demonstra um fluxo de eventos inspirado em Azure Event Hubs, mas executando localmente com Redpanda como broker Kafka-compatible, sem uso de servicos reais de nuvem.

Redpanda simula localmente um padrao semelhante ao Azure Event Hubs / Kafka, permitindo publicar e consumir eventos de forma simples, reproduzivel e adequada para testes de integracao.

Origem dos eventos:

- `data/samples/events_sample.jsonl`

Topico usado:

- `customer-events`

Destino dos eventos consumidos:

- `data/landing/events/events.jsonl`

Comandos para subir o ambiente:

```bash
make up
docker compose ps
```

Comandos para executar:

```bash
make streaming-producer
make streaming-consumer
```

Comando opcional:

```bash
make streaming-demo
```

Se o Redpanda Console estiver habilitado, ele pode ser acessado em:

- `http://localhost:8080`

## Status inicial do projeto

- Etapa atual: estrutura base com servicos locais, fontes de dados sinteticas, utilitarios Python reutilizaveis e pipelines batch e streaming locais.
- Escopo desta entrega: organizacao de diretorios, arquivos de configuracao, documentacao inicial, infraestrutura local de apoio, datasets pequenos para testes, base Python para ingestao, I/O, auditoria, ingestao batch e demonstracao streaming local.
- Sem uso de servicos Azure reais.
- Sem uso de Snowflake real.

## Arquitetura proposta

A proposta e evoluir o repositorio para uma arquitetura local com as seguintes camadas:

1. Ingestao batch para carregar dados brutos e simular processos de aterrissagem.
2. Ingestao streaming para representar eventos e micro-lotes em tempo quase real.
3. Camada de armazenamento local para dados de entrada e artefatos intermediarios.
4. Camada analitica em DuckDB para transformacoes, consultas e publicacao de datasets curados.
5. Camada de modelagem com dbt para organizar modelos, testes e documentacao de dados.
6. Camada de qualidade e governanca para validacoes, padroes e rastreabilidade.
7. Camada de entrega com queries analiticas, dashboards, evidencias e automacao CI/CD.

## Como este projeto simula Azure + Snowflake localmente

Este projeto nao executa Azure real nem Snowflake real. Em vez disso, utiliza equivalencias locais para estudar padroes arquiteturais:

- Azure Blob Storage: sera representado por Azurite para simular armazenamento de objetos e padroes de landing zone.
- Snowflake: nao roda localmente; os conceitos de warehouse, camadas analiticas e consultas serao simulados com DuckDB.
- Azure Event Hubs: os padroes de streaming serao demonstrados com Redpanda ou Apache Kafka em ambiente local.
- Orquestracao e automacao: serao representadas por scripts locais, Makefile e pipelines de CI/CD no GitHub Actions.

O foco do laboratorio e aprender desenho de solucao, integracao entre componentes, boas praticas de engenharia e preparo para uma futura migracao para servicos gerenciados.

## Limitacoes conhecidas

- O ambiente local nao reproduz elasticidade, seguranca e operacao gerenciada de Azure e Snowflake.
- Custos, performance distribuida e recursos corporativos avancados nao serao identicos ao ambiente de nuvem.
- Algumas integracoes serao simuladas por convencao arquitetural e nao por compatibilidade total de produto.
- A fidelidade do streaming local dependera das ferramentas escolhidas nas proximas etapas.
