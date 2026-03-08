import sys
from forms.tela_rel_receita_despesa import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import layout_cabec_tab, lanca_tabela, extrair_tabela
from comandos.conversores import valores_para_float, float_para_moeda_reais, moeda_reais_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import inspect
import os
from datetime import datetime
import traceback


class TelaRelatorioReceitaDespesa(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.categ_impostos = "103, 110, 158, 181, 109"

        self.manipula_dados()

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

    def manipula_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            receitas = self.obter_receitas_total()
            despesas = self.obter_despesas_total()

            total_receitas_ano = sum(receitas)
            total_despesas_ano = sum(despesas)
            saldo_ano = total_receitas_ano - total_despesas_ano

            linha_receita = ["Receita"] + [
                float_para_moeda_reais(v) for v in receitas
            ] + [float_para_moeda_reais(total_receitas_ano)]

            linha_despesa = ["Despesas"] + [
                float_para_moeda_reais(v) for v in despesas
            ] + [float_para_moeda_reais(total_despesas_ano)]

            saldo_mensal = [
                receitas[i] - despesas[i] for i in range(12)
            ]

            linha_saldo = ["Saldo"] + [
                float_para_moeda_reais(v) for v in saldo_mensal
            ] + [float_para_moeda_reais(saldo_ano)]

            lista_com_saldo = [
                linha_receita,
                linha_despesa,
                linha_saldo
            ]

            lanca_tabela(self.table_Lista, lista_com_saldo)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_receitas_total(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("""
                           SELECT MONTH(data) AS mes,
                                  SUM(
                                          IF(id_categoria IN (1, 2, 3, 4, 5, 151), qtde_ent, 0)
                                  )           AS total_receita
                           FROM movimentacao
                           WHERE YEAR(data) = YEAR(CURDATE())
                           GROUP BY MONTH(data)
                           ORDER BY MONTH(data)
                           """)

            receitas = [0] * 12  # jan → dez

            for mes, total in cursor.fetchall():
                receitas[mes - 1] = total or 0

            return receitas

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_despesas_total(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT 
                    MONTH(data) AS mes,
                    SUM(qtde_sai) AS total_despesas
                FROM movimentacao AS mov
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                WHERE YEAR(data) = YEAR(CURDATE())
                  AND gr.id NOT IN (1, 2, 14)
                  AND cat.id NOT IN ({self.categ_impostos})
                GROUP BY MONTH(data)
                ORDER BY MONTH(data)
            """)

            despesas = [0] * 12  # jan → dez

            for mes, total in cursor.fetchall():
                despesas[mes - 1] = total or 0

            return despesas

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioReceitaDespesa()
    tela.show()
    qt.exec_()
