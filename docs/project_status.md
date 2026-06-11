# Status do Projeto

## Visao objetiva

O laboratorio ja cobre uma esteira local de Engenharia de Dados com ingestao, transformacao, consumo analitico, qualidade de dados e validacao automatizada.

## Funcionalidades concluidas

- pipelines batch para `customers`, `orders` e `payments`
- pipeline streaming local com Redpanda
- camada `landing` em arquivos locais
- modelagem com dbt sobre DuckDB
- modelos `staging`, `intermediate` e `marts`
- testes dbt
- testes Python com `pytest`
- relatorio de qualidade
- SQL analitico e exemplos compativeis com Snowflake
- dashboard local em Streamlit
- workflows GitHub Actions para Python, dbt e documentacao

## Validacoes disponiveis

- `python3 -m compileall src dashboard`
- `make test`
- `make quality-report`
- `make dbt-build`
- `make ci-python`
- `make ci-dbt`
- `make ci-docs`

## Comandos principais

```bash
make up
make batch
make streaming-demo
make dbt-build
make test
make quality-report
make dashboard
```

## Limitacoes conhecidas

- nao usa Azure real
- nao usa Snowflake real
- depende de captura manual para evidencias visuais
- o fluxo streaming em CI e simplificado por `prepare-dbt-inputs`

## Proximos passos possiveis

- versionar capturas reais em `evidence/screenshots/`
- ampliar cobertura de testes Python
- explorar modelos incrementais no dbt
- adicionar exemplos de deploy controlado
- aprofundar observabilidade e monitoramento
