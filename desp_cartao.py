import sys
from forms.tela_desp_cartao import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.telas import tamanho_aplicacao
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_float
from funcao_padrao import grava_erro_banco, trata_excecao, mensagem_alerta, limpa_tabela, pergunta_confirmacao
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from datetime import datetime
from dateutil.relativedelta import relativedelta
import inspect
import os


class TelaDespCartao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Lista)

        self.id_usuario = "1"

        self.combo_Banco.activated.connect(self.conecta_banco_lanca_fatura)
        self.combo_Fatura.activated.connect(self.lanca_saldo_bc)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)

        self.combo_Grupo.activated.connect(self.lanca_combo_categoria)

        self.combo_Consulta_Banco.activated.connect(self.procura_por_banco_fatura)
        self.combo_Consulta_Fatura.activated.connect(self.procura_por_banco_fatura)

        self.table_Lista.viewport().installEventFilter(self)

        self.lanca_numero()
        self.lanca_combo_banco()
        self.lanca_combo_grupo()
        self.lanca_combo_cidade()
        self.lanca_combo_estabelecimento()

        self.spin_Parcelas.setValue(1)

        self.date_Emissao.setFocus()

    def conecta_banco_lanca_fatura(self):
        try:
            self.lanca_combo_fatura()
            self.lanca_saldo_bc()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def calcula_valor_parcela(self, valor, parcelas):
        try:
            divisao = valor / parcelas

            parcela_arred = round(divisao, 2)

            valor_tot_c_arred = parcela_arred * parcelas

            dif = valor_tot_c_arred - valor

            primeira_parcela = parcela_arred - dif
            primeira_parcela_arred = round(primeira_parcela, 2)

            return primeira_parcela_arred, parcela_arred

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

    def lanca_saldo_bc(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            fatura = self.combo_Fatura.currentText()

            saldo_anterior = 0

            if banco and fatura:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                faturatete = fatura.find(" - ")
                id_fatura = fatura[:faturatete]

                id_tipo = "1"

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_saldo, qtde_ent, qtde_sai FROM movimentacao "
                               f"where id_fatura = {id_fatura};")
                saldo_conta = cursor.fetchall()

                if saldo_conta:
                    for i in saldo_conta:
                        id_saldo, qtde_ent, qtde_sai = i
                        saldo_anterior += valores_para_float(qtde_ent)
                        saldo_anterior -= valores_para_float(qtde_sai)
                else:
                    saldo_anterior = 0.00

                saldo_arred = round(saldo_anterior, 2)
                self.label_Saldo.setText(str(saldo_arred))

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

    def lanca_combo_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Banco.clear()
            self.combo_Consulta_Banco.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.id, bc.descricao "
                           f"FROM liga_banco_usuario AS lig_bc_us "
                           f"left JOIN cadastro_banco as bc ON lig_bc_us.id_banco = bc.id "
                           f"INNER JOIN liga_banco_tipo AS lig_bc_tp ON lig_bc_tp.id_banco = bc.id "
                           f"where lig_bc_us.id_usuario = {self.id_usuario} "
                           f"and lig_bc_tp.id_tipoconta = 1 "
                           f"order by bc.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Banco.addItems(nova_lista)
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

    def lanca_combo_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            if banco:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                self.combo_Fatura.clear()
                self.combo_Consulta_Fatura.clear()
                nova_lista = [""]

                cursor = conecta.cursor()
                cursor.execute(f"""
                    SELECT fat.id, fat.mes, fat.ano 
                    FROM cadastro_fatura AS fat 
                    INNER JOIN saldo_banco AS sal_bc ON fat.id_saldo = sal_bc.id 
                    WHERE sal_bc.id_banco = {id_banco} 
                    AND fat.status = 'A' 
                    ORDER BY fat.ano, fat.mes;
                """)
                lista_completa = cursor.fetchall()

                for ides, mes, ano in lista_completa:
                    mes_formatado = str(mes).zfill(2)
                    dd = f"{ides} - {mes_formatado}/{ano}"
                    nova_lista.append(dd)

                if nova_lista:
                    self.combo_Fatura.addItems(nova_lista)
                    self.combo_Consulta_Fatura.addItems(nova_lista)

                    item_count = self.combo_Fatura.count()
                    for i in range(item_count):
                        item_text = self.combo_Fatura.itemText(i)
                        if dd in item_text:
                            self.combo_Fatura.setCurrentText(item_text)

                self.define_fatura_atual()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def define_fatura_atual(self):
        data_atual = datetime.now()

        fatura_atual = data_atual.strftime("%m/%Y")
        print(fatura_atual)

        item_count = self.combo_Fatura.count()
        for i in range(item_count):
            item_text = self.combo_Fatura.itemText(i)
            print(item_text)
            if fatura_atual in item_text:
                self.combo_Fatura.setCurrentText(item_text)

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

    def lanca_combo_categoria(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Categoria.clear()

            nova_lista = [""]

            grupo = self.combo_Grupo.currentText()
            if grupo:
                grupotete = grupo.find(" - ")
                id_grupo = grupo[:grupotete]

                cursor = conecta.cursor()
                cursor.execute(f'SELECT id, descricao FROM cadastro_categoria '
                               f'where id_grupo = {id_grupo} '
                               f'order by descricao;')
                lista_completa = cursor.fetchall()
                for ides, descr in lista_completa:
                    dd = f"{ides} - {descr}"
                    nova_lista.append(dd)

                self.combo_Categoria.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_cidade(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Cidade.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_cidade order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Cidade.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_estabelecimento(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Estab.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_estabelecimento order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Estab.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def procura_por_banco_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Consulta_Banco.currentText()
            fatura = self.combo_Consulta_Fatura.currentText()
            if banco and fatura:
                banco_tete = banco.find(" - ")
                id_banco = banco[:banco_tete]

                fatura_tete = fatura.find(" - ")
                id_fatura = fatura[:fatura_tete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                               f"banc.descricao, gr.descricao, cat.descricao, "
                               f"mov.qtde_sai, "
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
                               f"WHERE cat.id_GRUPO NOT IN (1, 2, 14) "
                               f"and tip.id = 1 "
                               f"and banc.id = {id_banco}  "
                               f"and mov.id_fatura = {id_fatura} "
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

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.combo_Banco.setCurrentText("")
            self.combo_Fatura.setCurrentText("")
            self.combo_Grupo.setCurrentText("")
            self.combo_Consulta_Banco.setCurrentText("")
            self.combo_Categoria.setCurrentText("")
            self.combo_Estab.setCurrentText("")
            self.combo_Cidade.setCurrentText("")

            self.date_Emissao.setDate(QDate(2000, 1, 1))

            self.spin_Parcelas.setValue(1)

            self.line_Valor.clear()

            self.label_Saldo.clear()

            self.plain_Obs.clear()
            limpa_tabela(self.table_Lista)

            self.lanca_numero()
            self.lanca_combo_banco()
            self.lanca_combo_grupo()
            self.lanca_combo_estabelecimento()

            self.date_Emissao.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def eventFilter(self, source, event):
        try:
            if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                    event.buttons() == QtCore.Qt.LeftButton and
                    source is self.table_Lista.viewport()):
                item = self.table_Lista.currentItem()

                dados = extrair_tabela(self.table_Lista)
                selecao = dados[item.row()]
                data_string, banco, grupo, categoria, valor, estab, cidade, obs = selecao

                self.line_Valor.setText(valor)
                self.plain_Obs.setPlainText(obs)

                banco_count = self.combo_Banco.count()
                for banco_ in range(banco_count):
                    banco_text = self.combo_Banco.itemText(banco_)
                    if banco in banco_text:
                        self.combo_Banco.setCurrentText(banco_text)

                self.lanca_saldo_bc()

                grupo_count = self.combo_Grupo.count()
                for grupo_ in range(grupo_count):
                    grupo_text = self.combo_Grupo.itemText(grupo_)
                    if grupo in grupo_text:
                        self.combo_Grupo.setCurrentText(grupo_text)

                self.lanca_combo_categoria()

                categoria_count = self.combo_Categoria.count()
                for categoria_ in range(categoria_count):
                    categoria_text = self.combo_Categoria.itemText(categoria_)
                    if categoria in categoria_text:
                        self.combo_Categoria.setCurrentText(categoria_text)

                estab_count = self.combo_Estab.count()
                for estab_ in range(estab_count):
                    estab_text = self.combo_Estab.itemText(estab_)
                    if estab in estab_text:
                        self.combo_Estab.setCurrentText(estab_text)

                cidade_count = self.combo_Cidade.count()
                for cidade_ in range(cidade_count):
                    cidade_text = self.combo_Cidade.itemText(cidade_)
                    if cidade in cidade_text:
                        self.combo_Cidade.setCurrentText(cidade_text)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def verifica_salvamento(self):
        try:
            banco = self.combo_Banco.currentText()
            grupo = self.combo_Grupo.currentText()
            categoria = self.combo_Categoria.currentText()
            estab = self.combo_Estab.currentText()
            cidade = self.combo_Cidade.currentText()
            fatura = self.combo_Fatura.currentText()

            valor = self.line_Valor.text()

            parcelas = self.spin_Parcelas.value()

            data_emissao = self.date_Emissao.date()

            if data_emissao == QDate(2000, 1, 1):
                mensagem_alerta('O campo "Emissão" deve ser preenchido!')
                self.date_Emissao.setFocus()
            elif not banco:
                mensagem_alerta('O campo "Banco" não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not fatura:
                mensagem_alerta('O campo "Fatura" não pode estar vazio!')
                self.combo_Fatura.setCurrentText("")
                self.combo_Fatura.setFocus()
            elif not grupo:
                mensagem_alerta('O campo "Grupo" não pode estar vazio!')
                self.combo_Grupo.setCurrentText("")
                self.combo_Grupo.setFocus()
            elif not categoria:
                mensagem_alerta('O campo "Categoria" não pode estar vazio!')
                self.combo_Categoria.setCurrentText("")
                self.combo_Categoria.setFocus()
            elif not estab:
                mensagem_alerta('O campo "Estabelecimento" não pode estar vazio!')
                self.combo_Estab.setCurrentText("")
                self.combo_Estab.setFocus()
            elif not cidade:
                mensagem_alerta('O campo "Cidade" não pode estar vazio!')
                self.combo_Cidade.setCurrentText("")
                self.combo_Cidade.setFocus()
            elif not valor:
                mensagem_alerta('O campo "R$" não pode estar vazio!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif valor == "R$ 0,00":
                mensagem_alerta('O campo "R$" não pode ser igual a Zero!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif parcelas == 0:
                mensagem_alerta('O campo "Número de Parcelas" não pode ser igual a Zero!')
                self.spin_Parcelas.setFocus()
            else:
                self.confere_emissao_com_fatura()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def confere_emissao_com_fatura(self):
        try:
            fatura = self.combo_Fatura.currentText()
            faturatete = fatura.find(" - ")
            nome_fatura = fatura[faturatete + 3:]

            mes_str, ano_str = nome_fatura.split('/')
            mes = int(mes_str)
            ano = int(ano_str)

            data_fatura = QDate(ano, mes, 1)

            data_emissao = self.date_Emissao.date()

            if data_emissao.month() == data_fatura.month() and data_emissao.year() == data_fatura.year():
                self.criar_saldo()
            else:
                msg = "A Data de Emissão não confere com o mês da Fatura.\nDeseja continuar??"
                if pergunta_confirmacao(msg):
                    self.criar_saldo()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def criar_saldo(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            id_tipo = "1"

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

            self.verifica_numero_parcelas()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_numero_parcelas(self):
        conecta = conectar_banco_nuvem()
        try:
            parcelas = self.spin_Parcelas.value()

            if parcelas == 1:
                self.salvar_1_parcela()
            else:
                obs = self.plain_Obs.toPlainText()
                if not obs:
                    obs_maiusculo = ""
                else:
                    obs_sem_quebra = obs.replace('\n', ' ')
                    obs_maiusculo = obs_sem_quebra.upper()

                valor = self.line_Valor.text()
                valor_float = valores_para_float(valor)

                if not obs:
                    mensagem_alerta('O campo "Observação" não pode estar vazio!')
                    self.plain_Obs.setFocus()
                else:
                    cursor = conecta.cursor()
                    cursor.execute(f"INSERT INTO mov_parcela (DESCRICAO, VALOR, NUM_PARCELAS) "
                                   f"VALUES ('{obs_maiusculo}','{valor_float}', {parcelas});")

                    id_inserido = cursor.lastrowid
                    conecta.commit()

                    self.salvar_mais_parcelas(id_inserido)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_1_parcela(self):
        conecta = conectar_banco_nuvem()
        try:
            data_emissao = self.date_Emissao.date()
            data_mysql = data_emissao.toString("yyyy-MM-dd")

            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            fatura = self.combo_Fatura.currentText()
            faturatete = fatura.find(" - ")
            id_fatura = fatura[:faturatete]

            categoria = self.combo_Categoria.currentText()
            categoriatete = categoria.find(" - ")
            id_categoria = categoria[:categoriatete]

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab = estab[:estabtete]

            cidade = self.combo_Cidade.currentText()
            cidadetete = cidade.find(" - ")
            id_cidade = cidade[:cidadetete]

            valor = self.line_Valor.text()
            valor_float = valores_para_float(valor)

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_sem_quebra = obs.replace('\n', ' ')
                obs_maiusculo = obs_sem_quebra.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco} and "
                           f"id_tipoconta = 1;")
            saldo_conta = cursor.fetchall()
            id_saldo, saldo = saldo_conta[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, id_fatura, obs) '
                           f'values ("{data_mysql}", {id_saldo}, {id_categoria}, '
                           f'0, {valor_float}, {id_estab}, {id_cidade}, {id_fatura}, "{obs_maiusculo}");')

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

    def salvar_mais_parcelas(self, id_parcela):
        conecta = conectar_banco_nuvem()
        try:
            data_emissao = self.date_Emissao.date()
            data_mysql = data_emissao.toString("yyyy-MM-dd")

            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            fatura = self.combo_Fatura.currentText()
            faturatete = fatura.find(" - ")
            id_fatura = fatura[:faturatete]

            categoria = self.combo_Categoria.currentText()
            categoriatete = categoria.find(" - ")
            id_categoria = categoria[:categoriatete]

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab = estab[:estabtete]

            cidade = self.combo_Cidade.currentText()
            cidadetete = cidade.find(" - ")
            id_cidade = cidade[:cidadetete]

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_sem_quebra = obs.replace('\n', ' ')
                obs_maiusculo = obs_sem_quebra.upper()

            parcelas = self.spin_Parcelas.value()

            valor = self.line_Valor.text()
            valor_float = valores_para_float(valor)

            valor_primeira, valor_rest = self.calcula_valor_parcela(valor_float, parcelas)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco} and "
                           f"id_tipoconta = 1;")
            saldo_conta = cursor.fetchall()
            id_saldo, saldo = saldo_conta[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, id_fatura, id_parcela, obs) '
                           f'values ("{data_mysql}", {id_saldo}, {id_categoria}, '
                           f'0, {valor_primeira}, {id_estab}, {id_cidade}, {id_fatura}, {id_parcela}, '
                           f'"{obs_maiusculo}");')

            conecta.commit()

            dados_p_salvar = [data_mysql, id_categoria, valor_rest, id_estab, id_cidade, id_parcela, obs_maiusculo]

            self.salvar_outras_parcelas(id_fatura, parcelas, dados_p_salvar)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_outras_parcelas(self, id_fatura, parcelas, dados_finais):
        conecta = conectar_banco_nuvem()
        try:
            data_mysql, id_categoria, valor_float, id_estab, id_cidade, id_parcela, obs_maiusculo = dados_finais
            data_mysql = datetime.strptime(data_mysql, "%Y-%m-%d")

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, id_saldo, mes, ano FROM cadastro_fatura WHERE id = {id_fatura};")
            lista_completa = cursor.fetchall()
            id_fatiry, id_saldo, mes_fatura, ano_fatura = lista_completa[0]

            # Criando um objeto datetime para a fatura
            data_fatura = datetime(ano_fatura, mes_fatura, 1)

            for i in range(1, parcelas):
                dia_fatura = i + 1
                mes_fatura_proxima = (data_fatura + relativedelta(months=dia_fatura)).strftime("%m/%Y")
                proxima_data = (data_mysql + relativedelta(months=i)).strftime("%Y-%m-%d")

                cursor.execute(f"SELECT vencimento FROM saldo_banco WHERE id = {id_saldo};")
                dia_venc = cursor.fetchone()[0]

                # Gerando data de vencimento para a próxima fatura
                data_vencimento = datetime.strptime(f"{dia_venc:02d}/{mes_fatura_proxima}", "%d/%m/%Y").strftime(
                    "%Y-%m-%d")

                cursor.execute(f"SELECT id, mes, ano FROM cadastro_fatura "
                               f"WHERE id_saldo = {id_saldo} "
                               f"AND mes = {mes_fatura_proxima.split('/')[0]} "
                               f"AND ano = {mes_fatura_proxima.split('/')[1]};")
                dados_faturas = cursor.fetchall()

                if not dados_faturas:
                    cursor.execute(
                        f"INSERT INTO cadastro_fatura (id_saldo, mes, ano, vencimento, VALOR_FINAL, STATUS) "
                        f"VALUES ({id_saldo}, {mes_fatura_proxima.split('/')[0]}, {mes_fatura_proxima.split('/')[1]}, "
                        f"'{data_vencimento}', '0', 'A');")

                    id_inserido = cursor.lastrowid
                    conecta.commit()

                    cursor.execute(f'INSERT INTO movimentacao (data, id_saldo, '
                                   f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, id_fatura, '
                                   f'id_parcela, obs) '
                                   f'VALUES ("{proxima_data}", {id_saldo}, {id_categoria}, '
                                   f'0, {valor_float}, {id_estab}, {id_cidade}, {id_inserido}, {id_parcela}, '
                                   f'"{obs_maiusculo}");')

                else:
                    id_fatiura, mes_fatura, ano_fatura = dados_faturas[0]
                    cursor.execute(f'INSERT INTO movimentacao (data, id_saldo, '
                                   f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, id_fatura, '
                                   f'id_parcela, obs) '
                                   f'VALUES ("{proxima_data}", {id_saldo}, {id_categoria}, '
                                   f'0, {valor_float}, {id_estab}, {id_cidade}, {id_fatiura}, {id_parcela}, '
                                   f'"{obs_maiusculo}");')

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


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaDespCartao()
    tela.show()
    qt.exec_()
