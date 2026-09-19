import pandas as pd
from config import engine_erp, engine_dw  # trás a cadeia de conexão do arquivo config


sql_vendas = """
SELECT
    p.id_pedido,
    p.data_pedido,
    p.status AS status_pedido,
    c.id_cliente,
    c.nome AS cliente,
    c.cidade,
    c.estado,
    i.id_produto,
    pr.nome AS produto,
    cat.nome AS categoria,
    m.nome AS marca,
    i.quantidade,
    i.preco_unitario,
    i.desconto
FROM vendas.pedidos p
INNER JOIN cadastro.clientes c
    ON c.id_cliente = p.id_cliente
INNER JOIN vendas.itens_pedido i
    ON i.id_pedido = p.id_pedido
INNER JOIN cadastro.produtos pr
    ON pr.id_produto = i.id_produto
INNER JOIN cadastro.categorias cat
    ON cat.id_categoria = pr.id_categoria
INNER JOIN cadastro.marcas m
    ON m.id_marca = pr.id_marca;
"""

# Para conseguir executar, precisa criar uma função com essa parte

def extrair_erp():

    print("Extraindo dados do banco de dados Loja Brasil...")

    df_vendas = pd.read_sql(sql_vendas, engine_erp)

    df_vendas.to_sql(
        "erp_vendas",
        engine_dw,
        schema="bronze",
        if_exists="replace",
        index=False
    )

    print("Extrção do banco de dados LOJA BRASIL concluída")
    print("Dados gravados na camada Bronze")

    