import mysql.connector
from mysql.connector import errorcode


def conectar_banco_local():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='anderson',
            password='anderson',
            database='despesas')

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
