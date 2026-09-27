# Projeto ETL: TechStore

Projeto didático de ETL com **Python, Pandas, SQLAlchemy e PostgreSQL**. O
objetivo é integrar os produtos da base TechStore com dados de fornecedores,
tratar problemas de qualidade, carregar as camadas do processo e analisar o
resultado.

## Objetivo e fluxo do projeto

O projeto simula um cenário em que os dados de fornecedores chegam em um CSV
com problemas que precisam ser tratados antes de serem usados. O fluxo é:

```text
gerar_csv_fornecedores.py
        |
        v
data/raw/techstore_fornecedores.csv
        |
        | Extração: CSV + banco TechStore
        v
PostgreSQL: raw_fornecedores e raw_produtos
        |
        | Transformação com Pandas
        | Padronização, conversão, integração e margens
        v
PostgreSQL: processed_produtos e estatisticas_produtos
data/processed/relatorio_produtos.xlsx
        |
        v
notebooks/analise_estatisticas.ipynb
        |
        v
Estatísticas descritivas e gráfico de margem por produto
```

### Geração dos dados raw

O arquivo `gerar_csv_fornecedores.py` cria dados sintéticos de fornecedores e
grava o arquivo `data/raw/techstore_fornecedores.csv`. Esse arquivo é o ponto
de partida para a extração dos fornecedores.

Os dados foram criados com inconsistências intencionais, como espaços extras e
diferenças de capitalização no nome dos fornecedores. Isso permite demonstrar
por que um processo ETL é necessário: os dados precisam ser tratados antes da
integração com os produtos da TechStore.

Execute o gerador na raiz do projeto:

```bash
python gerar_csv_fornecedores.py
```

O CSV usa `;` como separador e codificação `utf-8-sig`, configurações que são
utilizadas novamente pelo módulo de extração.

## Arquitetura de pastas e arquivos

```text
projeto-techstore-etl/
├── data/
│   ├── raw/
│   │   └── techstore_fornecedores.csv       # Entrada bruta dos fornecedores
│   └── processed/
│       └── relatorio_produtos.xlsx          # Saída processada do ETL
├── notebooks/
│   └── analise_estatisticas.ipynb           # Análise após o ETL
├── sql/
│   ├── 01_criar_tabelas_etl.sql             # Banco e tabelas de apoio
│   └── 02_consultas_validacao.sql            # Consultas de conferência
├── src/
│   ├── database.py                           # Conexões com os bancos
│   ├── extract.py                            # Extração das duas fontes
│   ├── transform.py                          # Tratamento e integração
│   ├── load.py                               # Carga e exportação
│   └── run_etl.py                            # Orquestração do pipeline
├── etl_techstore.ipynb                       # Construção didática do ETL
├── gerar_csv_fornecedores.py                 # Geração do CSV raw
├── .env                                      # Configurações locais do PostgreSQL
├── .gitignore                                # Arquivos que não devem ser versionados
├── requirements.txt                           # Dependências Python
└── README.md                                 # Documentação do projeto
```

As pastas `data/raw` e `data/processed` são usadas como áreas de entrada e
saída de arquivos. A camada raw também é carregada no banco `techstore_etl`,
onde serve de base para a transformação.

## Responsabilidade dos arquivos em `src`

### `src/database.py`

Carrega as variáveis do `.env` com `python-dotenv` e cria dois engines do
SQLAlchemy:

- `engine_techstore`: conexão com a base original, de onde vêm produtos e
  categorias;
- `engine_etl`: conexão com a base destinada às tabelas do processo ETL.

### `src/extract.py`

Implementa a etapa **Extract**:

- `extract_produtos()` consulta `produtos` e `categorias` na base TechStore e
  grava o resultado em `public.raw_produtos`;
- `extract_fornecedores()` lê o CSV de `data/raw` e grava os dados em
  `public.raw_fornecedores`.

As duas tabelas representam a camada raw no banco. A carga usa
`if_exists="replace"`, portanto as tabelas são recriadas a cada execução.

### `src/transform.py`

Implementa a etapa **Transform**. Lê as tabelas raw e:

- normaliza nomes de colunas;
- remove espaços extras dos textos;
- padroniza o nome dos fornecedores com `.title()`;
- converte a data de atualização;
- converte as colunas numéricas;
- integra produtos e fornecedores por `id_produto` e `produto`;
- calcula `margem_valor` e `margem_percentual`;
- cria o DataFrame de indicadores estatísticos.

As margens são calculadas por:

```text
margem_valor = preco_venda - custo_aquisicao
margem_percentual = (margem_valor / preco_venda) * 100
```

### `src/load.py`

Implementa a etapa **Load**:

- grava os produtos em `public.processed_produtos`;
- grava os indicadores em `public.estatisticas_produtos`;
- exporta os produtos processados para
  `data/processed/relatorio_produtos.xlsx`.

