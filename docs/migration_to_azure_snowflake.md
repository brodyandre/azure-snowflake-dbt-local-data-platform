# Migracao Futura para Azure + Snowflake

## Objetivo

Registrar como este laboratorio local pode evoluir para uma arquitetura real em Azure + Snowflake sem perder a disciplina de modelagem, testes, automacao e rastreabilidade ja adotada no repositorio.

## Ponto de partida do laboratorio

Hoje o projeto roda totalmente local:

- Azurite representa a ideia de object storage.
- DuckDB representa a camada analitica local.
- Redpanda demonstra eventos e consumo streaming.
- dbt organiza transformacoes e testes.
- Makefile e GitHub Actions concentram automacao operacional.

Essa base nao tenta reproduzir a nuvem por completo. O valor aqui esta em manter contratos de dados, camadas claras, SQL legivel e uma esteira reproduzivel.

## Mapeamento conceitual entre local e cloud

| Laboratorio local | Destino futuro | Papel arquitetural |
| --- | --- | --- |
| Azurite | Azure Blob Storage ou ADLS Gen2 | Landing zone, arquivos de entrada, armazenamento de artefatos e zonas raw |
| DuckDB | Snowflake | Camada analitica, transformacoes, marts e consultas SQL |
| Redpanda | Azure Event Hubs | Ingestao de eventos, buffering e distribuicao de mensagens |
| dbt + DuckDB profile | dbt + Snowflake profile | Modelagem em camadas, testes, documentacao e promocao entre ambientes |
| Makefile + GitHub Actions | GitHub Actions + secrets + ambientes | Automacao, validacao, execucao controlada e rastreabilidade |

## DuckDB para Snowflake

DuckDB foi escolhido porque simplifica a execucao local e permite iterar rapido em SQL, dbt e testes. Em uma migracao real, o alvo analitico seria Snowflake, mas a estrutura do projeto ja ajuda nessa transicao:

- os modelos dbt seguem separacao em `staging`, `intermediate` e `marts`
- os contratos de qualidade continuam validos mesmo trocando o engine
- a nomenclatura das entidades finais, como `dim_customers`, `fct_orders` e `mart_customer_360`, continua portavel
- a pasta `sql/snowflake_compatible` mostra exemplos de DDL e procedures em sintaxe orientada a Snowflake

O que mudaria na pratica:

- o `profiles.yml` do dbt passaria a apontar para uma conta Snowflake
- tabelas externas ou cargas para schemas `RAW` substituiriam leituras diretas de arquivos locais
- escolhas de materializacao poderiam variar entre `view`, `table` e `incremental` conforme volume e custo

## Azurite para Azure Blob Storage ou ADLS Gen2

No laboratorio, os dados entram por arquivos locais e zonas como `data/landing`. Em Azure real, o caminho natural seria publicar esses dados em Blob Storage ou ADLS Gen2 com uma convencao de paths por dominio, data e tipo de carga.

Evolucao esperada:

- trocar caminhos locais por containers e pastas controladas
- usar naming padrao para `raw`, `landing`, `curated` e `artifacts`
- registrar politicas de retencao, lifecycle e permissao de acesso por zona
- gerar logs de carga e manifests em storage para auditoria

## Redpanda para Azure Event Hubs

O fluxo de eventos deste laboratorio existe para mostrar integracao e consumo, nao para simular toda a operacao gerenciada de um broker cloud. Em uma migracao real, o topico `customer-events` poderia virar um Event Hub com produtores e consumidores autenticados por identidade gerenciada ou credenciais controladas.

O que permanece util:

- padrao de evento JSON
- separacao entre produtor, consumidor e persistencia na landing
- necessidade de idempotencia, controle de offset e observabilidade

## dbt com Snowflake

dbt continua sendo a ponte mais natural entre o laboratorio e um ambiente corporativo. A mudanca principal seria o adapter e o profile, nao a estrutura do projeto.

Aspectos que seguem iguais:

- organizacao por camadas
- testes `not_null`, `unique`, `relationships` e `accepted_values`
- documentacao por modelo e por coluna
- `dbt build` como comando de validacao ponta a ponta

Aspectos que precisariam de ajuste:

- configuracao do adapter `dbt-snowflake` em ambiente real
- definicao de database, schema e warehouse por ambiente
- estrategia de materializacao para custo e performance
- uso de `sources`, `stages` e possivelmente tabelas externas

## Variaveis, profiles e seguranca

O laboratorio local versiona apenas configuracoes nao sensiveis. Em uma migracao real, o caminho profissional seria:

- manter `profiles.yml` sensivel fora do repositorio
- usar `env vars` para credenciais e nomes de ambiente
- guardar segredos em GitHub Secrets, Azure Key Vault ou outra solucao apropriada
- separar credenciais por ambiente, sem reaproveitar usuario de desenvolvimento em producao

Boas praticas recomendadas:

- nunca commitar tokens, chaves ou contas de servico
- usar roles dedicadas para carga, transformacao e leitura analitica
- limitar permissoes ao minimo necessario

## CI/CD para dbt e SQL

Em um ambiente com Snowflake, a automacao poderia seguir a mesma disciplina ja usada aqui:

1. Pull request valida lint, testes Python e `dbt build`.
2. Merge em branch principal publica modelos aprovados em ambiente controlado.
3. Scripts SQL de DDL e procedures rodam em etapa separada, com revisao e rastreabilidade.
4. Logs, manifests e relatarios ficam salvos como artifacts do pipeline.

Esse desenho ajuda especialmente em Engenharia de Dados porque evita mudancas manuais diretas no warehouse e cria historico claro de quem alterou o que.

## Custos, RBAC, roles, warehouses e governanca

Snowflake traz vantagens operacionais, mas exige disciplina para custo e seguranca.

Pontos importantes para uma evolucao madura:

- definir warehouses separados para desenvolvimento, transformacao e consumo
- habilitar auto-suspend e auto-resume para evitar custo ocioso
- usar roles por funcao, como `loader`, `transformer`, `analyst` e `read_only`
- aplicar governanca por schema, ownership claro e politicas de acesso
- considerar masking, tagging e classificacao de dados sensiveis quando o dominio exigir

## Caminho de evolucao sugerido

1. Publicar os dados de entrada em Blob Storage ou ADLS.
2. Criar schemas `RAW`, `STAGING`, `INTERMEDIATE`, `MARTS` e `CONTROL` em Snowflake.
3. Configurar um profile dbt especifico para ambiente cloud.
4. Adaptar ingestao batch e streaming para gravar em storage e/ou tabelas controladas.
5. Promover o `dbt build` e os SQLs compativeis com Snowflake para uma esteira CI/CD com aprovacao.
6. Acrescentar observabilidade operacional, custos e politicas de acesso.

## Observacao final

Este repositorio nao usa Azure nem Snowflake reais nesta fase. A proposta e preparar o desenho tecnico e os habitos de engenharia para que a migracao futura seja mais previsivel, menos manual e melhor documentada.
