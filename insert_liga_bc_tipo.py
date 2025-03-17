from conexao_nuvem import conectar_banco_nuvem

# 1 - CARTÃO DE CREDITO / 2 - CONTA CORRENTE / 3 - INVESTIMENTOS / 4 - VALE ALIMENTACAO / 6 - DOLAR


conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f'INSERT INTO `liga_banco_tipo`(`ID_BANCO`, `ID_TIPOCONTA`) VALUES (26, 2);')

    conecta.commit()


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
