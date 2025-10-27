from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                   f"where id_usuario = 2 and "
                   f"id_banco = 12 and "
                   f"id_tipoconta = 2;")
    saldo_conta = cursor.fetchall()
    id_saldo, saldo = saldo_conta[0]
    print(id_saldo)

    #estabelecimento de mercado
    #603 = FRUTEIRA DO JAPONES, 734 = MERCADO DIA

    #CIDADE
    # 5 = ESTANCIA, 7 = IVOTI

    data_mysql = "2025-09-26"
    valor_float = 13.96
    id_categoria = 23
    id_estab = 734
    id_cidade = 5
    obs_maiusculo = "IVANIA PAGOU"

    cursor = conecta.cursor()
    cursor.execute(f'Insert into movimentacao (data, id_saldo, id_categoria, qtde_ent , qtde_sai, id_estab, '
                   f'id_cidade, obs) '
                   f'values ("{data_mysql}", {id_saldo}, {id_categoria}, '
                   f'0, {valor_float}, {id_estab}, {id_cidade}, "{obs_maiusculo}");')

    conecta.commit()

finally:
    if 'conexao' in locals():
        conecta.close()