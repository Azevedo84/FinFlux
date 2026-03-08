import sys
from banco_dados.controle_erros import grava_erro_banco
from PyQt5.QtCore import QLocale, QRegExp
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator
from PyQt5 import QtCore
from datetime import date
import os
import inspect
import traceback
from PyQt5 import QtGui

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivo = os.path.basename(nome_arquivo_com_caminho)


def trata_excecao(nome_funcao, mensagem, arquivo, excecao):
    try:
        tb = traceback.extract_tb(excecao)
        num_linha_erro = tb[-1][1]

        traceback.print_exc()
        print(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}"\n{mensagem} {num_linha_erro}')

        grava_erro_banco(nome_funcao, mensagem, arquivo, num_linha_erro)

    except Exception as e:
        nome_funcao_trat = inspect.currentframe().f_code.co_name
        exc_traceback = sys.exc_info()[2]
        tb = traceback.extract_tb(exc_traceback)
        num_linha_erro = tb[-1][1]
        print(f'Houve um problema no arquivo: {nome_arquivo} na função: "{nome_funcao_trat}"\n'
              f'{e} {num_linha_erro}')
        grava_erro_banco(nome_funcao_trat, e, nome_arquivo, num_linha_erro)


def define_combo_com_id(nome_combo, valor):
    try:
        combo_count = nome_combo.count()
        for combo_ in range(combo_count):
            combo_text = nome_combo.itemText(combo_)

            if combo_text:
                tete = combo_text.find(" - ")
                nomezinho = combo_text[tete + 3:]
            else:
                nomezinho = ""

            if valor == nomezinho:
                nome_combo.setCurrentText(combo_text)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        exc_traceback = sys.exc_info()[2]
        trata_excecao(nome_funcao, str(e), nome_arquivo, exc_traceback)

def define_combo_so_string(nome_combo, valor):
    try:
        combo_count = nome_combo.count()
        for combo_ in range(combo_count):
            combo_text = nome_combo.itemText(combo_)

            if valor == combo_text:
                nome_combo.setCurrentText(combo_text)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        exc_traceback = sys.exc_info()[2]
        trata_excecao(nome_funcao, str(e), nome_arquivo, exc_traceback)