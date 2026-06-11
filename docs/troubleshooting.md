# Troubleshooting

## Objetivo

Este guia reune problemas reais e provaveis do laboratorio, com solucoes objetivas para execucao local e validacao em CI.

## Python nao encontrado no WSL2

Sintoma:

- `python: command not found`

Solucao:

- usar `python3` em vez de `python`
- criar o ambiente virtual com `python3 -m venv .venv`

## Ambiente virtual nao ativado

Sintoma:

- bibliotecas como `dbt`, `pytest` ou `streamlit` nao sao encontradas

Solucao:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependencias nao instaladas

Sintoma:

- erro de import em `duckdb`, `pandas`, `streamlit` ou `dbt`

Solucao:

```bash
pip install -r requirements.txt
```

## Docker nao iniciado

Sintoma:

- `docker compose up` falha
- `make up` nao sobe Azurite ou Redpanda

Solucao:

- iniciar o Docker Desktop ou o daemon do Docker
- confirmar com `docker compose ps`

## Redpanda indisponivel

Sintoma:

- `make streaming-demo` nao publica ou consome eventos

Solucao:

```bash
make up
make ps
make streaming-demo
```

Se necessario, validar o broker com `docker compose ps` e abrir o Redpanda Console em `http://localhost:8080`.

## Streamlit pedindo e-mail na primeira execucao

Sintoma:

- o Streamlit mostra onboarding na primeira subida do dashboard

Solucao:

- o projeto inclui `.streamlit/config.toml` com `gatherUsageStats = false`
- rode novamente `make dashboard`

## Localhost recusando conexao

Sintoma:

- `http://localhost:8501` nao abre

Solucao:

- confirmar se o Streamlit esta rodando com `make dashboard`
- verificar se a porta `8501` nao esta ocupada
- em WSL2, garantir que o navegador esta acessando `http://localhost:8501`

## dbt nao encontra events.jsonl

Sintoma:

- erro relacionado a `data/landing/events/events.jsonl`

Solucao local:

```bash
make streaming-demo
make dbt-build
```

Solucao para CI ou validacao sem Redpanda:

```bash
make prepare-dbt-inputs
make dbt-build
```

## Problema de view dbt com caminho relativo

Sintoma:

- consultas ao DuckDB falham fora do contexto do dbt
- erro como `No files found that match the pattern ../data/landing/events/events.jsonl`

Causa provavel:

- modelos `staging` materializados como `view` apontando para arquivos externos

Solucao adotada no projeto:

- materializar `staging` como `table`

Isso estabiliza o consumo pelo dashboard e por outras ferramentas que consultam o DuckDB diretamente.

## GitHub Actions sem Redpanda

Sintoma:

- o runner de CI nao deve depender de broker ou Docker para validar dbt

Solucao adotada:

- usar `prepare-dbt-inputs` para copiar `data/samples/events_sample.jsonl` para `data/landing/events/events.jsonl`

## Comandos uteis para recuperacao

```bash
python3 -m compileall src dashboard
make batch
make streaming-demo
make prepare-dbt-inputs
make dbt-build
make test
make quality-report
make dashboard
```
