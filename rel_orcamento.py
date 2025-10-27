import sys
from forms.tela_rel_orcamento import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import layout_cabec_tab, lanca_tabela, extrair_tabela
from comandos.conversores import valores_para_float, float_para_moeda_reais, moeda_reais_para_float
from comandos.cores import cor_branco, cor_vermelho
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QColor, QFont
import inspect
import os
from datetime import datetime
import traceback


class TelaRelatorioOrcamento(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Mensal)
        layout_cabec_tab(self.table_Acumulado)

        self.lancar_data_atual()
        self.manipula_dados()

        self.btn_Consulta.clicked.connect(self.manipula_dados)
        
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

    def lancar_data_atual(self):
        try:
            data_atual = datetime.now()
            mes_atual = data_atual.month
            ano_atual = data_atual.year

            for i in range(self.combo_Meses.count()):
                item_text = self.combo_Meses.itemText(i)
                if item_text.startswith(f"{mes_atual} -"):
                    self.combo_Meses.setCurrentIndex(i)
                    break

            self.line_Ano.setText(str(ano_atual))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def manipula_dados(self):
        conecta = conectar_banco_nuvem()

        if not self.processando:
            try:
                self.processando = True

                meses = self.combo_Meses.currentText()
                ano = self.line_Ano.text()

                if meses and ano:
                    meses_tete = meses.find(" - ")
                    num_mes = meses[:meses_tete]

                    ano_int = int(ano)

                    self.total_mensal(ano_int, num_mes)

                    self.total_acumulado(ano_int, num_mes)

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False
                if 'conexao' in locals():
                    conecta.close()


    def total_mensal(self, ano_int, num_mes):
        conecta = conectar_banco_nuvem()
        try:
            lista_mensal = []

            valor_m_orcado = 0
            valor_m_real = 0

            cursor = conecta.cursor()
            cursor.execute('SELECT orc.grupo_id, gr.descricao, orc.valor '
                           'FROM orcamento as orc '
                           'INNER JOIN cadastro_grupo as gr ON orc.grupo_id = gr.id;')
            valores_orcamento = cursor.fetchall()
            if valores_orcamento:
                for i in valores_orcamento:
                    id_grupo, descr_grupo, valor_orcado = i

                    valor_orcado_float = valores_para_float(valor_orcado)
                    valor_orcado_rs = float_para_moeda_reais(valor_orcado_float)

                    valor_m_orcado += valor_orcado_float

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                                    SELECT gr.descricao, 
                                           SUM(mov.qtde_sai) AS total_valor 
                                    FROM movimentacao AS mov 
                                    INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                                    INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                                    WHERE MONTH(mov.data) = {num_mes} 
                                    AND YEAR(mov.data) = {ano_int} 
                                    AND gr.id = {id_grupo}
                                    GROUP BY gr.descricao
                                    ORDER BY total_valor DESC;
                                """)
                    valores_reais = cursor.fetchall()

                    if valores_reais:
                        for ii in valores_reais:
                            descr, valor_real = ii

                            valor_real_float = valores_para_float(valor_real)

                            valor_m_real += valor_real_float

                            dif = valor_orcado_float - valor_real_float
                            dif_arred = round(dif, 2)

                            valor_real_rs = float_para_moeda_reais(valor_real_float)
                            dif_arred_rs = float_para_moeda_reais(dif_arred)

                            dados_mensal = (descr_grupo, valor_orcado_rs, valor_real_rs, dif_arred_rs)
                            lista_mensal.append(dados_mensal)

                    else:
                        dif = valor_orcado_float - 0
                        dif_arred = round(dif, 2)
                        dif_arred_rs = float_para_moeda_reais(dif_arred)

                        dados_mensal = (descr_grupo, valor_orcado_rs, "R$ 0,00", dif_arred_rs)
                        lista_mensal.append(dados_mensal)

                    if lista_mensal:
                        lista_mensal.sort(key=lambda x: moeda_reais_para_float(x[2]), reverse=True)

                        lanca_tabela(self.table_Mensal, lista_mensal, altura_linha=25, fonte_texto=8)
                        self.pintar_tabela_mensal()

                    if valor_m_orcado:
                        valor_m_orcado_arred = round(valor_m_orcado, 2)
                        valor_m_orcado_rs = float_para_moeda_reais(valor_m_orcado_arred)
                        self.label_M_Orca.setText(str(valor_m_orcado_rs))

                    if valor_m_real:
                        valor_m_real_arred = round(valor_m_real, 2)
                        valor_m_real_rs = float_para_moeda_reais(valor_m_real_arred)
                        self.label_M_Real.setText(str(valor_m_real_rs))

                    valor_m_dif = valor_m_orcado - valor_m_real
                    valor_m_dif_arred = round(valor_m_dif, 2)
                    valor_m_dif_rs = float_para_moeda_reais(valor_m_dif_arred)
                    self.label_M_Dif.setText(str(valor_m_dif_rs))


        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_acumulado(self, ano_int, num_mes):
        conecta = conectar_banco_nuvem()
        try:
            lista_mensal = []

            valor_m_orcado = 0
            valor_m_real = 0

            cursor = conecta.cursor()
            cursor.execute('SELECT orc.grupo_id, gr.descricao, orc.valor '
                           'FROM orcamento as orc '
                           'INNER JOIN cadastro_grupo as gr ON orc.grupo_id = gr.id;')
            valores_orcamento = cursor.fetchall()
            if valores_orcamento:
                for i in valores_orcamento:
                    id_grupo, descr_grupo, valor_orcado = i

                    valor_orcado_floa = valores_para_float(valor_orcado)

                    valor_orcado_float = valor_orcado_floa * int(num_mes)

                    valor_m_orcado += valor_orcado_float

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                                    SELECT gr.descricao, 
                                           SUM(mov.qtde_sai) AS total_valor 
                                    FROM movimentacao AS mov 
                                    INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                                    INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                                    WHERE YEAR(mov.data) = {ano_int} 
                                    AND MONTH(mov.data) <= {num_mes}
                                    AND gr.id = {id_grupo}
                                    GROUP BY gr.descricao
                                    ORDER BY total_valor DESC;
                                """)
                    valores_reais = cursor.fetchall()

                    if valores_reais:
                        for ii in valores_reais:
                            descr, valor_real = ii

                            valor_real_float = valores_para_float(valor_real)

                            valor_m_real += valor_real_float

                            dif = valor_orcado_float - valor_real_float
                            dif_arred = round(dif, 2)

                            valor_orcado_rs = float_para_moeda_reais(valor_orcado_float)
                            valor_real_rs = float_para_moeda_reais(valor_real_float)
                            dif_arred_rs = float_para_moeda_reais(dif_arred)

                            dados_mensal = (descr_grupo, valor_orcado_rs, valor_real_rs, dif_arred_rs)
                            lista_mensal.append(dados_mensal)

                    if lista_mensal:
                        lista_mensal.sort(key=lambda x: moeda_reais_para_float(x[2]), reverse=True)

                        lanca_tabela(self.table_Acumulado, lista_mensal, altura_linha=25, fonte_texto=8)
                        self.pintar_tabela_acumulado()

                    if valor_m_orcado:
                        valor_m_orcado_arred = round(valor_m_orcado, 2)
                        valor_m_orcado_rs = float_para_moeda_reais(valor_m_orcado_arred)
                        self.label_A_Orca.setText(str(valor_m_orcado_rs))

                    if valor_m_real:
                        valor_m_real_arred = round(valor_m_real, 2)
                        valor_m_real_rs = float_para_moeda_reais(valor_m_real_arred)
                        self.label_A_Real.setText(str(valor_m_real_rs))

                    valor_m_dif = valor_m_orcado - valor_m_real
                    valor_m_dif_arred = round(valor_m_dif, 2)
                    valor_m_dif_rs = float_para_moeda_reais(valor_m_dif_arred)
                    self.label_A_Dif.setText(str(valor_m_dif_rs))


        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def pintar_tabela_mensal(self):
        try:
            extrai_tabela = extrair_tabela(self.table_Mensal)

            for index, itens in enumerate(extrai_tabela):
                grupo, orcado, real, dif = itens
                dif_float = moeda_reais_para_float(dif)

                if dif_float < 0:
                    font = QFont()
                    font.setBold(True)

                    self.table_Mensal.item(index, 3).setBackground(QColor(cor_vermelho))
                    self.table_Mensal.item(index, 3).setFont(font)
                    self.table_Mensal.item(index, 3).setForeground(QColor(cor_branco))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def pintar_tabela_acumulado(self):
        try:
            extrai_tabela = extrair_tabela(self.table_Acumulado)

            for index, itens in enumerate(extrai_tabela):
                grupo, orcado, real, dif = itens
                dif_float = moeda_reais_para_float(dif)

                if dif_float < 0:
                    font = QFont()
                    font.setBold(True)

                    self.table_Acumulado.item(index, 3).setBackground(QColor(cor_vermelho))
                    self.table_Acumulado.item(index, 3).setFont(font)
                    self.table_Acumulado.item(index, 3).setForeground(QColor(cor_branco))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioOrcamento()
    tela.show()
    qt.exec_()
