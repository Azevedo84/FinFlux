import sys
from forms.tela_mov_alteracao import *
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


class TelaAlterarMov(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "compras.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.id_usuario = "1"

        self.combo_Banco.activated.connect(self.lanca_combo_tipo)
        self.combo_Consulta_Banco.activated.connect(self.lanca_combo_consulta_tipo)

        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Alterar.clicked.connect(self.alterar_movimento)

        self.combo_Consulta_Tipo.activated.connect(self.verifica_movimentacao)

        self.table_Lista.viewport().installEventFilter(self)

        self.lanca_numero()
        self.lanca_combo_banco()
        self.lanca_combo_categoria()
        self.lanca_combo_consulta_banco()
        self.lanca_combo_estabelecimento()
        self.lanca_combo_cidade()

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

    def verifica_movimentacao(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Consulta_Banco.currentText()
            tipo = self.combo_Consulta_Tipo.currentText()

            if banco and tipo:
                self.limpa_dados()
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

                self.lanca_movimentacao(id_banco, id_tipo)

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

    def lanca_movimentacao(self, id_banco, id_tipo):
        conecta = conectar_banco_nuvem()
        try:
            limpa_tabela(self.table_Lista)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.id, DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                           f"banc.descricao, tip.descricao, cat.descricao, COALESCE(mov.qtde_ent, ''), "
                           f"COALESCE(mov.qtde_sai, ''), "
                           f"estab.descricao, cit.descricao, COALESCE(mov.obs, '') "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id "
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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_consulta_banco(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Consulta_Banco.clear()
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

            self.combo_Consulta_Banco.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_consulta_tipo(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Consulta_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            self.combo_Consulta_Tipo.clear()
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

            self.combo_Consulta_Tipo.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_categoria(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Categoria.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, descricao FROM cadastro_categoria '
                           f'order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Categoria.addItems(nova_lista)

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
            cursor.execute('SELECT id, descricao FROM cadastro_estabelecimento order by descricao;')
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
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.combo_Banco.setCurrentText("")
            self.combo_Tipo.setCurrentText("")
            self.combo_Categoria.setCurrentText("")
            self.combo_Consulta_Banco.setCurrentText("")
            self.combo_Consulta_Tipo.setCurrentText("")
            self.combo_Estab.setCurrentText("")
            self.combo_Cidade.setCurrentText("")
            self.combo_Fatura.setCurrentText("")

            self.line_Entrada.clear()
            self.line_Saida.clear()

            self.plain_Obs.clear()
            self.table_Lista.setRowCount(0)

            self.date_Emissao.setDate(QDate(2000, 1, 1))

            self.lanca_numero()
            self.lanca_combo_banco()
            self.lanca_combo_estabelecimento()

            self.date_Emissao.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_dados(self):
        try:
            self.line_Num.clear()
            self.combo_Banco.setCurrentText("")
            self.combo_Tipo.setCurrentText("")
            self.combo_Categoria.setCurrentText("")
            self.combo_Estab.setCurrentText("")

            self.line_Entrada.clear()
            self.line_Saida.clear()

            self.plain_Obs.clear()

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
                id_mov, data_string, banco, tipo, categoria, entrada, saida, estab, cidade, obs = selecao

                dia, mes, ano = map(int, data_string.split('/'))
                data = QDate(ano, mes, dia)
                self.date_Emissao.setDate(data)

                self.line_Entrada.setText(entrada)
                self.line_Saida.setText(saida)

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

                cidade_count = self.combo_Cidade.count()
                for cidade_ in range(cidade_count):
                    cidade_text = self.combo_Cidade.itemText(cidade_)
                    if cidade in cidade_text:
                        self.combo_Cidade.setCurrentText(cidade_text)

                self.line_Num.setText(f"{id_mov}")

                combo_tipo = self.combo_Consulta_Tipo.currentText()

                self.combo_Fatura.setCurrentText("")

                if "1 - CARTAO DE CREDITO" == combo_tipo:
                    self.lanca_combo_fatura(id_mov)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_combo_fatura(self, id_mov):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            if banco:
                bancotete = banco.find(" - ")
                id_banco = banco[:bancotete]

                self.combo_Fatura.clear()
                nova_lista = [""]

                cursor = conecta.cursor()
                cursor.execute(f"""
                    SELECT fat.id, fat.mes, fat.ano 
                    FROM cadastro_fatura AS fat 
                    INNER JOIN saldo_banco AS sal_bc ON fat.id_saldo = sal_bc.id 
                    WHERE sal_bc.id_banco = {id_banco} 
                    ORDER BY fat.ano, fat.mes;
                """)
                lista_completa = cursor.fetchall()

                for ides, mes, ano in lista_completa:
                    dd = f"{ides} - {mes}/{ano}"
                    nova_lista.append(dd)

                self.combo_Fatura.addItems(nova_lista)
                self.define_fatura_atual(id_mov)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def define_fatura_atual(self, id_mov):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                                SELECT mov.id_fatura, fat.mes, fat.ano  
                                FROM movimentacao mov 
                                INNER JOIN cadastro_fatura AS fat ON mov.id_fatura = fat.id 
                                WHERE mov.id = {id_mov};
                            """)
            lista_completa = cursor.fetchall()

            id_fatura, mes, ano = lista_completa[0]
            print("definido", lista_completa[0])

            msg = f"{mes}/{ano}"
            item_count = self.combo_Fatura.count()
            for i in range(item_count):
                item_text = self.combo_Fatura.itemText(i)
                if msg in item_text:
                    self.combo_Fatura.setCurrentText(item_text)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def alterar_movimento(self):
        try:
            id_mov = self.line_Num.text()
            banco = self.combo_Banco.currentText()
            tipo = self.combo_Tipo.currentText()
            categoria = self.combo_Categoria.currentText()
            estab = self.combo_Estab.currentText()
            cidade = self.combo_Cidade.currentText()

            entrada = self.line_Entrada.text()
            saida = self.line_Saida.text()

            data_emissao = self.date_Emissao.date()

            if not id_mov:
                self.mensagem_alerta('O campo "Código" não pode estar vazio!')
                self.line_Num.setFocus()
            elif data_emissao == QDate(2000, 1, 1):
                self.mensagem_alerta('O campo "Emissão" deve ser preenchido!')
                self.date_Emissao.setFocus()
            elif not banco:
                self.mensagem_alerta('O campo "Banco" não pode estar vazio!')
                self.combo_Banco.setCurrentText("")
                self.combo_Banco.setFocus()
            elif not tipo:
                self.mensagem_alerta('O campo "Tipo de Conta" não pode estar vazio!')
                self.combo_Tipo.setCurrentText("")
                self.combo_Tipo.setFocus()
            elif not categoria:
                self.mensagem_alerta('O campo "Categoria" não pode estar vazio!')
                self.combo_Categoria.setCurrentText("")
                self.combo_Categoria.setFocus()
            elif not estab:
                self.mensagem_alerta('O campo "Estabelecimento" não pode estar vazio!')
                self.combo_Estab.setCurrentText("")
                self.combo_Estab.setFocus()
            elif not cidade:
                self.mensagem_alerta('O campo "Cidade" não pode estar vazio!')
                self.combo_Cidade.setCurrentText("")
                self.combo_Cidade.setFocus()
            elif not entrada or not saida:
                self.mensagem_alerta('O campo "Entrada" ou "Saída" não pode estar vazio!')
                self.line_Entrada.clear()
                self.line_Entrada.setFocus()

                self.line_Saida.clear()
                self.line_Saida.setFocus()
            else:
                self.verifica_fatura()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def verifica_fatura(self):
        conecta = conectar_banco_nuvem()
        try:
            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = banco[:bancotete]

            tipo = self.combo_Tipo.currentText()
            tipotete = tipo.find(" - ")
            id_tipo = tipo[:tipotete]

            if id_tipo == "1":
                fatura = self.combo_Fatura.currentText()
                if fatura:
                    faturatete = fatura.find(" - ")
                    id_fatura = fatura[:faturatete]

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                    SELECT id, mes, ano  
                    FROM cadastro_fatura
                    WHERE id = {id_fatura};""")
                    dados_fatura = cursor.fetchall()

                    if dados_fatura:
                        self.verifica_saldo()
            else:
                self.verifica_saldo()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_saldo(self):
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
                self.mensagem_alerta("Este banco não possui cadastro deste tipo!")
            else:
                lista_diferenca = self.unifica_dados()

                if lista_diferenca:
                    if id_tipo == "1":
                        self.atualizar_dados_com_fatura(lista_diferenca)
                    else:
                        self.atualizar_dados(lista_diferenca)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def unifica_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            campos_atualizados = []

            id_mov = self.line_Num.text()

            data_emissao = self.date_Emissao.date()
            data_mysql = data_emissao.toPyDate()

            banco = self.combo_Banco.currentText()
            bancotete = banco.find(" - ")
            id_banco = int(banco[:bancotete])

            tipo = self.combo_Tipo.currentText()
            tipotete = tipo.find(" - ")
            id_tipo = int(tipo[:tipotete])

            categoria = self.combo_Categoria.currentText()
            categoriatete = categoria.find(" - ")
            id_categoria = int(categoria[:categoriatete])

            estab = self.combo_Estab.currentText()
            estabtete = estab.find(" - ")
            id_estab = int(estab[:estabtete])

            cidade = self.combo_Cidade.currentText()
            cidadetete = cidade.find(" - ")
            id_cidade = int(cidade[:cidadetete])

            entrada = self.line_Entrada.text()
            entrada_float = valores_para_float(entrada)

            saida = self.line_Saida.text()
            saida_float = valores_para_float(saida)

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, banc.id, tip.id, cat.id, mov.qtde_ent, "
                           f"mov.qtde_sai, estab.id, mov.id_cidade, mov.obs "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"WHERE mov.id = {id_mov};")
            lists = cursor.fetchall()

            if lists:
                data_bc, banco_bc, tipo_bc, cat_bc, entr_bc, said_bc, estab_bc, cidade_bc, obs_bc = lists[0]

                entrada_bc_float = valores_para_float(entr_bc)
                saida_bc_float = valores_para_float(said_bc)

                if data_bc != data_mysql:
                    campos_atualizados.append(f'data = "{data_mysql}"')
                if banco_bc != id_banco or tipo_bc != id_tipo:
                    cursor.execute(f"SELECT id FROM saldo_banco "
                                   f"WHERE id_usuario = {self.id_usuario} "
                                   f"and id_banco = {id_banco} "
                                   f"and id_tipoconta = {id_tipo};")
                    id_saldo = cursor.fetchone()[0]
                    campos_atualizados.append(f"id_saldo = {id_saldo}")
                if cat_bc != id_categoria:
                    campos_atualizados.append(f"id_categoria = {id_categoria}")
                if entrada_bc_float != entrada_float:
                    campos_atualizados.append(f"qtde_ent = {entrada_float}")
                if saida_bc_float != saida_float:
                    campos_atualizados.append(f"qtde_sai = {saida_float}")
                if estab_bc != id_estab:
                    campos_atualizados.append(f"id_estab = {id_estab}")
                if cidade_bc != id_cidade:
                    campos_atualizados.append(f"id_cidade = {id_cidade}")
                if obs_bc != obs_maiusculo:
                    campos_atualizados.append(f'obs = "{obs_maiusculo}"')

            if campos_atualizados:
                campos_update = ", ".join(campos_atualizados)

                return campos_update

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def atualizar_dados_com_fatura(self, campos_update):
        conecta = conectar_banco_nuvem()
        try:
            id_mov = self.line_Num.text()

            fatura = self.combo_Fatura.currentText()
            if fatura:
                faturatete = fatura.find(" - ")
                id_fatura = fatura[:faturatete]

                print("Atualizar dados com fatura", campos_update, id_fatura)

                cursor = conecta.cursor()
                cursor.execute(f"UPDATE movimentacao SET {campos_update} "
                               f"where id = {id_mov};")

                conecta.commit()

                self.mensagem_alerta(f'A movimentação {id_mov} foi alterada com sucesso!')

                self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def atualizar_dados(self, campos_update):
        conecta = conectar_banco_nuvem()
        try:
            id_mov = self.line_Num.text()

            print("Atualizar dados sem fatura", campos_update)

            cursor = conecta.cursor()
            cursor.execute(f"UPDATE movimentacao SET {campos_update} "
                           f"where id = {id_mov};")

            conecta.commit()

            self.mensagem_alerta(f'A movimentação {id_mov} foi alterada com sucesso!')

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
    tela = TelaAlterarMov()
    tela.show()
    qt.exec_()
