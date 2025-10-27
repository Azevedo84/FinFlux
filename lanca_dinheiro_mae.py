from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    id_usuario = 1
    id_banco = 8
    id_tipo = 2

    cursor = conecta.cursor()
    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                   f"where id_usuario = {id_usuario} and "
                   f"id_banco = {id_banco} and "
                   f"id_tipoconta = {id_tipo};")
    saldo_conta = cursor.fetchall()
    id_saldo, saldo = saldo_conta[0]

    id_categoria = 182

    valor_float = 2000.0
    id_estab = 319
    id_cidade = 19

    obs_maiusculo = "PRA PAGAR DENTES PAI"

    cursor = conecta.cursor()
    cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                   f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                   f'values ("2025-02-04", {id_saldo}, {id_categoria}, '
                   f'0, {valor_float}, {id_estab}, {id_cidade}, "{obs_maiusculo}");')

    conecta.commit()


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()