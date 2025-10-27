from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    # BRADESCO = 5 / C6 = 6 / NUBANK = 12 / XP = 19 / SAMSUNG = 22 / AMAZON = 27

    id_banco = 27
    mes = "10"
    ano = "2025"
    vencimento = "2025-11-15"

    cursor = conecta.cursor()
    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                   f"where id_usuario = 1 and "
                   f"id_banco = {id_banco} and "
                   f"id_tipoconta = 1;")
    saldo_conta = cursor.fetchall()
    id_saldo, saldo = saldo_conta[0]

    cursor = conecta.cursor()
    cursor.execute(f"INSERT INTO cadastro_fatura (ID_SALDO, MES, ANO, VENCIMENTO, VALOR_FINAL, STATUS) "
                   f"VALUES ({id_saldo}, '{mes}', '{ano}', '{vencimento}', 0, 'A');")

    conecta.commit()
    print("SALVO FATURA")


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
