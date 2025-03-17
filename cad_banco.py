import sys
from forms.tela_banco import *
from conexao_nuvem import conectar_banco_nuvem
from funcao_padrao import grava_erro_banco, trata_excecao, mensagem_alerta, lanca_tabela, limpa_tabela
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
from datetime import date
import inspect
import os


def obter_dados(palavra_chave):
    conecta = conectar_banco_nuvem()
    try:
        cursor = conecta.cursor()
        cursor.execute(f'SELECT id, criacao, descricao, COALESCE(obs, "") '
                       f'FROM cadastro_banco WHERE descricao LIKE "%{palavra_chave}%";')
        lista_completa = cursor.fetchall()

        return lista_completa

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
        trata_excecao(nome_funcao, str(e), nome_arquivo)
        grava_erro_banco(nome_funcao, e, nome_arquivo)

    finally:
        if 'conexao' in locals():
            conecta.close()


class TelaBanco(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.btn_Consulta.clicked.connect(self.procura_palavra)

        self.table_Lista.viewport().installEventFilter(self)

        self.line_Consulta.returnPressed.connect(lambda: self.procura_palavra())

        self.layout_tabela()
        self.lanca_numero()
        self.data_emissao()
        self.obter_todos_dados()
        self.lanca_combo_estabelecimento()

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM cadastro_banco;")
            dados = cursor.fetchall()
            if not dados:
                self.line_Num.setText("1")
                self.line_Descricao.setFocus()
            else:
                num = dados[0]
                num_escolha = num[0]
                num_plano_int = int(num_escolha) + 1
                num_plano_str = str(num_plano_int)
                self.line_Num.setText(num_plano_str)
                self.line_Descricao.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def data_emissao(self):
        try:
            data_hoje = date.today()
            self.date_Emissao.setDate(data_hoje)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def layout_tabela(self):
        try:
            qwidget_table = self.table_Lista

            qwidget_table.setColumnWidth(0, 35)
            qwidget_table.setColumnWidth(1, 80)
            qwidget_table.setColumnWidth(2, 80)
            qwidget_table.setColumnWidth(3, 120)
            qwidget_table.setColumnWidth(4, 90)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def lanca_combo_estabelecimento(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Estab.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_estabelecimento order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Estab.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.line_Descricao.clear()
            self.plain_Obs.clear()
            self.line_Consulta.clear()

            limpa_tabela(self.table_Lista)

            self.combo_Estab.setCurrentText("")

            self.layout_tabela()
            self.lanca_numero()
            self.data_emissao()
            self.obter_todos_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def obter_todos_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            cursor = conecta.cursor()
            cursor.execute('SELECT bc.id, bc.criacao, bc.descricao, COALESCE(estab.descricao, ""), '
                           'COALESCE(bc.obs, "") '
                           'FROM cadastro_banco as bc '
                           'LEFT JOIN cadastro_estabelecimento AS estab ON estab.id = bc.id_estab '
                           'order by bc.descricao;')
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    id_empr, data, descricao, estab, obs = i

                    formato_brasileiro = "%d/%m/%Y"
                    data_brasileira = data.strftime(formato_brasileiro)

                    dados = (id_empr, data_brasileira, descricao, estab, obs)
                    tabela_nova.append(dados)

                lanca_tabela(self.table_Lista, tabela_nova)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def procura_palavra(self):
        try:
            tabela_nova = []

            palavra_consulta = self.line_Consulta.text()

            if not palavra_consulta:
                mensagem_alerta('O Campo "Consulta Descrição" não pode estar vazio!')
                self.line_Consulta.clear()
            else:
                palavra = obter_dados(palavra_consulta)

                if not palavra:
                    mensagem_alerta(f'Não foi encontrado nenhum item com a descrição:\n"{palavra_consulta}"!')
                    self.line_Consulta.clear()
                else:
                    for i in palavra:
                        id_empr, data, descricao, obs = i

                        formato_brasileiro = "%d/%m/%Y"
                        data_brasileira = data.strftime(formato_brasileiro)

                        dados = (id_empr, data_brasileira, descricao, obs)
                        tabela_nova.append(dados)

                    lanca_tabela(self.table_Lista, tabela_nova)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def eventFilter(self, source, event):
        try:
            if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                    event.buttons() == QtCore.Qt.LeftButton and
                    source is self.table_Lista.viewport()):
                item = self.table_Lista.currentItem()

                dados = self.extrair_tabela()
                selecao = dados[item.row()]
                ids, criacao, descr, estab, obs = selecao

                self.line_Num.setText(ids)
                self.line_Descricao.setText(descr)

                if estab:
                    estab_count = self.combo_Estab.count()
                    for estab_ in range(estab_count):
                        estab_text = self.combo_Estab.itemText(estab_)
                        if estab in estab_text:
                            self.combo_Estab.setCurrentText(estab_text)

                self.plain_Obs.setPlainText(obs)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def lanca_tabela(self, dados):
        try:
            linhas_est = (len(dados))
            colunas_est = (len(dados[0]))
            self.table_Lista.setRowCount(linhas_est)
            self.table_Lista.setColumnCount(colunas_est)
            for i in range(0, linhas_est):
                self.table_Lista.setRowHeight(i, 24)
                for j in range(0, colunas_est):
                    alinha_cetralizado = AlignDelegate(self.table_Lista)
                    self.table_Lista.setItemDelegateForColumn(j, alinha_cetralizado)
                    self.table_Lista.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))

            self.table_Lista.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_Lista.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_Lista.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:#6b6b6b }")
            font = QFont()
            font.setBold(True)
            self.table_Lista.horizontalHeader().setFont(font)

            self.table_Lista.resizeColumnsToContents()

            total_width = self.table_Lista.verticalHeader().width()
            for col in range(self.table_Lista.columnCount()):
                total_width += self.table_Lista.columnWidth(col)

            last_column = self.table_Lista.columnCount() - 1

            for column in range(self.table_Lista.columnCount() - 1):
                valores = self.table_Lista.columnWidth(column)
                total_width -= valores
            self.table_Lista.setColumnWidth(last_column, total_width)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def extrair_tabela(self):
        try:
            row_count = self.table_Lista.rowCount()
            column_count = self.table_Lista.columnCount()
            lista_final_itens = []
            linha = []
            for row in range(row_count):
                for column in range(column_count):
                    widget_item = self.table_Lista.item(row, column)
                    lista_item = widget_item.text()
                    linha.append(lista_item)
                    if len(linha) == column_count:
                        lista_final_itens.append(linha)
                        linha = []
            return lista_final_itens

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            descricao = self.line_Descricao.text()

            if not descricao:
                mensagem_alerta('O campo "Descrição:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif descricao == "0":
                mensagem_alerta('O campo "Descrição:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif not codigo:
                mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"SELECT * from cadastro_banco where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from movimentacao where id_banco = {codigo};")
                    registro_mov = cursor.fetchall()

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from estrutura_banco where id_banco = {codigo};")
                    registro_estrut = cursor.fetchall()

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from cadastro_fatura where id_banco = {codigo};")
                    registro_fatura = cursor.fetchall()

                    if registro_mov:
                        mensagem_alerta(f'O banco {descricao} não pode ser excluído pois possui movimentação!')
                        self.reiniciando_tela()
                    elif registro_estrut:
                        mensagem_alerta(f'O banco {descricao} não pode ser excluído pois possui estruturas vinculadas!')
                        self.reiniciando_tela()
                    elif registro_fatura:
                        mensagem_alerta(f'O banco {descricao} não pode ser excluído pois possui faturas vinculadas!')
                        self.reiniciando_tela()
                    else:
                        cursor = conecta.cursor()
                        cursor.execute(f"DELETE from cadastro_banco where id = {codigo};")
                        conecta.commit()

                        mensagem_alerta(f'O Banco {descricao} foi excluído com sucesso!')
                        self.reiniciando_tela()

                else:
                    mensagem_alerta(f'O código {codigo} do Banco não existe!')
                    self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_salvamento(self):
        try:
            codigo = self.line_Num.text()
            descricao = self.line_Descricao.text()
            estab = self.combo_Estab.currentText()

            if not descricao:
                mensagem_alerta('O campo "Descrição:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif descricao == "0":
                mensagem_alerta('O campo "Descrição:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif not codigo:
                mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            elif not estab:
                mensagem_alerta('O campo "Estabelecimento" não pode estar vazio!')
                self.combo_Estab.setCurrentText("")
                self.combo_Estab.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()

            descricao = self.line_Descricao.text()
            descr_maiuscula = descricao.upper()

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab = estab[:estabtete]

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from cadastro_banco where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE cadastro_banco "
                               f"SET descricao = '{descr_maiuscula}', "
                               f"id_estab = {id_estab}, "
                               f"obs = '{obs_maiusculo}' "
                               f"where id = {codigo};")

                mensagem_alerta(f'O Banco {descr_maiuscula} foi alterado com sucesso!')

                conecta.commit()

                self.reiniciando_tela()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"Insert into cadastro_banco "
                               f"(descricao, id_estab, obs) "
                               f"values ('{descr_maiuscula}', {id_estab}, '{obs_maiusculo}');")

                mensagem_alerta(f'O Banco {descr_maiuscula} foi atualizado com sucesso!')

                conecta.commit()

                self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaBanco()
    tela.show()
    qt.exec_()
