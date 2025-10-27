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

    data_mysql = "2025-09-15"
    valor_float = 157.44
    id_categoria = 20
    id_estab = 386
    id_cidade = 19
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