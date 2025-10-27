import sys
from forms.tela_nota_corretagem import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_float, valores_para_virgula, float_para_moeda_reais
from comandos.cores import cor_verde, cor_azul, cor_vermelho, widgets
from comandos.lines import validador_inteiro
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import date
import inspect
import os
import traceback


class TelaNotaCorretagem(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "compras.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.processando = False

        self.line_Num.setFocus()
        validador_inteiro(self.line_Num)
        self.line_Num.editingFinished.connect(self.verifica_line_mov)

        validador_inteiro(self.line_num_nota)

        self.line_Qtde.editingFinished.connect(self.verifica_line_qtde)
        self.line_Unit.editingFinished.connect(self.verifica_line_unit)

        self.line_Taxa_Liquidacao.editingFinished.connect(self.atualiza_mascara_taxa_liq)
        self.line_Emolumentos.editingFinished.connect(self.atualiza_mascara_emolumentos)
        self.line_Taxa_Transf.editingFinished.connect(self.atualiza_mascara_taxa_trans)
        self.line_Valor_Bruto.editingFinished.connect(self.atualiza_mascara_valor_bruto)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)

        self.btn_Excluir_Item.clicked.connect(self.excluir_item_con)

        self.btn_Consumir.clicked.connect(self.consumir_produto_tabela)

        self.definir_bloqueios()

        self.lanca_combo_ativo()
        self.data_emissao()

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

    def definir_bloqueios(self):
        try:
            self.date_Emissao.setReadOnly(True)
            self.line_Valor.setReadOnly(True)

            self.line_Banco.setReadOnly(True)
            self.line_Tipo.setReadOnly(True)
            self.line_Estab.setReadOnly(True)
            self.line_Cidade.setReadOnly(True)
            self.plain_Obs.setReadOnly(True)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def data_emissao(self):
        try:
            data_hoje = date.today()
            self.date_Emissao.setDate(data_hoje)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def excluir_item_con(self):
        try:
            table_name = self.table_Lista

            extrai_recomendados = extrair_tabela(table_name)
            if not extrai_recomendados:
                self.mensagem_alerta(f'A tabela está vazia!')
            else:
                linha_selecao = table_name.currentRow()
                if linha_selecao >= 0:
                    table_name.removeRow(linha_selecao)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def consumir_produto_tabela(self):
        try:
            lista_nova = []

            extrai_produtos = extrair_tabela(self.table_Lista)

            if extrai_produtos:
                for i in extrai_produtos:
                    id_nota, id_ativo, ativo, c_v, qtde, unit, total, obs = i

                    dados = (id_nota, id_ativo, ativo, c_v, qtde, unit, total, obs)
                    lista_nova.append(dados)

            codigo = self.line_Num.text()
            ativo = self.combo_Ativo.currentText()
            compra_venda = self.combo_C_V.currentText()
            mercado = self.combo_Mercado.currentText()
            qtde = self.line_Qtde.text()
            unit = self.line_Unit.text()
            total = self.line_Total.text()

            if not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif not ativo:
                self.mensagem_alerta('O campo "Ativo:" não pode estar vazio!')
                self.combo_Ativo.setFocus()
            elif not compra_venda:
                self.mensagem_alerta('O campo "C/V:" não pode estar vazio!')
                self.combo_Ativo.setFocus()
            elif not mercado:
                self.mensagem_alerta('O campo "Mercado:" não pode estar vazio!')
                self.combo_Ativo.setFocus()
            elif not qtde:
                self.mensagem_alerta('O campo "Quantidade:" não pode estar vazio!')
                self.line_Qtde.clear()
                self.line_Qtde.setFocus()
            elif qtde == "0":
                self.mensagem_alerta('O campo "Quantidade:" não pode ser "0"!')
                self.line_Qtde.clear()
                self.line_Qtde.setFocus()
            elif not unit:
                self.mensagem_alerta('O campo "R$ Und.:" não pode estar vazio!')
                self.line_Unit.clear()
                self.line_Unit.setFocus()
            elif unit == "0":
                self.mensagem_alerta('O campo "R$ Und.:" não pode ser "0"!')
                self.line_Unit.clear()
                self.line_Unit.setFocus()
            else:
                unit_rs = float_para_moeda_reais(valores_para_float(unit))
                total_rs = float_para_moeda_reais(valores_para_float(total))

                ativotete = ativo.find(" - ")
                id_ativo = ativo[:ativotete]

                # Descrição é o restante sem a unidade
                descricao = ativo[ativotete:]

                if compra_venda == "COMPRA":
                    c_v = "C"
                else:
                    c_v = "V"

                obs = self.plain_Obs_Prod.toPlainText()
                if not obs:
                    obs_maiusculo = ""
                else:
                    obs_maiusculo = obs.upper()

                dados = ("", id_ativo, descricao, c_v, qtde, unit_rs, total_rs, obs_maiusculo)

                lista_nova.append(dados)

            if lista_nova:
                lanca_tabela(self.table_Lista, lista_nova)
                self.atualiza_valor_total()
                self.limpa_dados_ativo()

            self.confere_valores()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def verifica_line_mov(self):
        if not self.processando:
            conecta = conectar_banco_nuvem()
            try:
                self.processando = True

                self.atualiza_valor_total()

                num_mov = self.line_Num.text()
                if num_mov:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * FROM movimentacao "
                                   f"WHERE id = {num_mov};")
                    lista_registro = cursor.fetchall()
                    if lista_registro:
                        cursor = conecta.cursor()
                        cursor.execute(f"SELECT * FROM movimentacao "
                                       f"WHERE id = {num_mov} and (id_categoria = 114 or id_categoria = 122);")
                        lista_completa = cursor.fetchall()
                        if lista_completa:
                            self.lanca_dados_mov()
                        else:
                            self.mensagem_alerta("Este Registro não se trata de uma despesa de mercado!")
                            self.reiniciando_tela()
                    else:
                        self.mensagem_alerta("Este Registro de despesa não existe!")
                        self.reiniciando_tela()
                else:
                    self.combo_Ativo.setFocus()

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                if 'conexao' in locals():
                    conecta.close()
                self.processando = False

    def lanca_dados_mov(self):
        conecta = conectar_banco_nuvem()
        try:
            self.limpa_dados_mov()

            num_mov = self.line_Num.text()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, "
                           f"banc.descricao, tip.descricao, mov.qtde_sai, "
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
                           f"WHERE mov.id = {num_mov};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                data, banco, tipo, valor, estab, cidade, obs = lista_completa[0]

                self.date_Emissao.setDate(data)

                valores_br = float_para_moeda_reais(valor)

                self.line_Valor.setText(valores_br)

                self.line_Banco.setText(banco)
                self.line_Tipo.setText(tipo)
                self.line_Estab.setText(estab)
                self.line_Cidade.setText(cidade)
                self.plain_Obs.setPlainText(obs)

                self.line_num_nota.setFocus()

                self.lanca_dados_nota()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_dados_nota(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            num_mov = self.line_Num.text()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, IFNULL(NUM_NOTA, ''), IFNULL(TAXA_LIQUIDACAO, ''), "
                           f"IFNULL(EMOLUMENTOS, ''), IFNULL(TAXA_TRANSF_ATIVO, ''), "
                           f"VALOR_BRUTO "
                           f"FROM nota_corretagem "
                           f"WHERE ID_MOVIMENTACAO = {num_mov};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                if len(lista_completa) > 1:
                    self.mensagem_alerta("Existem mais de uma nota vinculada ao movimento!")
                else:
                    id_nota, num_nota, taxa_liq, emolumentos, taxa_trans, bruto, obs = lista_completa[0]

                    self.line_Id_Nota.setText(id_nota)
                    self.line_num_nota.setText(num_nota)
                    self.line_Taxa_Liquidacao.setText(taxa_liq)
                    self.line_Emolumentos.setText(emolumentos)
                    self.line_Taxa_Transf.setText(taxa_trans)
                    self.line_Valor_Bruto.setText(bruto)

                    self.lanca_dados_ativos_tabela(id_nota)

                    self.combo_Ativo.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_dados_ativos_tabela(self, id_nota):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            num_mov = self.line_Num.text()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT nota.ID_NOTA_CORRETAGEM, NOTA.ID_ATIVO, ATIVO.TICKER, NOTA.COMPRA_VENDA, "
                           f"NOTA.QTDE, (NOTA.VALOR_TOTAL / NOTA.QTDE) as unit, NOTA.VALOR_TOTAL, NOTA.OBS "
                           f"FROM nota_ativos as nota "
                           f"INNER JOIN cadastro_ativo AS ativo ON nota.id_ativo = ativo.id "
                           f"WHERE nota.ID_NOTA_CORRETAGEM = {id_nota};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                for i in lista_completa:
                    id_nota, id_ativo, nome_ativo, c_v, qtde, unit, total, obs = i

                    qtde_float = valores_para_float(qtde)
                    unit_float = valores_para_float(unit)

                    total = round(qtde_float * unit_float, 2)

                    qtde_virg = valores_para_virgula(qtde)

                    unit_moeda = float_para_moeda_reais(unit_float)
                    total_moeda = float_para_moeda_reais(total)

                    dados = (id_nota, id_ativo, nome_ativo, c_v, qtde_virg, unit_moeda, total_moeda, obs)
                    tabela_nova.append(dados)

            if tabela_nova:
                lanca_tabela(self.table_Lista, tabela_nova)
                self.atualiza_valor_total()

            self.confere_valores()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def atualiza_valor_total(self):
        try:
            extrai_produtos = extrair_tabela(self.table_Lista)

            total_mercadorias = 0.00

            if extrai_produtos:
                for i in extrai_produtos:
                    id_nota, id_ativo, nome_ativo, c_v, qtde, unit, total, obs = i

                    total_float = valores_para_float(total)

                    total_mercadorias += total_float

            total_geral_2casas = ("%.2f" % total_mercadorias)
            valor_geral_string = valores_para_virgula(total_geral_2casas)
            valor_geral_final = "R$ " + valor_geral_string
            self.label_Total.setText(valor_geral_final)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def confere_valores(self):
        try:
            valor_produtos = self.label_Total.text()
            valor_produtos_float = valores_para_float(valor_produtos)

            valor_despesa = self.line_Valor.text()
            valor_despesa_float = valores_para_float(valor_despesa)

            if valor_despesa_float < valor_produtos_float:
                self.widget_Total.setStyleSheet(f"background-color: {cor_vermelho};")
            elif valor_despesa_float == valor_produtos_float:
                self.widget_Total.setStyleSheet(f"background-color: {cor_verde};")
            elif valor_despesa_float > valor_produtos_float:
                self.widget_Total.setStyleSheet(f"background-color: {cor_azul};")

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()

            self.limpa_dados_mov()
            self.limpa_dados_ativo()

            self.data_emissao()
            self.lanca_combo_ativo()
            self.line_Num.setFocus()

            self.widget_Total.setStyleSheet(f"background-color: {widgets};")

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_dados_ativo(self):
        try:
            self.combo_Ativo.setCurrentText("")
            self.combo_C_V.setCurrentText("")
            self.combo_Mercado.setCurrentText("")

            self.line_Qtde.clear()
            self.line_Unit.clear()
            self.line_Total.clear()

            self.plain_Obs_Prod.clear()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_dados_mov(self):
        try:
            self.line_Valor.clear()
            self.line_Banco.clear()
            self.line_Tipo.clear()
            self.line_Estab.clear()
            self.line_Cidade.clear()
            self.plain_Obs.clear()

            self.table_Lista.setRowCount(0)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_combo_ativo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Ativo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT id, TICKER FROM cadastro_ativo order by TICKER;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Ativo.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_line_qtde(self):
        if not self.processando:
            try:
                self.processando = True

                qtde = self.line_Qtde.text()

                if len(qtde) == 0:
                    self.mensagem_alerta('O campo "Qtde:" não pode estar vazio')
                    self.line_Qtde.clear()
                    self.line_Qtde.setFocus()
                elif qtde == "0":
                    self.mensagem_alerta('O campo "Qtde:" não pode ser "0"')
                    self.line_Qtde.clear()
                    self.line_Qtde.setFocus()
                else:
                    qtde_com_virgula = valores_para_virgula(qtde)

                    self.line_Qtde.setText(qtde_com_virgula)
                    self.atualiza_mascara_unit()
                    self.line_Unit.setFocus()

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def verifica_line_unit(self):
        if not self.processando:
            try:
                self.processando = True

                unit = self.line_Unit.text()

                if len(unit) == 0:
                    self.mensagem_alerta('O campo "R$/Unid:" não pode estar vazio')
                    self.line_Unit.clear()
                    self.line_Unit.setFocus()
                elif unit == "0":
                    self.mensagem_alerta('O campo "R$/Unid:" não pode ser "0"')
                    self.line_Unit.clear()
                    self.line_Unit.setFocus()
                else:
                    self.atualiza_mascara_unit()

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def atualiza_mascara_unit(self):
        try:
            unit = self.line_Unit.text()

            unit_float = valores_para_float(unit)
            unit_2casas = ("%.4f" % unit_float)
            valor_string = valores_para_virgula(unit_2casas)
            valor_final = "R$ " + valor_string
            self.line_Unit.setText(valor_final)

            self.calcular_valor_total_prod()
            self.plain_Obs_Prod.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def atualiza_mascara_taxa_liq(self):
        try:
            unit = self.line_Taxa_Liquidacao.text()

            if unit:
                unit_float = valores_para_float(unit)
                unit_2casas = ("%.2f" % unit_float)
                valor_string = valores_para_virgula(unit_2casas)
                valor_final = "R$ " + valor_string
                self.line_Taxa_Liquidacao.setText(valor_final)

            self.line_Emolumentos.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def atualiza_mascara_emolumentos(self):
        try:
            unit = self.line_Emolumentos.text()

            if unit:
                unit_float = valores_para_float(unit)
                unit_2casas = ("%.2f" % unit_float)
                valor_string = valores_para_virgula(unit_2casas)
                valor_final = "R$ " + valor_string
                self.line_Emolumentos.setText(valor_final)

            self.line_Taxa_Transf.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def atualiza_mascara_taxa_trans(self):
        try:
            unit = self.line_Taxa_Transf.text()

            if unit:
                unit_float = valores_para_float(unit)
                unit_2casas = ("%.2f" % unit_float)
                valor_string = valores_para_virgula(unit_2casas)
                valor_final = "R$ " + valor_string
                self.line_Taxa_Transf.setText(valor_final)

            self.line_Valor_Bruto.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def atualiza_mascara_valor_bruto(self):
        try:
            unit = self.line_Valor_Bruto.text()

            if unit:
                unit_float = valores_para_float(unit)
                unit_2casas = ("%.2f" % unit_float)
                valor_string = valores_para_virgula(unit_2casas)
                valor_final = "R$ " + valor_string
                self.line_Valor_Bruto.setText(valor_final)

            self.combo_Ativo.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def calcular_valor_total_prod(self):
        try:
            qtde = self.line_Qtde.text()
            unit = self.line_Unit.text()

            if qtde and unit:
                qtde_float = valores_para_float(qtde)

                unit_float = valores_para_float(unit)

                valor_total = qtde_float * unit_float

                total_2casas = ("%.2f" % valor_total)
                valor_string = valores_para_virgula(total_2casas)

                valor_final = "R$ " + valor_string
                self.line_Total.setText(valor_final)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def verifica_salvamento(self):
        try:
            codigo = self.line_Num.text()

            if not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            id_mov = self.line_Num.text().strip()



        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conecta' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaNotaCorretagem()
    tela.show()
    qt.exec_()
