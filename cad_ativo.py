import sys
from forms.tela_cad_ativo import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco
from comandos.telas import tamanho_aplicacao, icone, cor_fundo_tela
from comandos.tabelas import lanca_tabela, layout_cabec_tab, extrair_tabela
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore
from datetime import date
import inspect
import os
import traceback


class TelaAtivos(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        cor_fundo_tela(self)
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        layout_cabec_tab(self.table_Lista)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciando_tela)
        self.btn_Excluir.clicked.connect(self.excluir_cadastro)

        self.table_Lista.viewport().installEventFilter(self)

        try:
            self.lanca_numero()
            self.data_emissao()
            self.obter_todos_dados()

            self.lanca_combo_classe()
            self.lanca_combo_setor()
            self.lanca_combo_subsetor()
            self.lanca_combo_segmento()
            self.lanca_combo_seg_listagem()

        except Exception as e:
            # Aqui você lida com a falha de conexão de forma mais amigável
            print("⚠️ Não foi possível conectar ao banco de dados.")
            print(f"Detalhe técnico: {e}")
            self.mensagem_alerta(
                f"Não foi possível conectar ao banco de dados.\n\nVerifique sua internet ou o servidor.\n\n"
                f"Detalhe: {e}")
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

    def lanca_numero(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute("SELECT MAX(id) as id FROM cadastro_ativo;")
            dados = cursor.fetchall()
            num = dados[0][0]
            if not num:
                self.line_Num.setText("1")
                self.line_Ticker.setFocus()
            else:
                num = dados[0][0]
                num_plano_int = int(num) + 1
                num_plano_str = str(num_plano_int)
                self.line_Num.setText(num_plano_str)
                self.line_Ticker.setFocus()

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
            cursor.execute('SELECT ativo.id, ativo.criacao, ativo.ticker, ativo.EMPRESA_NOME, ativo.NOME_PREGAO, '
                           'ativo.CNPJ, '
                           'classe.descricao, setor.descricao, subsetor.descricao, segmento.descricao, '
                           'seg_list.descricao, COALESCE(ativo.obs, "") '
                           'FROM cadastro_ativo as ativo '
                           'INNER JOIN cadastro_classe_acao AS classe ON ativo.ID_CLASSE_ACAO = classe.id '
                           'INNER JOIN cadastro_setor_acao AS setor ON ativo.ID_SETOR = setor.id '
                           'INNER JOIN cadastro_subsetor_acao AS subsetor ON ativo.ID_SUBSETOR = subsetor.id '
                           'INNER JOIN cadastro_segmento_acao AS segmento ON ativo.ID_SEGMENTO = segmento.id '
                           'INNER JOIN cadastro_segmento_listagem AS seg_list ON ativo.ID_SEGMENTO_LISTAGEM	 = seg_list.id;')
            lista_completa = cursor.fetchall()

            dados_ordenados = sorted(lista_completa, key=lambda x: (x[2], x[3]))

            if lista_completa:
                for i in lista_completa:
                    id_empr, data, ticker, empresa, n_pregao, cnpj, classe, setor, subsetor, segm, seg_lista, obs = i

                    formato_brasileiro = "%d/%m/%Y"
                    data_br = data.strftime(formato_brasileiro)

                    dados = (id_empr, data_br, ticker, empresa, n_pregao, cnpj, classe, setor, subsetor, segm, seg_lista, obs)
                    tabela_nova.append(dados)

                lanca_tabela(self.table_Lista, tabela_nova)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_classe(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Classe.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_classe_acao order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Classe.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_setor(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Setor.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_setor_acao order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Setor.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_subsetor(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Subsetor.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_subsetor_acao order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Subsetor.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_segmento(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Segmento.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_segmento_acao order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Segmento.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def lanca_combo_seg_listagem(self):
        conecta = conectar_banco_nuvem()
        try:
            self.combo_Seg_List.clear()

            nova_lista = [""]

            cursor = conecta.cursor()
            cursor.execute('SELECT id, descricao FROM cadastro_segmento_listagem order by descricao;')
            lista_completa = cursor.fetchall()
            for ides, descr in lista_completa:
                dd = f"{ides} - {descr}"
                nova_lista.append(dd)

            self.combo_Seg_List.addItems(nova_lista)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()

    def data_emissao(self):
        try:
            data_hoje = date.today()
            self.date_Emissao.setDate(data_hoje)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def reiniciando_tela(self):
        try:
            self.line_Num.clear()
            self.line_Ticker.clear()
            self.line_Nome_Completo.clear()
            self.line_Nome_Pregao.clear()
            self.line_CNPJ.clear()
            self.table_Lista.setRowCount(0)
            self.plain_Obs.clear()

            self.lanca_numero()
            self.data_emissao()
            self.obter_todos_dados()

            self.lanca_combo_classe()
            self.lanca_combo_setor()
            self.lanca_combo_subsetor()
            self.lanca_combo_segmento()
            self.lanca_combo_seg_listagem()

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
                id_empr, data_br, ticker, empresa, n_pregao, cnpj, classe, setor, subsetor, segm, seg_lista, obs = selecao

                item_count = self.combo_Classe.count()
                for i in range(item_count):
                    item_text = self.combo_Classe.itemText(i)
                    tete = item_text.find(" - ")
                    nome_classe = item_text[tete + 3:]
                    if classe == nome_classe:
                        self.combo_Classe.setCurrentText(item_text)

                item_count = self.combo_Setor.count()
                for i in range(item_count):
                    item_text = self.combo_Setor.itemText(i)
                    tete = item_text.find(" - ")
                    nome_setor = item_text[tete + 3:]
                    if setor == nome_setor:
                        self.combo_Setor.setCurrentText(item_text)

                item_count = self.combo_Subsetor.count()
                for i in range(item_count):
                    item_text = self.combo_Subsetor.itemText(i)
                    tete = item_text.find(" - ")
                    nome_subsetor = item_text[tete + 3:]
                    if subsetor == nome_subsetor:
                        self.combo_Subsetor.setCurrentText(item_text)

                item_count = self.combo_Segmento.count()
                for i in range(item_count):
                    item_text = self.combo_Segmento.itemText(i)
                    tete = item_text.find(" - ")
                    nome_segm = item_text[tete + 3:]
                    if segm == nome_segm:
                        self.combo_Segmento.setCurrentText(item_text)

                item_count = self.combo_Seg_List.count()
                for i in range(item_count):
                    item_text = self.combo_Seg_List.itemText(i)
                    tete = item_text.find(" - ")
                    nome_seg_lista = item_text[tete + 3:]
                    if seg_lista == nome_seg_lista:
                        self.combo_Seg_List.setCurrentText(item_text)

                self.line_Num.setText(id_empr)
                self.line_Ticker.setText(ticker)
                self.line_Nome_Completo.setText(empresa)
                self.line_Nome_Pregao.setText(n_pregao)
                self.line_CNPJ.setText(cnpj)
                self.plain_Obs.setPlainText(obs)

            return super(QMainWindow, self).eventFilter(source, event)

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

    def excluir_cadastro(self):
        conecta = conectar_banco_nuvem()
        try:
            codigo = self.line_Num.text()
            ticker = self.line_Ticker.text()
            nome_completo = self.line_Nome_Completo.text()
            nome_pregao = self.line_Nome_Pregao.text()
            cnpj =self.line_CNPJ.text()
            classe = self.combo_Classe.currentText()
            setor = self.combo_Setor.currentText()
            subsetor = self.combo_Subsetor.currentText()
            segmento = self.combo_Segmento.currentText()
            seg_list = self.combo_Seg_List.currentText()

            if not nome_completo:
                self.mensagem_alerta('O campo "Nome Comp:" não pode estar vazio!')
                self.line_Nome_Completo.clear()
                self.line_Nome_Completo.setFocus()
            elif nome_completo == "0":
                self.mensagem_alerta('O campo "Nome Comp:" não pode ser "0"!')
                self.line_Nome_Completo.clear()
                self.line_Nome_Completo.setFocus()
            elif not ticker:
                self.mensagem_alerta('O campo "Ticker:" não pode estar vazio!')
                self.line_Ticker.clear()
                self.line_Ticker.setFocus()
            elif ticker == "0":
                self.mensagem_alerta('O campo "Ticker:" não pode ser "0"!')
                self.line_Ticker.clear()
                self.line_Ticker.setFocus()
            elif not nome_pregao:
                self.mensagem_alerta('O campo "Nome Preg:" não pode estar vazio!')
                self.line_Nome_Pregao.clear()
                self.line_Nome_Pregao.setFocus()
            elif nome_pregao == "0":
                self.mensagem_alerta('O campo "Nome Preg:" não pode ser "0"!')
                self.line_Nome_Pregao.clear()
                self.line_Nome_Pregao.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif not cnpj:
                self.mensagem_alerta('O campo "CNPJ:" não pode estar vazio!')
                self.line_CNPJ.clear()
                self.line_CNPJ.setFocus()
            elif cnpj == "0":
                self.mensagem_alerta('O campo "CNPJ:" não pode ser "0"!')
                self.line_CNPJ.clear()
                self.line_CNPJ.setFocus()
            elif not classe:
                self.mensagem_alerta('O campo "Classe Ação:" não pode estar vazio!')
                self.combo_Classe.setFocus()
            elif not setor:
                self.mensagem_alerta('O campo "Setor:" não pode estar vazio!')
                self.combo_Setor.setFocus()
            elif not subsetor:
                self.mensagem_alerta('O campo "Subsetor:" não pode estar vazio!')
                self.combo_Subsetor.setFocus()
            elif not segmento:
                self.mensagem_alerta('O campo "Segmento:" não pode estar vazio!')
                self.combo_Segmento.setFocus()
            elif not seg_list:
                self.mensagem_alerta('O campo "S. Listagem:" não pode estar vazio!')
                self.combo_Seg_List.setFocus()
            else:
                cursor = conecta.cursor()
                cursor.execute(f"SELECT * from cadastro_ativo where id = {codigo};")
                registro_id = cursor.fetchall()

                if registro_id:
                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT * from nota_ativos where id_ativo = {codigo};")
                    registro_operacoes = cursor.fetchall()

                    if registro_operacoes:
                        self.mensagem_alerta(f'O Ativo {nome_pregao} não pode ser excluído pois possui operações!')
                        self.reiniciando_tela()
                    else:
                        cursor = conecta.cursor()
                        cursor.execute(f"DELETE from cadastro_ativo where id = {codigo};")
                        conecta.commit()

                        self.mensagem_alerta(f'O Ativo {nome_pregao} foi excluída com sucesso!')
                        self.reiniciando_tela()

                else:
                    self.mensagem_alerta(f'O código {codigo} do Ativo não existe!')
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
            ticker = self.line_Ticker.text()
            nome_completo = self.line_Nome_Completo.text()
            nome_pregao = self.line_Nome_Pregao.text()
            cnpj = self.line_CNPJ.text()
            classe = self.combo_Classe.currentText()
            setor = self.combo_Setor.currentText()
            subsetor = self.combo_Subsetor.currentText()
            segmento = self.combo_Segmento.currentText()
            seg_list = self.combo_Seg_List.currentText()

            if not nome_completo:
                self.mensagem_alerta('O campo "Nome Comp:" não pode estar vazio!')
                self.line_Nome_Completo.clear()
                self.line_Nome_Completo.setFocus()
            elif nome_completo == "0":
                self.mensagem_alerta('O campo "Nome Comp:" não pode ser "0"!')
                self.line_Nome_Completo.clear()
                self.line_Nome_Completo.setFocus()
            elif not ticker:
                self.mensagem_alerta('O campo "Ticker:" não pode estar vazio!')
                self.line_Ticker.clear()
                self.line_Ticker.setFocus()
            elif ticker == "0":
                self.mensagem_alerta('O campo "Ticker:" não pode ser "0"!')
                self.line_Ticker.clear()
                self.line_Ticker.setFocus()
            elif not nome_pregao:
                self.mensagem_alerta('O campo "Nome Preg:" não pode estar vazio!')
                self.line_Nome_Pregao.clear()
                self.line_Nome_Pregao.setFocus()
            elif nome_pregao == "0":
                self.mensagem_alerta('O campo "Nome Preg:" não pode ser "0"!')
                self.line_Nome_Pregao.clear()
                self.line_Nome_Pregao.setFocus()
            elif not codigo:
                self.mensagem_alerta('O campo "Código:" não pode estar vazio!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif codigo == "0":
                self.mensagem_alerta('O campo "Código:" não pode ser "0"!')
                self.line_Num.clear()
                self.line_Num.setFocus()
            elif not cnpj:
                self.mensagem_alerta('O campo "CNPJ:" não pode estar vazio!')
                self.line_CNPJ.clear()
                self.line_CNPJ.setFocus()
            elif cnpj == "0":
                self.mensagem_alerta('O campo "CNPJ:" não pode ser "0"!')
                self.line_CNPJ.clear()
                self.line_CNPJ.setFocus()
            elif not classe:
                self.mensagem_alerta('O campo "Classe Ação:" não pode estar vazio!')
                self.combo_Classe.setFocus()
            elif not setor:
                self.mensagem_alerta('O campo "Setor:" não pode estar vazio!')
                self.combo_Setor.setFocus()
            elif not subsetor:
                self.mensagem_alerta('O campo "Subsetor:" não pode estar vazio!')
                self.combo_Subsetor.setFocus()
            elif not segmento:
                self.mensagem_alerta('O campo "Segmento:" não pode estar vazio!')
                self.combo_Segmento.setFocus()
            elif not seg_list:
                self.mensagem_alerta('O campo "S. Listagem:" não pode estar vazio!')
                self.combo_Seg_List.setFocus()
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
            ticker = self.line_Ticker.text()
            nome_pregao = self.line_Nome_Pregao.text()
            cnpj = self.line_CNPJ.text()

            nome_completo = self.line_Nome_Completo.text()
            nome_completo_m = nome_completo.upper()

            nome_pregao = self.line_Nome_Pregao.text()
            nome_pregao_m = nome_pregao.upper()

            ticker = self.line_Ticker.text()
            ticker_maiuscula = ticker.upper()

            obs = self.plain_Obs.toPlainText()
            if not obs:
                obs_maiusculo = ""
            else:
                obs_maiusculo = obs.upper()

            classe = self.combo_Classe.currentText()
            tete = classe.find(" - ")
            id_classe = classe[:tete]

            setor = self.combo_Setor.currentText()
            tete = setor.find(" - ")
            id_setor = setor[:tete]

            subsetor = self.combo_Subsetor.currentText()
            tete = subsetor.find(" - ")
            id_subsetor = subsetor[:tete]

            segmento = self.combo_Segmento.currentText()
            tete = segmento.find(" - ")
            id_segmento = segmento[:tete]

            seg_list = self.combo_Seg_List.currentText()
            tete = seg_list.find(" - ")
            id_seg_list = seg_list[:tete]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT * from cadastro_ativo where id = {codigo};")
            registro_id = cursor.fetchall()

            if registro_id:
                cursor = conecta.cursor()
                cursor.execute(f"UPDATE cadastro_ativo SET ticker = '{ticker_maiuscula}', "
                               f"EMPRESA_NOME = '{nome_completo_m}', NOME_PREGAO = '{nome_pregao_m}', "
                               f"CNPJ = '{cnpj}', ID_CLASSE_ACAO = {id_classe}, ID_SETOR = {id_setor}, "
                               f"ID_SUBSETOR = {id_subsetor}, ID_SEGMENTO = {id_segmento}, "
                               f"ID_SEGMENTO_LISTAGEM = {id_seg_list}, obs = '{obs_maiusculo}'"
                               f" where id = {codigo};")

                self.mensagem_alerta(f'O Ativo {ticker_maiuscula} foi alterado com sucesso!')
            else:
                cursor = conecta.cursor()
                cursor.execute(
                    'INSERT INTO cadastro_ativo (ticker, EMPRESA_NOME, NOME_PREGAO, CNPJ, ID_CLASSE_ACAO, '
                    'ID_SETOR, ID_SUBSETOR, ID_SEGMENTO, ID_SEGMENTO_LISTAGEM, obs) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (ticker_maiuscula, nome_completo_m, nome_pregao_m, cnpj, id_classe, id_setor, id_subsetor,
                     id_segmento, id_seg_list, obs_maiusculo)
                )

                self.mensagem_alerta(f'O Ativo {ticker_maiuscula} foi criada com sucesso!')

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
    tela = TelaAtivos()
    tela.show()
    qt.exec_()
