# Governanca de Dados

## Diretrizes iniciais

- Organizar dados por estagio de processamento.
- Preservar rastreabilidade entre origem, transformacao e consumo.
- Versionar apenas artefatos adequados ao Git, evitando dados sensiveis ou volumosos.
- Registrar evidencias de execucao quando fizer sentido para auditoria tecnica.

## Convencoes propostas

- Scripts Python em `snake_case`.
- Consultas SQL separadas entre compatibilidade analitica e uso exploratorio.
- Documentacao em Markdown com foco tecnico e objetivo.
- Dados brutos nao devem ser versionados por padrao.

## Qualidade e controle

- Testes automatizados serao adicionados progressivamente.
- Regras de qualidade devem acompanhar a evolucao dos datasets.
- Mudancas de estrutura devem ser refletidas na documentacao do repositorio.

## Controles implementados

- Contratos de dados documentam formato, campos esperados e regras minimas das fontes sinteticas.
- Testes automatizados com `dbt` verificam integridade dos modelos analiticos no DuckDB local.
- Testes Python com `pytest` validam fontes de entrada, artefatos de landing e consistencia dos logs de auditoria.
- A auditoria de execucao em `pipeline_audit.jsonl` preserva rastreabilidade basica das execucoes locais.
- O relatorio `data_quality_report.md` consolida verificacoes operacionais por dataset para inspecao rapida.

## Rastreabilidade local

Mesmo sem Azure real ou Snowflake real, o laboratorio mantem uma trilha tecnica clara entre:

- arquivos de origem sinteticos
- pipelines batch e streaming
- camadas `staging`, `intermediate` e `marts` no dbt
- logs de auditoria e evidencias geradas localmente

## Evolucao para Azure + Snowflake

Em uma arquitetura Azure + Snowflake real, esses mesmos controles poderiam ser expandidos com:

- contratos de dados publicados em catalogos corporativos
- testes dbt executados em pipelines CI/CD e ambientes promovidos
- auditoria centralizada em storage e monitoramento gerenciado
- rastreabilidade integrada entre ingestao, transformacao, observabilidade e governanca
