# Requisitos de Negocio

## Contexto

O projeto busca demonstrar uma plataforma de dados local que possa servir como portfolio tecnico e ambiente de estudo para Engenharia de Dados moderna.

## Objetivos de negocio

- Demonstrar dominio pratico de pipelines batch e streaming.
- Evidenciar uso disciplinado de SQL, dbt, testes e documentacao.
- Criar um ambiente reproduzivel para evoluir cenarios de ingestao, transformacao e consumo analitico.
- Manter o projeto compativel com uma futura migracao para componentes Azure e Snowflake reais.

## Capacidades esperadas

- Carregar datasets brutos e processa-los por camadas.
- Simular eventos de streaming e consumo analitico.
- Produzir modelos curados com dbt.
- Aplicar verificacoes basicas de qualidade de dados.
- Gerar evidencias para fins de documentacao e auditoria tecnica.

## Perguntas de negocio

Os modelos analiticos da camada `marts` devem responder, de forma simples e reproduzivel, as seguintes perguntas de negocio:

- Qual e a receita liquida por cliente?
- Quais clientes possuem maior valor acumulado?
- Quais canais concentram mais pedidos?
- Quais clientes tem eventos digitais sem compra concluida?
- Quais pedidos possuem problemas ou pendencias de pagamento?

## Restricoes

- Nao utilizar servicos pagos.
- Nao depender de cloud real nesta etapa.
- Priorizar simplicidade operacional em WSL2 no Windows 11.
