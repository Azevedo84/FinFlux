import sys
from forms.tela_cad_energia import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from banco_dados.consulta_padrao import lanca_numero
from comandos.telas import tamanho_aplicacao, icone, cor_fundo_tela
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_int, float_para_moeda_reais, valores_para_float
from comandos.lines import validador_inteiro
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from datetime import date
import inspect
import os
import traceback


class TelaCadastroEnergia(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        cor_fundo_tela(self)
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.processando = False

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)
        layout_cabec_tab(self.table_Lista_2)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.line_Valor_Consumo.editingFinished.connect(self.atualiza_mascara_consumo)
        self.line_Valor_Bandeira.editingFinished.connect(self.atualiza_mascara_bandeira)
        self.line_Valor_Outros.editingFinished.connect(self.atualiza_mascara_outro)

        self.line_Leitura_Anterior.editingFinished.connect(self.atualiza_kwh)
        self.line_Leitura_Atual.editingFinished.connect(self.atualiza_kwh)

        self.table_Lista.viewport().installEventFilter(self)

        try:
            lanca_numero("controle_energia", self.line_Num)
            self.data_emissao()
            self.obter_todos_dados()
            self.mov_sem_vinculo()
            self.line_Movimentacao.setFocus()

            validador_inteiro(self.line_Num)
            validador_inteiro(self.line_Movimentacao)
            validador_inteiro(self.line_Leitura_Anterior)
            validador_inteiro(self.line_Leitura_Atual)

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

    def mov_sem_vinculo(self):
        conecta = conectar_banco_nuvem()
        try:
            select_padrao = """SELECT mov.id, user.descricao, 
                               DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada,
                               banc.descricao AS banco, tip.descricao, mov.qtde_sai, IFNULL(mov.obs, '') AS obs
                                FROM movimentacao AS mov
                                INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                                INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id
                                INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id
                                INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id
                                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                                INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id
                                INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id
                                LEFT JOIN controle_energia AS energ 
                                       ON mov.id = energ.id_movimentacao
                                WHERE mov.id_categoria = 20
                                  AND mov.data >= '2024-04-30'
                                  AND energ.id_movimentacao IS NULL
                                ORDER BY mov.data; """
            cursor = conecta.cursor()
            cursor.execute(f"{select_padrao}")
            lista_completa = cursor.fetchall()

            if lista_completa:
                lanca_tabela(self.table_Lista_2, lista_completa)

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
            cursor.execute('SELECT energ.id, mov.data, energ.id_movimentacao, '
                           'energ.data_anterior, energ.leitura_anterior, '
                           'energ.data_atual, energ.leitura_atual, '
                           'energ.valor_consumo, energ.bandeira, '
                           'energ.valor_bandeira, energ.outras_taxas, COALESCE(energ.obs, "") '
                           'FROM controle_energia as energ '
                           'INNER JOIN movimentacao AS mov ON energ.id_movimentacao = mov.id '
                           'order by mov.data;')
            lista_completa = cursor.fetchall()

            if lista_completa:
                for i in lista_completa:
                    id_e, data, id_mov, dt_ant, leit_ant, dt_atual, leit_atual, rs_cons, band, rs_band, rs_out, obs = i

                    formato_brasileiro = "%d/%m/%Y"
                    datas = data.strftime(formato_brasileiro)

                    dt_ant = dt_ant.strftime(formato_brasileiro)
                    dt_atual = dt_atual.strftime(formato_brasileiro)

                    kwh = leit_atual - leit_ant

                    rs_cons = float_para_moeda_reais(rs_cons)

                    if rs_band:
                        rs_band_rs = float_para_moeda_reais(rs_band)
                    else:
                        rs_band_rs = ""

                    if rs_out:
                        rs_out_rs = float_para_moeda_reais(rs_out)
                    else:
                        rs_out_rs = ""

                    dados = (id_e, datas, id_mov, dt_ant, leit_ant, dt_atual, leit_atual, kwh, rs_cons,
                             band, rs_band_rs, rs_out_rs, obs)
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
            self.line_Leitura_Anterior.clear()
            self.line_Leitura_Atual.clear()
            self.line_Valor_Consumo.clear()
            self.line_Valor_Bandeira.clear()
            self.line_Valor_Outros.clear()
            self.plain_Obs.clear()

            self.table_Lista.setRowCount(0)
            self.table_Lista_2.setRowCount(0)

            self.combo_Bandeira.setCurrentIndex(0)

            self.date_Anterior.setDate(QDate(2000, 1, 1))
            self.date_Atual.setDate(QDate(2000, 1, 1))

            lanca_numero("controle_energia", self.line_Num)
            self.data_emissao()
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
                (id_e, datas, id_mov, dt_ant, leit_ant, dt_atual, leit_atual, kwh, rs_cons,
                 band, rs_band, rs_out, obs) = selecao

                if "-" in datas:
                    ano, mes, dia = map(int, datas.split('-'))
                else:
                    dia, mes, ano = map(int, datas.split('/'))

                data = QDate(ano, mes, dia)
                self.date_Emissao.setDate(data)

                if "-" in dt_ant:
                    ano, mes, dia = map(int, dt_ant.split('-'))
                else:
                    dia, mes, ano = map(int, dt_ant.split('/'))

                data1 = QDate(ano, mes, dia)
                self.date_Anterior.setDate(data1)

                if "-" in dt_atual:
                    ano, mes, dia = map(int, dt_atual.split('-'))
                else:
                    dia, mes, ano = map(int, dt_atual.split('/'))

                data2 = QDate(ano, mes, dia)
                self.date_Atual.setDate(data2)

                self.plain_Obs.setPlainText(obs)

                self.line_Num.setText(id_e)
                self.line_Movimentacao.setText(id_mov)

                self.line_Leitura_Anterior.setText(leit_ant)
                self.line_Leitura_Atual.setText(leit_atual)
                self.line_Valor_Consumo.setText(rs_cons)

                if rs_band:
                    print(rs_band)
                    self.line_Valor_Bandeira.setText(rs_band)

                if rs_out:
                    self.line_Valor_Outros.setText(rs_out)

                bandeira_count = self.combo_Bandeira.count()
                for bandeira_ in range(bandeira_count):
                    bandeira_text = self.combo_Bandeira.itemText(bandeira_)
                    if band in bandeira_text:
                        self.combo_Bandeira.setCurrentText(bandeira_text)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def atualiza_mascara_consumo(self):
        if not self.processando:
            try:
                self.processando = True

                valor = self.line_Valor_Consumo.text()

                if valor:
                    valor_final = float_para_moeda_reais(valores_para_float(valor))

                    self.line_Valor_Consumo.setText(valor_final)

                    self.combo_Bandeira.setFocus()

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def atualiza_mascara_bandeira(self):
        if not self.processando:
            try:
                self.processando = True

                valor = self.line_Valor_Bandeira.text()

                if valor:
                    valor_final = float_para_moeda_reais(valores_para_float(valor))

                    self.line_Valor_Bandeira.setText(valor_final)

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def atualiza_mascara_outro(self):
        if not self.processando:
            try:
                self.processando = True

                valor = self.line_Valor_Outros.text()

                if valor:
                    valor_final = float_para_moeda_reais(valores_para_float(valor))

                    self.line_Valor_Outros.setText(valor_final)

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def atualiza_kwh(self):
        if not self.processando:
            try:
                self.processando = True

                leitura_anterior = self.line_Leitura_Anterior.text()
                leitura_atual = self.line_Leitura_Atual.text()

                if leitura_anterior and leitura_atual:
                    leitura_anterior_int = valores_para_int(leitura_anterior)

                    leitura_atual_int = valores_para_int(leitura_atual)

                    saldo = leitura_atual_int - leitura_anterior_int

                    self.label_Kwh.setText(str(saldo))

            except Exception as e:
                nome_funcao = inspect.currentframe().f_code.co_name
                exc_traceback = sys.exc_info()[2]
                self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

            finally:
                self.processando = False

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            id_mov = self.line_Movimentacao.text()

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
                cursor.execute(f"SELECT * from controle_energia where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"DELETE from controle_energia where id = {codigo};")
                    conecta.commit()

                    self.mensagem_alerta(f'A Energia {codigo} foi excluída com sucesso!')
                    self.reiniciando_tela()

                else:
                    self.mensagem_alerta(f'O código {codigo} de Energia não existe!')
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

            data_anter = self.date_Anterior.date()
            data_atu = self.date_Atual.date()

            leitura_anterior = self.line_Leitura_Anterior.text()
            leitura_atual = self.line_Leitura_Atual.text()
            valor_consumo = self.line_Valor_Consumo.text()

            bandeira = self.combo_Bandeira.currentText()

            if not id_mov:
                self.mensagem_alerta('O campo "Mov.:" não pode estar vazio!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif id_mov == "0":
                self.mensagem_alerta('O campo "Mov.:" não pode ser "0"!')
                self.line_Movimentacao.clear()
                self.line_Movimentacao.setFocus()
            elif not leitura_anterior:
                self.mensagem_alerta('O campo "L. Anterior:" não pode estar vazio!')
                self.line_Leitura_Anterior.clear()
                self.line_Leitura_Anterior.setFocus()
            elif leitura_anterior == "0":
                self.mensagem_alerta('O campo "L. Anterior:" não pode ser "0"!')
                self.line_Leitura_Anterior.clear()
                self.line_Leitura_Anterior.setFocus()
            elif not leitura_atual:
                self.mensagem_alerta('O campo "L. Atual:" não pode estar vazio!')
                self.line_Leitura_Atual.clear()
                self.line_Leitura_Atual.setFocus()
            elif leitura_atual == "0":
                self.mensagem_alerta('O campo "L. Atual:" não pode ser "0"!')
                self.line_Leitura_Atual.clear()
                self.line_Leitura_Atual.setFocus()
            elif not valor_consumo:
                self.mensagem_alerta('O campo "R$ Consumo:" não pode estar vazio!')
                self.line_Valor_Consumo.clear()
                self.line_Valor_Consumo.setFocus()
            elif valor_consumo == "0":
                self.mensagem_alerta('O campo "R$ Consumo:" não pode ser "0"!')
                self.line_Valor_Consumo.clear()
                self.line_Valor_Consumo.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.reiniciando_tela()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.reiniciando_tela()
            elif not bandeira:
                self.mensagem_alerta('O campo "Bandeira:" não pode estar vazio!')
                self.combo_Bandeira.setFocus()
            elif not data_anter:
                self.mensagem_alerta('O campo "D. Anterior:" não pode estar vazio!')
                self.date_Anterior.setFocus()
            elif not data_atu:
                self.mensagem_alerta('O campo "D. Atual:" não pode estar vazio!')
                self.date_Atual.setFocus()
            else:
                self.salvar_dados()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def salvar_dados(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text().strip()
            id_mov = self.line_Movimentacao.text().strip()

            # tenta converter id/codigo para int quando fizer sentido, senão None
            codigo_val = int(codigo) if codigo.isdigit() else None
            id_mov_val = int(id_mov) if id_mov.isdigit() else None

            # datas (objetos date)
            data_anter = self.date_Anterior.date()
            data_anterior = data_anter.toPyDate() if data_anter.isValid() else None

            data_atu = self.date_Atual.date()
            data_atual = data_atu.toPyDate() if data_atu.isValid() else None

            # leituras/valores: só converte se houver texto
            leitura_anterior_txt = self.line_Leitura_Anterior.text().strip()
            leitura_anterior = valores_para_int(leitura_anterior_txt) if leitura_anterior_txt else None

            leitura_atual_txt = self.line_Leitura_Atual.text().strip()
            leitura_atual = valores_para_int(leitura_atual_txt) if leitura_atual_txt else None

            valor_consumo_txt = self.line_Valor_Consumo.text().strip()
            valor_consumo = valores_para_float(valor_consumo_txt) if valor_consumo_txt else None

            bandeira = self.combo_Bandeira.currentText() or None

            obs = self.plain_Obs.toPlainText().strip()
            obs_maiusculo = obs.upper() if obs else None

            rs_band_txt = self.line_Valor_Bandeira.text().strip()
            rs_band = valores_para_float(rs_band_txt) if rs_band_txt else None

            rs_outros_txt = self.line_Valor_Outros.text().strip()
            rs_outros = valores_para_float(rs_outros_txt) if rs_outros_txt else None

            cursor = conecta.cursor()

            # verificar existência (apenas se temos um id numérico)
            registro_id = None
            if codigo_val is not None:
                cursor.execute("SELECT 1 FROM controle_energia WHERE id = %s", (codigo_val,))
                registro_id = cursor.fetchone()

            if registro_id:
                sql = """
                    UPDATE controle_energia
                    SET id_movimentacao = %s,
                        data_anterior = %s,
                        leitura_anterior = %s,
                        data_atual = %s,
                        leitura_atual = %s,
                        valor_consumo = %s,
                        bandeira = %s,
                        valor_bandeira = %s,
                        outras_taxas = %s,
                        obs = %s
                    WHERE id = %s
                """
                valores = (id_mov_val, data_anterior, leitura_anterior, data_atual,
                           leitura_atual, valor_consumo, bandeira, rs_band, rs_outros,
                           obs_maiusculo, codigo_val)
                cursor.execute(sql, valores)
                self.mensagem_alerta(f'A Energia {codigo} foi alterada com sucesso!')
            else:
                sql = """
                    INSERT INTO controle_energia
                    (id_movimentacao, data_anterior, leitura_anterior,
                     data_atual, leitura_atual, valor_consumo, bandeira,
                     valor_bandeira, outras_taxas, obs)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (id_mov_val, data_anterior, leitura_anterior, data_atual,
                           leitura_atual, valor_consumo, bandeira, rs_band, rs_outros,
                           obs_maiusculo)
                cursor.execute(sql, valores)
                self.mensagem_alerta(f'A Energia {codigo} foi criada com sucesso!')

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
    tela = TelaCadastroEnergia()
    tela.show()
    qt.exec_()
