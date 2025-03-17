import sys
from forms.tela_menu import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from cad_banco import TelaBanco
from cad_categoria import TelaCategoria
from cad_cidade import TelaCidade
from cad_estab import TelaEstab
from cad_grupo import TelaGrupo
from cad_tipo import TelaTipo
from desp_cartao import TelaDespCartao
from pag_cartao import TelaPagaCartao
from mov_entrada import TelaEntrada
from mov_saida import TelaSaida
from mov_transf import TelaTransferencia
from movimentacao import TelaMovimentacao
from saldos import TelaSaldos
from rel_mov_mensal_anual import TelaRelatorioMovMensal
from mov_altera import TelaAlterarMov


class TelaMenu(QMainWindow, Ui_Menu_Principal):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.movimentacao = []
        self.saldos = []
        self.grafico = []

        self.alterar_mov = []

        self.cad_banco = []
        self.cad_categoria = []
        self.cad_cidade = []
        self.cad_estab = []
        self.cad_grupo = []
        self.cad_tipo = []

        self.desp_cartao = []
        self.pag_cartao = []

        self.entrada = []
        self.saida = []
        self.tranf = []

        self.actionAlterar.triggered.connect(self.chama_alterar_mov)

        self.actionMovimenta_o.triggered.connect(self.chama_movimentacao)
        self.actionSaldos_4.triggered.connect(self.chama_saldos)
        self.actionGr_fico_Despesas.triggered.connect(self.chama_grafico)

        self.btn_desp_cartao.clicked.connect(self.chama_desp_cartao)
        self.btn_pagar_cartao.clicked.connect(self.chama_pag_cartao)

        self.btn_Entradas.clicked.connect(self.chama_entradas)
        self.btn_Saidas.clicked.connect(self.chama_saidas)
        self.btn_Transf.clicked.connect(self.chama_transf)

        self.action_Banco.triggered.connect(self.chama_banco)
        self.action_Categoria.triggered.connect(self.chama_categoria)
        self.action_Cidade.triggered.connect(self.chama_cidade)
        self.action_Estab.triggered.connect(self.chama_estab)
        self.action_Grupo.triggered.connect(self.chama_grupo)
        self.action_Tipo.triggered.connect(self.chama_tipo)

    def chama_alterar_mov(self):
        self.alterar_mov = TelaAlterarMov()
        self.alterar_mov.show()

    def chama_movimentacao(self):
        self.movimentacao = TelaMovimentacao()
        self.movimentacao.show()

    def chama_saldos(self):
        print('saldos')
        self.saldos = TelaSaldos()
        self.saldos.show()

    def chama_grafico(self):
        self.grafico = TelaRelatorioMovMensal()
        self.grafico.show()

    def chama_banco(self):
        self.cad_banco = TelaBanco()
        self.cad_banco.show()

    def chama_categoria(self):
        self.cad_categoria = TelaCategoria()
        self.cad_categoria.show()

    def chama_cidade(self):
        self.cad_cidade = TelaCidade()
        self.cad_cidade.show()

    def chama_estab(self):
        self.cad_estab = TelaEstab()
        self.cad_estab.show()

    def chama_grupo(self):
        self.cad_grupo = TelaGrupo()
        self.cad_grupo.show()

    def chama_tipo(self):
        self.cad_tipo = TelaTipo()
        self.cad_tipo.show()

    def chama_desp_cartao(self):
        self.desp_cartao = TelaDespCartao()
        self.desp_cartao.show()

    def chama_pag_cartao(self):
        self.pag_cartao = TelaPagaCartao()
        self.pag_cartao.show()

    def chama_entradas(self):
        self.entrada = TelaEntrada()
        self.entrada.show()

    def chama_saidas(self):
        self.saida = TelaSaida()
        self.saida.show()

    def chama_transf(self):
        self.tranf = TelaTransferencia()
        self.tranf.show()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela_menu = TelaMenu()
    tela_menu.show()
    sys.exit(qt.exec_())
