import sys
from forms.tela_relatorio_filtro import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from comandos.telas import tamanho_aplicacao
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import valores_para_float
from funcao_padrao import grava_erro_banco, trata_excecao
from PyQt5.QtWidgets import QMainWindow, QApplication
import inspect
import os
from datetime import datetime


class TelaRelatorioMovFiltros(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        layout_cabec_tab(self.table_Banco)
        layout_cabec_tab(self.table_Grupo)
        layout_cabec_tab(self.table_Categoria)
        layout_cabec_tab(self.table_Cidade)
        layout_cabec_tab(self.table_Estab)
        tamanho_aplicacao(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.processando = False

        self.id_usuario = "1"

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

                    self.total_mensal_banco(num_mes, ano_int)
                    self.total_mensal_grupo(num_mes, ano_int)
                    self.total_mensal_categoria(num_mes, ano_int)
                    self.total_mensal_cidade(num_mes, ano_int)
                    self.total_mensal_estab(num_mes, ano_int)

                elif ano and not meses:
                    ano_int = int(ano)

                    self.total_anual_banco(ano_int)
                    self.total_anual_grupo(ano_int)
                    self.total_anual_categoria(ano_int)
                    self.total_anual_cidade(ano_int)
                    self.total_anual_estab(ano_int)

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

    def total_mensal_banco(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT banc.descricao, tip.descricao, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY banc.descricao, tip.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[2]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Banco, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Banco.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_mensal_grupo(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT gr.descricao AS grupo, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY gr.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Grupo, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Grupo.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_mensal_categoria(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT cat.descricao AS catega, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY cat.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Categoria, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Categoria.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_mensal_cidade(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT cit.descricao AS cidade, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id 
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id 
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY cit.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Cidade, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Cidade.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_mensal_estab(self, num_mes, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT estab.descricao AS estab, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id 
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id 
                WHERE user.id = {self.id_usuario}
                  AND MONTH(mov.data) = {num_mes}
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY estab.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Estab, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Estab.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_banco(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT banc.descricao, tip.descricao, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario} 
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY banc.descricao, tip.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[2]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Banco, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Banco.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_grupo(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT gr.descricao AS grupo, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario} 
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY gr.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Grupo, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Grupo.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_categoria(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT cat.descricao AS catega, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                WHERE user.id = {self.id_usuario} 
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY cat.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Categoria, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Categoria.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_cidade(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT cit.descricao AS cidade, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id 
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id 
                WHERE user.id = {self.id_usuario} 
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY cit.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Cidade, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Cidade.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def total_anual_estab(self, ano_int):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT estab.descricao AS estab, SUM(mov.qtde_sai) AS total_despesas 
                FROM movimentacao AS mov 
                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id 
                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id 
                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id 
                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id 
                WHERE user.id = {self.id_usuario} 
                  AND YEAR(mov.data) = {ano_int} 
                  AND gr.id NOT IN (1, 2, 14) 
                GROUP BY estab.descricao
                ORDER BY total_despesas DESC;
            """)
            lista_completa = cursor.fetchall()

            total = 0

            if lista_completa:
                for i in lista_completa:
                    valor = i[1]

                    saldo_float = valores_para_float(valor)

                    total += saldo_float

                lanca_tabela(self.table_Estab, lista_completa)

            if total:
                total_arred = round(total, 2)
                self.label_Total_Estab.setText(str(total_arred))

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
    tela = TelaRelatorioMovFiltros()
    tela.show()
    qt.exec_()
