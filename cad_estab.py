import sys
from forms.tela_estab import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.telas import tamanho_aplicacao
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from funcao_padrao import grava_erro_banco, trata_excecao, mensagem_alerta, limpa_tabela
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
from datetime import date
import inspect
import os


class TelaEstab(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Lista)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.btn_Consulta.clicked.connect(self.procura_palavra)

        self.table_Lista.viewport().installEventFilter(self)

        self.line_Consulta.returnPressed.connect(lambda: self.procura_palavra())

        self.layout_inicial_tabela()
        self.lanca_numero()
        self.data_emissao()

    def obter_dados(self, palavra_chave):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, criacao, descricao, COALESCE(telefone, ""), COALESCE(email, ""), '
                           f'COALESCE(site, ""), COALESCE(obs, "") '
                           f'FROM cadastro_estabelecimento WHERE descricao LIKE "%{palavra_chave}%";')
            lista_completa = cursor.fetchall()

            return lista_completa

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM cadastro_estabelecimento;")
            dados = cursor.fetchall()

            if not dados or dados[0][0] is None:
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

    def layout_inicial_tabela(self):
        try:
            self.table_Lista.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_Lista.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_Lista.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:#6b6b6b }")

            font = QFont()
            font.setBold(True)
            self.table_Lista.horizontalHeader().setFont(font)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.line_Descricao.clear()
            self.line_Telefone.clear()
            self.line_Email.clear()
            self.line_Site.clear()
            self.plain_Obs.clear()
            self.line_Consulta.clear()

            self.layout_inicial_tabela()
            self.lanca_numero()
            self.data_emissao()
            limpa_tabela(self.table_Lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def procura_palavra(self):
        try:
            tabela_nova = []

            palavra_consulta = self.line_Consulta.text()

            if not palavra_consulta:
                mensagem_alerta(f'O Campo "Consulta Descrição" não pode estar vazio!')
                self.line_Consulta.clear()
            else:
                palavra = self.obter_dados(palavra_consulta)

                if not palavra:
                    mensagem_alerta(f'Não foi encontrado nenhum item com a descrição:\n"{palavra_consulta}"!')
                    self.line_Consulta.clear()
                else:
                    for i in palavra:
                        id_empr, data, descricao, telefone, email, site, obs = i

                        formato_brasileiro = "%d/%m/%Y"
                        data_brasileira = data.strftime(formato_brasileiro)

                        dados = (id_empr, data_brasileira, descricao, telefone, email, site, obs)
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

                dados = extrair_tabela(self.table_Lista)
                selecao = dados[item.row()]
                ids, criacao, descr, telefone, email, site, obs = selecao

                self.line_Num.setText(ids)
                self.line_Descricao.setText(descr)
                self.line_Telefone.setText(telefone)
                self.line_Email.setText(email)
                self.line_Site.setText(site)
                self.plain_Obs.setPlainText(obs)

            return super(QMainWindow, self).eventFilter(source, event)

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
                cursor.execute(f"SELECT * from cadastro_estabelecimento where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from movimentacao where id_estab = {codigo};")
                    registro_mov = cursor.fetchall()

                    if registro_mov:
                        mensagem_alerta(f'O Estabelecimento {descricao} '
                                        f'não pode ser excluído pois possui movimentação!')
                        self.reiniciando_tela()
                    else:
                        cursor = conecta.cursor()
                        cursor.execute(f"DELETE from cadastro_estabelecimento where id = {codigo};")
                        conecta.commit()

                        mensagem_alerta(f'O Estabelecimento {descricao} foi excluído com sucesso!')
                        self.reiniciando_tela()

                else:
                    mensagem_alerta(f'O código {codigo} do Estabelecimento não existe!')
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

            telefone = self.line_Telefone.text()
            email = self.line_Email.text()
            site = self.line_Site.text()

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from cadastro_estabelecimento where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE cadastro_estabelecimento SET descricao = '{descr_maiuscula}', "
                               f"obs = '{obs_maiusculo}', telefone = '{telefone}', "
                               f"email = '{email}', site = '{site}' "
                               f"where id = {codigo};")

                mensagem_alerta(f'O Estabelecimento {descr_maiuscula} foi alterado com sucesso!')
            else:
                cursor = conecta.cursor()
                cursor.execute(f"Insert into cadastro_estabelecimento "
                               f"(descricao, telefone, email, site, obs) "
                               f"values ('{descr_maiuscula}', '{telefone}', '{email}', '{site}', '{obs_maiusculo}');")

                mensagem_alerta(f'O Estabelecimento {descr_maiuscula} foi atualizado com sucesso!')

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
    tela = TelaEstab()
    tela.show()
    qt.exec_()
