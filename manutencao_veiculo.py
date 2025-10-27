import sys
from forms.tela_manutencao_veiculo import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from banco_dados.consulta_padrao import lanca_numero
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


class TelaManutencaoVeiculo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "compras.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.processando = False

        validador_inteiro(self.line_Num)
        self.line_Num.editingFinished.connect(self.verifica_line_mov)

        self.line_Qtde.editingFinished.connect(self.verifica_line_qtde)
        self.line_Unit.editingFinished.connect(self.verifica_line_unit)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)

        self.btn_Excluir_Item.clicked.connect(self.excluir_item_con)

        self.btn_Consumir.clicked.connect(self.consumir_produto_tabela)

        self.definir_bloqueios()

        self.lanca_combo_produto()
        self.lanca_combo_veiculo()
        self.data_emissao()
        self.line_Num.setFocus()

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
            self.plain_Obs_Mov.setReadOnly(True)

            self.line_Manut.setReadOnly(True)

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

                    self.atualiza_valor_total()

                self.confere_valores()

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
                    id_prod, produto, um, qtde, unit, total, obs = i

                    dados = (id_prod, produto, um, qtde, unit, total, obs)
                    lista_nova.append(dados)

            id_mov = self.line_Num.text()
            id_manut = self.line_Manut.text()
            produto = self.combo_Produto.currentText()
            qtde = self.line_Qtde.text()
            unit = self.line_Unit.text()
            total = self.line_Total.text()

            if not id_manut:
                self.mensagem_alerta('O campo "Id Manut:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif id_manut == "0":
                self.mensagem_alerta('O campo "Id Manut:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            if not id_mov:
                self.mensagem_alerta('O campo "Id Mov:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif id_mov == "0":
                self.mensagem_alerta('O campo "Id Mov:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif not produto:
                self.mensagem_alerta('O campo "Produto:" não pode estar vazio!')
                self.combo_Produto.setFocus()
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

                produtotete = produto.find(" - ")
                id_produto = produto[:produtotete]

                # Pega o texto depois do " - "
                desc_um = produto[produtotete + 3:].strip()  # "CUCA KG"

                # Unidade de medida são os 2 últimos caracteres
                um = desc_um[-2:].strip()  # "KG"

                # Descrição é o restante sem a unidade
                descricao = desc_um[:-2].strip()  # "CUCA"

                obs = self.plain_Obs_Prod.toPlainText()
                if not obs:
                    obs_maiusculo = ""
                else:
                    obs_maiusculo = obs.upper()

                dados = (id_produto, descricao, um, qtde, unit_rs, total_rs, obs_maiusculo)

                lista_nova.append(dados)

            if lista_nova:
                lanca_tabela(self.table_Lista, lista_nova)
                self.atualiza_valor_total()
                self.limpa_dados_produto()

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

                if not num_mov:
                    self.mensagem_alerta('O campo "Id Mov.:" não pode estar vazio!')
                    self.line_Num.clear()
                    self.line_Num.setFocus()
                elif num_mov == "0":
                    self.mensagem_alerta('O campo "Id Mov.:" não pode ser "0"!')
                    self.line_Num.clear()
                    self.line_Num.setFocus()
                else:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * FROM movimentacao "
                                   f"WHERE id = {num_mov};")
                    lista_registro = cursor.fetchall()
                    if lista_registro:
                        cursor = conecta.cursor()
                        cursor.execute(f"SELECT * FROM movimentacao "
                                       f"WHERE id = {num_mov} and id_categoria in (55, 58, 60, 61);")
                        lista_completa = cursor.fetchall()
                        if lista_completa:
                            self.lanca_dados_mov()
                        else:
                            self.mensagem_alerta("Este Registro não se trata de uma despesa de mecânico!")
                            self.reiniciando_tela()
                    else:
                        self.mensagem_alerta("Este Registro de despesa não existe!")
                        self.reiniciando_tela()

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
                           f"banc.descricao, tip.descricao, mov.qtde_sai, parcela.valor, "
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
                           f"LEFT JOIN mov_parcela AS parcela ON mov.id_parcela = parcela.id "
                           f"WHERE mov.id = {num_mov};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                data, banco, tipo, valor_deps, valor_total, estab, cidade, obs = lista_completa[0]

                self.date_Emissao.setDate(data)

                if valor_total:
                    valor = valor_total
                else:
                    valor = valor_deps

                valores_br = float_para_moeda_reais(valor)

                self.line_Valor.setText(valores_br)

                self.line_Banco.setText(banco)
                self.line_Tipo.setText(tipo)
                self.line_Estab.setText(estab)
                self.line_Cidade.setText(cidade)
                self.plain_Obs_Mov.setPlainText(obs)

                self.lanca_dados_manut()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_dados_manut(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            id_mov = self.line_Num.text()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT manut.id, manut.id_veiculo, veic.modelo, manut.km_atual, manut.obs "
                           f"FROM manutencao_veiculo as manut "
                           f"INNER JOIN cadastro_veiculo AS veic ON manut.id_veiculo = veic.id "
                           f"WHERE manut.id_movimentacao = {id_mov};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                id_manut, id_veiculo, veiculo, km_atual, obs = lista_completa[0]

                dd = f"{id_veiculo} - {veiculo}"

                self.line_Manut.setText(str(id_manut))

                veiculo_count = self.combo_Veiculo.count()
                for veiculo_ in range(veiculo_count):
                    veiculo_text = self.combo_Veiculo.itemText(veiculo_)
                    if dd in veiculo_text:
                        self.combo_Veiculo.setCurrentText(veiculo_text)

                if km_atual:
                    self.line_KM.setText(str(km_atual))

                if obs:
                    self.plain_Obs_Manut.setPlainText(obs)

                self.lanca_produtos_manut()

                self.combo_Produto.setFocus()

            else:
                lanca_numero("manutencao_veiculo", self.line_Manut)
                self.combo_Veiculo.setFocus()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_produtos_manut(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            id_manut = self.line_Manut.text()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT prod.id, prod.descricao, prod.um, prod_manut.qtde, "
                           f"prod_manut.unit, prod_manut.obs "
                           f"FROM manutencao_veiculo_produto AS prod_manut "
                           f"INNER JOIN manutencao_veiculo AS manut ON prod_manut.id_manut = manut.id "
                           f"INNER JOIN cadastro_produto_veiculo AS prod ON prod_manut.id_produto = prod.id "
                           f"WHERE prod_manut.id_manut = {id_manut};")
            lista_completa = cursor.fetchall()
            if lista_completa:
                for i in lista_completa:
                    id_prod, produto, um, qtde, unit, obs = i

                    qtde_float = valores_para_float(qtde)
                    unit_float = valores_para_float(unit)

                    total = round(qtde_float * unit_float, 2)

                    qtde_virg = valores_para_virgula(qtde)

                    unit_moeda = float_para_moeda_reais(unit_float)
                    total_moeda = float_para_moeda_reais(total)

                    dados = (id_prod, produto, um, qtde_virg, unit_moeda, total_moeda, obs)
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
                    id_prod, produto, um, qtde, unit, total, obs = i

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
            self.limpa_dados_manut()
            self.limpa_dados_produto()

            self.data_emissao()
            self.lanca_combo_produto()
            self.lanca_combo_veiculo()
            self.line_Num.setFocus()

            self.table_Lista.setRowCount(0)

            self.label_Total.setText("")
            self.widget_Total.setStyleSheet(f"background-color: {widgets};")

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_dados_manut(self):
        try:
            self.combo_Veiculo.setCurrentText("")

            self.line_Manut.clear()
            self.line_KM.clear()
            self.plain_Obs_Manut.clear()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def limpa_dados_produto(self):
        try:
            self.combo_Produto.setCurrentText("")

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
            self.plain_Obs_Mov.clear()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_combo_produto(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Produto.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT id, descricao, um FROM cadastro_produto_veiculo order by descricao;")
            lista_completa = cursor.fetchall()
            for ides, descr, um in lista_completa:
                dd = f"{ides} - {descr} {um}"
                nova_lista.append(dd)

            self.combo_Produto.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_veiculo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Veiculo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute("SELECT id, modelo FROM cadastro_veiculo order by modelo;")
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Veiculo.addItems(nova_lista)

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
            id_manut = self.line_Manut.text()

            veiculo = self.combo_Veiculo.currentText()

            if not codigo:
                self.mensagem_alerta('O campo "Id Mov.:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Id Mov.:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            if not id_manut:
                self.mensagem_alerta('O campo "Id Manut.:" não pode estar vazio!')
                self.line_Manut.clear()
                lanca_numero("manutencao_veiculo", self.line_Manut)
                self.combo_Veiculo.setFocus()
            elif id_manut == "0":
                self.mensagem_alerta('O campo "Id Manut.:" não pode ser "0"!')
                self.line_Manut.clear()
                lanca_numero("manutencao_veiculo", self.line_Manut)
                self.combo_Veiculo.setFocus()
            elif not veiculo:
                self.mensagem_alerta('O campo "Veículo:" não pode estar vazio!')
                self.combo_Veiculo.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            num_mov = self.line_Num.text()

            id_manut = self.line_Manut.text()

            veiculo = self.combo_Veiculo.currentText()
            tete = veiculo.find(" - ")
            id_veiculo = veiculo[:tete]

            km_atual = self.line_KM.text() or None

            obs = self.plain_Obs_Manut.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from manutencao_veiculo where id = {id_manut};")
            registro_id = cursor.fetchall()

            if registro_id:
                if registro_id:
                    sql = """
                        UPDATE manutencao_veiculo SET 
                        id_movimentacao = %s, 
                        id_veiculo = %s, 
                        km_atual = %s, 
                        obs = %s 
                        where id = %s
                    """
                    valores = (num_mov, id_veiculo, km_atual, obs_maiusculo,
                               id_manut)
                    cursor.execute(sql, valores)
            else:
                sql = """
                        Insert into manutencao_veiculo 
                        (id_movimentacao, id_veiculo, km_atual, obs) 
                        values (%s, %s, %s, %s)
                        """
                valores = (num_mov, id_veiculo, km_atual, obs_maiusculo)
                cursor.execute(sql, valores)

            conecta.commit()
            self.salvar_dados_produtos()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def salvar_dados_produtos(self):
        conecta = conectar_banco_nuvem()
        try:
            id_manut = self.line_Manut.text()

            cursor = conecta.cursor()
            cursor.execute("""
                SELECT prod_manut.id_produto, prod.descricao, prod.um, prod_manut.qtde, 
                prod_manut.unit, (prod_manut.qtde * prod_manut.unit) as total, prod_manut.obs
                FROM manutencao_veiculo_produto as prod_manut
                INNER JOIN cadastro_produto_veiculo AS prod ON prod_manut.id_produto = prod.id 
                WHERE prod_manut.id_manut = %s;
            """, (id_manut,))
            dados_banco = cursor.fetchall()

            # Remove FOR inútil e já padroniza tipos
            banco_dict = {
                int(id_prod_b): (
                    valores_para_float(qtde_b),
                    valores_para_float(unit_b),
                    (obs_b.strip() if obs_b else "")
                )
                for id_prod_b, produto_b, um_b, qtde_b, unit_b, total_b, obs_b in dados_banco
            }

            # Extrai tabela e padroniza tipos
            dados_tabela = extrair_tabela(self.table_Lista) or []
            tabela_dict = {
                int(id_prod_t): (
                    valores_para_float(qtde_t),
                    valores_para_float(unit_t),
                    (obs_t.strip() if obs_t else "")
                )
                for id_prod_t, produto_t, um_t, qtde_t, unit_t, total_t, obs_t in dados_tabela
            }

            # INSERT → existe na tabela mas não existe no banco
            inserts = []
            for id_prod, values in tabela_dict.items():
                if id_prod not in banco_dict:
                    qtde, unit, obs = values
                    inserts.append((id_manut, id_prod, qtde, unit, obs))

            # UPDATE → existe nos dois, mas os valores mudaram
            updates = []
            for id_prod, values in tabela_dict.items():
                if id_prod in banco_dict and banco_dict[id_prod] != values:
                    qtde, unit, obs = values
                    updates.append((qtde, unit, obs, id_manut, id_prod))

            # DELETE → existe no banco mas não na tabela
            deletes = []
            for id_prod in banco_dict.keys():
                if id_prod not in tabela_dict:
                    deletes.append((id_manut, id_prod))

            # Executa operações
            cursor = conecta.cursor()

            # INSERT
            for id_manut, id_prod, qtde, unit, obs in inserts:
                cursor.execute("""
                    INSERT INTO manutencao_veiculo_produto (id_manut, id_produto, qtde, unit, obs)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_manut, id_prod, qtde, unit, obs))

            # UPDATE
            for qtde, unit, obs, id_manut, id_prod in updates:
                cursor.execute("""
                    UPDATE manutencao_veiculo_produto
                    SET qtde = %s, unit = %s, obs = %s
                    WHERE id_manut = %s AND id_produto = %s
                """, (qtde, unit, obs, id_manut, id_prod))

            # DELETE
            for id_manut, id_prod in deletes:
                cursor.execute("""
                    DELETE FROM manutencao_veiculo_produto
                    WHERE id_manut = %s AND id_produto = %s
                """, (id_manut, id_prod))

            conecta.commit()

            self.mensagem_alerta("Manutenção atualizada com sucesso!")
            self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conecta' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaManutencaoVeiculo()
    tela.show()
    qt.exec_()
