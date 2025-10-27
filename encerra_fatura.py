from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    # BRADESCO = 5 / C6 = 6 / NUBANK = 12 / XP = 19 / SAMSUNG = 22

    id_banco = 5
    fatura = "10/2024"
    valor_final = "116.64"

    cursor = conecta.cursor()
    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                   f"where id_usuario = 1 and "
                   f"id_banco = {id_banco} and "
                   f"id_tipoconta = 1;")
    saldo_conta = cursor.fetchall()
    id_saldo, saldo = saldo_conta[0]

    cursor = conecta.cursor()
    cursor.execute(f"SELECT * FROM cadastro_fatura "
                   f"where fatura = '{fatura}' and id_saldo = {id_saldo};")
    dados_faturas = cursor.fetchall()
    print(dados_faturas)

    if dados_faturas:
        cursor = conecta.cursor()
        cursor.execute(f"UPDATE cadastro_fatura SET status = 'F', valor_final = '{valor_final}' "
                       f"where fatura = '{fatura}' "
                       f"and id_saldo = {id_saldo};")

        conecta.commit()
        print("Fatura encerrada!!")

    else:
        print("Essa fatura não existe!")


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
