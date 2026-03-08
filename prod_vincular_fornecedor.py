import sys
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from forms.tela_prod_vincular_fornecedor import *
from banco_dados.controle_erros import grava_erro_banco
from comandos.tabelas import lanca_tabela, extrair_tabela
from comandos.telas import tamanho_aplicacao, icone
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import inspect
import os
import traceback

import socket
import getpass

from PyQt5.QtCore import QTimer


class TelaVincularProdutoFornecedor(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.processando = False

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.nome_computador = socket.gethostname()
        self.username = getpass.getuser()

        icone(self, "menu.png")
        tamanho_aplicacao(self)

        self.timer_busca = QTimer()
        self.timer_busca.setSingleShot(True)  # dispara uma vez só
        self.timer_busca.timeout.connect(self.buscar_produto)

        self.line_Filtro_Siger1.textChanged.connect(self.iniciar_timer_busca)

        self.combo_Fornecedor.activated.connect(self.lanca_produtos_fornecedor)

        self.table_Prod_Forn.viewport().installEventFilter(self)
        self.table_Prod_Nosso.viewport().installEventFilter(self)

        self.btn_Vincular.clicked.connect(self.confere_vinculo_para_vincular)

        self.btn_Desvincular.clicked.connect(self.confere_vinculo_para_desvincular)

        self.btn_limpar.clicked.connect(self.limpa_tudo)

        self.radio_SemVinculo.setChecked(True)
        self.radio_SemVinculo.clicked.connect(self.definir_radios)
        self.radio_Todos.clicked.connect(self.definir_radios)

        self.definir_combo_fornecedor()

    def pergunta_confirmacao(self, mensagem):
        try:
            confirmacao = QMessageBox()
            confirmacao.setIcon(QMessageBox.Question)
            confirmacao.setText(mensagem)
            confirmacao.setWindowTitle("Confirmação")

            sim_button = confirmacao.addButton("Sim", QMessageBox.YesRole)
            nao_button = confirmacao.addButton("Não", QMessageBox.NoRole)

            confirmacao.setDefaultButton(nao_button)

            confirmacao.exec_()

            if confirmacao.clickedButton() == sim_button:
                return True
            else:
                return False

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

    def limpa_tudo(self):
        try:
            self.limpa_tabelas()
            self.limpa_filtros()
            self.limpa_campos_selecionados()

            self.radio_SemVinculo.setChecked(True)

            self.definir_combo_fornecedor()

            self.lanca_produtos_fornecedor()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def definir_radios(self):
        try:
            self.definir_combo_fornecedor()

            self.lanca_produtos_fornecedor()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_campos_selecionados(self):
        try:
            self.line_cod_s.clear()
            self.line_descr_s.clear()
            self.line_um_s.clear()

            self.line_cod_f.clear()
            self.line_descr_f.clear()
            self.line_um_f.clear()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_tabelas(self):
        try:
            self.table_Prod_Nosso.setRowCount(0)

            self.table_Prod_Forn.setRowCount(0)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_filtros(self):
        try:
            self.line_Filtro_F1.clear()
            self.line_Filtro_Siger1.clear()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def reinicia_com_fornecedor_definido(self):
        try:
            self.limpa_tabelas()
            self.limpa_campos_selecionados()

            self.limpa_filtros()

            self.radio_SemVinculo.setChecked(True)

            self.definir_combo_fornecedor()

            self.lanca_produtos_fornecedor()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def eventFilter(self, sources, event):
        conecta = conectar_banco_nuvem()
        try:
            if (event.type() == QtCore.QEvent.MouseButtonDblClick and event.buttons() == QtCore.Qt.LeftButton
                    and sources is self.table_Prod_Forn.viewport()):
                item = self.table_Prod_Forn.currentItem()

                if item:
                    self.limpa_campos_selecionados()

                    dados_fornecedor = extrair_tabela(self.table_Prod_Forn)

                    item_selecionado_f = dados_fornecedor[item.row()]
                    cod_f, descr_f, um_f, codigo_nosso = item_selecionado_f

                    if codigo_nosso == "-":
                        self.line_descr_s.setText("PRODUTO NÃO VINCULADO")
                    else:
                        cur = conecta.cursor()
                        cur.execute("""
                                        SELECT id, descricao, um 
                                        FROM cadastro_produto_mercado
                                        WHERE id = %s
                                        """, (codigo_nosso,))
                        select_prod = cur.fetchall()
                        if select_prod:
                            cod_s, descr_s, um_s = select_prod[0]

                            self.line_cod_s.setText(str(cod_s))
                            self.line_descr_s.setText(descr_s)
                            self.line_um_s.setText(um_s)

                    self.line_cod_f.setText(cod_f)
                    self.line_descr_f.setText(descr_f)
                    self.line_um_f.setText(um_f)

            elif (event.type() == QtCore.QEvent.MouseButtonDblClick and event.buttons() == QtCore.Qt.LeftButton
                  and sources is self.table_Prod_Nosso.viewport()):
                item_s = self.table_Prod_Nosso.currentItem()
                if item_s:
                    cod_selecionado = self.line_cod_f.text()
                    if cod_selecionado:
                        dados_siger = extrair_tabela(self.table_Prod_Nosso)

                        item_selecionado_s = dados_siger[item_s.row()]
                        cod_s, descr_s, um_s = item_selecionado_s

                        self.line_cod_s.setText(cod_s)
                        self.line_descr_s.setText(descr_s)
                        self.line_um_s.setText(um_s)

            return super(QMainWindow, self).eventFilter(sources, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def normalizar_um(self, um):
        try:
            if not um:
                return ""

            um = um.strip().upper()

            equivalentes_unidade = ["UN", "PC", "PÇ", "PCA", "PCS", "BB", "PCT"]

            if um in equivalentes_unidade:
                return "UN"

            return um

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def iniciar_timer_busca(self):
        try:
            self.timer_busca.start(400)  # 400 ms (ajuste se quiser)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def buscar_produto(self):
        try:
            self.table_Prod_Nosso.setRowCount(0)

            texto = self.line_Filtro_Siger1.text().strip()

            if texto:
                if texto.isdigit():
                    produto = self.lanca_produtos_siger_por_cod(texto)
                    if not produto:
                        self.lanca_produtos_siger_por_descricao(texto)
                else:
                    self.lanca_produtos_siger_por_descricao(texto)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def definir_combo_fornecedor(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Fornecedor.clear()

            tabela = []

            branco = ""
            tabela.append(branco)

            cursor = conecta.cursor()

            sem_vinculo = self.radio_SemVinculo.isChecked()

            if sem_vinculo:
                sql = """
                SELECT DISTINCT pre.id_fornecedor, forn.descricao
                FROM compras_produto_forn as pre 
                INNER JOIN cadastro_fornecedor as forn ON pre.id_fornecedor = forn.id 
                where pre.ID_PROD_NOSSO is NULL
                """
            else:
                sql = """
                SELECT DISTINCT pre.id_fornecedor, forn.descricao
                FROM compras_produto_forn as pre 
                INNER JOIN cadastro_fornecedor as forn ON pre.id_fornecedor = forn.id 
                """

            cursor.execute(sql)
            ids_fornecedores = cursor.fetchall()

            if ids_fornecedores:
                for dadus in ids_fornecedores:
                    ides, razao = dadus
                    msg = f"{ides} - {razao}"
                    tabela.append(msg)

                self.combo_Fornecedor.addItems(tabela)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_produtos_fornecedor(self):
        conecta = conectar_banco_nuvem()
        try:
            self.limpa_tabelas()
            self.limpa_campos_selecionados()
            self.line_Filtro_Siger1.clear()

            fornecedor = self.combo_Fornecedor.currentText()

            if fornecedor:
                fornecedor_tete = fornecedor.find(" - ")
                id_fornecedor = fornecedor[:fornecedor_tete]

                sem_vinculo = self.radio_SemVinculo.isChecked()
                filtro = self.line_Filtro_F1.text().strip()

                sql = """
                      SELECT pre.COD_PROD, \
                             pre.DESCRICAO, \
                             pre.UM, \
                             COALESCE(pre.ID_PROD_NOSSO, '-')
                      FROM compras_produto_forn as pre
                      WHERE pre.ID_FORNECEDOR = %s \
                      """
                parametros = [id_fornecedor]

                # 🔹 Filtro sem vínculo
                if sem_vinculo:
                    sql += " AND pre.ID_PROD_NOSSO IS NULL"

                # 🔹 Filtro por texto
                if filtro:
                    sql += " AND pre.DESCRICAO LIKE ?"
                    parametros.append(f"%{filtro}%")

                sql += " order by pre.DESCRICAO"

                cur = conecta.cursor()
                cur.execute(sql, parametros)
                detalhes_produto = cur.fetchall()

                if detalhes_produto:
                    lanca_tabela(self.table_Prod_Forn, detalhes_produto)

                self.line_Filtro_Siger1.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_produtos_siger_por_cod(self, codigo):
        conecta = conectar_banco_nuvem()
        try:
            detalhes_limpos = []

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, descricao, um  "
                           f"FROM cadastro_produto_mercado where id = {codigo};")
            detalhes_produto = cursor.fetchall()

            if detalhes_produto:
                for produto in detalhes_produto:
                    codigo, descricao, unidade = produto

                    detalhes_limpos.append((codigo, descricao, unidade))

                lanca_tabela(self.table_Prod_Nosso, detalhes_limpos)

            return detalhes_limpos

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_produtos_siger_por_descricao(self, descricao):
        conecta = conectar_banco_nuvem()
        try:
            detalhes_limpos = []

            cursor = conecta.cursor()
            cursor.execute(
                "SELECT id, descricao, um "
                "FROM cadastro_produto_mercado WHERE UPPER(descricao) LIKE UPPER(%s) order by descricao",
                (f"%{descricao}%",)
            )
            detalhes_produto = cursor.fetchall()

            if detalhes_produto:
                for produto in detalhes_produto:
                    codigo, descricao, unidade = produto

                    detalhes_limpos.append((codigo, descricao, unidade))

                lanca_tabela(self.table_Prod_Nosso, detalhes_limpos)

            return detalhes_limpos

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def confere_vinculo_para_desvincular(self):
        try:
            cod_s = self.line_cod_s.text()
            cod_f = self.line_cod_f.text()
            fornecedor = self.combo_Fornecedor.currentText()

            if cod_s and cod_f and fornecedor:
                self.remover_vinculo(fornecedor)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def remover_vinculo(self, fornecedor):
        conecta = conectar_banco_nuvem()
        try:
            fornecedor_tete = fornecedor.find(" - ")
            id_fornecedor = fornecedor[:fornecedor_tete]

            cod_f = self.line_cod_f.text()

            cursor = conecta.cursor()
            cursor.execute("""
                           UPDATE compras_produto_forn
                           SET ID_PROD_NOSSO = NULL
                           WHERE ID_FORNECEDOR = %s
                             AND COD_PROD = %s
                           """, (id_fornecedor, cod_f))
            conecta.commit()

            self.mensagem_alerta("Produto desvinculado com sucesso!")

            self.reinicia_com_fornecedor_definido()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def confere_vinculo_para_vincular(self):
        try:
            cod_s = self.line_cod_s.text()
            cod_f = self.line_cod_f.text()
            fornecedor = self.combo_Fornecedor.currentText()

            if cod_s and cod_f and fornecedor:
                self.salvar_vinculo(fornecedor)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_vinculo(self, fornecedor):
        conecta = conectar_banco_nuvem()
        try:
            fornecedor_tete = fornecedor.find(" - ")
            id_fornecedor = fornecedor[:fornecedor_tete]

            cod_f = self.line_cod_f.text()

            cod_s = self.line_cod_s.text()

            cur = conecta.cursor()
            cur.execute("""
                        SELECT id, descricao
                        FROM cadastro_produto_mercado
                        WHERE id = %s
                        """, (cod_s,))

            select_prod = cur.fetchall()

            if select_prod:
                id_prod, descr_prod = select_prod[0]

                cursor = conecta.cursor()
                cursor.execute("""
                               UPDATE compras_produto_forn
                               SET ID_PROD_NOSSO = %s
                               WHERE ID_FORNECEDOR = %s
                                 AND COD_PROD = %s
                               """, (id_prod, id_fornecedor, cod_f))

                conecta.commit()

                self.mensagem_alerta("Produto vinculado com sucesso!")

                self.reinicia_com_fornecedor_definido()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()



if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaVincularProdutoFornecedor()
    tela.show()
    qt.exec_()
