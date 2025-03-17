import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Dados de exemplo
data = {
    "Categoria": ["Alimentação", "Transporte", "Educação", "Saúde", "Lazer",
                  "Moradia", "Outros", "Alimentação", "Transporte", "Educação"],
    "Valor": [500, 300, 800, 200, 150, 1200, 100, 600, 400, 900],
    "Data": ["2024-01-15", "2024-01-20", "2024-02-10", "2024-02-18", "2024-03-05",
             "2024-03-12", "2024-03-20", "2024-04-08", "2024-04-15", "2024-04-22"],
    "Cartão": ["Visa", "Mastercard", "Elo", "Visa", "Elo", "Mastercard", "Visa", "Visa", "Elo", "Visa"]
}

df = pd.DataFrame(data)
df['Data'] = pd.to_datetime(df['Data'])
df['Mês'] = df['Data'].dt.to_period('M').astype(str)

# 1. Gráfico de Pizza: Top 5 categorias de despesas
top_categorias = df.groupby("Categoria")["Valor"].sum().nlargest(5).reset_index()
fig_pizza = px.pie(
    top_categorias,
    names="Categoria",
    values="Valor",
    title="Top 5 Categorias de Despesas"
)

# 2. Gráfico de Linhas: Despesas totais por mês
despesas_mes = df.groupby("Mês")["Valor"].sum().reset_index()
fig_linhas_mes = px.line(
    despesas_mes,
    x="Mês",
    y="Valor",
    title="Despesas Totais por Mês",
    markers=True,
    labels={"Mês": "Mês", "Valor": "Total de Gastos"}
)

# 3. Tabela: Top 10 maiores gastos do mês
top_gastos = df.sort_values(by="Valor", ascending=False).head(10)

# 4. Gráfico de Linhas: Total de gastos por cartão de crédito
gastos_cartao = df.groupby(["Cartão", "Mês"])["Valor"].sum().reset_index()
fig_linhas_cartao = px.line(
    gastos_cartao,
    x="Mês",
    y="Valor",
    color="Cartão",
    title="Total de Gastos por Cartão de Crédito",
    markers=True,
    labels={"Mês": "Mês", "Valor": "Total de Gastos"}
)

# Inicializando o app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Despesas Familiares", style={'text-align': 'center'}),

    html.Div([
        # Gráfico de Pizza
        html.Div(dcc.Graph(figure=fig_pizza), style={'grid-column': '1 / 2', 'grid-row': '1'}),

        # Gráfico de Linhas (Despesas por mês)
        html.Div(dcc.Graph(figure=fig_linhas_mes), style={'grid-column': '2 / 3', 'grid-row': '1'}),

        # Gráfico de Linhas (Gastos por cartão de crédito)
        html.Div(dcc.Graph(figure=fig_linhas_cartao), style={'grid-column': '1 / 3', 'grid-row': '2'}),

        # Tabela (Top 10 maiores gastos)
        html.Div([
            html.H3("Top 10 Maiores Gastos do Mês", style={'text-align': 'center'}),
            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in top_gastos.columns])),
                html.Tbody([
                    html.Tr([html.Td(top_gastos.iloc[i][col]) for col in top_gastos.columns])
                    for i in range(len(top_gastos))
                ])
            ])
        ], style={'grid-column': '3 / 4', 'grid-row': '1 / 3', 'overflow': 'auto'})
    ], style={
        'display': 'grid',
        'grid-template-columns': 'repeat(3, 1fr)',
        'grid-template-rows': 'auto auto',
        'gap': '20px',
        'padding': '20px'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
