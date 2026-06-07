# azure-snowflake-dbt-local-data-platform

## Objetivo

Construir um laboratorio local de Engenharia de Dados para demonstrar, de forma profissional e evolutiva, padroes inspirados em uma arquitetura Azure + Snowflake usando somente ferramentas gratuitas e executadas localmente.

## Visao geral

Este repositorio servira como ambiente pratico para estudar e demonstrar ingestao batch, streaming, modelagem analitica com dbt, qualidade de dados, governanca, consultas SQL, automacao CI/CD e documentacao tecnica.

Nesta fase inicial, o projeto estabelece apenas a base estrutural do repositorio, com diretorios, convencoes e documentos-guia para as proximas etapas.

## Tecnologias planejadas

- Python para orquestracao, ingestao e utilitarios.
- DuckDB como warehouse analitico local para simular conceitos de armazenamento e processamento inspirados no Snowflake.
- dbt para transformacao, testes e organizacao das camadas analiticas.
- Azurite para simular conceitos de Azure Blob Storage em ambiente local.
- Redpanda ou Apache Kafka para demonstrar padroes de streaming inspirados em Azure Event Hubs.
- SQL para modelagem analitica e consultas exploratorias.
- GitHub Actions para CI/CD local ao repositorio.
- Documentacao em Markdown para registrar requisitos, arquitetura e governanca.

## Status inicial do projeto

- Etapa atual: inicializacao da estrutura base.
- Escopo desta entrega: organizacao de diretorios, arquivos de configuracao e documentacao inicial.
- Sem pipelines implementados nesta fase.
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
