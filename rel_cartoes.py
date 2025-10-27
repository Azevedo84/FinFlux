import sys
from forms.tela_rel_cartoes import *
from banco_dados.conexao_nuvem import conectar_banco_nuvem
from comandos.tabelas import layout_cabec_tab, lanca_tabela
from comandos.telas import tamanho_aplicacao
from funcao_padrao import grava_erro_banco, trata_excecao
from PyQt5.QtWidgets import QMainWindow, QApplication
import inspect
import os


class TelaRelatorioCartoes(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        tamanho_aplicacao(self)
        layout_cabec_tab(self.table_Bradesco)
        layout_cabec_tab(self.table_NU)
        layout_cabec_tab(self.table_C6)
        layout_cabec_tab(self.table_XP)
        layout_cabec_tab(self.table_Samsung)
        layout_cabec_tab(self.table_Total)

        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.id_usuario = "1"


        self.criar_tabelas()

    def criar_tabelas(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute('SELECT bc.id, bc.id_banco '
                           'FROM saldo_banco as bc '
                           'WHERE bc.id_tipoconta = 1;')
            lista_completa = cursor.fetchall()

            if lista_completa:
                # Dicionário para armazenar o total por fatura
                totais_por_fatura = {}

                for i in lista_completa:
                    lista_tabela = []

                    id_saldo, id_banco = i
                    banco = None  # Inicializa a variável 'banco' aqui

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                        SELECT fat.mes, fat.ano, banc.descricao, SUM(mov.qtde_sai) 
                        FROM movimentacao as mov
                        INNER JOIN cadastro_fatura AS fat ON mov.id_fatura = fat.id
                        INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id
                        INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id 
                        WHERE banc.id = {id_banco} 
                        GROUP BY banc.descricao, fat.mes, fat.ano;
                    """)
                    saldo_conta = cursor.fetchall()
                    if saldo_conta:
                        for ii in saldo_conta:
                            mes, ano, banco, valor = ii

                            fatura = f"{mes}/{ano}"

                            # Adiciona os dados à lista
                            dados = (f"{mes}/{ano}", valor)
                            lista_tabela.append(dados)

                            # Acumula o total por fatura
                            if fatura not in totais_por_fatura:
                                totais_por_fatura[fatura] = 0

                            totais_por_fatura[fatura] += valor

                        # Ordena a lista de faturas pela fatura mais antiga (ano, mes)
                        lista_tabela = sorted(lista_tabela,
                                              key=lambda x: (int(x[0].split('/')[1]), int(x[0].split('/')[0])))

                        # Agora, a lista está ordenada pela fatura mais antiga
                        for dados in lista_tabela:
                            mes_ano, valor = dados
                            mes, ano = mes_ano.split('/')

                            # Lança na tabela do banco específico
                            if banco == "BRADESCO":
                                lanca_tabela(self.table_Bradesco, lista_tabela)
                            elif banco == "C6 BANK":
                                lanca_tabela(self.table_C6, lista_tabela)
                            elif banco == "NUBANK":
                                lanca_tabela(self.table_NU, lista_tabela)
                            elif banco == "XP":
                                lanca_tabela(self.table_XP, lista_tabela)
                            elif banco == "SAMSUNG":
                                lanca_tabela(self.table_Samsung, lista_tabela)

                # Após o loop, insira o total por fatura na tabela "self.table_Total"
                listinha = []
                for fatura, total in totais_por_fatura.items():
                    dadus = (fatura, total)
                    listinha.append(dadus)

                if listinha:
                    listinha.sort(key=lambda x: (int(x[0].split('/')[1]), int(x[0].split('/')[0])))

                    lanca_tabela(self.table_Total, listinha)



        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            trata_excecao(nome_funcao, str(e), self.nome_arquivo)
            grava_erro_banco(nome_funcao, e, self.nome_arquivo)

        finally:
            if 'conexao' in locals():
                conecta.close()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    tela = TelaRelatorioCartoes()
    tela.show()
    qt.exec_()
