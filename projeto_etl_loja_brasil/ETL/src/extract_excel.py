import openpyxl
import pandas as pd
from config import engine_dw

ARQUIVO="dados/metas_vendas.xlsx"      # é uma constante que vai informar o caminho do arquivo, por isso que está escrita em maiúsculo. 
                                     #Precisa informar o diretório que o arquivo está, assim ele tenta procurar nessa pasta e não acha

def extrair_excel():
    
    df_metas = pd.read_excel(ARQUIVO)  

    df_metas.to_sql(
        "metas_vendas",
        engine_dw,
        schema="bronze",
        if_exists="replace",
        index=False
    )

    print("Extrção do excel concluída")
    print("Dados gravados na camada Bronze")