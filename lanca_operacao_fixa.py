from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f"select id, data, id_categoria, qtde_ent, qtde_sai from movimentacao "
                   f"WHERE id_saldo = 16;")
    lista_completa = cursor.fetchall()
    for i in lista_completa:
        id_mov, data, id_cat, qtde_ent, qtde_sai = i

        categoria = ""
        valor = 0

        if id_cat == 115:
            categoria = "DEPÓSITO FGTS"
        elif id_cat == 117:
            categoria = "RENDIMENTO"
        elif id_cat == 134:
            categoria = "PARTICIP. RESULTADOS"
        elif id_cat == 7:
            categoria = "RESGATE"

        if qtde_ent > 0:
            valor = qtde_ent
        elif qtde_sai > 0:
            valor = qtde_sai * -1

        obs = "FGTS"

        if categoria or valor:
            cursor = conecta.cursor()
            cursor.execute(f"select ID_ATIVO, ID_MOVIMENTACAO from fixa_operacao "
                           f"WHERE ID_MOVIMENTACAO = {id_mov};")
            lista_operacao = cursor.fetchall()

            if not lista_operacao:
                cursor = conecta.cursor()
                cursor.execute(f"INSERT INTO fixa_operacao (ID_ATIVO, ID_MOVIMENTACAO, TIPO_MOVIMENTO, VALOR, OBS) "
                               f"VALUES (19, {id_mov}, '{categoria}', '{valor}', '{obs}');")

                conecta.commit()
                print("LANÇADO", id_mov, categoria, valor, obs)
        else:
            print("NÃO DEU", id_mov, categoria)


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
