-- Consultas de validação do projeto ETL

SELECT *
FROM raw_fornecedores
ORDER BY id_produto;

SELECT COUNT(*) AS total_raw
FROM raw_fornecedores;

SELECT
    COUNT(*) AS total_produtos,
    MIN(custo_aquisicao) AS menor_custo,
    MAX(custo_aquisicao) AS maior_custo,
    AVG(custo_aquisicao) AS custo_medio
FROM raw_fornecedores;

SELECT
    status_fornecimento,
    COUNT(*) AS quantidade
FROM raw_fornecedores
GROUP BY status_fornecimento
ORDER BY quantidade DESC;

SELECT
    id_produto,
    produto,
    fornecedor,
    custo_aquisicao
FROM raw_fornecedores
WHERE custo_aquisicao IS NULL
   OR fornecedor IS NULL;

-- Consulta opcional para validar a tabela processada,
-- caso ela seja carregada futuramente.
SELECT *
FROM processed_produtos
ORDER BY id_produto;
