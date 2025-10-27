import pandas as pd

# Dados fictícios
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

colunas = ["id", "data", "banco", "grupo", "categoria", "qtde_ent", "qtde_sai",
           "estabelecimento", "cidade", "id_fatura", "obs"]

df = pd.DataFrame(lista_completa, columns=colunas)

# Converte para numérico
df["qtde_ent"] = pd.to_numeric(df["qtde_ent"], errors="coerce").fillna(0)
df["qtde_sai"] = pd.to_numeric(df["qtde_sai"], errors="coerce").fillna(0)

# Valor líquido = entradas - saídas
df["valor"] = df["qtde_ent"] - df["qtde_sai"]

# Filtra só gastos e exclui investimentos
df_gastos = df[(df["valor"] < 0) & (df["grupo"] != "Investimento")].copy()
df_gastos["valor"] = df_gastos["valor"].abs()

# Soma total gastos
total_gastos = df_gastos["valor"].sum()

# Categorias essenciais e desejos
essenciais = ["Alimentação", "Casa", "Saúde", "Transporte", "Educação"]
desejos = ["Lazer"]

# Soma por grupo
gastos_por_grupo = df_gastos.groupby("grupo")["valor"].sum()

gastos_essenciais = gastos_por_grupo[gastos_por_grupo.index.isin(essenciais)].sum()
gastos_desejos = gastos_por_grupo[gastos_por_grupo.index.isin(desejos)].sum()

investimentos = df[df["grupo"] == "Investimento"]["qtde_ent"].sum()

# Renda estimada
renda_estimada = total_gastos + investimentos

# Metas 50/30/20
meta_essenciais = renda_estimada * 0.50
meta_desejos = renda_estimada * 0.30
meta_poupanca = renda_estimada * 0.20

print(f"Renda estimada: R$ {renda_estimada:.2f}\n")

def alerta(nome, gasto, meta):
    if gasto > meta:
        print(f"⚠️ ALERTA: {nome} ultrapassou o limite! Gastou R$ {gasto:.2f}, limite R$ {meta:.2f}")
    else:
        print(f"✔️ {nome} dentro do limite. Gastou R$ {gasto:.2f}, limite R$ {meta:.2f}")

# Alertas
alerta("Gastos essenciais", gastos_essenciais, meta_essenciais)
alerta("Gastos com desejos", gastos_desejos, meta_desejos)

if investimentos < meta_poupanca:
    print(f"⚠️ ALERTA: Investimentos abaixo da meta! Invista mais R$ {meta_poupanca - investimentos:.2f}")
else:
    print(f"✔️ Investimentos dentro ou acima da meta. Valor investido: R$ {investimentos:.2f}")
