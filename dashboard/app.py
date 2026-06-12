from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_PATH = REPO_ROOT / "data" / "warehouse" / "local_warehouse.duckdb"
REQUIRED_MODELS = {
    "mart_customer_360",
    "fct_orders",
    "dim_customers",
    "int_customer_events",
}


def format_integer(value: int | float) -> str:
    return f"{int(value):,}".replace(",", ".")


def format_currency(value: int | float) -> str:
    formatted = f"{float(value):,.2f}"
    localized = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {localized}"


def render_rebuild_instructions() -> None:
    st.code(
        "\n".join(
            [
                "make batch",
                "make streaming-demo",
                "make dbt-build",
                "make dashboard",
            ]
        ),
        language="bash",
    )


def run_query(query: str) -> pd.DataFrame:
    with duckdb.connect(str(WAREHOUSE_PATH), read_only=True) as connection:
        return connection.execute(query).df()


def get_available_models() -> set[str]:
    query = """
        select lower(table_name) as table_name
        from information_schema.tables
        where lower(table_schema) = 'main'
    """
    models_df = run_query(query)
    return set(models_df["table_name"].tolist())


def load_kpis() -> pd.DataFrame:
    query = """
        select
            (select count(*) from dim_customers) as total_customers,
            (select count(*) from fct_orders) as total_orders,
            (select coalesce(sum(net_amount), 0) from fct_orders) as total_net_revenue,
            (select coalesce(sum(total_events), 0) from int_customer_events) as total_events,
            (
                select count(*)
                from fct_orders
                where order_status = 'completed'
            ) as completed_orders,
            (
                select count(*)
                from fct_orders
                where order_status in ('pending', 'canceled')
            ) as pending_or_canceled_orders
    """
    return run_query(query)


def load_customer_360_overview() -> pd.DataFrame:
    query = """
        select
            customer_id,
            full_name,
            customer_segment,
            total_orders,
            total_net_amount,
            total_events,
            customer_lifecycle_status
        from mart_customer_360
        order by total_net_amount desc, total_events desc
        limit 10
    """
    return run_query(query)


def load_revenue_by_channel() -> pd.DataFrame:
    query = """
        select
            sales_channel,
            count(*) as total_orders,
            round(sum(gross_amount), 2) as gross_revenue,
            round(sum(discount_amount), 2) as total_discount,
            round(sum(net_amount), 2) as net_revenue
        from fct_orders
        group by sales_channel
        order by net_revenue desc
    """
    return run_query(query)


def load_customers_by_segment() -> pd.DataFrame:
    query = """
        select
            customer_segment,
            count(*) as total_customers,
            round(sum(total_net_amount), 2) as total_net_amount
        from mart_customer_360
        group by customer_segment
        order by total_net_amount desc, total_customers desc
    """
    return run_query(query)


def load_payment_quality() -> pd.DataFrame:
    query = """
        select
            payment_quality_status,
            count(*) as total_orders,
            round(
                sum(
                    case
                        when payment_quality_status = 'paid' then paid_amount
                        else 0
                    end
                ),
                2
            ) as total_paid_amount
        from fct_orders
        group by payment_quality_status
        order by total_orders desc
    """
    return run_query(query)


def load_customer_360_table() -> pd.DataFrame:
    query = """
        select
            customer_id,
            full_name,
            city,
            state,
            customer_segment,
            total_orders,
            round(total_net_amount, 2) as total_net_amount,
            total_events,
            customer_lifecycle_status
        from mart_customer_360
        order by total_net_amount desc, total_orders desc
    """
    return run_query(query)


def render_kpis(kpis_df: pd.DataFrame) -> None:
    metrics = kpis_df.iloc[0].to_dict()
    col_1, col_2, col_3 = st.columns(3)
    col_4, col_5, col_6 = st.columns(3)

    col_1.metric("Total de clientes", format_integer(metrics["total_customers"]))
    col_2.metric("Total de pedidos", format_integer(metrics["total_orders"]))
    col_3.metric("Receita liquida total", format_currency(metrics["total_net_revenue"]))
    col_4.metric("Total de eventos digitais", format_integer(metrics["total_events"]))
    col_5.metric("Pedidos concluidos", format_integer(metrics["completed_orders"]))
    col_6.metric(
        "Pedidos pendentes ou cancelados",
        format_integer(metrics["pending_or_canceled_orders"]),
    )


