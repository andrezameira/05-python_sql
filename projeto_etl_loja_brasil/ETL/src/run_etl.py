# Arquivo onde ficam a ordem de execução
"""Pipeline ETL - Fluxo de execução"""


# Importação dos módulos
from setup_dw import configurar_dw
from extract_erp import extrair_erp              # Importar os módulos referente a exportação dos arquivos
from extract_ibge import extrair_ibge
from extract_excel import extrair_excel
from silver import processar_silver
from gold import processar_gold

# função de execução - função principal
def main():
    # Garantindo existência das camadas
    configurar_dw()

    # Extrair dados (Extract)
    extrair_erp()
    extrair_ibge()
    extrair_excel()

    # Transformar dado (Transform)
    processar_silver()

    # Carregar dados (Load)
    processar_gold()

    print("Pipeline ETL concluído")


if __name__ == "__main__":    # essa parte permite rodar todo o pipeline ao clicar 2x no arquivo
    main()  
