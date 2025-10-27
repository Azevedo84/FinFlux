import sys
from banco_dados.conexao_nuvem import conectar_banco_nuvem
import os
import inspect

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivo = os.path.basename(nome_arquivo_com_caminho)


def lanca_numero(nome_tabela, nome_campo):
    conecta = conectar_banco_nuvem()
    try:
        cursor = conecta.cursor()
        cursor.execute(f"SELECT MAX(id) as id FROM {nome_tabela};")
        row = cursor.fetchone()  # pega só a primeira linha
        if not row or row[0] is None:
            next_id = 1
        else:
            next_id = int(row[0]) + 1

        nome_campo.setText(str(next_id))

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        exc_traceback = sys.exc_info()[2]
        self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    finally:
        if 'conexao' in locals():
            conecta.close()