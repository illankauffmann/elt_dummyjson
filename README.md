# Pipeline de Ingestão de Dados (ELT) - DummyJSON para o BigQuery

Este projeto realiza a extração de dados de uma API REST ([DummyJSON](https://dummyjson.com/)) e faz a carga bruta no Google BigQuery utilizando Python.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12+
* **Data Warehouse:** Google BigQuery
* **CLI / Autenticação:** Google Cloud SDK (`gcloud`)
* **Bibliotecas Principais:** `pandas`, `requests`, `google-cloud-bigquery`, `db-dtypes`
* **Versionamento:** Git & GitHub

## 🚀 Estrutura da Ingestão
O script `extract_api.py` realiza os seguintes passos:
1. Extração paginada dos endpoints: `/products`, `/carts` e `/users`.
2. Normalização de dados aninhados (`carts_items`) via Pandas.
3. Carga idempotente (`WRITE_TRUNCATE`) nas tabelas do dataset `dados_brutos` no BigQuery:
   * `raw_products`
   * `raw_carts`
   * `raw_carts_items`
   * `raw_users`

## ⚙️ Como Executar o Projeto

### 1. Pré-requisitos
* Ter o **Google Cloud CLI (`gcloud`)** instalado na máquina. [(Instruções de instalação da GCP)](https://cloud.google.com/sdk/docs/install)
* Ter acesso a um projeto ativo no Google Cloud Platform com a API do BigQuery habilitada.

### 2. Configuração do Ambiente Python
No terminal, clone o repositório, crie e ative o ambiente virtual:

```bash
# Criar e ativar o venv (Git Bash no Windows)
python -m venv venv
source venv/Scripts/activate

# Instalar dependências
pip install -r requirements.txt