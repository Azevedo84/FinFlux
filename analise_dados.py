import sys
from conexao_nuvem import conectar_banco_nuvem

import inspect
import os
import traceback

import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


class DadosOrdensDeProducao:
    def __init__(self):
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.calculo_1_dados_previsao()

    def trata_excecao(self, nome_funcao, mensagem, arquivo, excecao):
        try:
            tb = traceback.extract_tb(excecao)
            num_linha_erro = tb[-1][1]

            traceback.print_exc()
            print(f'Houve um problema no arquivo: {arquivo} na função: "{nome_funcao}"\n{mensagem} {num_linha_erro}')
            print(f'Houve um problema no arquivo:\n\n{arquivo}\n\n'
                  f'Comunique o desenvolvedor sobre o problema descrito abaixo:\n\n'
                  f'{nome_funcao}: {mensagem}')

        except Exception as e:
            nome_funcao_trat = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            tb = traceback.extract_tb(exc_traceback)
            num_linha_erro = tb[-1][1]
            print(f'Houve um problema no arquivo: {self.nome_arquivo} na função: "{nome_funcao_trat}"\n'
                  f'{e} {num_linha_erro}')

    def calculo_1_dados_previsao(self):
        conecta = conectar_banco_nuvem()
        try:
            cursor = conecta.cursor()
            cursor.execute(f"""
                SELECT mov.data, gr.descricao, cat.descricao, mov.qtde_sai, mov.obs 
                FROM movimentacao AS mov 
                INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id 
                INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id 
                WHERE gr.id NOT IN (1, 2, 14);""")
            dados_mov = cursor.fetchall()

            pd.set_option('display.max_rows', None)  # Para exibir todas as linhas
            pd.set_option('display.max_columns', None)  # Para exibir todas as colunas
            pd.set_option('display.width', None)  # Para não limitar a largura das colunas
            pd.set_option('display.max_colwidth', None)  # Para não truncar os valores das colunas

            df = pd.DataFrame(dados_mov, columns=['Data', 'Grupo', 'Categoria', 'Despesa', 'Obs'])
            # Converte a coluna 'Data' para datetime
            df['Data'] = pd.to_datetime(df['Data'])

            df.index = pd.date_range(start="2024-01-01", periods=len(df), freq='D')

            # Certifique-se de que a coluna 'Despesa' é numérica
            df['Despesa'] = pd.to_numeric(df['Despesa'], errors='coerce')  # Converte não numéricos em NaN
            df = df.dropna(subset=['Despesa'])  # Remove linhas com valores NaN na coluna 'Despesa'

            # Usando Isolation Forest para detectar anomalias nas despesas
            model = IsolationForest(contamination=0.1)  # Ajuste o parâmetro de contaminação conforme necessário
            df['Anomalia'] = model.fit_predict(df[['Despesa']])

            # Filtra as anomalias (valores -1 são anômalos)
            anomalies = df[df['Anomalia'] == -1]
            # print("\nAnomalias Detectadas:")
            # print(anomalies)

            # Agregar por categoria e somar as despesas
            categoria_despesas = df.groupby('Categoria')['Despesa'].sum().sort_values(ascending=False)

            # Exibir as categorias com maior despesa
            # print(categoria_despesas)

            # Agrupar por mês
            df['Mês'] = df['Data'].dt.to_period('M')  # Extrai o mês da data
            despesas_mensais = df.groupby('Mês')['Despesa'].sum().sort_values(ascending=False)

            # Exibir as despesas mensais
            # print(despesas_mensais)

            # Agrupar por subcategoria ou grupo
            grupo_despesas = df.groupby('Grupo')['Despesa'].sum().sort_values(ascending=False)

            # Exibir os gastos por grupo
            # print(grupo_despesas)

            # Agrupar por mês e visualizar
            despesas_mensais = df.groupby('Mês')['Despesa'].sum()
            despesas_mensais.plot(kind='line', figsize=(10, 6))
            plt.title('Despesas Mensais ao Longo do Tempo')
            plt.ylabel('Despesa')
            plt.xlabel('Mês')
            plt.show()

        except Exception as e:
            nome_funcao = inspect.currentframe().f_code.co_name
            exc_traceback = sys.exc_info()[2]
            self.trata_excecao(nome_funcao, str(e), self.nome_arquivo, exc_traceback)

        finally:
            if 'conexao' in locals():
                conecta.close()


chama_classe = DadosOrdensDeProducao()