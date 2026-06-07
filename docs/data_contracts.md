# Contratos de Dados

## Visao geral dos contratos de dados

Este documento descreve os contratos das fontes sinteticas usadas no laboratorio local. O objetivo e deixar explicitas as expectativas de estrutura, tipos, obrigatoriedade, regras basicas de negocio e pontos de validacao para apoiar pipelines, modelagem com dbt, testes e governanca.

Todos os datasets descritos aqui sao 100% ficticios e foram criados apenas para fins didaticos e tecnicos.

## Contrato da fonte customers.csv

- Nome da fonte: `customers.csv`
- Descricao: cadastro sintetico de clientes para representar uma origem similar a um sistema de CRM ou master data.
- Formato do arquivo: CSV com cabecalho.

### Campos esperados

| Campo | Descricao | Tipo esperado | Obrigatorio | Regra de negocio basica |
| --- | --- | --- | --- | --- |
| `customer_id` | Identificador unico do cliente | string | sim | Deve ser unico e seguir um padrao como `C001` |
| `full_name` | Nome completo sintetico do cliente | string | sim | Nao deve estar vazio |
| `email` | E-mail sintetico para testes | string | sim | Deve conter `@` e usar dominio ficticio |
| `city` | Cidade principal do cliente | string | sim | Deve representar uma localidade valida no contexto do dataset |
| `state` | UF do cliente | string | sim | Deve usar siglas brasileiras como `SP`, `RJ`, `MG`, `PR` e `BA` |
| `created_at` | Data de criacao do cadastro | timestamp ISO-8601 | sim | Deve representar quando o cliente entrou na base |
| `customer_segment` | Segmento comercial do cliente | string | sim | Deve estar entre `retail`, `corporate`, `premium` e `digital` |

### Exemplos de validacao

- Validar se `customer_id` e unico e nao nulo.
- Validar se `email` possui formato basico aceitavel e dominio ficticio.
- Validar se `customer_segment` pertence ao conjunto permitido.
- Validar se `created_at` pode ser convertido para timestamp.

## Contrato da fonte orders.csv

- Nome da fonte: `orders.csv`
- Descricao: pedidos sinteticos para simular uma fonte transacional de vendas multicanal.
- Formato do arquivo: CSV com cabecalho.

### Campos esperados

| Campo | Descricao | Tipo esperado | Obrigatorio | Regra de negocio basica |
| --- | --- | --- | --- | --- |
| `order_id` | Identificador unico do pedido | string | sim | Deve ser unico e seguir um padrao como `O1001` |
| `customer_id` | Cliente associado ao pedido | string | sim | Deve existir em `customers.csv` |
| `order_date` | Data do pedido | date ISO-8601 | sim | Deve representar a data comercial do pedido |
| `sales_channel` | Canal de venda | string | sim | Deve estar entre `ecommerce`, `marketplace`, `sales_team` e `mobile_app` |
| `order_status` | Status operacional do pedido | string | sim | Deve estar entre `completed`, `canceled` e `pending` |
| `gross_amount` | Valor bruto antes de desconto | decimal(10,2) | sim | Deve ser maior que zero |
| `discount_amount` | Valor de desconto aplicado | decimal(10,2) | sim | Deve ser maior ou igual a zero e menor ou igual ao valor bruto |

### Exemplos de validacao

- Validar integridade referencial de `customer_id` contra `customers.csv`.
- Validar se `discount_amount <= gross_amount`.
- Validar se existe pelo menos um pedido `completed`, um `pending` e um `canceled`.
- Validar se `sales_channel` pertence ao conjunto permitido.

## Contrato da fonte payments.json

- Nome da fonte: `payments.json`
- Descricao: eventos de pagamento sinteticos associados aos pedidos, representando liquidacao, falha, pendencia e estorno.
- Formato do arquivo: JSON com lista de objetos.

### Campos esperados

