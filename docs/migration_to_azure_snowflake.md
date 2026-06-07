# Migracao Futura para Azure + Snowflake

## Objetivo

Registrar como os componentes locais deste laboratorio podem orientar uma transicao futura para uma arquitetura em nuvem.

## Mapeamento conceitual inicial

- Azurite -> Azure Blob Storage
- DuckDB -> Snowflake como plataforma analitica alvo
- Redpanda ou Apache Kafka -> padroes inspirados em Azure Event Hubs
- Scripts locais e Makefile -> pipelines de automacao com CI/CD e orquestracao em nuvem

## Consideracoes

- O mapeamento e conceitual, nao produto a produto.
- Regras de seguranca, observabilidade e escalabilidade precisarao ser revistas na migracao real.
- Modelos de dados e padroes de transformacao devem ser mantidos o mais portaveis possivel.
