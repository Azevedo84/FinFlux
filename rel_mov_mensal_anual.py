import sys
from forms.tela_rel_mensal_anual import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.telas import tamanho_aplicacao
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import valores_para_float
from funcao_padrao import grava_erro_banco, trata_excecao
from PyQt5.QtWidgets import QMainWindow, QApplication
import inspect
import os
from datetime import datetime


from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class TelaRelatorioMovMensal(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        layout_cabec_tab(self.table_Lista)
        tamanho_aplicacao(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.processando = False

        self.id_usuario = "1"

        self.lanca_combo_grupo()

        self.configurar_data_atual()

        self.btn_Consulta.clicked.connect(self.manipula_dados)

        self.line_Ano.editingFinished.connect(self.manipula_dados)

    def configurar_data_atual(self):
        try:
            # Obter o mês e o ano atuais
            data_atual = datetime.now()
            mes_atual = data_atual.month  # Exemplo: 11 para novembro
            ano_atual = data_atual.year  # Exemplo: 2024

            # Encontrar o índice do mês atual no combo box e selecioná-lo
            for i in range(self.combo_Meses.count()):
                item_text = self.combo_Meses.itemText(i)
                if item_text.startswith(f"{mes_atual} -"):
                    self.combo_Meses.setCurrentIndex(i)
                    break

            # Configurar o ano atual no QLineEdit
            self.line_Ano.setText(str(ano_atual))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def lanca_combo_grupo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Grupo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT id, descricao FROM cadastro_grupo "
                           "WHERE id NOT IN (1, 2, 14) "
                           "order by descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Grupo.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def manipula_dados(self):
        conecta = conectar_banco_nuvem()

        if not self.processando:
            try:
                self.processando = True

                meses = self.combo_Meses.currentText()
                ano = self.line_Ano.text()

                grupo = self.combo_Grupo.currentText()

                classifica = self.combo_Classifica.currentText()

                if classifica == "MAIOR VALOR":
                    order_by = "ORDER BY mov.qtde_sai DESC"
                elif classifica == "MENOR VALOR":
                    order_by = "ORDER BY mov.qtde_sai"
                elif classifica == "GRUPO":
                    order_by = "ORDER BY gr.descricao"
                elif classifica == "CATEGORIA":
                    order_by = "ORDER BY cat.descricao"
                elif classifica == "ESTABELECIMENTO":
                    order_by = "ORDER BY estab.descricao"
                elif classifica == "CIDADE":
                    order_by = "ORDER BY cit.descricao"
                else:
                    order_by = "ORDER BY mov.data"

                if meses and ano:
                    if not grupo:
                        meses_tete = meses.find(" - ")
                        num_mes = meses[:meses_tete]

                        ano_int = int(ano)

                        self.total_mensal(num_mes, ano_int, order_by)
                        self.adicionar_grafico(num_mes, ano_int)
                    else:
                        meses_tete = meses.find(" - ")
                        num_mes = meses[:meses_tete]

                        ano_int = int(ano)

                        grupo_tete = grupo.find(" - ")
                        num_grupo = grupo[:grupo_tete]

                        self.total_mensal_grupo(num_mes, ano_int, num_grupo, order_by)
                        self.adicionar_grafico(num_mes, ano_int)

                elif ano and not meses:
                    if not grupo:
                        ano_int = int(ano)

                        self.total_anual(ano_int, order_by)
                        self.adicionar_grafico_ano(ano_int)
                    else:
                        ano_int = int(ano)

                        grupo_tete = grupo.find(" - ")
                        num_grupo = grupo[:grupo_tete]

                        self.total_anual_grupo(ano_int, num_grupo, order_by)
                        self.adicionar_grafico_ano(ano_int)

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
                nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
                trata_excecao(nome_funcao, str(e), nome_arquivo)
                grava_erro_banco(nome_funcao, e, nome_arquivo)

            finally:
                self.processando = False
                if 'conexao' in locals():
                    conecta.close()

    def select_padrao(self):
        try:
            texto_padrao = """SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada,
                               banc.descricao, cat.descricao,
                               mov.qtde_sai,
                               estab.descricao, cit.descricao, IFNULL(mov.obs, '')
                        FROM movimentacao AS mov
                        INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                        INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id
                        INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id
                        INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id
                        INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                        INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                        INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id
                        INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id """

            return texto_padrao

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

    def total_mensal(self, num_mes, ano_int, order_by):
        conecta = conectar_banco_nuvem()
        try:
            self.table_Lista.setRowCount(0)
            
            texto_padrao = self.select_padrao()

            cursor = conecta.cursor()
            cursor.execute(f"""{texto_padrao}
                        WHERE user.id = {self.id_usuario}
                          AND MONTH(mov.data) = {num_mes}
                          AND YEAR(mov.data) = {ano_int} 
                          AND gr.id NOT IN (1, 2, 14)
                        {order_by};
                    """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[3]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Lista, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Lista.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_mensal_grupo(self, num_mes, ano_int, num_grupo, order_by):
        conecta = conectar_banco_nuvem()
        try:
            self.table_Lista.setRowCount(0)

            texto_padrao = self.select_padrao()

            cursor = conecta.cursor()
            cursor.execute(f"""{texto_padrao}
                        WHERE user.id = {self.id_usuario}
                          AND MONTH(mov.data) = {num_mes}
                          AND YEAR(mov.data) = {ano_int} 
                          AND gr.id NOT IN (1, 2, 14) 
                          AND gr.id = {num_grupo} 
                        {order_by};
                    """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[3]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Lista, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Lista.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def adicionar_grafico(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            # Criar a série de dados
            series = QPieSeries()

            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT gr.descricao, 
                       SUM(mov.qtde_sai) AS total_valor
                FROM movimentacao AS mov
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int}
                  AND gr.id NOT IN (1, 2, 14)
                GROUP BY gr.descricao
                ORDER BY total_valor DESC;
            """)
            lista_totais = cursor.fetchall()
            if lista_totais:
                # Definir uma paleta de cores
                cores = [
                    QColor("#FF5733"), QColor("#33FF57"), QColor("#3357FF"),
                    QColor("#FF33A1"), QColor("#A133FF"), QColor("#FF8333"),
                    QColor("#33FFF5"), QColor("#F533FF")
                ]

                total = 0

                for i, (categoria, valor) in enumerate(lista_totais):
                    valor_float = valores_para_float(valor)

                    total += valor_float

                    fatia = series.append(categoria, valor_float)

                    # Atribuir uma cor da paleta, usando o índice de forma cíclica
                    fatia.setBrush(cores[i % len(cores)])

                    # Exibir rótulos fora da fatia com descrição e valor
                    fatia.setLabelPosition(QPieSlice.LabelOutside)
                    fatia.setLabel(f"{categoria}: {valor_float:.2f}")
                    fatia.setLabelVisible(True)

                # Criar o gráfico
                chart = QChart()
                chart.addSeries(series)

                # Configurar a legenda
                chart.legend().setVisible(True)  # Tornar a legenda visível
                chart.legend().setAlignment(Qt.AlignRight)  # Posicionar a legenda à direita

                # Configurar o ChartView
                chart_view = QChartView(chart)
                chart_view.setRenderHint(QPainter.Antialiasing)

                # Adicionar o ChartView ao widget da interface
                layout = self.widget_grafico.layout()  # Obtém o layout do widget
                if not layout:  # Se o layout não existir, cria um
                    from PyQt5.QtWidgets import QVBoxLayout
                    layout = QVBoxLayout(self.widget_grafico)
                else:  # Remove gráficos antigos do layout
                    for i in reversed(range(layout.count())):
                        layout.itemAt(i).widget().deleteLater()

                layout.addWidget(chart_view)  # Adiciona o gráfico ao layout

                if total:
                    total_arred = round(total, 2)
                    self.label_Total_Grafico.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual(self, ano_int, order_by):
        conecta = conectar_banco_nuvem()
        try:
            self.table_Lista.setRowCount(0)

            texto_padrao = self.select_padrao()

            cursor = conecta.cursor()
            cursor.execute(f"""{texto_padrao}
                        WHERE user.id = {self.id_usuario}
                          AND YEAR(mov.data) = {ano_int} 
                          AND gr.id NOT IN (1, 2, 14)
                        {order_by};
                    """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[3]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Lista, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Lista.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_grupo(self, ano_int, num_grupo, order_by):
        conecta = conectar_banco_nuvem()
        try:
            self.table_Lista.setRowCount(0)

            texto_padrao = self.select_padrao()

            cursor = conecta.cursor()
            cursor.execute(f"""{texto_padrao}
                        WHERE user.id = {self.id_usuario}
                          AND YEAR(mov.data) = {ano_int} 
                          AND gr.id NOT IN (1, 2, 14) 
                          AND gr.id = {num_grupo} 
                        {order_by};
                    """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[3]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Lista, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Lista.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def adicionar_grafico_ano(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            # Criar a série de dados
            series = QPieSeries()

            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT gr.descricao, 
                       SUM(mov.qtde_sai) AS total_valor
                FROM movimentacao AS mov
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id
                WHERE user.id = {self.id_usuario}
                  AND YEAR(mov.data) = {ano_int}
                  AND gr.id NOT IN (1, 2, 14)
                GROUP BY gr.descricao
                ORDER BY total_valor DESC;
            """)
            lista_totais = cursor.fetchall()
            if lista_totais:
                # Definir uma paleta de cores
                cores = [
                    QColor("#FF5733"), QColor("#33FF57"), QColor("#3357FF"),
                    QColor("#FF33A1"), QColor("#A133FF"), QColor("#FF8333"),
                    QColor("#33FFF5"), QColor("#F533FF")
                ]

                total = 0

                for i, (categoria, valor) in enumerate(lista_totais):
                    valor_float = valores_para_float(valor)

                    total += valor_float

                    fatia = series.append(categoria, valor_float)

                    # Atribuir uma cor da paleta, usando o índice de forma cíclica
                    fatia.setBrush(cores[i % len(cores)])

                    # Exibir rótulos fora da fatia com descrição e valor
                    fatia.setLabelPosition(QPieSlice.LabelOutside)
                    fatia.setLabel(f"{categoria}: {valor_float:.2f}")
                    fatia.setLabelVisible(True)

                # Criar o gráfico
                chart = QChart()
                chart.addSeries(series)

                # Configurar a legenda
                chart.legend().setVisible(True)  # Tornar a legenda visível
                chart.legend().setAlignment(Qt.AlignRight)  # Posicionar a legenda à direita

                # Configurar o ChartView
                chart_view = QChartView(chart)
                chart_view.setRenderHint(QPainter.Antialiasing)

                # Adicionar o ChartView ao widget da interface
                layout = self.widget_grafico.layout()  # Obtém o layout do widget
                if not layout:  # Se o layout não existir, cria um
                    from PyQt5.QtWidgets import QVBoxLayout
                    layout = QVBoxLayout(self.widget_grafico)
                else:  # Remove gráficos antigos do layout
                    for i in reversed(range(layout.count())):
                        layout.itemAt(i).widget().deleteLater()

                layout.addWidget(chart_view)  # Adiciona o gráfico ao layout

                if total:
                    total_arred = round(total, 2)
                    self.label_Total_Grafico.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioMovMensal()
    tela.show()
    qt.exec_()
