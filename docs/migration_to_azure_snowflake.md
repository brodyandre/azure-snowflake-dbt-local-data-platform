# Migracao Futura para Azure + Snowflake

## Objetivo

Registrar como este laboratorio local pode evoluir para uma arquitetura real em Azure + Snowflake sem perder a disciplina de modelagem, testes, automacao, rastreabilidade e governanca ja praticada no repositorio.

## Principio orientador

O mapeamento deste documento e conceitual. O laboratorio nao tenta afirmar que os componentes locais sao equivalentes completos aos servicos cloud. A proposta e mostrar uma trilha plausivel de evolucao, mantendo o desenho tecnico portavel.

## Mapeamento principal

| Laboratorio local | Destino futuro | Papel arquitetural |
| --- | --- | --- |
| DuckDB | Snowflake | Camada analitica, transformacoes e datasets finais |
| Azurite | Azure Blob Storage ou ADLS Gen2 | Landing zone, artefatos de carga e armazenamento de arquivos |
| Redpanda | Azure Event Hubs | Publicacao e consumo de eventos |
| GitHub Actions local-first | GitHub Actions e/ou Azure DevOps | Validacao, automacao e promocao entre ambientes |
| dbt local com DuckDB | dbt com Snowflake | Modelagem, testes, documentacao e governanca de transformacoes |

## DuckDB para Snowflake

O DuckDB foi escolhido por simplicidade operacional. Ele permite validar:

- modelagem em camadas
- SQL analitico
- testes dbt
- consumo local por dashboard

Na migracao para Snowflake, a maior mudanca estaria em:

- profile do dbt
- configuracao de databases, schemas e warehouses
- estrategia de materializacao
- controle de custo e concorrencia

O que tende a permanecer:

- nomes de modelos
- contratos analiticos
- logica de negocio
- estrutura `staging` -> `intermediate` -> `marts`

## Azurite para Azure Blob Storage ou ADLS

No laboratorio, a camada `landing` e local. Em Azure real, esse papel seria absorvido por Blob Storage ou ADLS Gen2.

Pontos de evolucao:

- containers por zona de dados
- convencoes de paths por dominio e data
- retention policy
- separacao entre `raw`, `landing`, `curated` e `artifacts`
- logs operacionais centralizados

## Redpanda para Azure Event Hubs

O papel do Redpanda no laboratorio e demonstrar integracao e persistencia de eventos. Em um ambiente corporativo, isso pode migrar para Azure Event Hubs ou outra infraestrutura gerenciada de mensageria.

O que continua relevante:

- padrao do evento
- separacao entre produtor e consumidor
- persistencia em camada de aterrissagem
- preocupacao com idempotencia, offset e observabilidade

## GitHub Actions para GitHub Actions ou Azure DevOps

O projeto ja usa GitHub Actions para validar Python, dbt e documentacao. Em um ambiente corporativo, isso pode continuar em GitHub Actions ou ser promovido para Azure DevOps, dependendo do padrao da empresa.

Evolucoes naturais:

- aprovacao por ambiente
- promocoes entre `dev`, `staging` e `prod`
- artifacts de build e manifestos
- gates de qualidade mais fortes
- integracao com secrets manager

## dbt local para dbt com Snowflake

O dbt ja organiza a plataforma em camadas reutilizaveis. Em uma migracao real:

- o adapter mudaria para `dbt-snowflake`
- o profile deixaria de apontar para o DuckDB local
- tabelas externas, stages e cargas controladas poderiam substituir parte da leitura direta dos arquivos

O valor da abordagem atual e que a disciplina de modelagem ja esta pronta antes da troca de engine.

## Cuidados com RBAC

Em Snowflake, a governanca de acesso precisa ser tratada com mais rigor. Alguns cuidados importantes:

- separar roles por responsabilidade
- evitar uso excessivo de ownership compartilhado
- definir roles para carga, transformacao e consumo
- limitar privilegios ao minimo necessario

Exemplos de papeis:

- `loader`
- `transformer`
- `analyst`
- `read_only`

## Cuidados com secrets

O laboratorio atual nao usa segredos reais. Em ambiente cloud, isso precisa mudar de forma controlada:

- nunca versionar credenciais no repositorio
- usar `env vars`, GitHub Secrets, Azure Key Vault ou solucao equivalente
- separar credenciais por ambiente
- evitar compartilhamento de usuario tecnico entre multiplos fluxos

## Cuidados com custos

Ao migrar para Snowflake e Azure, custo vira parte da arquitetura. Alguns cuidados esperados:

- limitar processamento ocioso
- revisar frequencia de jobs
- definir materializacoes compativeis com volume real
- evitar warehouse superdimensionado

## Cuidados com warehouses

Snowflake traz elasticidade, mas tambem exige criterio operacional. Boas praticas comuns:

- warehouses separados por finalidade
- `auto-suspend` e `auto-resume`
- isolamento entre cargas pesadas e consumo analitico
- observacao de concorrencia e tempo de execucao

## Cuidados com governanca

A governanca local deste laboratorio pode migrar para um desenho mais robusto com:

- catalogo de dados
- classificacao de dados sensiveis
- mascaramento
- linhagem
- auditoria centralizada
- politicas de retencao

## Caminho sugerido de evolucao

1. Migrar a landing para Blob Storage ou ADLS.
2. Configurar profile dbt para Snowflake.
3. Criar schemas por camada analitica.
4. Adaptar automacao para ambientes promoviveis.
5. Introduzir secrets e RBAC de forma segura.
6. Ajustar materializacoes e warehouses conforme custo e volume.

## Observacao final

O valor deste laboratorio nao esta em fingir que a migracao ja aconteceu. O valor esta em mostrar um repositorio organizado o bastante para que essa migracao futura seja possivel com menos improviso e mais previsibilidade.
