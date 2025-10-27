import pandas as pd

# Lista fictícia (a mesma do exemplo anterior)
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

# Converte entradas e saídas para números
df["qtde_ent"] = pd.to_numeric(df["qtde_ent"], errors="coerce").fillna(0)
df["qtde_sai"] = pd.to_numeric(df["qtde_sai"], errors="coerce").fillna(0)

# Calcula valor líquido (entrada - saída)
df["valor"] = df["qtde_ent"] - df["qtde_sai"]

# Filtra gastos reais (valor negativo) e exclui investimentos
df_gastos = df[(df["valor"] < 0) & (df["grupo"] != "Investimento")].copy()
df_gastos["valor"] = df_gastos["valor"].abs()

# Soma total de gastos
total_gastos = df_gastos["valor"].sum()

# Definir categorias essenciais, desejos e investimentos (simplificado)
essenciais = ["Alimentação", "Casa", "Saúde", "Transporte", "Educação"]
desejos = ["Lazer"]

# Soma gastos por grupo
gastos_por_grupo = df_gastos.groupby("grupo")["valor"].sum()

# Gastos em cada grupo definido
gastos_essenciais = gastos_por_grupo[gastos_por_grupo.index.isin(essenciais)].sum()
gastos_desejos = gastos_por_grupo[gastos_por_grupo.index.isin(desejos)].sum()
gastos_outros = total_gastos - gastos_essenciais - gastos_desejos  # gastos que não se encaixam nas categorias acima

# Investimentos atuais
investimentos = df[df["grupo"] == "Investimento"]["qtde_ent"].sum()

# Regras 50/30/20 baseadas no total de gastos + investimentos (assumindo renda = gastos + investimentos)
renda_estimada = total_gastos + investimentos

meta_essenciais = renda_estimada * 0.50
meta_desejos = renda_estimada * 0.30
meta_poupanca = renda_estimada * 0.20

print(f"📊 Análise e metas segundo a regra 50/30/20 (estimativa com base nos seus dados):\n")

print(f"Renda estimada (gastos + investimentos): R$ {renda_estimada:.2f}\n")

print(f"Atuais gastos em essenciais: R$ {gastos_essenciais:.2f} (Meta: R$ {meta_essenciais:.2f})")
print(f"Atuais gastos em desejos:    R$ {gastos_desejos:.2f} (Meta: R$ {meta_desejos:.2f})")
print(f"Atuais gastos em outros:    R$ {gastos_outros:.2f} (não categorizados)")
print(f"Investimentos atuais:       R$ {investimentos:.2f} (Meta: R$ {meta_poupanca:.2f})")

print("\n🔍 Sugestões:")
if gastos_essenciais > meta_essenciais:
    print(f"- Você está gastando mais que o ideal em essenciais. Considere reduzir em R$ {gastos_essenciais - meta_essenciais:.2f}.")
else:
    print(f"- Gastos essenciais dentro da meta.")

if gastos_desejos > meta_desejos:
    print(f"- Gastos com desejos acima da meta. Tente cortar R$ {gastos_desejos - meta_desejos:.2f}.")
else:
    print(f"- Gastos com desejos dentro da meta.")

if investimentos < meta_poupanca:
    print(f"- Você poderia aumentar seus investimentos/poupança em R$ {meta_poupanca - investimentos:.2f} para atingir a meta.")
else:
    print(f"- Investimentos dentro ou acima da meta, ótimo!")

