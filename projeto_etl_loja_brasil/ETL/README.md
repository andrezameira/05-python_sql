# Projeto ETL — Loja Brasil

## Visão geral

Este repositório contém o projeto de ETL da Loja Brasil, com duas formas de execução e estudo:

1. Um notebook com a versão completa do fluxo, para análise e demonstração.
2. Uma implementação em Python organizada em módulos dentro da pasta `ETL`, com execução coordenada pelo arquivo `run_etl.py`.

A estrutura foi organizada para refletir a realidade do projeto atual, com a pasta principal do projeto em um nível acima da implementação do pipeline.

## Estrutura real do projeto

```text
projeto_etl_loja_brasil/
├── ETL/
│   ├── .env
│   ├── .gitignore
│   ├── README.md
│   ├── requirements.txt
│   ├── dados/
│   │   └── metas_vendas.xlsx
│   └── src/
│       ├── config.py
│       ├── extract_erp.py
│       ├── extract_excel.py
│       ├── extract_ibge.py
│       ├── gold.py
│       ├── run_etl.py
│       ├── setup_dw.py
│       └── silver.py
├── metas_vendas.xlsx
├── projeto_etl_completo.ipynb
└── README.md (opcional, se for criado na raiz)
```

## Organização das pastas

- `ETL/`: concentra o código do pipeline ETL, dependências e dados de suporte.
- `ETL/src/`: arquivos Python responsáveis por cada etapa do processo.
- `ETL/dados/`: arquivos de dados locais usados no fluxo, como a planilha de metas.
- `projeto_etl_completo.ipynb`: versão completa em notebook do projeto.
- `metas_vendas.xlsx`: arquivo de apoio localizado na raiz do projeto.

## Fluxo do ETL

O pipeline é executado pela função principal em `ETL/src/run_etl.py` na seguinte ordem:

```python
configurar_dw()

extrair_erp()
extrair_ibge()
extrair_excel()

processar_silver()
processar_gold()
```

## Arquitetura do banco

O projeto trabalha com duas bases de dados PostgreSQL:

```text
ERP / loja_brasil
      │
      │ Python + SQLAlchemy + Pandas
      ▼
DW / data warehouse
├── bronze
├── silver
└── gold
      │
      ▼
Power BI / consultas analíticas
```

- `loja_brasil`: banco operacional/ERP.
- `dw`: ambiente analítico com camadas de bronze, silver e gold.

## Fontes de dados

- Dados do ERP (`loja_brasil`)
- Dados de localidades do IBGE
- Arquivo de metas (`ETL/dados/metas_vendas.xlsx`)

## Configuração do ambiente

1. Acesse a pasta `ETL`.
2. Crie um arquivo `.env` com as variáveis de conexão.
3. Configure usuário, senha, host, porta e nome dos bancos ERP e DW.
4. Não envie o `.env` para o Git.

Exemplo de estrutura esperada:

```text
ERP_USUARIO=...
ERP_SENHA=...
ERP_HOST=...
ERP_PORTA=...
ERP_BANCO=...

DW_USUARIO=...
DW_SENHA=...
DW_HOST=...
DW_PORTA=...
DW_BANCO=...
```

## Instalação

Dentro da pasta `ETL`:

```bash
pip install -r requirements.txt
```

## Execução

A execução do pipeline acontece na pasta `ETL`:

```bash
cd ETL
python src/run_etl.py
```

## Camadas do pipeline

### Bronze

Recebe os dados extraídos das fontes:

```text
ERP   -> bronze.erp_vendas
IBGE  -> bronze.ibge_municipios
Excel -> bronze.metas_vendas
```

### Silver

Lê a camada bronze, realiza limpeza, padronização, integração e validações.

```text
bronze
  ↓
tratamento e padronização
  ↓
validação
  ↓
silver
```

### Gold

Cria as tabelas analíticas finais para uso em relatórios e dashboards.

```text
silver -> gold.fato_vendas
silver -> gold.dim_municipios
silver -> gold.metas_vendas
```

## Objetivo do projeto

O objetivo é demonstrar um fluxo ETL completo, desde a extração dos dados até a entrega em camada analítica, respeitando a separação de responsabilidades por módulo e mantendo a execução organizada e legível.
