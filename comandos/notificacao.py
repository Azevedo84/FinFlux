from PyQt5.QtWidgets import QMessageBox
import traceback
import socket
import os
import inspect

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivu = os.path.basename(nome_arquivo_com_caminho)


def grava_erro_banco(nome_funcao, e, nome_arquivo):
    try:
        nome_computador = socket.gethostname()

        msg_editada = str(e).replace("'", "*")
        msg_editada1 = msg_editada.replace('"', '*')

        """
        cursor = conecta.cursor()
        cursor.execute(f"Insert into ZZZ_ERROS (id, arquivo, funcao, mensagem, nome_pc) "
                       f"values (GEN_ID(GEN_ZZZ_ERROS_ID,1), '{nome_arquivo}', '{nome_funcao}', '{msg_editada1}', "
                       f"'{nome_computador}');")
        conecta.commit()
        """

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivu)


def trata_excecao(nome_funcao, mensagem, arquivo):
    try:
        traceback.print_exc()
        print(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}"\n{mensagem}')
        mensagem_alerta(f'Houve um problema no arquivo:\n\n'
                        f'          {arquivo}\n\n'
                        f'Comunique o desenvolvedor sobre o problema descrito abaixo:\n\n'
                        f'{nome_funcao}: {mensagem}')

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivu)


def mensagem_alerta(mensagem):
    try:
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setText(mensagem)
        alert.setWindowTitle("Atenção")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivu)


def pergunta_confirmacao(mensagem):
    try:
        confirmacao = QMessageBox()
        confirmacao.setIcon(QMessageBox.Question)
        confirmacao.setText(mensagem)
        confirmacao.setWindowTitle("Confirmação")

        sim_button = confirmacao.addButton("Sim", QMessageBox.YesRole)
        nao_button = confirmacao.addButton("Não", QMessageBox.NoRole)

        confirmacao.setDefaultButton(nao_button)

        confirmacao.exec_()

        if confirmacao.clickedButton() == sim_button:
            return True
        else:
            return False

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivu)


def tratar_notificar_erros(erro, nome_funcao, nome_arquivo):
    try:
        grava_erro_banco(nome_funcao, erro, nome_arquivo)
        trata_excecao(nome_funcao, str(erro), nome_arquivo)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivu)
