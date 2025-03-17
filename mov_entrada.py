import sys
from forms.tela_mov_entrada import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_float
from comandos.telas import tamanho_aplicacao
from funcao_padrao import grava_erro_banco, trata_excecao, mensagem_alerta, limpa_tabela
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
import inspect
import os


class TelaEntrada(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Lista)

        self.id_usuario = "1"
        self.combo_Banco.activated.connect(self.lanca_combo_tipo)
        self.combo_Tipo.activated.connect(self.lanca_saldo_bc)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)

        self.combo_Consulta_Categoria.activated.connect(self.procura_por_categoria)

        self.table_Lista.viewport().installEventFilter(self)

        self.lanca_numero()
        self.lanca_combo_banco()
        self.lanca_combo_categoria()
        self.lanca_combo_estabelecimento()

        self.date_Emissao.setFocus()

    def lanca_saldo_bc(self):
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

                self.label_Saldo.setText(str(saldo_anterior))

                self.lanca_movimentacao(id_banco, id_tipo)

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

    def lanca_movimentacao(self, id_banco, id_tipo):
        conecta = conectar_banco_nuvem()
        try:
            limpa_tabela(self.table_Lista)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                           f"banc.descricao, tip.descricao, cat.descricao, mov.qtde_ent, "
                           f"estab.descricao, COALESCE(mov.obs, '') "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"WHERE user.id = {self.id_usuario} "
                           f"and tip.id = {id_tipo} "
                           f"and banc.id = {id_banco} "
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
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.id, bc.descricao "
                           f"FROM liga_banco_usuario AS lig_bc_us "
                           f"left JOIN cadastro_banco as bc ON lig_bc_us.id_banco = bc.id "
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

    def lanca_combo_categoria(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Categoria.clear()
            self.combo_Consulta_Categoria.clear()
            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao '
                           'FROM cadastro_categoria '
                           'where (id_grupo = 1 or id_grupo = 14) '
                           'order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Categoria.addItems(nova_lista)
            self.combo_Consulta_Categoria.addItems(nova_lista)

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

    def procura_por_categoria(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            tipo = self.combo_Tipo.currentText()
            categoria = self.combo_Consulta_Categoria.currentText()

            if banco and tipo and categoria:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                tipotete = tipo.find(" - ")
                id_tipo = tipo[:tipotete]

                limpa_tabela(self.table_Lista)

                tete = categoria.find(" - ")
                id_categoria = categoria[:tete]

                cursor = conecta.cursor()
                cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                               f"banc.descricao, tip.descricao, cat.descricao, mov.qtde_ent, "
                               f"estab.descricao, COALESCE(mov.obs, '') "
                               f"FROM movimentacao AS mov "
                               f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                               f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                               f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                               f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                               f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                               f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                               f"WHERE user.id = {self.id_usuario} "
                               f"and tip.id = {id_tipo} "
                               f"and banc.id = {id_banco} "
                               f"and cat.id = {id_categoria} "
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
            self.combo_Tipo.setCurrentText("")
            self.combo_Categoria.setCurrentText("")
            self.combo_Consulta_Categoria.setCurrentText("")
            self.combo_Estab.setCurrentText("")

            self.line_Valor.clear()

            self.label_Saldo.clear()

            self.plain_Obs.clear()
            self.table_Lista.setRowCount(0)

            self.date_Emissao.setDate(QDate(2000, 1, 1))

            self.lanca_numero()
            self.lanca_combo_banco()
            self.lanca_combo_categoria()
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
                data_string, banco, tipo, categoria, valor, estab, obs = selecao

                self.line_Valor.setText(valor)

                self.plain_Obs.setPlainText(obs)

                banco_count = self.combo_Banco.count()
                for banco_ in range(banco_count):
                    banco_text = self.combo_Banco.itemText(banco_)
                    if banco in banco_text:
                        self.combo_Banco.setCurrentText(banco_text)

                self.lanca_combo_tipo()

                tipo_count = self.combo_Tipo.count()
                for tipo_ in range(tipo_count):
                    tipo_text = self.combo_Tipo.itemText(tipo_)
                    if tipo in tipo_text:
                        self.combo_Tipo.setCurrentText(tipo_text)

                categoria_count = self.combo_Categoria.count()
                for categoria_ in range(categoria_count):
                    categoria_text = self.combo_Categoria.itemText(categoria_)
                    if categoria in categoria_text:
                        index = self.combo_Categoria.findText(categoria_text)
                        if index != -1:
                            self.combo_Categoria.setCurrentIndex(index)
                            break

                estab_count = self.combo_Estab.count()
                for estab_ in range(estab_count):
                    estab_text = self.combo_Estab.itemText(estab_)
                    if estab in estab_text:
                        self.combo_Estab.setCurrentText(estab_text)

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
            tipo = self.combo_Tipo.currentText()
            categoria = self.combo_Categoria.currentText()
            estab = self.combo_Estab.currentText()

            valor = self.line_Valor.text()

            data_emissao = self.date_Emissao.date()

            if data_emissao == QDate(2000, 1, 1):
                mensagem_alerta('O campo "Emissão" deve ser preenchido!')
                self.date_Emissao.setFocus()

            elif not banco:
                mensagem_alerta('O campo "Banco" não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not tipo:
                mensagem_alerta('O campo "Tipo de Conta" não pode estar vazio!')
                self.combo_Tipo.setCurrentText("")
                self.combo_Tipo.setFocus()
            elif not categoria:
                mensagem_alerta('O campo "Categoria" não pode estar vazio!')
                self.combo_Categoria.setCurrentText("")
                self.combo_Categoria.setFocus()
            elif not estab:
                mensagem_alerta('O campo "Estabelecimento" não pode estar vazio!')
                self.combo_Estab.setCurrentText("")
                self.combo_Estab.setFocus()
            elif not valor:
                mensagem_alerta('O campo "R$" não pode estar vazio!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            elif valor == "R$ 0,00":
                mensagem_alerta('O campo "R$" não pode ser igual a Zero!')
                self.line_Valor.clear()
                self.line_Valor.setFocus()
            else:
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

            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            tipo = self.combo_Tipo.currentText()
            tipotete = tipo.find(" - ")
            id_tipo = tipo[:tipotete]

            categoria = self.combo_Categoria.currentText()
            categoriatete = categoria.find(" - ")
            id_categoria = categoria[:categoriatete]

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab = estab[:estabtete]

            valor = self.line_Valor.text()
            valor_float = valores_para_float(valor)

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                           f"where id_usuario = {self.id_usuario} and "
                           f"id_banco = {id_banco} and "
                           f"id_tipoconta = {id_tipo};")
            saldo_conta = cursor.fetchall()
            id_saldo, saldo = saldo_conta[0]

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                           f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                           f'values ("{data_mysql}", {id_saldo}, {id_categoria}, '
                           f'{valor_float}, 0, {id_estab}, 19, "{obs_maiusculo}");')

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
    tela = TelaEntrada()
    tela.show()
    qt.exec_()