| Campo | Descricao | Tipo esperado | Obrigatorio | Regra de negocio basica |
| --- | --- | --- | --- | --- |
| `payment_id` | Identificador unico do pagamento | string | sim | Deve ser unico e seguir um padrao como `P9001` |
| `order_id` | Pedido relacionado ao pagamento | string | sim | Deve existir em `orders.csv` |
| `payment_method` | Metodo de pagamento | string | sim | Deve estar entre `credit_card`, `pix`, `boleto` e `bank_transfer` |
| `payment_status` | Status do pagamento | string | sim | Deve estar entre `paid`, `pending`, `failed` e `refunded` |
| `paid_amount` | Valor financeiro do pagamento | decimal(10,2) | sim | Deve ser maior ou igual a zero |
| `paid_at` | Momento da liquidacao ou captura | timestamp ISO-8601 ou null | sim | Pode ser `null` em casos `pending` ou `failed` |

### Exemplos de validacao

- Validar integridade referencial de `order_id` contra `orders.csv`.
- Validar se `payment_status = paid` implica `paid_at` preenchido.
- Validar se `payment_status IN (pending, failed)` permite `paid_at` nulo.
- Validar se `paid_amount` nao e negativo.

## Contrato da fonte events_sample.jsonl

- Nome da fonte: `events_sample.jsonl`
- Descricao: trilha de eventos digitais sinteticos para simular navegacao, conversao e contato em canais digitais.
- Formato do arquivo: JSON Lines, com um JSON valido por linha.

### Campos esperados

| Campo | Descricao | Tipo esperado | Obrigatorio | Regra de negocio basica |
| --- | --- | --- | --- | --- |
| `event_id` | Identificador unico do evento | string | sim | Deve ser unico e seguir um padrao como `E0001` |
| `customer_id` | Cliente associado ao evento | string | sim | Deve existir em `customers.csv` |
| `event_type` | Tipo do evento | string | sim | Deve estar entre `page_view`, `product_view`, `add_to_cart`, `checkout_started`, `purchase_completed` e `support_contact` |
| `event_timestamp` | Momento do evento | timestamp ISO-8601 | sim | Deve representar o horario de ocorrencia |
| `source_system` | Sistema emissor do evento | string | sim | Deve estar entre `web_app`, `mobile_app`, `crm` e `ecommerce` |

### Exemplos de validacao

- Validar se cada linha pode ser parseada como JSON.
- Validar se `customer_id` existe em `customers.csv`.
- Validar se `event_type` pertence ao conjunto permitido.
- Validar se `event_timestamp` pode ser convertido para timestamp.

## Regras de qualidade esperadas

- Chaves primarias devem ser unicas em cada fonte.
- Chaves estrangeiras devem ser consistentes entre clientes, pedidos, pagamentos e eventos.
- Valores categoricos devem respeitar os dominios definidos em contrato.
- Campos monetarios nao devem ser negativos.
- `discount_amount` nao deve ultrapassar `gross_amount`.
- Datas e timestamps devem seguir padroes parseaveis e coerentes.
- `paid_at` pode ser nulo apenas em cenarios compativeis com o status do pagamento.

## Possiveis problemas de qualidade

- IDs duplicados ou ausentes.
- Pedido associado a um cliente inexistente.
- Pagamento associado a um pedido inexistente.
- Evento com `customer_id` desconhecido.
- Segmento, status ou canal fora do dominio previsto.
- Valor de desconto maior que o valor bruto.
- Pagamento `paid` sem `paid_at`.
- Linhas invalidas em `events_sample.jsonl`.

## Como esses contratos ajudam em governanca de dados

- Criam uma referencia comum para engenharia, analytics e qualidade de dados.
- Facilitam a automacao de testes em pipelines e modelos dbt.
- Reduzem ambiguidades sobre estrutura, semantica e regras basicas das fontes.
- Melhoram rastreabilidade entre origem, transformacao e consumo.
- Apoiam evolucao controlada do repositorio e futura migracao para ambientes gerenciados.
