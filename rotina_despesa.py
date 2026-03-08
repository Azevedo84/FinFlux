import os
import pandas as pd
from datetime import datetime
from banco_dados.conexao_nuvem import conectar_banco_nuvem


# ==================================================
# GRUPOS PRIORITÁRIOS (IDs REAIS DO BANCO)
# ==================================================
GRUPOS_PRIORITARIOS = {
    5: "ALIMENTAÇÃO",
    8: "VEÍCULO",
    15: "MERCADO",
    11: "LAZER"
}

# ==================================================
# LIMITES MENSAIS POR GRUPO
# ==================================================
LIMITES_GRUPO = {
    5: 1200.00,   # Alimentação
    8: 1300.00,    # Veículo
    15: 1000.00,   # Mercado
    11: 400.00    # Lazer
}


# ==================================================
# QUERY BASE
# ==================================================
def select_base_gastos():
    return """
        SELECT
            gr.id AS id_grupo,
            gr.descricao AS grupo,
            cat.id AS id_categoria,
            cat.descricao AS categoria,
            SUM(mov.qtde_sai) AS total
        FROM movimentacao mov
        INNER JOIN cadastro_categoria cat ON mov.id_categoria = cat.id
        INNER JOIN cadastro_grupo gr ON cat.id_grupo = gr.id
        WHERE MONTH(mov.data) = %s
          AND YEAR(mov.data) = %s
        GROUP BY gr.id, cat.id
    """


# ==================================================
# BUSCAR GASTOS DO MÊS ATUAL
# ==================================================
def buscar_gastos_mes_atual(conexao):
    hoje = datetime.today()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        select_base_gastos(),
        (hoje.month, hoje.year)
    )

    return cursor.fetchall()


# ==================================================
# ANALISAR GRUPOS PRIORITÁRIOS
# ==================================================
def analisar_grupos(gastos):
    grupos = {}

    for g in gastos:
        id_grupo = g['id_grupo']

        if id_grupo not in GRUPOS_PRIORITARIOS:
            continue

        if id_grupo not in grupos:
            grupos[id_grupo] = {
                'grupo': g['grupo'],
                'total': 0.0,
                'categorias': []
            }

        valor = float(g['total'])
        grupos[id_grupo]['total'] += valor
        grupos[id_grupo]['categorias'].append({
            'categoria': g['categoria'],
            'valor': valor
        })

    return grupos


# ==================================================
# DETECTAR EXCESSOS E CATEGORIAS VILÃS
# ==================================================
def detectar_excessos(grupos):
    alertas = []

    for id_grupo, dados in grupos.items():
        limite = LIMITES_GRUPO.get(id_grupo)

        if not limite:
            continue

        total = round(dados['total'], 2)

        if total > limite:
            categorias_ordenadas = sorted(
                dados['categorias'],
                key=lambda x: x['valor'],
                reverse=True
            )

            for c in categorias_ordenadas:
                alertas.append({
                    'grupo': dados['grupo'],
                    'categoria': c['categoria'],
                    'gasto_categoria': round(c['valor'], 2),
                    'total_grupo': total,
                    'limite_grupo': limite,
                    'excesso_grupo': round(total - limite, 2)
                })

    return alertas


# ==================================================
# GERAR EXCEL NO DESKTOP
# ==================================================
def gerar_excel_desktop(alertas):
    if not alertas:
        return False

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    hoje = datetime.now().strftime("%Y-%m-%d")

    caminho = os.path.join(
        desktop,
        f"alerta_gastos_{hoje}.xlsx"
    )

    df = pd.DataFrame(alertas)

    df = df[
        [
            'grupo',
            'categoria',
            'gasto_categoria',
            'total_grupo',
            'limite_grupo',
            'excesso_grupo'
        ]
    ]

    df.to_excel(caminho, index=False)
    return True


# ==================================================
# ROTINA PRINCIPAL
# ==================================================
def rotina_diaria_verificacao():
    conexao = conectar_banco_nuvem()

    try:
        gastos = buscar_gastos_mes_atual(conexao)
        grupos = analisar_grupos(gastos)
        alertas = detectar_excessos(grupos)

        if gerar_excel_desktop(alertas):
            print("⚠️ Grupos estourados — Excel gerado no Desktop")
        else:
            print("✅ Tudo dentro dos limites")

    except Exception as e:
        print("Erro na rotina:", e)

    finally:
        conexao.close()


# ==================================================
# EXECUÇÃO
# ==================================================
if __name__ == "__main__":
    rotina_diaria_verificacao()
