import pandas as pd
import os
import re

from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    # Caminho para o arquivo na área de trabalho
    usuario = os.getlogin()
    caminho = f"C:/Users/{usuario}/Desktop/clear.xlsx"

    # Lê a planilha sem cabeçalho
    df = pd.read_excel(caminho, sheet_name="Planilha1", header=None)

    # Encontra a linha onde começa a tabela (procura por "Movimentação")
    linha_header = df[df.apply(lambda row: row.astype(str).str.contains("Movimentação").any(), axis=1)].index[0]

    # Reimporta usando essa linha como cabeçalho
    df = pd.read_excel(caminho, sheet_name="Planilha1", header=linha_header)

    # Filtra só colunas que interessam
    mov = df[['Movimentação', 'Liquidação', 'Lançamento', 'Valor (R$)']].dropna()

    # Descarta linhas que não têm valores numéricos
    mov = mov[mov['Valor (R$)'].astype(str).str.contains(r'\d', na=False)]

    # Função para extrair ativo e tipo
    def extrair_ativo_tipo(texto):
        texto = str(texto)
        ativo = None
        tipo = None

        m = re.search(r'\b[A-Z]{4}[0-9]{1,2}\b', texto)
        if m:
            ativo = m.group(0)

        if "DIVIDENDOS" in texto.upper():
            tipo = "DIVIDENDO"
        elif "JUROS S/ CAPITAL" in texto.upper():
            tipo = "JCP"
        elif "RENDIMENTOS" in texto.upper():
            tipo = "RENDIMENTO FII"
        elif "OPERAÇÕES EM BOLSA" in texto.upper():
            tipo = "OPERAÇÕES EM BOLSA"
        elif "TED BCO" in texto.upper():
            tipo = "TED BCO"
        else:
            tipo = "OUTRO"

        return pd.Series([ativo, tipo])

    # Aplica a função
    mov[['Ativo', 'Tipo']] = mov['Lançamento'].apply(extrair_ativo_tipo)

    # Limpa valores
    mov['Valor (R$)'] = (
        mov['Valor (R$)']
        .astype(str)
        .replace(r'[R$\s]', '', regex=True)
        .str.replace(',', '.')
        .astype(float)
    )

    # Converte datas e ordena
    mov['Movimentação'] = pd.to_datetime(mov['Movimentação'], dayfirst=True, errors='coerce')
    mov['Liquidação'] = pd.to_datetime(mov['Liquidação'], dayfirst=True, errors='coerce')
    mov = mov.sort_values('Movimentação')

    # Lista de tuplas (enxuta)
    mov_tuplas = list(mov[['Movimentação', 'Ativo', 'Tipo', 'Valor (R$)']].itertuples(index=False, name=None))

    for item in mov_tuplas:
        data, ativo, tipo, valor = item

        # Converte a data para string YYYY-MM-DD
        data_str = data.strftime("%Y-%m-%d") if not pd.isna(data) else None

        if valor < 0:
            entrada = 0
            saida = valor * -1
        else:
            entrada = valor
            saida = 0

        if tipo == "OPERAÇÕES EM BOLSA":
            if entrada:
                id_categoria = 122
            else:
                id_categoria = 114

        elif tipo == "TED BCO":
            id_categoria = 7

        else:
            if entrada:
                id_categoria = 117


        select_padrao = (f"SELECT mov.id, mov.data, "
                         f"banc.descricao, gr.descricao, cat.descricao, mov.qtde_ent, mov.qtde_sai, "
                         f"estab.descricao, cit.descricao, mov.id_fatura, IFNULL(mov.obs, '') "
                         f"FROM movimentacao AS mov "
                         f"INNER JOIN saldo_banco AS sald ON mov.id_saldo = sald.id "
                         f"INNER JOIN cadastro_usuario AS user ON sald.id_usuario = user.id "
                         f"INNER JOIN cadastro_banco AS banc ON sald.id_banco = banc.id "
                         f"INNER JOIN cadastro_tipoconta AS tip ON sald.id_tipoconta = tip.id "
                         f"INNER JOIN cadastro_categoria AS cat ON mov.id_categoria = cat.id "
                         f"INNER JOIN cadastro_grupo AS gr ON cat.id_grupo = gr.id "
                         f"INNER JOIN cadastro_estabelecimento AS estab ON mov.id_estab = estab.id "
                         f"INNER JOIN cadastro_cidade AS cit ON mov.id_cidade = cit.id "
                         f"LEFT JOIN cadastro_fatura AS fat ON mov.id_fatura = fat.id ")

        id_banco = 26
        id_user = 1

        """cursor = conecta.cursor()
        cursor.execute(f"{select_padrao}"
                       f"WHERE banc.id = {id_banco} "
                       f"and mov.data = '{data_str}' "
                       f"and mov.qtde_ent = '{entrada}' "
                       f"and mov.qtde_sai = '{saida}' "
                       f"ORDER BY mov.data;")
        lista_completa = cursor.fetchall()"""

        cursor = conecta.cursor()
        cursor.execute(f"{select_padrao}"
                       f"WHERE banc.id = {id_banco} "
                       f"and mov.data = '{data_str}' "
                       f"and mov.qtde_ent = '{entrada}' "
                       f"and mov.qtde_sai = '{saida}' "
                       f"ORDER BY mov.data;")
        lista_completa = cursor.fetchall()
        if not lista_completa:
            id_saldo = 32
            id_estab = 107
            id_cidade = 19

            cursor = conecta.cursor()
            cursor.execute(f'Insert into movimentacao (data, id_saldo, id_categoria, qtde_ent , qtde_sai, id_estab, '
                           f'id_cidade, obs) '
                           f'values ("{data_str}", {id_saldo}, {id_categoria}, '
                           f'{entrada}, {saida}, {id_estab}, {id_cidade}, "{tipo}");')

            conecta.commit()

            print("LANÇADO COM SUCESSO!", data_str, ativo, tipo, "Entrada:", entrada,  "Saída:", saida)
            if id_categoria == 122:
                print("122 venda vairavel")
            if id_categoria == 7:
                print("7 transferencia")
            if id_categoria == 114:
                print("114 compra aççoes")
            if id_categoria == 117:
                print("117 rendimento")

finally:
    if 'conexao' in locals():
        conecta.close()
