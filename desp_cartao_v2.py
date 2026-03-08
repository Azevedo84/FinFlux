import sys
import inspect
import os
import traceback

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QDate

from forms.tela_desp_cartao_v2 import *

from banco_dados.conexao_nuvem import conectar_banco_nuvem
from banco_dados.controle_erros import grava_erro_banco

from comandos.telas import tamanho_aplicacao, icone
from comandos.conversores import valores_para_float


class TelaDespCartao(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)
        super().setupUi(self)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        icone(self, "gremio.png")
        tamanho_aplicacao(self)

        self.id_usuario = "1"

        # conexões
        self.combo_Banco.activated.connect(self.lanca_combo_fatura)
        self.combo_Grupo.activated.connect(self.lanca_combo_categoria)

        self.btn_Salvar.clicked.connect(self.verifica_salvamento)
        self.btn_Limpar.clicked.connect(self.reiniciar_tela)

        # inicialização
        self.lanca_combo_banco()
        self.lanca_combo_grupo()
        self.lanca_combo_cidade()

        self.spin_Parcelas.setValue(1)

        self.date_Compra.setDate(QDate.currentDate())

    # ---------------------------------------------------------

    def mensagem_alerta(self, mensagem):

        alert = QMessageBox()

        alert.setIcon(QMessageBox.Warning)
        alert.setText(mensagem)

        alert.setWindowTitle("Atenção")

        alert.setStandardButtons(QMessageBox.Ok)

        alert.exec_()

    # ---------------------------------------------------------

    def trata_excecao(self, nome_funcao, mensagem, arquivo, excecao):

        tb = traceback.extract_tb(excecao)
        num_linha_erro = tb[-1][1]

        traceback.print_exc()

        print(
            f'Houve um problema no arquivo: {arquivo}\n'
            f'Função: {nome_funcao}\n'
            f'{mensagem} linha {num_linha_erro}'
        )

        grava_erro_banco(nome_funcao, mensagem, arquivo, num_linha_erro)

    # ---------------------------------------------------------
    # COMBOS
    # ---------------------------------------------------------

    def lanca_combo_banco(self):

        conecta = conectar_banco_nuvem()

        try:

            self.combo_Banco.clear()

            lista = [""]

            cursor = conecta.cursor()

            cursor.execute("""
                SELECT id, descricao
                FROM cadastro_banco
                ORDER BY descricao
            """)

            dados = cursor.fetchall()

            for ides, descr in dados:

                lista.append(f"{ides} - {descr}")

            self.combo_Banco.addItems(lista)

        finally:

            conecta.close()

    # ---------------------------------------------------------

    def lanca_combo_fatura(self):

        conecta = conectar_banco_nuvem()

        try:

            banco = self.combo_Banco.currentText()

            if not banco:
                return

            id_banco = banco.split(" - ")[0]

            self.combo_Fatura.clear()

            lista = [""]

            cursor = conecta.cursor()

            cursor.execute(f"""
                SELECT id, mes, ano
                FROM cadastro_fatura
                WHERE id_saldo IN
                (
                    SELECT id
                    FROM saldo_banco
                    WHERE id_banco = {id_banco}
                )
                ORDER BY ano, mes
            """)

            dados = cursor.fetchall()

            for id_fat, mes, ano in dados:

                mes = str(mes).zfill(2)

                lista.append(f"{id_fat} - {mes}/{ano}")

            self.combo_Fatura.addItems(lista)

        finally:

            conecta.close()

    # ---------------------------------------------------------

    def lanca_combo_grupo(self):

        conecta = conectar_banco_nuvem()

        try:

            self.combo_Grupo.clear()

            lista = [""]

            cursor = conecta.cursor()

            cursor.execute("""
                SELECT id, descricao
                FROM cadastro_grupo
                ORDER BY descricao
            """)

            dados = cursor.fetchall()

            for ides, descr in dados:

                lista.append(f"{ides} - {descr}")

            self.combo_Grupo.addItems(lista)

        finally:

            conecta.close()

    # ---------------------------------------------------------

    def lanca_combo_categoria(self):

        conecta = conectar_banco_nuvem()

        try:

            self.combo_Categoria.clear()

            grupo = self.combo_Grupo.currentText()

            if not grupo:
                return

            id_grupo = grupo.split(" - ")[0]

            cursor = conecta.cursor()

            cursor.execute(f"""
                SELECT id, descricao
                FROM cadastro_categoria
                WHERE id_grupo = {id_grupo}
                ORDER BY descricao
            """)

            dados = cursor.fetchall()

            lista = [""]

            for ides, descr in dados:

                lista.append(f"{ides} - {descr}")

            self.combo_Categoria.addItems(lista)

        finally:

            conecta.close()

    # ---------------------------------------------------------

    def lanca_combo_cidade(self):

        conecta = conectar_banco_nuvem()

        try:

            self.combo_Cidade.clear()

            lista = [""]

            cursor = conecta.cursor()

            cursor.execute("""
                SELECT id, descricao
                FROM cadastro_cidade
                ORDER BY descricao
            """)

            dados = cursor.fetchall()

            for ides, descr in dados:

                lista.append(f"{ides} - {descr}")

            self.combo_Cidade.addItems(lista)

        finally:

            conecta.close()

    # ---------------------------------------------------------
    # REINICIAR
    # ---------------------------------------------------------

    def reiniciar_tela(self):

        self.combo_Banco.setCurrentText("")
        self.combo_Fatura.setCurrentText("")

        self.combo_Grupo.setCurrentText("")
        self.combo_Categoria.setCurrentText("")

        self.combo_Cidade.setCurrentText("")

        self.line_Estab.clear()

        self.line_Valor.clear()

        self.text_Obs.clear()

        self.spin_Parcelas.setValue(1)

        self.date_Compra.setDate(QDate.currentDate())

    # ---------------------------------------------------------
    # VALIDAÇÃO
    # ---------------------------------------------------------

    def verifica_salvamento(self):

        banco = self.combo_Banco.currentText()
        fatura = self.combo_Fatura.currentText()

        grupo = self.combo_Grupo.currentText()
        categoria = self.combo_Categoria.currentText()

        estab = self.line_Estab.text()

        cidade = self.combo_Cidade.currentText()

        valor = self.line_Valor.text()

        if not banco:
            self.mensagem_alerta("Banco não pode estar vazio")
            return

        if not fatura:
            self.mensagem_alerta("Fatura não pode estar vazia")
            return

        if not grupo:
            self.mensagem_alerta("Grupo não pode estar vazio")
            return

        if not categoria:
            self.mensagem_alerta("Categoria não pode estar vazia")
            return

        if not estab:
            self.mensagem_alerta("Estabelecimento não pode estar vazio")
            return

        if not cidade:
            self.mensagem_alerta("Cidade não pode estar vazia")
            return

        if not valor:
            self.mensagem_alerta("Valor não pode estar vazio")
            return

        self.salvar()

    # ---------------------------------------------------------
    # SALVAR
    # ---------------------------------------------------------

    def salvar(self):

        conecta = conectar_banco_nuvem()

        try:

            data = self.date_Compra.date().toString("yyyy-MM-dd")

            categoria = self.combo_Categoria.currentText().split(" - ")[0]

            cidade = self.combo_Cidade.currentText().split(" - ")[0]

            valor = valores_para_float(self.line_Valor.text())

            obs = self.text_Obs.toPlainText().upper()

            cursor = conecta.cursor()

            sql = """
                INSERT INTO movimentacao
                (data, id_categoria, qtde_sai, id_cidade, obs)
                VALUES (%s,%s,%s,%s,%s)
            """

            cursor.execute(sql, (data, categoria, valor, cidade, obs))

            conecta.commit()

            self.mensagem_alerta("Movimentação criada com sucesso")

            self.reiniciar_tela()

        finally:

            conecta.close()


# ---------------------------------------------------------

if __name__ == '__main__':

    app = QApplication(sys.argv)

    tela = TelaDespCartao()

    tela.show()

    sys.exit(app.exec_())