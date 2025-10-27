import pandas as pd

# Lista fictícia de movimentações
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

# Monta o DataFrame
colunas = ["id", "data", "banco", "grupo", "categoria", "qtde_ent", "qtde_sai",
           "estabelecimento", "cidade", "id_fatura", "obs"]

df = pd.DataFrame(lista_completa, columns=colunas)

# Converte entradas e saídas para número
df["qtde_ent"] = pd.to_numeric(df["qtde_ent"], errors="coerce").fillna(0)
df["qtde_sai"] = pd.to_numeric(df["qtde_sai"], errors="coerce").fillna(0)

# Valor líquido (entradas - saídas)
df["valor"] = df["qtde_ent"] - df["qtde_sai"]

# Filtra gastos reais (negativos) e converte para positivo
df_gastos = df[(df["valor"] < 0) & (df["grupo"] != "Investimento")].copy()
df_gastos["valor"] = df_gastos["valor"].abs()

# Separa investimentos (entradas positivas em "Investimento")
df_invest = df[df["grupo"] == "Investimento"]["qtde_ent"].sum()

# Ranking de gastos por grupo
gastos_por_grupo = df_gastos.groupby("grupo")["valor"].sum().sort_values(ascending=False)

# Percentual do total
total_gastos = gastos_por_grupo.sum()
percentuais = (gastos_por_grupo / total_gastos * 100).round(1)

# 👉 Mostrar ranking
print("🏆 Categorias que mais pesam no orçamento:\n")
for grupo, valor in gastos_por_grupo.items():
    print(f"{grupo:<15} R$ {valor:>7.2f}  ({percentuais[grupo]}%)")

print(f"\n💰 Total de gastos: R$ {total_gastos:.2f}")
print(f"📈 Investimentos realizados: R$ {df_invest:.2f}")

# 👉 Insight: onde cortar 10%
top_categoria = gastos_por_grupo.index[0]
economia_10 = gastos_por_grupo.iloc[0] * 0.10

print("\n💡 INSIGHTS PARA ECONOMIZAR:")
print(f"- A categoria que mais pesa é **{top_categoria}**, representando {percentuais.iloc[0]}% dos seus gastos.")
print(f"- Se você reduzir **10% em {top_categoria}**, economizaria **R$ {economia_10:.2f}/mês**.")
print(f"- Se mantiver essa economia por 1 ano, terá **R$ {economia_10*12:.2f}**, que poderia ser investido.")
