import requests # Biblioteca para importar dados de api
import pandas as pd
import logging #Biblioteca padrão (que já vem no python) para criar logs

# Configura o logger
logging.basicConfig(  
    level=logging.INFO,  # Mostra logs INFO ou mais graves (WARNING, ERROR, CRITICAL); todos menos DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem: data/hora, nível e mensagem
    handlers=[  
        logging.FileHandler("ingestao.log" , encoding='utf-8'),  # Salva os logs no arquivo ingestao.log
        logging.StreamHandler() # Exibe os logs no terminal também
    ]
)

### 1 - criando a função de generica de importação de dados da API
def importar_dados_api(endpoint, limit=20):
    """
    Função para importar dados de uma API e retornar um DataFrame do pandas.

    Parâmetros:
    endpoint (str): O endpoint da API a ser acessado. Ex: 'products', 'carts', 'users'.
    limit (int): O número máximo de registros a serem retornados por página. Ex: limit=20 Pega de 20 registros por página.
    skip (int): O número de registros a serem ignorados (para paginação). Ex: skip=0 Começa do registro 0.

    Retorna:
    list: Uma lista de dicionários contendo os dados importados da API.
    """
    logging.info(f"Iniciando extração do endpoint: {endpoint}")
    url_base = f"https://dummyjson.com/{endpoint}"
    skip = 0
    data = []

    #Vamos pegar os dados em blocos de 'limit' até que não haja mais dados a serem retornados
    while True:
        try:
            response = requests.get(url_base, params={'limit': limit, 'skip': skip}, timeout=10) #obtendo dados
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao conectar na API [{endpoint}]: {e}")
            raise ConnectionError(f"Erro ao conectar na API: {e}")
        
        if response.status_code != 200: #not OK
            logging.error(f"Falha na requisição. Status code: {response.status_code}")
            raise ConnectionError(f"Falha na requisição. Status code: {response.status_code}")

        try:
            #response.json() é um dicionário, então pegamos a chave 'endpoint' para obter os dados
            #response.json()[endpoint] vai retornar uma lista de dicionários, que utilizaremos para criar o DataFrame
            # Ex de response.json(): {"products": [{dict1}, {dict2},...,{dict100}], "total": 100, "skip": 0, "limit": 30}
            items = response.json()[endpoint] 
        except KeyError:
            raise ValueError(f"A chave '{endpoint}' não foi encontrada na resposta da API.")

        data.extend(items) # concatena os dados obtidos na lista 'data'
        skip+=limit # atualiza o valor de 'skip' para a próxima página

        if len(items) < limit: #se n_itens < limit, então não haveria mais dados a serem retornados no próximo loop, então podemos sair do loop
            break

    logging.info(f"Extração de {endpoint} concluída. Total de registros: {len(data)}")
    return data #retorna a lista de dicionários com os dados obtidos da API

# 2. EXECUÇÃO DO PIPELINE COMPLETO
if __name__ == "__main__":

    logging.info("--- INICIANDO PIPELINE DE INGESTÃO ---")

    # A- Importando os dados da API
    products = importar_dados_api('products')
    carts = importar_dados_api('carts')
    users = importar_dados_api('users')

    ## B - Criando a carts_items DataFrame a partir da "coluna" 'products' do "DataFrame" 'carts'
    carts_items = pd.json_normalize(
    carts, #"dataframe"
    record_path=['products'], #coluna que vai ser "explodida" em várias linhas
    meta=['id', 'userId'], #colunas da tabela pai que vão ser mantidas na tabela filha
    meta_prefix='cart_' #prefixo que vai vir antes do nome das colunas da tabela pai (ex: cart_id, cart_userId)
    )

    #C Criando os DataFrames de produtos
    df_products = pd.DataFrame(products)
    df_carts = pd.DataFrame(carts).drop(columns=['products']) #Coluna 'products' foi "explodida" na tabela 'carts_items', então não precisamos dela no DataFrame 'carts'
    df_users = pd.DataFrame(users)
    df_carts_items = pd.DataFrame(carts_items)

    logging.info("--- PIPELINE CONCLUÍDO COM SUCESSO! DATAFRAMES PRONTOS PARA CARGA ---")

##comentarios
##tags da tabela produtos vale fazer ARRAY_TO_STRING(tags, ', ') AS lista_tags no SQL