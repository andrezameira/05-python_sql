import pandas as pd
from sqlalchemy import text
from database import engine_techstore, engine_etl


def extract_produtos():
    """
    Extrai os dados da tabela produtos do banco techstore.
    """
    query_produtos = '''
        SELECT
            p.id_produto,
            p.nome AS produto,
            c.nome AS categoria,
            p.preco AS preco_venda
        FROM produtos p
        LEFT JOIN categorias c
            ON p.id_categoria = c.id_categoria
        ORDER BY p.id_produto;
    '''

    df_produtos_raw = pd.read_sql(text(query_produtos), con=engine_techstore)

    df_produtos_raw.to_sql(
        "raw_produtos",
        con=engine_etl,
        schema="public",
        if_exists="replace",
        index=False
    )

    print("Tabela public.raw_produtos gravada no banco techstore_etl.")


def extract_fornecedores():
    """
    Extrai os dados da tabela fornecedores de um arquivo CSV.
    """

    RAW_DIR = "data/raw"

    caminho_csv = f"{RAW_DIR}/techstore_fornecedores.csv"

    df_fornecedores_raw = pd.read_csv(
        caminho_csv,
        sep=";",
        encoding="utf-8-sig"
    )

    df_fornecedores_raw.to_sql(
        "raw_fornecedores",
        con=engine_etl,
        schema="public",
        if_exists="replace",
        index=False
    )

    print("Dados gravados em public.raw_fornecedores.")
