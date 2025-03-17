from PyQt5.QtWidgets import QTableWidget, QHeaderView
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox
from PyQt5 import QtCore, QtWidgets
import traceback
import inspect
import os


def grava_erro_banco(nome_funcao, e, nome_arquivo):
    msg_editada = str(e).replace("'", "*")
    msg_editada1 = msg_editada.replace('"', '*')
    print(nome_funcao, nome_arquivo, msg_editada1)

    """
    cursor = conecta.cursor()
    cursor.execute(f"Insert into ZZZ_ERROS (id, arquivo, funcao, mensagem) "
                   f"values (GEN_ID(GEN_ZZZ_ERROS_ID,1), '{nome_arquivo}', '{nome_funcao}', '{msg_editada1}');")
    conecta.commit()
    """


def mensagem_alerta(mensagem):
    alert = QMessageBox()
    alert.setIcon(QMessageBox.Warning)
    alert.setText(mensagem)
    alert.setWindowTitle("Atenção")
    alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()


def pergunta_confirmacao(mensagem):
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


def trata_excecao(nome_funcao, mensagem, arquivo):
    try:
        traceback.print_exc()
        print(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}":\n{mensagem}')
        mensagem_alerta(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}":\n{mensagem}')

    except Exception as e:
        print(e)


def lanca_tabela(qtable_widget, nova_tabela):
    try:
        linhas_est = (len(nova_tabela))
        colunas_est = (len(nova_tabela[0]))
        qtable_widget.setRowCount(linhas_est)
        qtable_widget.setColumnCount(colunas_est)
        for i in range(0, linhas_est):
            qtable_widget.setRowHeight(i, 18)
            for j in range(0, colunas_est):
                alinha_cetralizado = AlignDelegate(qtable_widget)
                qtable_widget.setItemDelegateForColumn(j, alinha_cetralizado)
                qtable_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(nova_tabela[i][j])))

                item = QtWidgets.QTableWidgetItem(str(nova_tabela[i][j]))
                fonte = QFont()
                fonte.setPointSize(7)
                item.setFont(fonte)
                qtable_widget.setItem(i, j, item)

        qtable_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        qtable_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        qtable_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color:#6b6b6b; font-weight: bold; }")

        for row in range(qtable_widget.rowCount()):
            if row % 2 == 0:
                for col in range(qtable_widget.columnCount()):
                    item = qtable_widget.item(row, col)
                    item.setBackground(QColor(220, 220, 220))

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
        trata_excecao(nome_funcao, str(e), nome_arquivo)
        grava_erro_banco(nome_funcao, e, nome_arquivo)


def extrair_tabela(qtable_widget):
    try:
        lista_final_itens = []

        total_linhas = qtable_widget.rowCount()
        if total_linhas:
            total_colunas = qtable_widget.columnCount()
            lista_final_itens = []
            linha = []
            for row in range(total_linhas):
                for column in range(total_colunas):
                    widget_item = qtable_widget.item(row, column)
                    if widget_item is not None:
                        lista_item = widget_item.text()
                        linha.append(lista_item)
                        if len(linha) == total_colunas:
                            lista_final_itens.append(linha)
                            linha = []
        return lista_final_itens

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
        trata_excecao(nome_funcao, e, nome_arquivo)
        grava_erro_banco(nome_funcao, e, nome_arquivo)


def limpa_tabela(qtable_widget):
    try:
        qtable_widget.setRowCount(0)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
        trata_excecao(nome_funcao, str(e), nome_arquivo)
        grava_erro_banco(nome_funcao, e, nome_arquivo)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
