import pandas as pd

# Lista fictícia de movimentações (id, data, banco, grupo, categoria, qtde_ent, qtde_sai, estabelecimento, cidade, id_fatura, obs)
lista_completa = [
    (1, "01/07/2025", "Banco X", "Alimentação", "Supermercado", "", 250.00, "Mercado Bom", "São Paulo", None, "Compra do mês"),
    (2, "03/07/2025", "Banco X", "Lazer", "Cinema", "", 60.00, "Cinemark", "São Paulo", None, ""),
    (3, "05/07/2025", "Banco X", "Transporte", "Combustível", "", 180.00, "Posto Shell", "São Paulo", None, ""),
    (4, "06/07/2025", "Banco X", "Alimentação", "Restaurante", "", 120.00, "Restaurante Sabor", "São Paulo", None, "Almoço com amigos"),
    (5, "10/07/2025", "Banco X", "Saúde", "Farmácia", "", 90.00, "DrogaMais", "São Paulo", None, "Remédios"),
    (6, "12/07/2025", "Banco X", "Educação", "Curso Online", "", 300.00, "Udemy", "Online", None, ""),
    (7, "15/07/2025", "Banco X", "Casa", "Conta de Luz", "", 200.00, "Enel", "São Paulo", None, ""),
    (8, "20/07/2025", "Banco X", "Casa", "Conta de Água", "", 80.00, "Sabesp", "São Paulo", None, ""),
    (9, "22/07/2025", "Banco X", "Lazer", "Show", "", 150.00, "Ticketmaster", "São Paulo", None, ""),
    (10,"25/07/2025", "Banco X", "Transporte", "Uber", "", 50.00, "Uber", "São Paulo", None, ""),
    (11,"28/07/2025", "Banco X", "Alimentação", "Supermercado", "", 320.00, "Mercado Bom", "São Paulo", None, "Compra extra"),
    (12,"30/07/2025", "Banco X", "Investimento", "Aporte", 500.00, "", "XP Investimentos", "São Paulo", None, "Investimento mensal"),
    (13,"01/08/2025", "Banco X", "Alimentação", "Restaurante", "", 140.00, "Churrascaria Boa", "São Paulo", None, ""),
    (14,"05/08/2025", "Banco X", "Saúde", "Consulta Médica", "", 350.00, "Clínica Saúde", "São Paulo", None, ""),
    (15,"08/08/2025", "Banco X", "Educação", "Livro", "", 80.00, "Amazon", "Online", None, "")
]

# ✅ Definir as colunas (de acordo com o SELECT do banco)
colunas = [
    "id", "data", "banco", "grupo", "categoria",
    "qtde_ent", "qtde_sai", "estabelecimento", "cidade", "id_fatura", "obs"
]

# ✅ Criar DataFrame
df = pd.DataFrame(lista_completa, columns=colunas)

# ✅ Converter colunas numéricas com segurança
df["qtde_ent"] = pd.to_numeric(df["qtde_ent"], errors="coerce").fillna(0)
df["qtde_sai"] = pd.to_numeric(df["qtde_sai"], errors="coerce").fillna(0)

# ✅ Calcular valor líquido (positivo para entradas, negativo para saídas)
df["valor"] = df["qtde_ent"] - df["qtde_sai"]

# ✅ Também podemos converter a data para um tipo datetime, se quisermos agrupar por mês
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

# ✅ Agora podemos fazer análises simples, por exemplo:
print("==== DataFrame Original ====")
print(df)

print("\n==== Total por GRUPO ====")
print(df.groupby("grupo")["valor"].sum())

print("\n==== Total geral ====")
print(df["valor"].sum())

print("\n==== Gastos por CATEGORIA ====")
print(df.groupby("categoria")["valor"].sum())