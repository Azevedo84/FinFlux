import sys
from forms.tela_rel_renda_fixa import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import float_para_moeda_reais, valores_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import inspect
import os
import traceback


class TelaRelatorioRendaFixa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.lanca_dados_abertos()

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

    def lanca_dados_abertos(self):
        conecta = conectar_banco_nuvem()
        try:
            lista_final = []

            valor_total = 0

            cursor = conecta.cursor()
            cursor.execute("SELECT ativ.id_movimentacao, DATE_FORMAT(mov.data, '%d/%m/%Y'), "
                           "banc.descricao, ativ.NOME_TITULO, ativ.VALOR, ativ.saldo, indexa.DESCRICAO, "
                           "tip.DESCRICAO, DATE_FORMAT(ativ.vencimento, '%d/%m/%Y'), "
                           "ativ.RENTABILIDADE, ativ.LIQUIDEZ "
                           "FROM fixa_cadastro_ativo as ativ "
                           "INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN fixa_cadastro_indexador AS indexa ON ativ.ID_INDEXADOR = indexa.id "
                           f"INNER JOIN fixa_cadastro_tipo AS tip ON ativ.ID_TIPO_FIXA = tip.id "
                           "where ativ.status = 'A' "
                           "order by mov.data;")
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    num_mov, data, banco, titulo, valor, saldo, indexa, tipo, venc, rent, liq = i

                    valor_float = valores_para_float(valor)
                    saldo_float = valores_para_float(saldo)

                    valor_total += saldo_float

                    valor_reais = float_para_moeda_reais(valor_float)
                    saldo_reais = float_para_moeda_reais(saldo_float)

                    dados = (num_mov, data, banco, titulo, valor_reais, saldo_reais, indexa, tipo, venc, rent, liq)
                    lista_final.append(dados)


                lanca_tabela(self.table_Lista, lista_final)

                total_arred = round(valor_total, 2)
                self.label_Total_Lista.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioRendaFixa()
    tela.show()
    qt.exec_()
