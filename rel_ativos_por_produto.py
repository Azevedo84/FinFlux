import sys
from forms.tela_rel_ativo_por_produto import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import float_para_moeda_reais, valores_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import inspect
import os
import traceback


class TelaRelatorioAtivoProduto(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.lanca_combo_ativo()
        self.lanca_combo_ativo_encerrados()

        self.btn_Consulta.clicked.connect(self.manipula_dados)

        self.combo_Ativos.activated.connect(self.zera_encerrados)
        self.combo_Encerrados.activated.connect(self.zera_ativos)

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

    def lanca_combo_ativo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Ativos.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT ativ.id, ativ.nome_titulo, DATE_FORMAT(mov.data, '%d/%m/%Y') "
                           "FROM fixa_cadastro_ativo as ativ "
                           "INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           "where ativ.status = 'A' "
                           "order by ativ.nome_titulo;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for ides, descr, data in lista_completa:
                    dd = f"{ides} - {descr}"
                    nova_lista.append(dd)

                self.combo_Ativos.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_ativo_encerrados(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Encerrados.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT ativ.id, ativ.nome_titulo, DATE_FORMAT(mov.data, '%d/%m/%Y') "
                           "FROM fixa_cadastro_ativo as ativ "
                           "INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           "where ativ.status = 'B' "
                           "order by ativ.nome_titulo;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for ides, descr, data in lista_completa:
                    dd = f"{ides} - {descr}"
                    nova_lista.append(dd)

                self.combo_Encerrados.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def zera_encerrados(self):
        try:
            self.combo_Encerrados.setCurrentText("")

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def zera_ativos(self):
        try:
            self.combo_Ativos.setCurrentText("")

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def manipula_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            ativo = self.combo_Ativos.currentText()
            encerrados = self.combo_Encerrados.currentText()

            if ativo:
                ativo_tete = ativo.find(" - ")
                num_ativo = ativo[:ativo_tete]

                self.lanca_dados_tabela(num_ativo)
                self.lanca_dados_ativo(num_ativo)
                self.definir_saldo(num_ativo)
            elif encerrados:
                encerrados_tete = encerrados.find(" - ")
                num_encerrados = encerrados[:encerrados_tete]

                self.lanca_dados_tabela(num_encerrados)
                self.lanca_dados_ativo(num_encerrados)
                self.definir_saldo(num_encerrados)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_dados_tabela(self, num_ativo):
        conecta = conectar_banco_nuvem()
        try:
            lista_final = []

            self.table_Lista.setRowCount(0)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y'), banc.descricao, mov.id, "
                           f"cat.descricao, (mov.qtde_ent - mov.qtde_sai) as valor, mov.obs "
                           f"FROM fixa_operacao as ope "
                           f"INNER JOIN movimentacao as mov ON ope.id_movimentacao = mov.id "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"where ope.id_ativo = {num_ativo} "
                           f"ORDER BY mov.data, valor DESC;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    data, banco, num_mov, tipo, qtde_ent, obs = i
                    dados = (data, banco, num_mov, tipo, qtde_ent, obs)
                    lista_final.append(dados)
            if lista_final:
                lanca_tabela(self.table_Lista, lista_final)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_dados_ativo(self, num_ativo):
        conecta = conectar_banco_nuvem()
        try:
            lista_final = []

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, ativ.NOME_TITULO, indexa.DESCRICAO, tip.DESCRICAO, ativ.RENTABILIDADE, "
                           f"ativ.LIQUIDEZ, ativ.VALOR, ativ.status "
                           f"FROM fixa_cadastro_ativo as ativ "
                           f"INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           f"INNER JOIN fixa_cadastro_indexador AS indexa ON ativ.ID_INDEXADOR = indexa.id "
                           f"INNER JOIN fixa_cadastro_tipo AS tip ON ativ.ID_TIPO_FIXA = tip.id "
                           f"where ativ.id = {num_ativo};")
            dados_ativo = cursor.fetchall()
            data, nome, indexa, tipo, rent, liq, valor, status = dados_ativo[0]

            valor_reais = float_para_moeda_reais(valores_para_float(valor))

            self.date_Emissao.setDate(data)

            self.line_Nome.setText(nome)
            self.line_Indexador.setText(indexa)
            self.line_Tipo.setText(tipo)
            self.line_Rentabilidade.setText(rent)
            self.line_Liquidez.setText(liq)
            self.line_Valor.setText(valor_reais)
            self.line_Status.setText(status)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def definir_saldo(self, num_ativo):
        conecta = conectar_banco_nuvem()
        try:
            valor = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, ativ.NOME_TITULO, indexa.DESCRICAO, tip.DESCRICAO, ativ.RENTABILIDADE, "
                           f"ativ.LIQUIDEZ, ativ.VALOR, ativ.status "
                           f"FROM fixa_cadastro_ativo as ativ "
                           f"INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           f"INNER JOIN fixa_cadastro_indexador AS indexa ON ativ.ID_INDEXADOR = indexa.id "
                           f"INNER JOIN fixa_cadastro_tipo AS tip ON ativ.ID_TIPO_FIXA = tip.id "
                           f"where ativ.id = {num_ativo};")
            dados_ativo = cursor.fetchall()
            data, nome, indexa, tipo, rent, liq, valor_compra, status = dados_ativo[0]

            valor_compra = valores_para_float(valor_compra)

            valor += valor_compra

            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y'), banc.descricao, mov.id, "
                           f"cat.descricao, (mov.qtde_ent - mov.qtde_sai) as valor, mov.obs "
                           f"FROM fixa_operacao as ope "
                           f"INNER JOIN movimentacao as mov ON ope.id_movimentacao = mov.id "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"where ope.id_ativo = {num_ativo} "
                           f"ORDER BY mov.data, valor DESC;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    data, banco, num_mov, tipo, valor_operacoes, obs = i

                    valor_operacoes = valores_para_float(valor_operacoes)
                    valor += valor_operacoes

            valor = round(valor, 2)
            valor = float_para_moeda_reais(valor)
            self.line_Saldo.setText(valor)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioAtivoProduto()
    tela.show()
    qt.exec_()
