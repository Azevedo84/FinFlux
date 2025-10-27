import sys
from forms.tela_pag_cartao import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela, limpa_tabela
from comandos.conversores import valores_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
import inspect
import os
import traceback


class TelaPagaCartao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Lista)

        self.id_usuario = "1"

        self.combo_Estab.activated.connect(self.conecta_banco_lanca_fatura)
        self.combo_Fatura.activated.connect(self.lanca_saldo_bc)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)

        self.btn_Consultar.clicked.connect(self.procura_por_banco_fatura)
        self.combo_Consulta_Banco.activated.connect(self.lanca_combo_fatura_consulta)

        self.table_Lista.viewport().installEventFilter(self)

        self.layout_tabela()
        self.lanca_numero()
        self.lanca_combo_banco()
        self.lanca_combo_banco_consulta()
        self.lanca_combo_estabelecimento()

        self.date_Emissao.setFocus()

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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def conecta_banco_lanca_fatura(self):
        try:
            self.lanca_combo_fatura()
            self.lanca_saldo_bc()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_saldo_bc(self):
        conecta = conectar_banco_nuvem()
        try:
            estab = self.combo_Estab.currentText()
            fatura = self.combo_Fatura.currentText()

            saldo_anterior = 0

            if estab and fatura:
                faturatete = fatura.find(" - ")
                id_fatura = fatura[:faturatete]

                id_tipo = "1"

                cursor = conecta.cursor()
                cursor.execute(f"SELECT id_saldo, qtde_ent, qtde_sai FROM movimentacao "
                               f"where id_fatura = {id_fatura};")
                saldo_conta = cursor.fetchall()
                print(id_fatura, saldo_conta)

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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def layout_tabela(self):
        try:
            qwidget_table = self.table_Lista

            qwidget_table.setColumnWidth(0, 55)
            qwidget_table.setColumnWidth(1, 55)
            qwidget_table.setColumnWidth(2, 70)
            qwidget_table.setColumnWidth(3, 100)
            qwidget_table.setColumnWidth(4, 60)
            qwidget_table.setColumnWidth(5, 60)
            qwidget_table.setColumnWidth(6, 110)
            qwidget_table.setColumnWidth(7, 95)
            qwidget_table.setColumnWidth(8, 250)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_combo_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Banco.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.id, bc.descricao "
                           f"FROM liga_banco_usuario AS lig_bc_us "
                           f"left JOIN cadastro_banco as bc ON lig_bc_us.id_banco = bc.id "
                           f"INNER JOIN liga_banco_tipo AS lig_bc_tp ON lig_bc_tp.id_banco = bc.id "
                           f"where lig_bc_us.id_usuario = {self.id_usuario} "
                           f"and lig_bc_tp.id_tipoconta = 2 "
                           f"order by bc.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Banco.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            estab = self.combo_Estab.currentText()
            if estab:
                estabtete = estab.find(" - ")
                id_estab = estab[:estabtete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT bc.id, bc.descricao "
                               f"FROM cadastro_banco as bc "
                               f"WHERE bc.id_estab = {id_estab};")
                lista_completa1 = cursor.fetchall()
                if lista_completa1:
                    id_banco, nome_banco = lista_completa1[0]

                    banco = f"{id_banco} - {nome_banco}"

                    self.combo_Fatura.clear()
                    nova_lista = [""]

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT fat.id, fat.mes, fat.ano "
                                   f"FROM cadastro_fatura as fat "
                                   f"INNER JOIN saldo_banco AS sal_bc ON fat.id_saldo = sal_bc.id "
                                   f"WHERE sal_bc.id_banco = {id_banco} "
                                   f"AND fat.status = 'A' and fat.ID_MOV_PAG is NULL "
                                   f"ORDER BY fat.ano, fat.mes;")
                    lista_completa = cursor.fetchall()

                    for ides, mes, ano in lista_completa:
                        dd = f"{ides} - {mes}/{ano}"
                        nova_lista.append(dd)

                    self.combo_Fatura.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_banco_consulta(self):
        conecta = conectar_banco_nuvem()
        try:
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

            self.combo_Consulta_Banco.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_fatura_consulta(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Consulta_Banco.currentText()
            if banco:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                self.combo_Consulta_Fatura.clear()
                nova_lista = [""]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT fat.id, fat.mes, fat.ano "
                               f"FROM cadastro_fatura as fat "
                               f"INNER JOIN saldo_banco AS sal_bc ON fat.id_saldo = sal_bc.id "
                               f"WHERE sal_bc.id_banco = {id_banco} "
                               f"AND fat.status = 'A' and fat.ID_MOV_PAG is NULL "
                               f"ORDER BY fat.ano, fat.mes;")
                lista_completa = cursor.fetchall()

                for ides, mes, ano in lista_completa:
                    dd = f"{ides} - {mes}/{ano}"
                    nova_lista.append(dd)

                self.combo_Consulta_Fatura.addItems(nova_lista)

                item_count = self.combo_Consulta_Banco.count()
                for i in range(item_count):
                    item_text = self.combo_Consulta_Banco.itemText(i)
                    if banco in item_text:
                        self.combo_Consulta_Banco.setCurrentText(item_text)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_estabelecimento(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Estab.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT estab.id, estab.descricao "
                           f"FROM cadastro_banco as bc "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON bc.id_estab = estab.id "
                           f"order by estab.descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Estab.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def procura_por_banco_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            valor_total = 0

            banco = self.combo_Consulta_Banco.currentText()
            fatura = self.combo_Consulta_Fatura.currentText()
            if banco and fatura:
                banco_tete = banco.find(" - ")
                id_banco = banco[:banco_tete]

                fatura_tete = fatura.find(" - ")
                id_fatura = fatura[:fatura_tete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT valor_final, vencimento FROM cadastro_fatura "
                               f"where id = {id_fatura};")
                dados_faturas = cursor.fetchall()
                valor_final, venc = dados_faturas[0]

                self.line_Valor_Final.setText(str(valor_final))
                self.date_Vencimento.setDate(venc)

                cursor = conecta.cursor()
                cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                               f"banc.descricao, gr.descricao, cat.descricao, "
                               f"CASE WHEN mov.qtde_ent = 0 THEN '' ELSE mov.qtde_ent END AS qtde_ent, "
                               f"CASE WHEN mov.qtde_sai = 0 THEN '' ELSE mov.qtde_sai END AS qtde_sai, "
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
                               f"WHERE tip.id = 1 "
                               f"and banc.id = {id_banco}  "
                               f"and mov.id_fatura = {id_fatura} "
                               f"and user.id = {self.id_usuario} "
                               f"ORDER BY mov.data;")
                lista_completa = cursor.fetchall()

                if lista_completa:
                    for i in lista_completa:
                        valor_sai = valores_para_float(i[5])

                        valor_total += valor_sai

                    lanca_tabela(self.table_Lista, lista_completa)
                    self.table_Lista.scrollToBottom()

                self.line_Valor_Final.setText(str(valor_total))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.combo_Banco.setCurrentText("")
            self.combo_Fatura.setCurrentText("")
            self.combo_Consulta_Banco.setCurrentText("")
            self.combo_Estab.setCurrentText("")

            self.date_Emissao.setDate(QDate(2000, 1, 1))

            self.line_Valor.clear()

            self.label_Saldo.clear()

            self.plain_Obs.clear()
            limpa_tabela(self.table_Lista)

            self.layout_tabela()
            self.lanca_numero()
            self.lanca_combo_banco()
            self.lanca_combo_estabelecimento()

            self.date_Emissao.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def eventFilter(self, source, event):
        try:
            if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                    event.buttons() == QtCore.Qt.LeftButton and
                    source is self.table_Lista.viewport()):
                item = self.table_Lista.currentItem()

                dados = extrair_tabela(self.table_Lista)
                selecao = dados[item.row()]
                data_string, banco, tipo, grupo, categoria, valor, estab, cidade, obs = selecao

                self.line_Valor.setText(valor)
                self.plain_Obs.setPlainText(obs)

                banco_count = self.combo_Banco.count()
                for banco_ in range(banco_count):
                    banco_text = self.combo_Banco.itemText(banco_)
                    if banco in banco_text:
                        self.combo_Banco.setCurrentText(banco_text)

                self.lanca_saldo_bc()

                estab_count = self.combo_Estab.count()
                for estab_ in range(estab_count):
                    estab_text = self.combo_Estab.itemText(estab_)
                    if estab in estab_text:
                        self.combo_Estab.setCurrentText(estab_text)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def verifica_salvamento(self):
        try:
            banco = self.combo_Banco.currentText()
            estab = self.combo_Estab.currentText()
            fatura = self.combo_Fatura.currentText()

            valor = self.line_Valor.text()

            saldo = self.label_Saldo.text()

            data_emissao = self.date_Emissao.date()

            if data_emissao == QDate(2000, 1, 1):
                self.mensagem_alerta('O campo "Emissão" deve ser preenchido!')
                self.date_Emissao.setFocus()
            elif not banco:
                self.mensagem_alerta('O campo "Banco" não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not fatura:
                self.mensagem_alerta('O campo "Fatura" não pode estar vazio!')
                self.combo_Fatura.setCurrentText("")
                self.combo_Fatura.setFocus()
            elif not estab:
                self.mensagem_alerta('O campo "Estabelecimento" não pode estar vazio!')
                self.combo_Estab.setCurrentText("")
                self.combo_Estab.setFocus()
            elif not valor:
                self.mensagem_alerta('O campo "R$" não pode estar vazio!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif valor == "0":
                self.mensagem_alerta('O campo "R$" não pode ser igual a Zero!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif not saldo:
                self.mensagem_alerta('O campo "Saldo" não pode estar vazio!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif saldo == "0":
                self.mensagem_alerta('O campo "Saldo" não pode ser igual a Zero!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            else:
                valor_float = valores_para_float(valor)
                saldo_float = valores_para_float(saldo) * -1

                if valor_float == saldo_float:
                    self.salvar_dados()
                else:
                    self.mensagem_alerta('O valor não pode ser diferente do Saldo!')

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            data_emissao = self.date_Emissao.date()
            data_mysql = data_emissao.toString("yyyy-MM-dd")

            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco1 = banco[:bancotete]

            fatura = self.combo_Fatura.currentText()
            faturatete = fatura.find(" - ")
            id_fatura2 = fatura[:faturatete]

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab1 = estab[:estabtete]

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
                           f"where id_usuario = {self.id_usuario} "
                           f"and id_banco = {id_banco1} "
                           f"and id_tipoconta = 2;")
            saldo_conta1 = cursor.fetchall()
            id_saldo1, saldo1 = saldo_conta1[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                           f'values ("{data_mysql}", {id_saldo1}, 6, '
                           f'0, {valor_float}, {id_estab1}, 19, "{obs_maiusculo}");')

            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, id_estab '
                           f'FROM cadastro_banco '
                           f'where id_estab = {id_estab1};')
            lista_completa1 = cursor.fetchall()
            id_banco2 = lista_completa1[0][0]

            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, id_estab '
                           f'FROM cadastro_banco '
                           f'where id = {id_banco1};')
            lista_completa2 = cursor.fetchall()
            id_estab2 = lista_completa2[0][1]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco2} and "
                           f"id_tipoconta = 1;")
            saldo_conta2 = cursor.fetchall()

            id_saldo2, saldo2 = saldo_conta2[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, id_fatura, obs) '
                           f'values ("{data_mysql}", {id_saldo2}, 6, '
                           f'{valor_float}, 0, {id_estab2}, 19, {id_fatura2}, "{obs_maiusculo}");')

            conecta.commit()

            self.mensagem_alerta(f'A Movimentação foi criada com sucesso!')

            self.salvar_id_mov_na_fatura(data_mysql, id_saldo2, 6, id_estab2, id_fatura2, valor_float)
            self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_id_mov_na_fatura(self, data_mov, id_saldo, id_categoria, id_estab, id_fatura, valor_final):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, id_saldo FROM movimentacao "
                           f"where data = '{data_mov}' "
                           f"and id_saldo = {id_saldo} "
                           f"and id_categoria = {id_categoria} "
                           f"and id_estab = {id_estab} "
                           f"and id_fatura = {id_fatura};")
            saldo_conta1 = cursor.fetchall()
            print(saldo_conta1)
            id_mov, id_saldus = saldo_conta1[0]

            cursor = conecta.cursor()
            cursor.execute(f"UPDATE cadastro_fatura SET "
                           f"status = 'F', "
                           f"ID_MOV_PAG = {id_mov}, "
                           f"valor_final = '{valor_final}' "
                           f"where id = {id_fatura};")

            conecta.commit()

            self.mensagem_alerta(f'Fatura marcada como pago!')
            self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaPagaCartao()
    tela.show()
    qt.exec_()
