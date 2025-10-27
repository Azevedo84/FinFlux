import sys
from forms.tela_cad_abastecimento import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from banco_dados.consulta_padrao import lanca_numero
from comandos.telas import tamanho_aplicacao, icone, cor_fundo_tela
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_float, valores_para_virgula, float_para_moeda_reais
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from datetime import date
import inspect
import os
import traceback


class TelaCadastroAbastecimento(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        cor_fundo_tela(self)
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)
        layout_cabec_tab(self.table_Lista_2)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.table_Lista.viewport().installEventFilter(self)

        try:
            lanca_numero("controle_abastecimento", self.line_Num)
            self.data_emissao()
            self.lanca_combo_veiculo()
            self.obter_todos_dados()
            self.mov_sem_vinculo()
            self.line_Movimentacao.setFocus()

        except Exception as e:
            # Aqui você lida com a falha de conexão de forma mais amigável
            print("⚠️ Não foi possível conectar ao banco de dados.")
            print(f"Detalhe técnico: {e}")
            self.mensagem_alerta(
                f"Não foi possível conectar ao banco de dados.\n\n"
                f"Verifique sua internet ou o servidor.\n\nDetalhe: {e}")
            self.close()

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

    def data_emissao(self):
        try:
            data_hoje = date.today()
            self.date_Emissao.setDate(data_hoje)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def lanca_combo_veiculo(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Veiculo.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, modelo FROM cadastro_veiculo order by modelo;')
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

    def mov_sem_vinculo(self):
        conecta = conectar_banco_nuvem()
        try:
            select_padrao = """SELECT mov.id,
                               DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada,
                               banc.descricao AS banco,
                               gr.descricao AS grupo,
                               cat.descricao AS categoria,
                               CASE WHEN mov.qtde_ent = 0 THEN '' ELSE mov.qtde_ent END AS qtde_ent,
                               CASE WHEN mov.qtde_sai = 0 THEN '' ELSE mov.qtde_sai END AS qtde_sai,
                               estab.descricao AS estabelecimento,
                               cit.descricao AS cidade,
                               mov.id_fatura,
                               IFNULL(mov.obs, '') AS obs
                                FROM movimentacao AS mov
                                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id
                                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id
                                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id
                                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id
                                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id
                                LEFT JOIN controle_abastecimento AS abast 
                                       ON mov.id = abast.id_movimentacao
                                WHERE mov.id_categoria = 51
                                  AND mov.data >= '2025-09-10'
                                  AND abast.id_movimentacao IS NULL
                                ORDER BY mov.data; """
            cursor = conecta.cursor()
            cursor.execute(f"{select_padrao}")
            lista_completa = cursor.fetchall()

            if lista_completa:
                lanca_tabela(self.table_Lista_2, lista_completa)
                self.table_Lista_2.scrollToBottom()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_todos_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            tabela_nova = []

            cursor = conecta.cursor()
            cursor.execute('SELECT abast.id, mov.data, abast.id_movimentacao, veic.modelo, abast.combustivel, '
                           'abast.KM_ATUAL, abast.LITROS, abast.VALOR_TOTAL, COALESCE(abast.obs, ""), '
                           'estab.descricao '
                           'FROM controle_abastecimento as abast '
                           'INNER JOIN cadastro_veiculo AS veic ON abast.id_veiculo = veic.id '
                           'INNER JOIN movimentacao AS mov ON abast.id_movimentacao = mov.id '
                           'INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id '
                           'order by abast.KM_ATUAL;')
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    id_abast, data, id_mov, modelo, combust, km, litros, total, obs, estab = i

                    formato_brasileiro = "%d/%m/%Y"
                    data_brasileira = data.strftime(formato_brasileiro)

                    litros_float = valores_para_float(litros)
                    total_float = valores_para_float(total)

                    unit_float = round(total_float / litros_float, 3)

                    litros_virg = valores_para_virgula(litros)

                    unit_moeda = float_para_moeda_reais(unit_float)
                    total_moeda = float_para_moeda_reais(total_float)

                    dados = (id_abast, data_brasileira, id_mov, modelo, combust, km, litros_virg, unit_moeda,
                             total_moeda, estab, obs)
                    tabela_nova.append(dados)

                lanca_tabela(self.table_Lista, tabela_nova)

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
            self.line_Movimentacao.clear()
            self.line_Km.clear()
            self.line_Litros.clear()
            self.plain_Obs.clear()

            self.table_Lista.setRowCount(0)
            self.table_Lista_2.setRowCount(0)

            self.combo_Veiculo.setCurrentIndex(0)
            self.combo_Combustivel.setCurrentIndex(0)

            lanca_numero("controle_abastecimento", self.line_Num)
            self.data_emissao()
            self.lanca_combo_veiculo()
            self.obter_todos_dados()
            self.mov_sem_vinculo()
            self.line_Movimentacao.setFocus()

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
                id_abast, data, id_mov, modelo, combust, km, litros, unit, total, estab, obs = selecao

                self.plain_Obs.setPlainText(obs)

                self.line_Num.setText(id_abast)
                self.line_Movimentacao.setText(id_mov)
                self.line_Km.setText(km)
                self.line_Litros.setText(litros)
                self.line_Total.setText(total)

                veiculo_count = self.combo_Veiculo.count()
                for veiculo_ in range(veiculo_count):
                    veiculo_text = self.combo_Veiculo.itemText(veiculo_)
                    if modelo in veiculo_text:
                        self.combo_Veiculo.setCurrentText(veiculo_text)

                combustivel_count = self.combo_Combustivel.count()
                for combustivel_ in range(combustivel_count):
                    combustivel_text = self.combo_Veiculo.itemText(combustivel_)
                    if combust in combustivel_text:
                        self.combo_Combustivel.setCurrentText(combustivel_text)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            id_mov = self.line_Movimentacao.text()
            km = self.line_Km.text()
            litros = self.line_Litros.text()
            total = self.line_Total.text()

            if not id_mov:
                self.mensagem_alerta('O campo "Mov.:" não pode estar vazio!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif id_mov == "0":
                self.mensagem_alerta('O campo "Mov.:" não pode ser "0"!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.reiniciando_tela()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.reiniciando_tela()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"SELECT * from controle_abastecimento where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"DELETE from controle_abastecimento where id = {codigo};")
                    conecta.commit()

                    self.mensagem_alerta(f'O Abastecimento {codigo} foi excluído com sucesso!')
                    self.reiniciando_tela()

                else:
                    self.mensagem_alerta(f'O código {codigo} de Abastecimento não existe!')
                    self.reiniciando_tela()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def verifica_salvamento(self):
        try:
            codigo = self.line_Num.text()
            id_mov = self.line_Movimentacao.text()
            km = self.line_Km.text()
            litros = self.line_Litros.text()
            total = self.line_Total.text()
            veiculo = self.combo_Veiculo.currentText()
            combust = self.combo_Combustivel.currentText()

            if not id_mov:
                self.mensagem_alerta('O campo "Mov.:" não pode estar vazio!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif id_mov == "0":
                self.mensagem_alerta('O campo "Mov.:" não pode ser "0"!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif not km:
                self.mensagem_alerta('O campo "KM:" não pode estar vazio!')
                self.line_Km.clear()
                self.line_Km.setFocus()
            elif km == "0":
                self.mensagem_alerta('O campo "KM:" não pode ser "0"!')
                self.line_Km.clear()
                self.line_Km.setFocus()
            elif not litros:
                self.mensagem_alerta('O campo "Litros:" não pode estar vazio!')
                self.line_Litros.clear()
                self.line_Litros.setFocus()
            elif litros == "0":
                self.mensagem_alerta('O campo "Litros:" não pode ser "0"!')
                self.line_Litros.clear()
                self.line_Litros.setFocus()
            elif not total:
                self.mensagem_alerta('O campo "Total:" não pode estar vazio!')
                self.line_Total.clear()
                self.line_Total.setFocus()
            elif total == "0":
                self.mensagem_alerta('O campo "Total:" não pode ser "0"!')
                self.line_Total.clear()
                self.line_Total.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.reiniciando_tela()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.reiniciando_tela()
            elif not veiculo:
                self.mensagem_alerta('O campo "Veículo:" não pode estar vazio!')
                self.combo_Veiculo.setFocus()
            elif not combust:
                self.mensagem_alerta('O campo "Combust.:" não pode estar vazio!')
                self.combo_Combustivel.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()

            id_mov = self.line_Movimentacao.text()

            km = self.line_Km.text()
            litros = self.line_Litros.text()
            litros_float = valores_para_float(litros)

            total = self.line_Total.text()
            total_float = valores_para_float(total)

            veiculo = self.combo_Veiculo.currentText()
            tete = veiculo.find(" - ")
            id_veiculo = veiculo[:tete]

            combust = self.combo_Combustivel.currentText()

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from controle_abastecimento where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE controle_abastecimento SET id_movimentacao = {id_mov}, "
                               f"id_veiculo = {id_veiculo}, combustivel = '{combust}', KM_ATUAL = '{km}', "
                               f"litros = '{litros_float}', valor_total = '{total_float}',  "
                               f"obs = '{obs_maiusculo}' "
                               f"where id = {codigo};")

                self.mensagem_alerta(f'O Abastecimento {codigo} foi alterado com sucesso!')
            else:
                cursor = conecta.cursor()
                cursor.execute(f'Insert into controle_abastecimento '
                               f'(id_movimentacao, id_veiculo, combustivel, KM_ATUAL, litros, valor_total, obs) '
                               f'values ({id_mov}, {id_veiculo}, "{combust}", "{km}", "{litros_float}", '
                               f'"{total_float}", "{obs_maiusculo}");')

                self.mensagem_alerta(f'O Abastecimento {codigo} foi criado com sucesso!')

            conecta.commit()
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
    tela = TelaCadastroAbastecimento()
    tela.show()
    qt.exec_()
