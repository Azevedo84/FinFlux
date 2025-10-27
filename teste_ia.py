lista_completa = [
    (1, "01/07/2025", "Banco X", "Alimentação", "Supermercado",
     "", 250.00, "Mercado Bom", "São Paulo", None, "Compra do mês"),
    (2, "03/07/2025", "Banco X", "Lazer", "Cinema",
     "", 60.00, "Cinemark", "São Paulo", None, ""),
    (3, "05/07/2025", "Banco X", "Transporte", "Combustível",
     "", 180.00, "Posto Shell", "São Paulo", None, "")
]

import pandas as pd

colunas = [
    "id", "data", "banco", "grupo", "categoria",
    "qtde_ent", "qtde_sai", "estabelecimento",
    "cidade", "id_fatura", "obs"
]

df = pd.DataFrame(lista_completa, columns=colunas)

# Transformar a data em formato datetime
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

# Criar coluna valor (considerando só saídas por enquanto)
df["valor"] = pd.to_numeric(df["qtde_sai"], errors="coerce").fillna(0)

print("💰 Total gasto:", df["valor"].sum())

print("\n🏆 Top categorias:")
print(df.groupby("categoria")["valor"].sum().sort_values(ascending=False).head(5))

print("\n📊 Gastos por mês:")
print(df.groupby(df["data"].dt.to_period("M"))["valor"].sum())