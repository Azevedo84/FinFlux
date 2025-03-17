import sys
from forms.tela_tipo import *
from conexao_nuvem import conectar_banco_nuvem
from funcao_padrao import grava_erro_banco, trata_excecao, extrair_tabela, lanca_tabela, mensagem_alerta
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
                       f'FROM cadastro_tipoconta WHERE descricao LIKE "%{palavra_chave}%";')
        lista_completa = cursor.fetchall()

        return lista_completa

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
        trata_excecao(nome_funcao, str(e), nome_arquivo)
        grava_erro_banco(nome_funcao, e, nome_arquivo)


class TelaTipo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.btn_Consulta.clicked.connect(self.procura_palavra)

        self.table_Lista.viewport().installEventFilter(self)

        self.line_Consulta.returnPressed.connect(lambda: self.procura_palavra())

        self.layout_inicial_tabela()
        self.lanca_numero()
        self.data_emissao()
        self.obter_todos_dados()

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM cadastro_tipoconta;")
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
            self.plain_Obs.clear()
            self.line_Consulta.clear()
    
            self.layout_inicial_tabela()
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
            cursor.execute('SELECT id, criacao, descricao, COALESCE(obs, "") '
                           'FROM cadastro_tipoconta order by descricao;')
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
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
            
        finally:
            if 'conexao' in locals():
                conecta.close()

    def procura_palavra(self):
        try:
            palavra_consulta = self.line_Consulta.text()

            if not palavra_consulta:
                mensagem_alerta(f'O Campo "Consulta Descrição" não pode estar vazio!')
                self.line_Consulta.clear()
            else:
                palavra = obter_dados(palavra_consulta)

                if not palavra:
                    mensagem_alerta(f'Não foi encontrado nenhum item com a descrição:\n"{palavra_consulta}"!')
                    self.line_Consulta.clear()
                else:
                    lanca_tabela(self.table_Lista, palavra)

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
                ids, criacao, descr, obs = selecao

                self.line_Num.setText(ids)
                self.line_Descricao.setText(descr)
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
                cursor.execute(f"SELECT * from cadastro_tipoconta where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from movimentacao where id_tipoconta = {codigo};")
                    registro_mov = cursor.fetchall()

                    if registro_mov:
                        mensagem_alerta(f'O Tipo de Conta {descricao} não pode ser excluído pois possui movimentação!')
                        self.reiniciando_tela()
                    else:
                        cursor = conecta.cursor()
                        cursor.execute(f"DELETE from cadastro_tipoconta where id = {codigo};")
                        conecta.commit()

                        mensagem_alerta(f'O Tipo de Conta {descricao} foi excluído com sucesso!')
                        self.reiniciando_tela()

                else:
                    mensagem_alerta(f'O código {codigo} do Tipo de Conta não existe!')
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

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = None
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from cadastro_tipoconta where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE cadastro_tipoconta SET descricao = '{descr_maiuscula}', "
                               f"obs = '{obs_maiusculo}' "
                               f"where id = {codigo};")

                mensagem_alerta(f'O Tipo de Conta {descr_maiuscula} foi alterado com sucesso!')
                self.reiniciando_tela()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"Insert into cadastro_tipoconta "
                               f"(descricao, obs) "
                               f"values ('{descr_maiuscula}', '{obs_maiusculo}');")

                mensagem_alerta(f'O Tipo de Conta {descr_maiuscula} foi atualizado com sucesso!')

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
    tela = TelaTipo()
    tela.show()
    qt.exec_()
