import sys
from forms.tela_saldos import *
from conexao_nuvem import conectar_banco_nuvem
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.conversores import valores_para_float
from funcao_padrao import grava_erro_banco, trata_excecao
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
import inspect
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar


class TelaSaldos(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.definir_tamanho_aplicacao()

        self.id_usuario = "1"

        layout_cabec_tab(self.table_Corrente)
        layout_cabec_tab(self.table_Cartao_Anterior)
        layout_cabec_tab(self.table_Cartao_Atual)

        self.manipula_saldo_conta_corrente()
        self.manipula_saldo_dolar()
        self.manipula_fatura_anterior()

    def definir_tamanho_aplicacao(self):
        try:
            monitor = QDesktopWidget().screenGeometry()
            monitor_width = monitor.width()
            monitor_height = monitor.height()

            if monitor_width > 1365 and monitor_height > 809:
                print("primeiro")
                interface_width = 1100
                interface_height = 720

            elif monitor_width > 1365 and monitor_height > 767:
                print("segundo")
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

    def layout_tabela_corrente(self):
        try:
            qwidget_table = self.table_Corrente

            qwidget_table.setColumnWidth(0, 35)
            qwidget_table.setColumnWidth(1, 60)
            qwidget_table.setColumnWidth(2, 50)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def layout_tabela_fatura_anterior(self):
        try:
            qwidget_table = self.table_Cartao_Anterior

            qwidget_table.setColumnWidth(0, 55)
            qwidget_table.setColumnWidth(1, 70)
            qwidget_table.setColumnWidth(2, 50)
            qwidget_table.setColumnWidth(3, 90)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def layout_tabela_fatura_atual(self):
        try:
            qwidget_table = self.table_Cartao_Atual

            qwidget_table.setColumnWidth(0, 55)
            qwidget_table.setColumnWidth(1, 70)
            qwidget_table.setColumnWidth(2, 50)
            qwidget_table.setColumnWidth(3, 90)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

    def manipula_saldo_conta_corrente(self):
        conecta = conectar_banco_nuvem()
        try:
            total = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id_banco, bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo > 0 "
                           f"AND sald.id_usuario = {self.id_usuario} "
                           f"AND (sald.id_tipoconta = 2 OR sald.id_tipoconta = 4) "
                           f"order by bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    id_banco, descr, saldo = i

                    saldo_float = valores_para_float(saldo)

                    total += saldo_float

                lanca_tabela(self.table_Corrente, dados_saldo)

            if total:
                total_arred = round(total, 2)
                self.label_T_Corrente.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def manipula_saldo_dolar(self):
        conecta = conectar_banco_nuvem()
        try:
            total = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id_banco, bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo > 0 "
                           f"AND sald.id_usuario = {self.id_usuario} "
                           f"AND sald.id_tipoconta = 6 "
                           f"order by bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    id_banco, descr, saldo = i

                    saldo_float = valores_para_float(saldo)

                    total += saldo_float

                lanca_tabela(self.table_Dolar_2, dados_saldo)

            if total:
                total_arred = round(total, 2)
                self.label_T_Dolar_2.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def entradas(self, mes_atual, ini, fim):
        conecta = conectar_banco_nuvem()
        try:
            valor_ivania = 2400
            pagamento = 0
            adiantamento = 1100

            lista_previsao = [("ADIANTAMENTO", adiantamento), ("PAGAMENTO", pagamento), ("PART. IVANIA", valor_ivania)]

            nova_lista = []

            # 2 - ADIANTAMENTO
            # 4 - PAGAMENTO
            # 151 - PART. IVANIA

            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                           f"cat.descricao, mov.qtde_ent "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"WHERE mov.DATA >= '{ini}' "
                           f"AND mov.DATA < '{fim}' "
                           f"and cat.id in (2, 3, 4, 151) "
                           f"ORDER BY mov.data;")
            lista_pagamento = cursor.fetchall()

            part_ivania = 0
            pagamento = 0
            adiantamento = 0

            if lista_pagamento:
                for i in lista_pagamento:
                    data, categoria, valor = i

                    if "PAGAMENTO" in i:
                        pagamento += 1
                    if "PAG. FERIAS" in i:
                        pagamento += 1
                    if "PART. IVANIA" in i:
                        valor_float = valores_para_float(valor)
                        part_ivania += valor_float
                    if "ADIANTAMENTO" in i:
                        adiantamento += 1

            if not part_ivania:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "PART. IVANIA":
                        dados = (mes_atual, cat_prev, valor_prev)
                        nova_lista.append(dados)

            elif part_ivania <= valor_ivania:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "PART. IVANIA":
                        valor_float_prev = valores_para_float(valor_prev)

                        saldo = valor_float_prev - part_ivania
                        dados = (mes_atual, cat_prev, saldo)
                        nova_lista.append(dados)

            if not pagamento:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "PAGAMENTO":
                        dados = (mes_atual, cat_prev, valor_prev)
                        nova_lista.append(dados)

            if not adiantamento:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "ADIANTAMENTO":
                        dados = (mes_atual, cat_prev, valor_prev)
                        nova_lista.append(dados)

            return nova_lista

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def saidas(self, mes_atual, ini, fim):
        conecta = conectar_banco_nuvem()
        try:
            luz = 300
            aguas = 70

            lista_previsao = [("AGUA", aguas), ("ENERGIA", luz)]

            nova_lista = []

            # 19 - AGUA
            # 20 - ENERGIA

            cursor = conecta.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(mov.data, '%d/%m/%Y') AS data_formatada, "
                           f"cat.descricao, mov.qtde_sai "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                           f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                           f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                           f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                           f"WHERE mov.DATA >= '{ini}' "
                           f"AND mov.DATA < '{fim}' "
                           f"and cat.id in (19, 20) "
                           f"ORDER BY mov.data;")
            lista_pagamento = cursor.fetchall()

            agua = 0
            energia = 0

            if lista_pagamento:
                for i in lista_pagamento:
                    data, categoria, valor = i

                    if "AGUA" in i:
                        agua += 1

                    if "ENERGIA" in i:
                        energia += 1

            if not agua:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "AGUA":
                        dados = (mes_atual, cat_prev, valor_prev)
                        nova_lista.append(dados)

            if not energia:
                for prev in lista_previsao:
                    cat_prev, valor_prev = prev

                    if cat_prev == "ENERGIA":
                        dados = (mes_atual, cat_prev, valor_prev)
                        nova_lista.append(dados)

            return nova_lista

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def manipula_fatura_anterior(self):
        conecta = conectar_banco_nuvem()
        try:
            # Obtendo o ano e mês atuais
            ano_atual = datetime.now().year
            mes_atual = datetime.now().month

            # Calculando o primeiro e último dia do mês atual
            ultimo_dia = calendar.monthrange(ano_atual, mes_atual)[1]
            primeiro_dia = datetime(ano_atual, mes_atual, 1)
            ultimo_dia = datetime(ano_atual, mes_atual, ultimo_dia)

            # Formatando as datas para o formato 'YYYY-MM-DD'
            ini = primeiro_dia.strftime('%Y-%m-%d')
            fim = ultimo_dia.strftime('%Y-%m-%d')

            total = 0
            nova_tabela = []

            # Obtendo os saldos bancários do usuário
            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id_banco, bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo > 0 "
                           f"AND sald.id_usuario = {self.id_usuario} "
                           f"AND bc.id = 1 "
                           f"AND (sald.id_tipoconta = 2 OR sald.id_tipoconta = 4) "
                           f"ORDER BY bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                saldis = dados_saldo[0][2]
                saldo_99 = valores_para_float(saldis)
            else:
                saldo_99 = 0

            saldo_acumula = saldo_99

            # Processando a fatura do mês anterior
            data_atual = datetime.now()
            data_mes_anterior = data_atual - relativedelta(months=1)
            fatura_anterior_mes = data_mes_anterior.month
            fatura_anterior_ano = data_mes_anterior.year

            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id, bc.descricao "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.id_usuario = {self.id_usuario} "
                           f"AND sald.id_tipoconta = 1 "
                           f"ORDER BY bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    id_saldo, nome_banco = i

                    saldo_anterior = 0
                    venc = ""

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT id, mes, ano, DATE_FORMAT(vencimento, '%d/%m/%Y') "
                                   f"FROM cadastro_fatura "
                                   f"WHERE mes = {fatura_anterior_mes} "
                                   f"AND ano = {fatura_anterior_ano} "
                                   f"AND id_saldo = {id_saldo};")
                    dados_faturas = cursor.fetchall()

                    if dados_faturas:
                        for ii in dados_faturas:
                            id_fatura, mes_fatura, ano_fatura, venc = ii

                            cursor = conecta.cursor()
                            cursor.execute(f"SELECT data, id_saldo, qtde_ent, qtde_sai FROM movimentacao "
                                           f"WHERE id_fatura = {id_fatura};")
                            saldo_conta = cursor.fetchall()

                            if saldo_conta:
                                for iii in saldo_conta:
                                    data, id_saldo, qtde_ent, qtde_sai = iii

                                    qtde_ent_float = valores_para_float(qtde_ent)
                                    qtde_sai_float = valores_para_float(qtde_sai)

                                    saldo_anterior += qtde_ent_float
                                    saldo_anterior -= qtde_sai_float

                                saldo_arred = round(saldo_anterior, 2)

                    saldo_arred = round(saldo_anterior, 2)

                    if saldo_arred != 0.0:
                        saldo_posi = saldo_arred * -1
                        saldo_float = valores_para_float(saldo_posi)
                        total += saldo_float

                        dados = (f"{fatura_anterior_mes}/{fatura_anterior_ano}", nome_banco, saldo_posi, venc)
                        nova_tabela.append(dados)

            # Atualizando a tabela com os dados processados
            if nova_tabela:
                lanca_tabela(self.table_Cartao_Anterior, nova_tabela)

            # Exibindo o total final
            if total:
                total_arred = round(total, 2)
                self.label_T_Anterior.setText(str(total_arred))

            # Atualizando a fatura atual
            self.manipula_fatura_atual(saldo_acumula)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
            nome_arquivo = os.path.basename(nome_arquivo_com_caminho)
            trata_excecao(nome_funcao, str(e), nome_arquivo)
            grava_erro_banco(nome_funcao, e, nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def manipula_fatura_atual(self, saldo_acumula):
        conecta = conectar_banco_nuvem()
        try:
            # Obtendo o ano e mês atuais
            ano_atual = datetime.now().year
            mes_atual = datetime.now().month

            primeiro_dia_mes = datetime(ano_atual, mes_atual, 1)
            ultimo_dia_mes_numero = calendar.monthrange(ano_atual, mes_atual)[1]
            ultimo_dia_atual = datetime(ano_atual, mes_atual, ultimo_dia_mes_numero)

            # Formatando as datas para o formato 'YYYY-MM-DD'
            ini = primeiro_dia_mes.strftime('%Y-%m-%d')
            fim = ultimo_dia_atual.strftime('%Y-%m-%d')
            print(ini, fim)

            total = 0
            nova_tabela = []
            total_entrada = 0
            saldo_acumula = 0

            # Obtendo a data atual para a fatura
            data_atual = datetime.now()
            fatura_atual = data_atual.strftime("%m/%Y")

            # Conectando ao banco de dados e obtendo os dados de saldo bancário
            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id, bc.descricao "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.id_usuario = {self.id_usuario} "
                           f"AND sald.id_tipoconta = 1 "
                           f"ORDER BY bc.descricao;")
            dados_saldo = cursor.fetchall()

            # Processando os saldos e faturas
            if dados_saldo:
                for i in dados_saldo:
                    id_saldo, nome_banco = i

                    saldo_anterior = 0
                    venc = ""

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT id, mes, ano, DATE_FORMAT(vencimento, '%d/%m/%Y') "
                                   f"FROM cadastro_fatura "
                                   f"WHERE mes = {mes_atual} AND ano = {ano_atual} "
                                   f"AND id_saldo = {id_saldo};")
                    dados_faturas = cursor.fetchall()

                    if dados_faturas:
                        for ii in dados_faturas:
                            id_fatura, mes_fatura, ano_fatura, venc = ii

                            cursor = conecta.cursor()
                            cursor.execute(f"SELECT data, id_saldo, qtde_ent, qtde_sai FROM movimentacao "
                                           f"WHERE id_fatura = {id_fatura} "
                                           f"AND id_saldo = {id_saldo};")
                            saldo_conta = cursor.fetchall()

                            if saldo_conta:
                                for iii in saldo_conta:
                                    data, id_saldo, qtde_ent, qtde_sai = iii

                                    qtde_ent_float = valores_para_float(qtde_ent)
                                    qtde_sai_float = valores_para_float(qtde_sai)

                                    saldo_anterior += qtde_ent_float
                                    saldo_anterior -= qtde_sai_float
                            else:
                                saldo_anterior = 0.00

                    saldo_arred = round(saldo_anterior, 2)

                    if saldo_arred != 0.0:
                        saldo_posi = saldo_arred * -1

                        saldo_float = valores_para_float(saldo_posi)
                        total += saldo_float

                        dados = (fatura_atual, nome_banco, saldo_posi, venc)
                        nova_tabela.append(dados)

            # Atualizando a tabela de faturas
            if nova_tabela:
                lanca_tabela(self.table_Cartao_Atual, nova_tabela)

            # Exibindo o total final
            if total:
                total_arred = round(total, 2)
                self.label_T_Atual.setText(str(total_arred))

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
    tela = TelaSaldos()
    tela.show()
    qt.exec_()
