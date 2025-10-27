import sys
from forms.tela_cad_produto_mercado import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from banco_dados.consulta_padrao import lanca_numero
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from datetime import date
import inspect
import os
import traceback


class TelaProdutoMercado(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "compras.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.combo_Consulta_Grupo.activated.connect(self.procura_por_grupo)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.table_Lista.viewport().installEventFilter(self)

        try:
            lanca_numero("cadastro_produto_mercado", self.line_Num)
            self.data_emissao()
            self.lanca_combo_grupo()
            self.obter_todos_dados()
            self.line_Descricao.setFocus()

        except Exception as e:
            # Aqui você lida com a falha de conexão de forma mais amigável
            print("⚠️ Não foi possível conectar ao banco de dados.")
            print(f"Detalhe técnico: {e}")
            self.mensagem_alerta(
                f"Não foi possível conectar ao banco de dados.\n\nVerifique sua internet ou o servidor.\n\nDetalhe: {e}")
            self.close()
            
    def mensagem_alerta(self, mensagem):
        try:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Warning)
            alert.setText(mensagem)
            alert.setWindowTitle("Atenção")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec_()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def trata_excecao(self, nome_funcao, mensagem, arquivo, excecao):
        try:
            tb = traceback.extract_tb(excecao)
            num_linha_erro = tb[-1][1]

            traceback.print_exc()
            print(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}"\n{mensagem} {num_linha_erro}')
            self.mensagem_alerta(f'Houve um problema no arquivo:\n\n{arquivo}\n\n'
                                 f'Comunique o desenvolvedor sobre o problema descrito abaixo:\n\n'
                                 f'{nome_funcao}: {mensagem}')

            grava_erro_banco(nome_funcao, mensagem, arquivo, num_linha_erro)

        except Exception as e:
            nome_funcao_trat = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            tb = traceback.extract_tb(exc_traceback)
            num_linha_erro = tb[-1][1]
            print(f'Houve um problema no arquivo: {self.nome_arquivo} na função: "{nome_funcao_trat}"\n'
                  f'{e} {num_linha_erro}')
            grava_erro_banco(nome_funcao_trat, e, self.nome_arquivo, num_linha_erro)

    def lanca_combo_grupo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Grupo.clear()
            self.combo_Consulta_Grupo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_gr_produto_mercado order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Grupo.addItems(nova_lista)
            self.combo_Consulta_Grupo.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def data_emissao(self):
        try:
            data_hoje = date.today()
            self.date_Emissao.setDate(data_hoje)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def procura_por_grupo(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            grupo = self.combo_Consulta_Grupo.currentText()

            if grupo:
                tete = grupo.find(" - ")
                id_grupo = grupo[:tete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT cat.id, cat.criacao, grup.descricao, cat.descricao, cat.um, "
                               f"COALESCE(cat.obs, '') "
                               f"FROM cadastro_produto_mercado as cat "
                               f"INNER JOIN cadastro_gr_produto_mercado as grup ON cat.id_gr_produto = grup.id "
                               f"where cat.id_gr_produto = '{id_grupo}' "
                               f"order by cat.descricao;")
                lista_completa = cursor.fetchall()

                if not lista_completa:
                    self.mensagem_alerta(f'Não foi encontrado nenhum item com Grupo:\n "{grupo}"!')
                    self.reiniciando_tela()
                else:
                    for i in lista_completa:
                        id_empr, data, grupo, descricao, um, obs = i

                        formato_brasileiro = "%d/%m/%Y"
                        data_brasileira = data.strftime(formato_brasileiro)

                        dados = (id_empr, data_brasileira, grupo, descricao, um, obs)
                        tabela_nova.append(dados)

                    lanca_tabela(self.table_Lista, tabela_nova)

            else:
                self.obter_todos_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_todos_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            cursor = conecta.cursor()
            cursor.execute(f"SELECT cat.id, cat.criacao, grup.descricao, cat.descricao, cat.um, "
                           f"COALESCE(cat.obs, '') "
                           f"FROM cadastro_produto_mercado as cat "
                           f"LEFT JOIN cadastro_gr_produto_mercado as grup ON cat.id_gr_produto = grup.id "
                           f"order by cat.descricao;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    id_empr, data, grupo, descricao, um, obs = i

                    formato_brasileiro = "%d/%m/%Y"
                    data_brasileira = data.strftime(formato_brasileiro)

                    dados = (id_empr, data_brasileira, grupo, descricao, um, obs)
                    tabela_nova.append(dados)

                lanca_tabela(self.table_Lista, tabela_nova)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.line_Descricao.clear()
            self.plain_Obs.clear()
            self.table_Lista.setRowCount(0)

            self.combo_UM.setCurrentIndex(0)

            self.combo_Grupo.setCurrentIndex(0)
            self.combo_Consulta_Grupo.setCurrentIndex(0)

            lanca_numero("cadastro_produto_mercado", self.line_Num)
            self.data_emissao()
            self.obter_todos_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def eventFilter(self, source, event):
        try:
            if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                    event.buttons() == QtCore.Qt.LeftButton and
                    source is self.table_Lista.viewport()):
                item = self.table_Lista.currentItem()

                dados = extrair_tabela(self.table_Lista)
                selecao = dados[item.row()]
                ids, criacao, grupo,  descr, um, obs = selecao

                self.line_Num.setText(ids)
                self.line_Descricao.setText(descr)
                self.plain_Obs.setPlainText(obs)

                banco_count = self.combo_UM.count()
                for banco_ in range(banco_count):
                    banco_text = self.combo_UM.itemText(banco_)
                    if um in banco_text:
                        self.combo_UM.setCurrentText(banco_text)

                item_count = self.combo_Grupo.count()
                for i in range(item_count):
                    item_text = self.combo_Grupo.itemText(i)
                    if grupo in item_text:
                        self.combo_Grupo.setCurrentText(item_text)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            descricao = self.line_Descricao.text()

            if not descricao:
                self.mensagem_alerta('O campo "Descrição:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif descricao == "0":
                self.mensagem_alerta('O campo "Descrição:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Num.setFocus()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"SELECT * from cadastro_produto_mercado where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT prod.id, prod.descricao, prod.um, comp.qtde, comp.unit, comp.obs "
                                   f"FROM compras_mercado as comp "
                                   f"INNER JOIN cadastro_produto_mercado AS prod ON comp.id_produto = prod.id "
                                   f"WHERE prod.id = {codigo};")
                    dados_compras = cursor.fetchall()

                    if dados_compras:
                        self.mensagem_alerta(f'O produto {descricao} não pode ser excluída pois possui movimentação!')
                        self.reiniciando_tela()
                    else:
                        cursor = conecta.cursor()
                        cursor.execute(f"DELETE from cadastro_produto_mercado where id = {codigo};")
                        conecta.commit()

                        self.mensagem_alerta(f'O produto {descricao} foi excluído com sucesso!')
                        self.reiniciando_tela()

                else:
                    self.mensagem_alerta(f'O código {codigo} do Banco não existe!')
                    self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_salvamento(self):
        conecta = conectar_banco_nuvem()
        try:
            descricao = self.line_Descricao.text()
            um = self.combo_UM.currentText()
            grupo = self.combo_Grupo.currentText()

            if not descricao:
                self.mensagem_alerta('O campo "Descrição:" não pode estar vazio!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            elif descricao == "0":
                self.mensagem_alerta('O campo "Descrição:" não pode ser "0"!')
                self.line_Descricao.clear()
                self.line_Descricao.setFocus()
            if not um:
                self.mensagem_alerta('O campo "UM:" não pode estar vazio!')
                self.combo_UM.setFocus()
            elif not grupo:
                self.mensagem_alerta('O campo "Grupo:" não pode estar vazio!')
                self.combo_Grupo.setCurrentText("")
                self.combo_Grupo.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()

            descricao = self.line_Descricao.text()
            descr_maiuscula = descricao.upper()

            um = self.combo_UM.currentText()

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            grupo = self.combo_Grupo.currentText()
            tete = grupo.find(" - ")
            id_grupo = grupo[:tete]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from cadastro_produto_mercado where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE cadastro_produto_mercado SET descricao = '{descr_maiuscula}', um = '{um}', "
                               f"obs = '{obs_maiusculo}', id_gr_produto = {id_grupo} "
                               f"where id = {codigo};")

                self.mensagem_alerta(f'O Produto {descr_maiuscula} foi alterado com sucesso!')
            else:
                cursor = conecta.cursor()
                cursor.execute(f'Insert into cadastro_produto_mercado '
                               f'(descricao, um, id_gr_produto, obs) '
                               f'values ("{descr_maiuscula}", "{um}", {id_grupo}, "{obs_maiusculo}");')

                self.mensagem_alerta(f'O Produto {descr_maiuscula} foi criado com sucesso!')

            conecta.commit()
            self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaProdutoMercado()
    tela.show()
    qt.exec_()
