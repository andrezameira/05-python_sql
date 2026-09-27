-- Tabelas de apoio ao projeto ETL TechStore
-- Execute este script manualmente no PostgreSQL.

CREATE DATABASE techstore_etl;

CREATE TABLE IF NOT EXISTS raw_fornecedores (
    id_produto INTEGER NOT NULL,
    produto VARCHAR(150),
    fornecedor VARCHAR(100),
    data_atualizacao DATE,
    custo_aquisicao NUMERIC(10, 2),
    prazo_entrega_dias INTEGER,
    quantidade_reposicao INTEGER,
    status_fornecimento VARCHAR(50),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processed_produtos (
    id_produto INTEGER PRIMARY KEY,
    produto VARCHAR(150),
    categoria VARCHAR(100),
    preco_venda NUMERIC(10, 2),
    estoque INTEGER,
    fornecedor VARCHAR(100),
    custo_aquisicao NUMERIC(10, 2),
    margem_valor NUMERIC(10, 2),
    margem_percentual NUMERIC(10, 2),
    quantidade_reposicao INTEGER,
    status_fornecimento VARCHAR(50),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estatisticas_produtos (
    indicador VARCHAR(100) PRIMARY KEY,
    valor NUMERIC(15, 2),
    descricao TEXT,
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
