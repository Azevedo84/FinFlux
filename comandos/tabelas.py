from comandos.notificacao import mensagem_alerta, tratar_notificar_erros
from comandos.cores import fundo_cabecalho_tab, fonte_cabecalho_tab, zebra_tab
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QStyledItemDelegate, QTableWidgetItem
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
import os
import inspect

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivo = os.path.basename(nome_arquivo_com_caminho)


def layout_cabec_tab(nome_tabela, fonte_cab=9):
    try:
        # Aplica o novo estilo com o tamanho de fonte desejado
        nome_tabela.horizontalHeader().setStyleSheet(
            f"QHeaderView::section {{ "
            f"background-color: {fundo_cabecalho_tab}; "
            f"font-weight: bold; "
            f"color: {fonte_cabecalho_tab}; "
            f"font-size: {fonte_cab}pt; "  # Define o tamanho da fonte
            f"}}"
        )

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def lanca_tabela(nome_tabela, dados_tab,
                 altura_linha=20,
                 zebra=True, largura_auto=True,
                 bloqueia_texto=True,
                 fonte_texto=7):
    try:
        linhas_est = len(dados_tab)
        colunas_est = len(dados_tab[0])
        nome_tabela.setRowCount(linhas_est)
        nome_tabela.setColumnCount(colunas_est)

        for i, linha in enumerate(dados_tab):
            nome_tabela.setRowHeight(i, altura_linha)
            for j, dado in enumerate(linha):
                item = QTableWidgetItem(str(dado))
                font = QFont()
                font.setPointSize(fonte_texto)
                item.setFont(font)
                nome_tabela.setItem(i, j, item)
                alinha_cetralizado = AlignDelegate(nome_tabela)
                nome_tabela.setItemDelegateForColumn(j, alinha_cetralizado)

        nome_tabela.setSelectionBehavior(QAbstractItemView.SelectRows)

        if largura_auto:
            nome_tabela.resizeColumnsToContents()

        if bloqueia_texto:
            nome_tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        if zebra:
            for row in range(nome_tabela.rowCount()):
                if row % 2 == 0:
                    for col in range(nome_tabela.columnCount()):
                        item = nome_tabela.item(row, col)
                        item.setBackground(QColor(zebra_tab))

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def extrair_tabela(nome_tabela):
    try:
        lista_final_itens = []

        total_linhas = nome_tabela.rowCount()
        if total_linhas:
            total_colunas = nome_tabela.columnCount()
            lista_final_itens = []
            linha = []
            for row in range(total_linhas):
                for column in range(total_colunas):
                    widget_item = nome_tabela.item(row, column)
                    if widget_item is not None:
                        lista_item = widget_item.text()
                        linha.append(lista_item)
                        if len(linha) == total_colunas:
                            lista_final_itens.append(linha)
                            linha = []
        return lista_final_itens

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def limpa_tabela(nome_tabela):
    try:
        nome_tabela.setRowCount(0)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def excluir_item_tab(nome_tabela, texto_tabela):
    try:
        extrai_recomendados = extrair_tabela(nome_tabela)
        if not extrai_recomendados:
            mensagem_alerta(f'A tabela "{texto_tabela}" está vazia!')
        else:
            linha_selecao = nome_tabela.currentRow()
            if linha_selecao >= 0:
                nome_tabela.removeRow(linha_selecao)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
