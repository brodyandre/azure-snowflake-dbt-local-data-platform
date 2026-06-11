# Governanca de Dados

## Objetivo da governanca neste laboratorio

A governanca deste projeto nao tenta replicar um programa corporativo completo. O objetivo aqui e mostrar, de forma local e didatica, como contratos, validacoes, auditoria e rastreabilidade podem ser tratados com seriedade mesmo em uma POC.

## Contratos de dados

Os contratos das fontes sinteticas estao documentados em [data_contracts.md](./data_contracts.md). Eles deixam explicitos:

- campos esperados
- tipos logicos
- obrigatoriedade
- dominios permitidos
- regras basicas de negocio
- exemplos de validacao

Isso reduz ambiguidade e ajuda a manter alinhamento entre ingestao, transformacao e consumo.

## Qualidade de dados

A qualidade de dados e tratada em dois niveis complementares:

- `pytest` valida contratos, fontes e artefatos gerados pelos pipelines
- `dbt` valida integridade, dominios e relacionamentos da camada analitica

Exemplos de controles ja implementados:

- `not_null`
- `unique`
- `relationships`
- `accepted_values`
- verificacao de artefatos de landing
- consistencia estrutural do log de auditoria

## Auditoria

O pipeline batch grava um log de auditoria em:

- `evidence/execution-logs/pipeline_audit.jsonl`

Esse arquivo ajuda a registrar, de forma simples:

- execucao do pipeline
- status da execucao
- momento da escrita
- consistencia basica da esteira local

Nao e uma trilha corporativa completa, mas demonstra a preocupacao com observabilidade e evidencia tecnica.

## Rastreabilidade

O projeto mantem uma linha de rastreabilidade clara entre:

- fontes em `data/samples`
- artefatos processados em `data/landing`
- modelos `staging`, `intermediate` e `marts`
- consultas SQL analiticas
- dashboard Streamlit
- logs e relatorios em `evidence/execution-logs`

Essa cadeia facilita entendimento, depuracao e demonstracao do fluxo ponta a ponta.

## Testes automatizados

Os testes sao parte da governanca do projeto, nao um detalhe isolado.

Camadas de validacao:

- testes Python em `tests/`
- testes dbt declarados nos arquivos `schema.yml`
- workflows GitHub Actions para repetibilidade em CI

Esse conjunto ajuda a impedir que o repositorio dependa apenas de validacao manual.

## Governanca local

Como o projeto foi desenhado para rodar localmente, a governanca tambem segue um desenho local-first:

- sem dados sensiveis reais
- sem secrets reais
- sem dependencia obrigatoria de cloud
- com documentacao versionada
- com comandos padronizados por `Makefile`

Esse modelo e suficiente para fins de portfolio, estudo e demonstracao tecnica.

## Como isso migraria para Azure + Snowflake

Em uma evolucao para ambiente corporativo, a governanca local poderia ser expandida com:

- contratos em catalogos ou repositorios corporativos
- controle de acesso por roles e ownership
- auditoria centralizada em storage e observabilidade gerenciada
- testes em multiplos ambientes com aprovacao
- politicas de classificacao, masking e retention

## Resumo

O laboratorio mostra que governanca nao precisa comecar apenas quando a plataforma chega em producao. Mesmo em um projeto local, ja e possivel demonstrar:

- contratos
- qualidade
- auditoria
- rastreabilidade
- validacao automatizada
