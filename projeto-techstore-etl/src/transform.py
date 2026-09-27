import pandas as pd
from sqlalchemy import text
from database import engine_etl


def transform():
    """
    Transforma os dados da tabela raw_produtos e raw_fornecedores.
    """

    # Leitura das tabelas da camada raw no banco techstore_etl
    df_produtos = pd.read_sql(
        "SELECT * FROM public.raw_produtos ORDER BY id_produto",
        con=engine_etl
    )

    df_fornecedores = pd.read_sql(
        "SELECT * FROM public.raw_fornecedores ORDER BY id_produto",
        con=engine_etl
    )

    print("Dados raw carregados para transformação.")

    # Transformação dos dados

    df_fornecedores_tratados = df_fornecedores.copy()

    df_fornecedores_tratados.columns = (
        df_fornecedores_tratados.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df_fornecedores_tratados["produto"] = (
        df_fornecedores_tratados["produto"]
        .astype("string")
        .str.strip()
    )

    df_fornecedores_tratados["fornecedor"] = (
        df_fornecedores_tratados["fornecedor"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    df_fornecedores_tratados["status_fornecimento"] = (
        df_fornecedores_tratados["status_fornecimento"]
        .astype("string")
        .str.strip()
    )

    df_fornecedores_tratados["data_atualizacao"] = pd.to_datetime(
        df_fornecedores_tratados["data_atualizacao"]
    )

    colunas_numericas = [
        "id_produto",
        "custo_aquisicao",
        "prazo_entrega_dias",
        "quantidade_reposicao",
    ]

    for coluna in colunas_numericas:
        df_fornecedores_tratados[coluna] = pd.to_numeric(
            df_fornecedores_tratados[coluna]
        )


    # Integração das tabelas raw_produtos e raw_fornecedores
    df_produtos_processados = df_produtos.merge(
    df_fornecedores_tratados,
    on=["id_produto", "produto"],
    how="left"
    )


    df_produtos_processados["margem_valor"] = (
        df_produtos_processados["preco_venda"]
        - df_produtos_processados["custo_aquisicao"]
    )

    df_produtos_processados["margem_percentual"] = (
        df_produtos_processados["margem_valor"]
        / df_produtos_processados["preco_venda"]
        * 100
    ).round(2)

    # Estatísticas dos produtos
    df_estatisticas = pd.DataFrame({
        "indicador": [
            "quantidade_produtos",
            "preco_medio",
            "custo_medio",
            "margem_media",
            "estoque_reposicao_total",
            "prazo_entrega_medio",
        ],
        "valor": [
            df_produtos_processados["id_produto"].nunique(),
            df_produtos_processados["preco_venda"].mean(),
            df_produtos_processados["custo_aquisicao"].mean(),
            df_produtos_processados["margem_percentual"].mean(),
            df_produtos_processados["quantidade_reposicao"].sum(),
            df_produtos_processados["prazo_entrega_dias"].mean(),
        ],
    })

    return df_produtos_processados, df_estatisticas