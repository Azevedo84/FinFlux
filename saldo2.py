import sys
from forms.tela_verifica_saldo import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone, cor_fundo_tela
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from comandos.conversores import valores_para_float, float_para_moeda_reais, moeda_reais_para_float
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QColor
import inspect
import os
from datetime import datetime, timedelta
import calendar
import traceback


class TelaSaldos(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        cor_fundo_tela(self)
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Mov)
        layout_cabec_tab(self.table_Corrente)
        layout_cabec_tab(self.table_Top10Categorias)
        layout_cabec_tab(self.table_Top10Grupos)

        self.valor_pagamento = 2100
        self.valor_adiantamento = 1000

        self.categ_impostos = "103, 110, 158, 181"

        self.obter_saldo_atual()
        self.obter_saldo_investimentos()

        self.obter_receitas_total_atual()
        self.obter_despesas_total_atual()

        self.obter_saldo_conta_corrente()
        self.obter_top_dez_categorias()
        self.obter_top_dez_grupos()

        self.definir_movimentacao()

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

    def obter_receitas_total_atual(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"SELECT "
                           f"SUM(CASE WHEN id_categoria IN (1, 2, 3, 4, 5, 151) THEN qtde_ent ELSE 0 END) - "
                           f"SUM(CASE WHEN id_categoria IN ({self.categ_impostos}) THEN qtde_sai ELSE 0 END) AS saldo "
                           f"FROM movimentacao "
                           f"WHERE YEAR(data) = YEAR(CURDATE()) "
                           f"AND MONTH(data) = MONTH(CURDATE());")

            saldo = cursor.fetchone()[0]

            saldo_certo = float_para_moeda_reais(saldo)
            self.label_Receitas.setText(saldo_certo)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_despesas_total_atual(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"SELECT SUM(qtde_sai) AS total_despesas "
                           f"FROM movimentacao AS mov "
                           f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                           f"INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id "
                           f"WHERE YEAR(data) = YEAR(CURDATE()) "
                           f"AND MONTH(data) = MONTH(CURDATE()) "
                           f"AND gr.id NOT IN (1, 2, 14) "
                           f"AND cat.id NOT IN ({self.categ_impostos});")
            despesas_total = cursor.fetchone()[0] or 0

            saldo_certo = float_para_moeda_reais(despesas_total)
            self.label_Despesas.setText(saldo_certo)

            receitas = valores_para_float(self.label_Receitas.text())
            despesas = valores_para_float(despesas_total)

            saldo_mes = round((receitas - despesas), 2)
            saldo_mes = float_para_moeda_reais(saldo_mes)
            self.label_Resultado.setText(saldo_mes)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_saldo_atual(self):
        conecta = conectar_banco_nuvem()
        try:
            total = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id_banco, bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo > 0 "
                           f"AND sald.id_usuario = 1 "
                           f"AND (sald.id_tipoconta = 2 OR sald.id_tipoconta = 4) and sald.id_banco = 1 "
                           f"order by bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    id_banco, descr, saldo = i

                    saldo_float = valores_para_float(saldo)

                    total += saldo_float
            if total:
                total_arred = round(total, 2)
                saldo_certo = float_para_moeda_reais(total_arred)
                self.label_SaldoAtual.setText(saldo_certo)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_saldo_investimentos(self):
        conecta = conectar_banco_nuvem()
        try:
            lista_tabela = []

            total = 0
            total_sub = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id_banco, bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo <> 0 "
                           f"AND sald.id_tipoconta = 3;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    id_banco, descr, saldo = i

                    saldo_float = valores_para_float(saldo)

                    if id_banco != 10:
                        total_sub += saldo_float

                    total_arreds = round(saldo, 2)
                    saldo_certos = float_para_moeda_reais(total_arreds)

                    dados = (descr, saldo_certos)
                    lista_tabela.append(dados)

                    total += saldo_float
            if total:
                total_arred = round(total, 2)
                saldo_certo = float_para_moeda_reais(total_arred)
                self.label_Investimentos.setText(saldo_certo)

                self.label_S_Investi.setText(saldo_certo)

            if total_sub:
                total_arred_sub = round(total_sub, 2)
                saldo_certo_sub = float_para_moeda_reais(total_arred_sub)
                self.label_Sub.setText(saldo_certo_sub)

            if lista_tabela:
                lanca_tabela(self.table_Investimentos, lista_tabela)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def definir_movimentacao(self):
        conecta = conectar_banco_nuvem()
        try:
            saldo_atual = self.label_SaldoAtual.text()

            lista_final = []

            # Obtendo a data atual para a fatura
            data_atual = datetime.now()
            fatura_atual = data_atual.strftime("%m/%Y")
            # Obtendo o ano e mês atuais
            ano_atual = data_atual.year
            mes_atual = data_atual.month

            # --- Descobre o mês anterior ---
            if mes_atual == 1:  # se for janeiro, volta para dezembro do ano anterior
                mes_anterior = 12
                ano_anterior = ano_atual - 1
            else:
                mes_anterior = mes_atual - 1
                ano_anterior = ano_atual

            primeiro_dia_mes = datetime(ano_atual, mes_atual, 1)
            ultimo_dia_mes_numero = calendar.monthrange(ano_atual, mes_atual)[1]
            ultimo_dia_atual = datetime(ano_atual, mes_atual, ultimo_dia_mes_numero)

            # Formatando as datas para o formato 'YYYY-MM-DD'
            ini_atual = primeiro_dia_mes.strftime('%Y-%m-%d')
            fim_atual = ultimo_dia_atual.strftime('%Y-%m-%d')

            # Descobre o próximo mês e ano
            if data_atual.month == 12:  # se for dezembro
                prox_mes = 1
                ano = data_atual.year + 1
            else:
                prox_mes = data_atual.month + 1
                ano = data_atual.year

            ini_prox = datetime(ano, prox_mes, 1)
            ultimo_dia = calendar.monthrange(ano, prox_mes)[1]
            fim_prox = datetime(ano, prox_mes, ultimo_dia) + timedelta(days=1)  # fim exclusivo

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, mov.qtde_ent "
                           f"FROM movimentacao AS mov "
                           f"WHERE mov.DATA >= '{ini_atual}' "
                           f"AND mov.DATA < '{fim_atual}' "
                           f"AND (mov.id_categoria = 4 OR mov.id_categoria = 3);")
            lista_pagamentos_atual = cursor.fetchall()

            if not lista_pagamentos_atual:
                dados = (f"05/{mes_atual}/{ano_atual}", f"PAGAMENTO", self.valor_pagamento, "")
                lista_final.append(dados)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, mov.qtde_ent "
                           f"FROM movimentacao AS mov "
                           f"WHERE mov.DATA >= '{ini_atual}' "
                           f"AND mov.DATA < '{fim_atual}' "
                           f"and mov.id_categoria = 2;")
            lista_adiantamentos_atual = cursor.fetchall()

            if not lista_adiantamentos_atual:
                dados = (f"21/{mes_atual}/{ano_atual}", f"ADIANTAMENTO", self.valor_adiantamento, "")
                lista_final.append(dados)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, mov.qtde_sai "
                           f"FROM movimentacao AS mov "
                           f"WHERE mov.DATA >= '{ini_atual}' "
                           f"AND mov.DATA < '{fim_atual}' "
                           f"and mov.id_categoria = 180;")
            lista_curso_atual = cursor.fetchall()

            if not lista_curso_atual:
                dados = (f"06/{mes_atual}/{ano_atual}", "CURSO PÓS", "", 99)
                lista_final.append(dados)

            cursor = conecta.cursor()
            cursor.execute(f"""
                    SELECT mov.data, mov.qtde_ent
                    FROM movimentacao AS mov
                    WHERE mov.DATA >= '{ini_prox.strftime("%Y-%m-%d")}'
                      AND mov.DATA < '{fim_prox.strftime("%Y-%m-%d")}'
                      AND (mov.id_categoria = 3 OR mov.id_categoria = 4);
                """)
            lista_pagamentos_proximo_mes = cursor.fetchall()

            if not lista_pagamentos_proximo_mes:
                dados = (f"05/{mes_atual + 1}/{ano}", f"PAGAMENTO", self.valor_pagamento, "")
                lista_final.append(dados)

            cursor = conecta.cursor()
            cursor.execute(f"""
                        SELECT mov.data, mov.qtde_ent
                        FROM movimentacao AS mov
                        WHERE mov.DATA >= '{ini_prox.strftime("%Y-%m-%d")}'
                          AND mov.DATA < '{fim_prox.strftime("%Y-%m-%d")}'
                          AND (mov.id_categoria = 2);
                    """)
            lista_adiantamentos_proximo_mes = cursor.fetchall()

            if not lista_adiantamentos_proximo_mes:
                dados = (f"21/{mes_atual + 1}/{ano}", f"ADIANTAMENTO", self.valor_adiantamento, "")
                lista_final.append(dados)

            cursor = conecta.cursor()
            cursor.execute(f"SELECT mov.data, mov.qtde_sai "
                           f"FROM movimentacao AS mov "
                           f"WHERE mov.DATA >= '{ini_prox.strftime("%Y-%m-%d")}' "
                           f"AND mov.DATA < '{fim_prox.strftime("%Y-%m-%d")}' "
                           f"and mov.id_categoria = 180;")
            lista_curso_proximo_mes = cursor.fetchall()

            if not lista_curso_proximo_mes:
                dados = (f"06/{mes_atual + 1}/{ano}", "CURSO PÓS", "", 99)
                lista_final.append(dados)

            # Conectando ao banco de dados e obtendo os dados de saldo bancário
            cursor = conecta.cursor()
            cursor.execute(f"SELECT sald.id, bc.descricao "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.id_usuario = 1 "
                           f"AND sald.id_tipoconta = 1 "
                           f"ORDER BY bc.descricao;")
            dados_saldo = cursor.fetchall()
            # Processando os saldos e faturas
            if dados_saldo:
                for i in dados_saldo:
                    id_saldo, nome_banco = i

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                        SELECT f.id, f.mes, f.ano, DATE_FORMAT(f.vencimento, '%d/%m/%Y')
                        FROM cadastro_fatura f
                        WHERE f.mes = {mes_atual} 
                          AND f.ano = {ano_atual}
                          AND f.id_saldo = {id_saldo}
                          AND NOT EXISTS (
                              SELECT 1
                              FROM movimentacao m
                              WHERE m.id_fatura = f.id
                                AND m.id_categoria = 6  -- pagamento de cartão
                          );
                    """)
                    dados_faturas = cursor.fetchall()

                    if dados_faturas:
                        for ii in dados_faturas:
                            id_fatura, mes_fatura, ano_fatura, venc = ii

                            cursor = conecta.cursor()
                            cursor.execute(f"""
                                    SELECT COALESCE(SUM(qtde_sai), 0) AS total_saida
                                    FROM movimentacao
                                    WHERE id_fatura = {id_fatura}
                                      AND id_saldo = {id_saldo};
                                """)
                            total_saida = cursor.fetchone()[0]
                            if total_saida:
                                dados = (venc, f"FATURA {nome_banco}", "", total_saida)
                                lista_final.append(dados)

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                                            SELECT f.id, f.mes, f.ano, DATE_FORMAT(f.vencimento, '%d/%m/%Y')
                                            FROM cadastro_fatura f
                                            WHERE f.mes = {mes_anterior} 
                                              AND f.ano = {ano_anterior}
                                              AND f.id_saldo = {id_saldo}
                                              AND NOT EXISTS (
                                                  SELECT 1
                                                  FROM movimentacao m
                                                  WHERE m.id_fatura = f.id
                                                    AND m.id_categoria = 6  -- pagamento de cartão
                                              );
                                        """)
                    dados_faturas_anterior = cursor.fetchall()

                    if dados_faturas_anterior:
                        for iiy in dados_faturas_anterior:
                            id_fatura_ant, mes_fatura_ant, ano_fatura_ant, venc_ant = iiy

                            cursor = conecta.cursor()
                            cursor.execute(f"""
                                                        SELECT COALESCE(SUM(qtde_sai), 0) AS total_saida
                                                        FROM movimentacao
                                                        WHERE id_fatura = {id_fatura_ant}
                                                          AND id_saldo = {id_saldo};
                                                    """)
                            total_saida_ant = cursor.fetchone()[0]
                            if total_saida_ant:
                                dados = (venc_ant, f"FATURA {nome_banco}", "", total_saida_ant)
                                lista_final.append(dados)

                if lista_final:
                    def chave_ordenacao(itemz):
                        dataz, tipoz, entradaz, saidaz = itemz
                        data_convertida = datetime.strptime(dataz, "%d/%m/%Y") \
                            if isinstance(dataz, str) \
                            else dataz
                        prioridade = 0 \
                            if entradaz \
                            else 1
                        return data_convertida, prioridade

                    lista_final.sort(key=chave_ordenacao)

                    saldo = moeda_reais_para_float(saldo_atual)

                    lista_com_saldo = []
                    for item in lista_final:
                        data, tipo, entrada, saida = item

                        entrada = float(entrada) if entrada not in ("", None) else 0.0
                        saida = float(saida) if saida not in ("", None) else 0.0

                        saldo += entrada
                        saldo -= saida

                        saldo_arred = round(saldo, 2)

                        saldo_certo = float_para_moeda_reais(saldo_arred)

                        lista_com_saldo.append((data, tipo, entrada, saida, saldo_certo))

                        self.label_Saldo_Final.setText(saldo_certo)

                    # Agora lança na tabela
                    lanca_tabela(self.table_Mov, lista_com_saldo)
                    self.pintar_tabela_movimentos()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def pintar_tabela_movimentos(self):
        try:
            tabela = self.table_Mov
            extrai_tabela = extrair_tabela(tabela)

            cor_vermelho = "#ff0000"
            cor_branco = "rgb(255, 255, 255)"

            for index, itens in enumerate(extrai_tabela):
                data, tipo, entrada, saida, saldo_certo = itens

                saldo_float = valores_para_float(saldo_certo)

                if saldo_float < 3000:
                    tabela.item(index, 4).setBackground(QColor(cor_vermelho))
                    tabela.item(index, 4).setForeground(QColor(cor_branco))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def obter_saldo_conta_corrente(self):
        conecta = conectar_banco_nuvem()
        try:
            nova_lista = []
            total = 0

            cursor = conecta.cursor()
            cursor.execute(f"SELECT bc.descricao, sald.saldo "
                           f"FROM saldo_banco as sald "
                           f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                           f"WHERE sald.saldo <> 0 AND sald.id_usuario = 1 "
                           f"AND sald.id_tipoconta in (2, 4) AND sald.id_banco <> 26 "
                           f"order by bc.descricao;")
            dados_saldo = cursor.fetchall()

            if dados_saldo:
                for i in dados_saldo:
                    descr, saldo = i

                    saldo_reais = float_para_moeda_reais(saldo)

                    saldo_float = valores_para_float(saldo)

                    total += saldo_float

                    dados = (descr, saldo_reais)
                    nova_lista.append(dados)

            if nova_lista:
                lanca_tabela(self.table_Corrente, nova_lista)

            if total:
                total_arred = round(total, 2)
                total_arred = float_para_moeda_reais(total_arred)
                self.label_T_Corrente.setText(str(total_arred))

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_top_dez_categorias(self):
        conecta = conectar_banco_nuvem()
        try:
            nova_lista = []

            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT cat.descricao AS categoria,
                       SUM(mov.qtde_sai) AS total_categoria
                FROM movimentacao AS mov
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                WHERE YEAR(mov.data) = YEAR(CURDATE())
                  AND MONTH(mov.data) = MONTH(CURDATE())
                  AND gr.id NOT IN (1, 2, 14)
                  AND cat.id NOT IN ({self.categ_impostos})
                GROUP BY cat.descricao
                ORDER BY total_categoria DESC
                LIMIT 10;
            """)

            top10_categorias = cursor.fetchall()

            if top10_categorias:
                for i in top10_categorias:
                    categoria, valor = i

                    valor_reais = float_para_moeda_reais(valor)

                    dados = (categoria, valor_reais)
                    nova_lista.append(dados)

            if nova_lista:
                lanca_tabela(self.table_Top10Categorias, nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def obter_top_dez_grupos(self):
        conecta = conectar_banco_nuvem()
        try:
            nova_lista = []

            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT gr.descricao,
                       SUM(mov.qtde_sai) as total_grupo
                FROM movimentacao AS mov
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id
                WHERE YEAR(mov.data) = YEAR(CURDATE())
                  AND MONTH(mov.data) = MONTH(CURDATE())
                  AND gr.id NOT IN (1, 2, 14)
                  AND cat.id NOT IN ({self.categ_impostos})
                GROUP BY gr.descricao
                ORDER BY total_grupo DESC
                LIMIT 10;
            """)

            top10_grupos = cursor.fetchall()

            if top10_grupos:
                for i in top10_grupos:
                    grupo, valor = i

                    valor_reais = float_para_moeda_reais(valor)

                    dados = (grupo, valor_reais)
                    nova_lista.append(dados)

            if nova_lista:
                lanca_tabela(self.table_Top10Grupos, nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaSaldos()
    tela.show()
    qt.exec_()
