from extract import extract_produtos, extract_fornecedores
from transform import transform
from load import load


def run_etl():

    # Extract
    extract_produtos()
    extract_fornecedores()

    # Transform
    df_produtos_processados, df_estatisticas = transform()

    # Load
    load(
        df_produtos_processados,
        df_estatisticas
    )


if __name__ == "__main__":
    run_etl()