### `src/run_etl.py`

É o orquestrador. Executa, na ordem, a extração dos produtos, a extração dos
fornecedores, a transformação e a carga.

## Arquivo `.env`

O `.env` guarda as configurações locais de conexão com o PostgreSQL. Ele não
deve ser publicado porque pode conter usuário, senha, host e nomes de bancos.
Este projeto utiliza as seguintes variáveis:

```env
TECHSTORE_DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/techstore
ETL_DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/techstore_etl
```

`TECHSTORE_DATABASE_URL` aponta para a base original, que deve conter as
tabelas `produtos` e `categorias`. `ETL_DATABASE_URL` aponta para a base que
receberá as tabelas raw, processadas e estatísticas.

O repositório não possui `.env.example`; crie o arquivo `.env` manualmente na
raiz do projeto e substitua `usuario` e `senha` pelos dados do seu ambiente.

## Pré-requisitos

- Python 3.10 ou superior;
- PostgreSQL em execução;
- base `techstore` criada e populada com `produtos` e `categorias`;
- base `techstore_etl` disponível;
- DBeaver ou outra ferramenta para executar os scripts SQL;
- ambiente virtual Python recomendado.

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

As principais bibliotecas são Pandas, SQLAlchemy, `psycopg2-binary`,
`python-dotenv`, Matplotlib, Jupyter e OpenPyXL (necessário para gerar o
Excel).

## Como executar

### 1. Configurar o banco e o ambiente

1. Crie ou disponibilize a base original `techstore` com as tabelas
   `produtos` e `categorias`.
2. Crie o `.env` na raiz com as duas URLs de conexão.
3. Execute `sql/01_criar_tabelas_etl.sql` no PostgreSQL. O script cria a base
   `techstore_etl` e as tabelas de apoio. Se a base for criada nesse momento,
   conecte-se a ela antes de executar comandos de criação de tabelas, quando a
   ferramenta SQL exigir uma conexão específica.

### 2. Gerar o arquivo de entrada

Na raiz do projeto:

```bash
python gerar_csv_fornecedores.py
```

Confira se o arquivo `data/raw/techstore_fornecedores.csv` foi criado.

### 3. Executar o ETL modular

Como os módulos atuais usam imports locais (`from extract import ...`), execute
o orquestrador a partir da pasta `src`:

```powershell
cd src
python run_etl.py
```

Ao finalizar, o processo deverá ter criado ou atualizado:

- `raw_produtos` e `raw_fornecedores` no banco ETL;
- `processed_produtos` e `estatisticas_produtos` no banco ETL;
- `data/processed/relatorio_produtos.xlsx`.

### 4. Validar os dados

Execute `sql/02_consultas_validacao.sql` conectado ao banco ETL. As consultas
mostram os registros raw, quantidade de linhas, estatísticas de custo,
distribuição de status e possíveis valores nulos.

### 5. Analisar o resultado

Somente depois de concluir o ETL, abra o notebook de análise:

```bash
jupyter notebook notebooks/analise_estatisticas.ipynb
```

Esse notebook lê `data/processed/relatorio_produtos.xlsx`, apresenta informações
descritivas, calcula indicadores e gera um gráfico de margem percentual por
produto.

## Notebooks

- `etl_techstore.ipynb`: versão didática e passo a passo do fluxo completo,
  desde a extração até a exportação para Excel. É útil para entender o ETL
  antes de usar a versão modular em `src`.
- `notebooks/analise_estatisticas.ipynb`: notebook de análise executado após o
  pipeline, usando a camada processed já gerada.

## Scripts SQL

- `sql/01_criar_tabelas_etl.sql`: cria o banco `techstore_etl` e as tabelas
  `raw_fornecedores`, `processed_produtos` e `estatisticas_produtos`.
- `sql/02_consultas_validacao.sql`: reúne consultas para verificar a carga raw,
  custos, status, valores nulos e a tabela processada.

## `.gitignore`

O `.gitignore` impede que arquivos locais e temporários sejam enviados ao
controle de versão:

- `.venv/` e `venv/`: ambientes virtuais, que podem ser recriados com Python;
- `.env`: credenciais e configurações locais do PostgreSQL;
- `__pycache__/` e `*.py[cod]`: cache e arquivos compilados do Python;
- `.ipynb_checkpoints/`: checkpoints automáticos do Jupyter.

## Tecnologias utilizadas

- Python;
- Pandas;
- SQLAlchemy;
- PostgreSQL;
- `psycopg2-binary`;
- `python-dotenv`;
- Jupyter Notebook;
- Matplotlib;
- OpenPyXL.

## Finalidade didática

O projeto demonstra, em um cenário controlado, os conceitos de extração de
múltiplas fontes, camada raw, qualidade e padronização de dados, transformação
com Pandas, carga em banco relacional, exportação de resultados e análise
estatística após o processamento.
