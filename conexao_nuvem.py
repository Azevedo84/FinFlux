import mysql.connector
from mysql.connector import errorcode


# Função para ler as configurações do banco de dados do arquivo de configuração
def get_database_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)  # Dividir apenas na primeira ocorrência do caractere '='
            config[key] = value
    return config


# Função para conectar ao banco de dados
def conectar_banco_nuvem():
    try:
        db_config = get_database_config()
        conexao = mysql.connector.connect(
            host=db_config['DB_HOST'],
            user=db_config['DB_USER'],
            password=db_config['DB_PASSWORD'],
            database=db_config['DB_DATABASE'])

        return conexao

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msgerro = "Usuário ou senha incorretos!"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msgerro = "Banco de Dados não existe!"
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            msgerro = "Endereço TCP/IP não encontrado!"
        else:
            msgerro = err
        raise Exception(f"Erro ao conectar ao banco de dados: {msgerro}")