def main() -> None:
    st.set_page_config(
        page_title="Azure + Snowflake Local Data Platform",
        layout="wide",
    )

    st.title("Azure + Snowflake Local Data Platform")
    st.write(
        "Dashboard local para consumo da camada analitica gerada por pipelines batch e "
        "streaming, transformada com dbt e publicada em DuckDB."
    )
    st.info(
        "Este painel consome somente dados locais do arquivo "
        "`data/warehouse/local_warehouse.duckdb`, gerado pelo dbt neste laboratorio."
    )
    st.caption(
        "Fluxo local de consumo: pipelines Python -> landing files -> dbt -> DuckDB -> "
        "Streamlit."
    )

    if not WAREHOUSE_PATH.exists():
        st.error("O arquivo do DuckDB local ainda nao foi encontrado.")
        st.write(
            "Antes de abrir o dashboard, execute os comandos abaixo para gerar a camada "
            "analitica do laboratorio."
        )
        render_rebuild_instructions()
        return

    try:
        available_models = get_available_models()
    except duckdb.Error as exc:
        st.error("Nao foi possivel conectar ao DuckDB local ou ler os metadados do warehouse.")
        st.write(f"Detalhe tecnico: `{exc}`")
        render_rebuild_instructions()
        return

    missing_models = sorted(REQUIRED_MODELS - available_models)
    if missing_models:
        st.error("A camada analitica ainda nao esta completa para alimentar o dashboard.")
        st.write(
            "Os modelos abaixo nao foram encontrados no DuckDB local: "
            + ", ".join(f"`{model}`" for model in missing_models)
        )
        st.write(
            "Isso normalmente acontece quando o ambiente ainda nao executou a ingestao, o "
            "streaming local ou o `dbt build`."
        )
        render_rebuild_instructions()
        return

    try:
        kpis_df = load_kpis()
        customer_360_overview_df = load_customer_360_overview()
        revenue_by_channel_df = load_revenue_by_channel()
        customers_by_segment_df = load_customers_by_segment()
        payment_quality_df = load_payment_quality()
        customer_360_df = load_customer_360_table()
    except duckdb.Error as exc:
        st.error("O dashboard encontrou um erro ao consultar os modelos analiticos locais.")
        st.write(f"Detalhe tecnico: `{exc}`")
        render_rebuild_instructions()
        return

    st.subheader("Visao geral")
    render_kpis(kpis_df)
    st.write("Resumo do `mart_customer_360` com foco em valor, atividade e lifecycle.")
    st.dataframe(customer_360_overview_df, width="stretch", hide_index=True)

    st.subheader("Receita por canal")
    st.write(
        "Consolidacao de pedidos, receita bruta, desconto e receita liquida por canal a "
        "partir de `fct_orders`."
    )
    st.dataframe(revenue_by_channel_df, width="stretch", hide_index=True)
    st.bar_chart(
        revenue_by_channel_df.set_index("sales_channel")[
            ["gross_revenue", "total_discount", "net_revenue"]
        ]
    )

    st.subheader("Clientes por segmento")
    st.write(
        "Distribuicao de clientes e receita liquida acumulada por segmento comercial."
    )
    st.dataframe(customers_by_segment_df, width="stretch", hide_index=True)

    st.subheader("Qualidade de pagamento")
    st.write(
        "Leitura operacional dos status de pagamento para apoiar acompanhamento financeiro "
        "e qualidade de dados."
    )
    st.dataframe(payment_quality_df, width="stretch", hide_index=True)

    st.subheader("Customer 360")
    st.write(
        "Tabela analitica detalhada para navegar pelos principais sinais de relacionamento, "
        "receita e comportamento digital."
    )
    st.dataframe(customer_360_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
