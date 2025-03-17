import sys
from forms.tela_movimentacao import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.telas import tamanho_aplicacao
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from funcao_padrao import grava_erro_banco, trata_excecao
from PyQt5.QtWidgets import QMainWindow, QApplication
import inspect
import os


class TelaMovimentacao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Lista)

        self.id_usuario = "1"

        self.combo_Banco.activated.connect(self.conecta_banco_fatura_tipo)

        self.btn_Consulta.clicked.connect(self.manipula_dados)

        self.layout_tabela()
        self.lanca_combo_banco()

    def layout_tabela(self):
        try:
            qwidget_table = self.table_Lista

            qwidget_table.setColumnWidth(0, 60)
            qwidget_table.setColumnWidth(1, 60)
            qwidget_table.setColumnWidth(2, 80)
            qwidget_table.setColumnWidth(3, 130)
            qwidget_table.setColumnWidth(4, 70)
            qwidget_table.setColumnWidth(5, 70)
            qwidget_table.setColumnWidth(6, 130)
            qwidget_table.setColumnWidth(7, 100)
            qwidget_table.setColumnWidth(8, 250)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def conecta_banco_fatura_tipo(self):
        try:
            self.lanca_combo_fatura()
            self.lanca_combo_tipo()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def lanca_combo_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Banco.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.id, bc.descricao "
                           f"FROM cadastro_banco as bc "
                           f"INNER JOIN liga_banco_usuario AS lig_bc_us ON bc.id = lig_bc_us.id_banco "
                           f"where lig_bc_us.id_usuario = {self.id_usuario} "
                           f"order by bc.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Banco.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_tipo(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            self.combo_Tipo.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT tip.id, tip.descricao "
                           f"FROM cadastro_tipoconta as tip "
                           f"INNER JOIN liga_banco_tipo AS lig_bc_tp ON tip.id = lig_bc_tp.id_tipoconta "
                           f"where lig_bc_tp.id_banco = {id_banco} "
                           f"order by tip.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Tipo.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            if banco:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                self.combo_Fatura.clear()
                nova_lista = [""]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT fat.id, fat.mes, fat.ano "
                               f"FROM cadastro_fatura as fat "
                               f"INNER JOIN saldo_banco AS sal_bc ON fat.id_saldo = sal_bc.id "
                               f"WHERE sal_bc.id_banco = {id_banco} "
                               f"ORDER BY fat.ano, fat.mes;")

                lista_completa = cursor.fetchall()

                for ides, mes, ano in lista_completa:
                    dd = f"{ides} - {mes}/{ano}"
                    nova_lista.append(dd)

                self.combo_Fatura.addItems(nova_lista)

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
        try:
            banco = self.combo_Banco.currentText()
            tipo = self.combo_Tipo.currentText()
            fatura = self.combo_Fatura.currentText()

            select_padrao = (f"SELECT mov.id, DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                             f"banc.descricao, gr.descricao, cat.descricao, "
                             f"CASE WHEN mov.qtde_ent = 0 THEN '' ELSE mov.qtde_ent END AS qtde_ent, "
                             f"CASE WHEN mov.qtde_sai = 0 THEN '' ELSE mov.qtde_sai END AS qtde_sai, "
                               f"estab.descricao, cit.descricao, mov.id_fatura, IFNULL(mov.obs, '') "
                               f"FROM movimentacao AS mov "
                               f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                               f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                               f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                               f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                               f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                               f"INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id "
                               f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                               f"INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id "
                               f"LEFT JOIN cadastro_fatura AS fat ON mov.id_fatura = fat.id ")

            if banco and fatura:
                banco_tete = banco.find(" - ")
                id_banco = banco[:banco_tete]

                fatura_tete = fatura.find(" - ")
                id_fatura = fatura[:fatura_tete]

                cursor = conecta.cursor()
                cursor.execute(f"{select_padrao}"
                               f"WHERE banc.id = {id_banco}  "
                               f"and mov.id_fatura = {id_fatura} "
                               f"and user.id = {self.id_usuario} "
                               f"ORDER BY mov.data;")
                lista_completa = cursor.fetchall()

                if lista_completa:
                    lanca_tabela(self.table_Lista, lista_completa)
                    self.table_Lista.scrollToBottom()

            elif banco and tipo and not fatura:
                banco_tete = banco.find(" - ")
                id_banco = banco[:banco_tete]

                tipo_tete = tipo.find(" - ")
                id_tipo = tipo[:tipo_tete]

                cursor = conecta.cursor()
                cursor.execute(f"{select_padrao}"
                               f"WHERE banc.id = {id_banco}  "
                               f"and tip.id = {id_tipo} "
                               f"and user.id = {self.id_usuario} "
                               f"ORDER BY mov.data;")
                lista_completa = cursor.fetchall()

                if lista_completa:
                    lanca_tabela(self.table_Lista, lista_completa)
                    self.table_Lista.scrollToBottom()

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
    tela = TelaMovimentacao()
    tela.show()
    qt.exec_()
