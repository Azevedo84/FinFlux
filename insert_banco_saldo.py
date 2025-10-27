from banco_dados.conexao_nuvem import conectar_banco_nuvem

# 1 - CARTÃO DE CREDITO / 2 - CONTA CORRENTE / 3 - INVESTIMENTOS / 4 - VALE ALIMENTACAO / 6 - DOLAR


conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f'INSERT INTO `saldo_banco`(`ID_USUARIO`, `ID_BANCO`, `ID_TIPOCONTA`) VALUES (1, 27, 1);')

    conecta.commit()


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
