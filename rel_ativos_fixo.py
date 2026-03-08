import sys
from forms.tela_rel_ativos_fixo import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import float_para_moeda_reais, valores_para_float, data_banco_para_brasileiro
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import inspect
import os
import traceback


class TelaRelatorioAtivosFix(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.lanca_dados()

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

    def lanca_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            nova_lista = []

            total_total = 0
            total_diaria = 0
            total_vencimento = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, banc.DESCRICAO, ativ.NOME_TITULO, indexa.DESCRICAO, "
                           f"tip.DESCRICAO, ativ.RENTABILIDADE, "
                           f"ativ.vencimento, ativ.LIQUIDEZ, ativ.VALOR, ativ.saldo, ativ.status "
                           f"FROM fixa_cadastro_ativo as ativ "
                           f"INNER JOIN movimentacao as mov ON ativ.id_movimentacao = mov.id "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN fixa_cadastro_indexador AS indexa ON ativ.ID_INDEXADOR = indexa.id "
                           f"INNER JOIN fixa_cadastro_tipo AS tip ON ativ.ID_TIPO_FIXA = tip.id "
                           f"where ativ.status = 'A' order by mov.data;")
            dados_ativo = cursor.fetchall()

            if dados_ativo:
                for i in dados_ativo:
                    data_mov, banco, nome, indexa, tipo, rent, venc, liq, valor, saldo, status = i

                    data_mov = data_banco_para_brasileiro(data_mov)
                    venc = data_banco_para_brasileiro(venc)

                    valor = float_para_moeda_reais(valor)
                    saldo = float_para_moeda_reais(saldo)

                    saldo_float = valores_para_float(saldo)
                    total_total += saldo_float

                    if liq == "DIÁRIA":
                        total_diaria += saldo_float
                    else:
                        total_vencimento += saldo_float

                    dados = (data_mov, banco, nome, indexa, tipo, rent, valor, venc, saldo, liq, status)

                    nova_lista.append(dados)

            if nova_lista:
                lanca_tabela(self.table_Lista, nova_lista)

                total_diaria_arred = float_para_moeda_reais(round(total_diaria, 2))
                self.label_Diaria.setText(total_diaria_arred)

                total_vencimento_arred = float_para_moeda_reais(round(total_vencimento, 2))
                self.label_Vencimento.setText(total_vencimento_arred)

                total_total_arred = float_para_moeda_reais(round(total_total, 2))
                self.label_Total.setText(total_total_arred)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioAtivosFix()
    tela.show()
    qt.exec_()