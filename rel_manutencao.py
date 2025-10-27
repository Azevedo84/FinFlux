from banco_dados.conexao_nuvem import conectar_banco_nuvem
import os
import pandas as pd

def calcular_proximas_trocas():
    conecta = conectar_banco_nuvem()
    try:
        cursor = conecta.cursor()
        cursor.execute("""
            SELECT m.id, m.data, mv.id_veiculo,
                   mv.km_atual 
            FROM manutencao_veiculo mv
            INNER JOIN movimentacao m ON m.id = mv.id_movimentacao 
            order by m.data
        """)
        dados = cursor.fetchall()
        for i in dados:
            print(i)

        # Cria DataFrame
        df = pd.DataFrame(dados, columns=["ID Mov", "Data", "ID Veículo", "KM Atual"])

        # Caminho da Área de Trabalho
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        # Nome do arquivo
        arquivo = os.path.join(desktop, "trocas_veiculo.xlsx")

        # Salva em Excel
        df.to_excel(arquivo, index=False)

        print(f"Arquivo salvo em: {arquivo}")

    finally:
        if 'conecta' in locals():
            conecta.close()

calcular_proximas_trocas()