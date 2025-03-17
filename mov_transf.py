import sys
from forms.tela_mov_transf import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.tabelas import lanca_tabela, layout_cabec_tab
from comandos.conversores import valores_para_float
from funcao_padrao import grava_erro_banco, trata_excecao, mensagem_alerta, limpa_tabela
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QApplication, QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate
import inspect
import os


class TelaTransferencia(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        layout_cabec_tab(self.table_Lista)
        self.definir_tamanho_aplicacao()

        self.id_usuario = "1"
        self.combo_Banco.activated.connect(self.lanca_saldo_bc1)
        self.combo_Tipo.activated.connect(self.lanca_saldo_tp1)

        self.combo_Banco_2.activated.connect(self.lanca_saldo_bc2)
        self.combo_Tipo_2.activated.connect(self.lanca_saldo_tp2)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.combo_Consulta_Banco.activated.connect(self.procura_por_banco)

        self.layout_inicial_tabela()
        self.lanca_numero()
        self.lanca_combo_banco()
        self.obter_todos_dados()

        self.date_Emissao.setFocus()
        
    def definir_tamanho_aplicacao(self):
        try:
            monitor = QDesktopWidget().screenGeometry()
            monitor_width = monitor.width()
            monitor_height = monitor.height()

            if monitor_width > 1199 and monitor_height > 809:
                interface_width = 1100
                interface_height = 720

            elif monitor_width > 1365 and monitor_height > 767:
                interface_width = 1050
                interface_height = 585
            else:
                interface_width = monitor_width - 165
                interface_height = monitor_height - 90

            x = (monitor_width - interface_width) // 2
            y = (monitor_height - interface_height) // 2

            self.setGeometry(x, y, interface_width, interface_height)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def lanca_saldo_bc1(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()

            if banco:
                self.lanca_combo_tipo1()

            tipo = self.combo_Tipo.currentText()

            if banco and tipo:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                tipotete = tipo.find(" - ")
                id_tipo = tipo[:tipotete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                               f"where id_usuario = {self.id_usuario} and "
                               f"id_banco = {id_banco} and "
                               f"id_tipoconta = {id_tipo};")
                saldo_conta = cursor.fetchall()

                if saldo_conta:
                    saldo_anterior = saldo_conta[0][1]
                else:
                    saldo_anterior = 0.00

                self.label_Saldo1.setText(str(saldo_anterior))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_saldo_tp1(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            tipo = self.combo_Tipo.currentText()

            if banco and tipo:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                tipotete = tipo.find(" - ")
                id_tipo = tipo[:tipotete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                               f"where id_usuario = {self.id_usuario} and "
                               f"id_banco = {id_banco} and "
                               f"id_tipoconta = {id_tipo};")
                saldo_conta = cursor.fetchall()

                if saldo_conta:
                    saldo_anterior = saldo_conta[0][1]
                else:
                    saldo_anterior = 0.00

                self.label_Saldo1.setText(str(saldo_anterior))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_saldo_bc2(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco_2.currentText()

            if banco:
                self.lanca_combo_tipo2()

            tipo = self.combo_Tipo_2.currentText()

            if banco and tipo:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                tipotete = tipo.find(" - ")
                id_tipo = tipo[:tipotete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                               f"where id_usuario = {self.id_usuario} and "
                               f"id_banco = {id_banco} and "
                               f"id_tipoconta = {id_tipo};")
                saldo_conta = cursor.fetchall()

                if saldo_conta:
                    saldo_anterior = saldo_conta[0][1]
                else:
                    saldo_anterior = 0.00

                self.label_Saldo2.setText(str(saldo_anterior))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_saldo_tp2(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco_2.currentText()
            tipo = self.combo_Tipo_2.currentText()

            if banco and tipo:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                tipotete = tipo.find(" - ")
                id_tipo = tipo[:tipotete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                               f"where id_usuario = {self.id_usuario} and "
                               f"id_banco = {id_banco} and "
                               f"id_tipoconta = {id_tipo};")
                saldo_conta = cursor.fetchall()

                if saldo_conta:
                    saldo_anterior = saldo_conta[0][1]
                else:
                    saldo_anterior = 0.00

                self.label_Saldo2.setText(str(saldo_anterior))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            self.line_Num.setReadOnly(True)
            self.line_Num.setFocusPolicy(False)

            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM movimentacao;")
            dados = cursor.fetchall()
            num = dados[0]
            num_escolha = num[0]
            if not num_escolha:
                self.line_Num.setText("1")
            else:
                num_plano_int = int(num_escolha) + 1
                num_plano_str = str(num_plano_int)
                self.line_Num.setText(num_plano_str)
            self.combo_Banco.setFocus()
            
        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def layout_inicial_tabela(self):
        try:
            self.table_Lista.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_Lista.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_Lista.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:#6b6b6b }")
    
            font = QFont()
            font.setBold(True)
            self.table_Lista.horizontalHeader().setFont(font)
            
        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def obter_todos_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                           f"banc.descricao, tip.descricao, mov.qtde_ent, mov.qtde_sai,  "
                           f"estab.descricao, cit.descricao, IFNULL(mov.obs, '') "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id "
                           f"WHERE gr.id = 2 "
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

    def lanca_combo_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Banco.clear()
            self.combo_Banco_2.clear()
            self.combo_Consulta_Banco.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.id, bc.descricao "
                           f"FROM liga_banco_usuario AS lig_bc_us "
                           f"left JOIN cadastro_banco as bc ON lig_bc_us.id_banco = bc.id "
                           f"where lig_bc_us.id_usuario = {self.id_usuario} "
                           f"and bc.id <> 2 "
                           f"and bc.id <> 22 "
                           f"order by bc.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Banco.addItems(nova_lista)
            self.combo_Banco_2.addItems(nova_lista)
            self.combo_Consulta_Banco.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_tipo1(self):
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
                           f"and tip.id <> 1 "
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

    def lanca_combo_tipo2(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco_2.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            self.combo_Tipo_2.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT tip.id, tip.descricao "
                           f"FROM cadastro_tipoconta as tip "
                           f"INNER JOIN liga_banco_tipo AS lig_bc_tp ON tip.id = lig_bc_tp.id_tipoconta "
                           f"where lig_bc_tp.id_banco = {id_banco} "
                           f"and tip.id <> 1 "
                           f"order by tip.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Tipo_2.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def procura_por_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Consulta_Banco.currentText()

            if banco:
                tete = banco.find(" - ")
                id_banco = banco[:tete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                               f"banc.descricao, tip.descricao, mov.qtde_ent, mov.qtde_sai,  "
                               f"estab.descricao, cit.descricao, IFNULL(mov.obs, '') "
                               f"FROM movimentacao AS mov "
                               f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                               f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                               f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                               f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                               f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                               f"INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id "
                               f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                               f"INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id "
                               f"WHERE banc.id = {id_banco} "
                               f"and gr.id = 2 "
                               f"and user.id = {self.id_usuario} "
                               f"ORDER BY mov.data;")
                lista_completa = cursor.fetchall()

                if not lista_completa:
                    mensagem_alerta(f'Não foi encontrado nenhum item com Banco: "{banco}"!')
                    self.reiniciando_tela()
                else:
                    lanca_tabela(self.table_Lista, lista_completa)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.combo_Banco.setCurrentText("")
            self.combo_Tipo.setCurrentText("")

            self.combo_Banco_2.setCurrentText("")
            self.combo_Tipo_2.setCurrentText("")
    
            self.line_Valor.clear()

            self.label_Saldo1.clear()
            self.label_Saldo2.clear()
    
            self.plain_Obs.clear()
            limpa_tabela(self.table_Lista)

            self.date_Emissao.setDate(QDate(2000, 1, 1))
    
            self.layout_inicial_tabela()
            self.lanca_numero()
            self.lanca_combo_banco()
            self.obter_todos_dados()

            self.date_Emissao.setFocus()
            
        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def extrai_estabelcimento_banco(self, id_banco):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, id_estab '
                           f'FROM cadastro_banco '
                           f'where id = {id_banco};')
            lista_completa = cursor.fetchall()
            id_estab = lista_completa[0][1]

            return id_estab

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_salvamento(self):
        try:
            banco1 = self.combo_Banco.currentText()
            tipo1 = self.combo_Tipo.currentText()

            banco2 = self.combo_Banco_2.currentText()
            tipo2 = self.combo_Tipo_2.currentText()

            valor = self.line_Valor.text()

            data_emissao = self.date_Emissao.date()

            if data_emissao == QDate(2000, 1, 1):
                mensagem_alerta('O campo "Emissão" deve ser preenchido!')
                self.date_Emissao.setFocus()
            elif not banco1:
                mensagem_alerta('O campo "Banco" da Origem não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not tipo1:
                mensagem_alerta('O campo "Tipo de Conta" da Origem não pode estar vazio!')
                self.combo_Tipo.setCurrentText("")
                self.combo_Tipo.setFocus()
            if not banco2:
                mensagem_alerta('O campo "Banco" do Destino não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not tipo2:
                mensagem_alerta('O campo "Tipo de Conta" do Destino não pode estar vazio!')
                self.combo_Tipo.setCurrentText("")
                self.combo_Tipo.setFocus()
            elif not valor:
                mensagem_alerta('O campo "R$" não pode estar vazio!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif valor == "R$ 0,00":
                mensagem_alerta('O campo "R$" não pode ser igual a Zero!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            else:
                self.criar_saldo1()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def criar_saldo1(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            tipo = self.combo_Tipo.currentText()
            tipotete = tipo.find(" - ")
            id_tipo = tipo[:tipotete]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco} and "
                           f"id_tipoconta = {id_tipo};")
            saldo_conta = cursor.fetchall()

            if not saldo_conta:
                cursor = conecta.cursor()
                cursor.execute(f'Insert into saldo_banco '
                               f'(id_usuario, id_banco, id_tipoconta, saldo, limite, vencimento) '
                               f'values ({self.id_usuario}, {id_banco}, {id_tipo}, "0", "0", "0");')

            conecta.commit()

            self.criar_saldo2()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def criar_saldo2(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco_2.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            tipo = self.combo_Tipo_2.currentText()
            tipotete = tipo.find(" - ")
            id_tipo = tipo[:tipotete]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id_usuario, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco} and "
                           f"id_tipoconta = {id_tipo};")
            saldo_conta = cursor.fetchall()

            if not saldo_conta:
                cursor = conecta.cursor()
                cursor.execute(f'Insert into saldo_banco '
                               f'(id_usuario, id_banco, id_tipoconta, saldo, limite, vencimento) '
                               f'values ({self.id_usuario}, {id_banco}, {id_tipo}, "0", "0", "0");')

            conecta.commit()

            self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            data_emissao = self.date_Emissao.date()
            data_mysql = data_emissao.toString("yyyy-MM-dd")

            banco1 = self.combo_Banco.currentText()
            bancotete1 = banco1.find(" - ")
            id_banco1 = banco1[:bancotete1]
            id_estab1 = self.extrai_estabelcimento_banco(id_banco1)

            tipo1 = self.combo_Tipo.currentText()
            tipotete1 = tipo1.find(" - ")
            id_tipo1 = tipo1[:tipotete1]

            banco2 = self.combo_Banco_2.currentText()
            bancotete2 = banco2.find(" - ")
            id_banco2 = banco2[:bancotete2]
            id_estab2 = self.extrai_estabelcimento_banco(id_banco2)

            tipo2 = self.combo_Tipo_2.currentText()
            tipotete2 = tipo2.find(" - ")
            id_tipo2 = tipo2[:tipotete2]

            valor = self.line_Valor.text()
            valor_float_sai_origem = valores_para_float(valor)

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco1} and "
                           f"id_tipoconta = {id_tipo1};")
            saldo_conta1 = cursor.fetchall()
            id_saldo1, saldo1 = saldo_conta1[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                           f'values ("{data_mysql}", {id_saldo1}, 7, '
                           f'0, {valor_float_sai_origem}, {id_estab2}, 19, "{obs_maiusculo}");')

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco2} and "
                           f"id_tipoconta = {id_tipo2};")
            saldo_conta2 = cursor.fetchall()
            id_saldo2, saldo2 = saldo_conta2[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                           f'values ("{data_mysql}", {id_saldo2}, 7, '
                           f'{valor_float_sai_origem}, 0, {id_estab1}, 19, "{obs_maiusculo}");')

            conecta.commit()

            mensagem_alerta(f'A Movimentação foi criada com sucesso!')
            self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaTransferencia()
    tela.show()
    qt.exec_()
