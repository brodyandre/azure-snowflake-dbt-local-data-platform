# Migracao Futura para Azure + Snowflake

## Objetivo

Explicar como o laboratorio local-first pode evoluir para uma arquitetura Azure + Snowflake real sem perder a disciplina de modelagem, testes, automacao, observabilidade e governanca que ja existe no repositorio.

## Principio orientador

Este mapeamento e conceitual. O projeto nao executa Azure real nem Snowflake real localmente. Os componentes locais existem para demonstrar arquitetura, organizacao e empregabilidade tecnica de forma reproduzivel.

## Mapeamento principal

| Laboratorio local | Destino futuro | Papel arquitetural |
| --- | --- | --- |
| DuckDB | Snowflake | Warehouse analitico, datasets curados e consumo SQL |
| Azurite | Azure Blob Storage ou ADLS Gen2 | Landing zone, arquivos de carga e artefatos operacionais |
| Redpanda | Azure Event Hubs | Publicacao, persistencia e consumo de eventos |
| dbt local com DuckDB | dbt com Snowflake | Camada ELT, testes, documentacao e governanca analitica |
| GitHub Actions local-first | GitHub Actions e/ou Azure DevOps | Validacao, CI/CD e promocao entre ambientes |

## DuckDB local para Snowflake

O DuckDB foi escolhido porque permite validar rapidamente:

- modelagem em camadas
- consultas SQL analiticas
- testes dbt
- consumo local por dashboard

Em uma migracao real, o DuckDB deixaria de ser o warehouse local e seria substituido por Snowflake. A maior mudanca estaria em:

- configuracao do profile do dbt
- definicao de database, schemas e warehouses
- estrategia de materializacao por ambiente
- observabilidade de custos, concorrencia e performance

Elementos que tendem a permanecer:

- nomes de modelos e convencoes
- contratos analiticos
- logica de negocio
- estrutura `staging` -> `intermediate` -> `marts`

## Azurite local para Azure Blob Storage ou ADLS

Hoje o laboratorio usa caminhos locais e Azurite para simular uma camada de aterrissagem. Em Azure real, esse papel seria absorvido por Blob Storage ou ADLS Gen2.

Mudancas esperadas:

- containers ou file systems por zona de dados
- convencoes de paths por dominio, data e ambiente
- retention policy e lifecycle management
- separacao entre `raw`, `landing`, `curated` e `artifacts`
- logs operacionais centralizados

## Redpanda local para Azure Event Hubs

O Redpanda demonstra padroes de streaming inspirados em Event Hubs, mas em ambiente local. Em uma arquitetura real, o destino natural seria Azure Event Hubs.

Aspectos que continuariam relevantes:

- padrao do evento
- separacao entre produtor e consumidor
- persistencia em camada de aterrissagem
- idempotencia, offsets e observabilidade
- estrategia de reprocessamento

## dbt local para dbt com Snowflake

O dbt ja organiza o fluxo em camadas reutilizaveis. Na migracao para Snowflake:

- o adapter passaria para `dbt-snowflake`
- o profile deixaria de apontar para o DuckDB local
- `sources`, `vars` e `target` seriam diferenciados por ambiente
- materializacoes poderiam variar entre `view`, `table`, `incremental` e `dynamic tables`, se adotadas

O valor da abordagem atual e que a disciplina de modelagem ja esta pronta antes da troca de engine.

## Variaveis, profiles e seguranca

O laboratorio atual nao usa segredos reais. Em ambiente cloud, a seguranca precisa ser tratada explicitamente:

- nunca versionar credenciais no repositorio
- usar variaveis de ambiente, GitHub Secrets, Azure Key Vault ou solucao equivalente
- manter `profiles.yml` com referencias parametrizadas, e nao com segredos fixos
- separar credenciais por ambiente e por responsabilidade tecnica

## CI/CD para dbt e SQL

Hoje o projeto valida Python, dbt e documentacao em GitHub Actions. Em um ambiente Azure + Snowflake, a mesma esteira poderia evoluir para:

- validacao de `dbt debug`, `dbt build` e testes por ambiente
- checagem de sintaxe SQL conceitual e de scripts promocionais
- execucao controlada de objetos como schemas, grants e tasks
- promocao entre `dev`, `staging` e `prod` com gates de aprovacao

GitHub Actions pode continuar sendo usado, ou a esteira pode migrar para Azure DevOps caso o contexto corporativo peca isso.

## Cuidados com custos, warehouses e RBAC

Ao migrar para Snowflake e Azure, custo e acesso deixam de ser detalhes e passam a fazer parte da arquitetura.

Pontos importantes:

- warehouses separados por finalidade, como transformacao e analytics
- `auto-suspend` e `auto-resume` para reduzir custo ocioso
- isolamento entre cargas pesadas e consumo analitico
- controle de concorrencia e observacao de tempo de execucao
- roles separadas para carga, transformacao, analise e governanca
- principio do menor privilegio

Exemplos conceituais de roles:

- `role_loader`
- `role_transformer`
- `role_analyst`
- `role_governance`
- `role_read_only`

## Governanca e rastreabilidade

Em Snowflake, a governanca pode evoluir a partir do que o laboratorio ja demonstra localmente:

- catalogo de dados e linhagem
- classificacao de dados sensiveis
- mascaramento e politicas de acesso
- auditoria centralizada
- politicas de retencao
- resultados de qualidade de dados armazenados em camada dedicada

## Caminho sugerido de evolucao

1. Migrar a landing para Azure Blob Storage ou ADLS.
2. Configurar warehouses e schemas em Snowflake.
3. Ajustar o `profiles.yml` do dbt para Snowflake com secrets externos.
4. Promover testes e `dbt build` para CI/CD por ambiente.
5. Definir RBAC, roles e grants por responsabilidade.
6. Monitorar custo, concorrencia e governanca operacional.

## Observacao final

O objetivo deste laboratorio nao e fingir que a migracao ja aconteceu. O objetivo e mostrar um repositorio organizado o bastante para tornar essa migracao futura plausivel, tecnica e explicavel.
