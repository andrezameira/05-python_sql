import pandas as pd

from database import engine_etl


def load(
    df_produtos_processados,
    df_estatisticas
):
    """
    Carrega os dados processados no banco
    e exporta os resultados para Excel.
    """

    # Gravar tabela processed_produtos
    df_produtos_processados.to_sql(
        "processed_produtos",
        con=engine_etl,
        schema="public",
        if_exists="replace",
        index=False
    )

    # Gravar tabela estatisticas_produtos
    df_estatisticas.to_sql(
        "estatisticas_produtos",
        con=engine_etl,
        schema="public",
        if_exists="replace",
        index=False
    )

    print("Tabelas processadas carregadas no PostgreSQL.")

    # Exportar para Excel
    PROCESSED_DIR = "data/processed"

    caminho_excel = f"{PROCESSED_DIR}/relatorio_produtos.xlsx"

    df_produtos_processados.to_excel(
        caminho_excel,
        index=False,
        engine="openpyxl"
    )

    print(f"Excel gerado: {caminho_excel}")