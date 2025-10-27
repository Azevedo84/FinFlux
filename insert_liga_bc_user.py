from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f'INSERT INTO `liga_banco_usuario`(`ID_BANCO`, `ID_USUARIO`) VALUES (20, 1);')

    conecta.commit()


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
