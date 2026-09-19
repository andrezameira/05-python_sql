from sqlalchemy import text
from config import engine_dw

# Para executar o arquivo
def configurar_dw():   # vai fazer a criação dos schemas, se eles não existirem
    print("Configurando o Data Warehouse...")

    with engine_dw.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))
    print("Schemas do DW criados.")



