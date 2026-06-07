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
