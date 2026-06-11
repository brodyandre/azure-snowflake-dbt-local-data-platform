# Requisitos de Negocio

## Contexto de negocio simulado

O laboratorio representa um cenario simplificado de uma operacao digital que combina cadastro de clientes, pedidos, pagamentos e eventos de navegacao. A ideia nao e reproduzir um dominio completo, mas criar um ambiente pequeno e coerente para demonstrar como Engenharia de Dados apoia operacao, analise e governanca.

As fontes sinteticas simulam:

- um cadastro mestre de clientes
- uma operacao de vendas multicanal
- um gateway de pagamentos
- sinais de comportamento digital e suporte

## Necessidades de negocio

Do ponto de vista do negocio, a plataforma precisa permitir:

- consolidar clientes, pedidos e pagamentos em uma base confiavel
- acompanhar receita liquida e desempenho por canal
- entender engajamento digital e lifecycle de clientes
- identificar pendencias e problemas de pagamento
- manter rastreabilidade minima das execucoes e validacoes

## Requisitos funcionais

O projeto deve ser capaz de:

1. Ler datasets sinteticos locais em formatos CSV, JSON e JSON Lines.
2. Processar essas fontes em pipelines Python de forma reprodutivel.
3. Publicar uma camada `landing` pronta para transformacao analitica.
4. Organizar transformacoes com dbt em `staging`, `intermediate` e `marts`.
5. Produzir datasets finais de consumo, incluindo `dim_customers`, `fct_orders` e `mart_customer_360`.
6. Validar qualidade minima com testes dbt e testes Python.
7. Gerar um relatorio operacional de qualidade.
8. Disponibilizar consultas analiticas e um dashboard local.
9. Validar o repositorio automaticamente por GitHub Actions.

## Requisitos nao funcionais

O laboratorio tambem precisa atender a alguns requisitos tecnicos e operacionais:

- execucao local em WSL2 sem cloud real
- baixo custo operacional
- reprodutibilidade dos comandos
- documentacao clara para estudo e portfolio
- separacao entre ingestao, transformacao, consumo e validacao
- ausencia de segredos reais e credenciais externas
- simplicidade suficiente para rodar localmente sem perder valor tecnico

## Perguntas analiticas respondidas pelo projeto

A camada analitica foi organizada para responder perguntas como:

- Qual e a receita liquida por cliente?
- Quais clientes concentram maior valor acumulado?
- Quais canais trazem mais pedidos e receita?
- Quais pagamentos estao pagos, pendentes, falhos ou sem registro?
- Quais clientes demonstram engajamento digital sem conversao?
- Como combinar sinais de pedidos, pagamentos e eventos em uma visao `customer 360`?

## Relacao com Engenharia de Dados corporativa

Mesmo sendo um laboratorio local, o projeto conversa diretamente com necessidades comuns em ambientes corporativos:

- ingestao de dados de multiplas fontes
- modelagem em camadas
- padronizacao de contratos e schemas
- qualidade de dados automatizada
- rastreabilidade de execucoes
- consumo analitico por tabelas e dashboard
- validacao continua por CI/CD

## Valor do laboratorio para portfolio

Este projeto serve como prova pratica de que o autor consegue:

- organizar uma plataforma de dados pequena, mas coerente
- transformar requisitos de negocio em componentes tecnicos
- explicar arquitetura, fluxos e validacoes com clareza
- conectar batch, streaming, dbt, SQL, dashboard e CI em um unico repositorio
