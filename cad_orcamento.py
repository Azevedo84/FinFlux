import sys
from forms.tela_orcamento import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import extrair_tabela, lanca_tabela, layout_cabec_tab
from comandos.conversores import valores_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from datetime import date
import inspect
import os
import traceback


class TelaOrcamento(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)
        
        layout_cabec_tab(self.table_Lista)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.table_Lista.viewport().installEventFilter(self)

        validator = QtGui.QDoubleValidator(0, 9999999.000, 3, self.line_Valor)
        locale = QtCore.QLocale("pt_BR")
        validator.setLocale(locale)
        self.line_Valor.setValidator(validator)

        self.obter_todos_dados()
        self.lanca_combo_grupo()
        self.lanca_numero()
        self.data_emissao()
        
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

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM orcamento;")
            dados = cursor.fetchall()
            if not dados[0][0]:
                self.line_Num.setText("1")
                self.combo_Grupo.setFocus()
            else:
                num = dados[0]
                num_escolha = num[0]
                num_plano_int = int(num_escolha) + 1
                num_plano_str = str(num_plano_int)
                self.line_Num.setText(num_plano_str)
                self.combo_Grupo.setFocus()

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

    def obter_todos_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            valor_total = 0

            cursor = conecta.cursor()
            cursor.execute('SELECT orc.id, orc.criacao, gr.descricao, orc.valor '
                           'FROM orcamento as orc '
                           'INNER JOIN cadastro_grupo as gr ON orc.grupo_id = gr.id;')
            lista_completa = cursor.fetchall()

            dados_ordenados = sorted(lista_completa, key=lambda x: (x[2], x[3]))

            if lista_completa:
                for i in lista_completa:
                    id_orc, data, grupo, valor = i

                    formato_brasileiro = "%d/%m/%Y"
                    data_brasileira = data.strftime(formato_brasileiro)

                    valor_float = valores_para_float(valor)

                    valor_total += valor_float

                    dados = (id_orc, data_brasileira, grupo, valor)
                    tabela_nova.append(dados)

                lanca_tabela(self.table_Lista, tabela_nova)

                if valor_total:
                    total_arred = round(valor_total, 2)
                    self.label_Total.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_grupo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Grupo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_grupo order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Grupo.addItems(nova_lista)

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
            self.line_Valor.clear()

            self.lanca_combo_grupo()
            self.lanca_numero()
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
                ids, criacao, grupo, valor = selecao

                item_count = self.combo_Grupo.count()
                for i in range(item_count):
                    item_text = self.combo_Grupo.itemText(i)
                    if grupo in item_text:
                        self.combo_Grupo.setCurrentText(item_text)

                self.line_Valor.setText(valor)

                self.line_Num.setText(ids)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            grupo = self.combo_Grupo.currentText()
            valor = self.line_Valor.text()

            if not grupo:
                self.mensagem_alerta('O campo "Grupo" não pode estar vazio!')
            elif not codigo:
                self.mensagem_alerta('O campo "Código" não pode estar vazio!')
                self.combo_Grupo.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código" não pode ser "0"!')
                self.line_Num.setFocus()
            elif not valor:
                self.mensagem_alerta('O campo "Valor" não pode estar vazio!')
                self.line_Valor.setFocus()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"DELETE from orcamento where id = {codigo};")
                conecta.commit()

                self.mensagem_alerta(f'O Orçamento do Grupo {grupo} foi excluída com sucesso!')
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
            codigo = self.line_Num.text()
            grupo = self.combo_Grupo.currentText()
            valor = self.line_Valor.text()

            if not grupo:
                self.mensagem_alerta('O campo "Grupo" não pode estar vazio!')
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.combo_Grupo.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Num.setFocus()
            elif not valor:
                self.mensagem_alerta('O campo "Valor" não pode estar vazio!')
                self.line_Valor.setFocus()
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

            valor = self.line_Valor.text()
            valor_float = valores_para_float(valor)

            grupo = self.combo_Grupo.currentText()
            tete = grupo.find(" - ")
            id_grupo = grupo[:tete]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from orcamento where id = {codigo};")
            registro_id = cursor.fetchall()
            print(registro_id, valor_float, id_grupo, grupo)

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE orcamento SET grupo_id = {id_grupo}, "
                               f"valor = '{valor_float}' "
                               f"where id = {codigo};")

                self.mensagem_alerta(f'O Orçamento do Grupo {grupo} foi alterada com sucesso!')
            else:
                cursor = conecta.cursor()
                cursor.execute(f'Insert into orcamento '
                               f'(grupo_id, valor) '
                               f'values ({id_grupo}, "{valor_float}");')

                self.mensagem_alerta(f'O Orçamento do Grupo {grupo} foi criada com sucesso!')

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
    tela = TelaOrcamento()
    tela.show()
    qt.exec_()
