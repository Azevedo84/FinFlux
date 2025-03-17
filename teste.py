import pandas as pd

# Carrega o arquivo Excel
arquivo_excel = 'Pasta1.xlsx'

# Lê os dados da planilha
dados = pd.read_excel(arquivo_excel)

# Converte os dados do DataFrame em uma lista de listas
lista_dados = dados.values.tolist()

# Itera sobre cada linha da lista
for linha in lista_dados:
    data, banco, tipo_conta, tipo_despesas, categoria, entradas, saidas, estabelecimento, observacao = linha
    print(data)
    print(type(data))