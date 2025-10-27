from banco_dados.conexao_nuvem import conectar_banco_nuvem

conecta = conectar_banco_nuvem()
try:
    cursor = conecta.cursor()
    cursor.execute(f'INSERT INTO `cadastro_cartao`(`ID_BANCO`, `ID_USUARIO`, `LIMITE`, `VENCIMENTO`) '
                   f'VALUES (12, 1, "14550", 7);')

    conecta.commit()


except Exception as e:
    print(e)

finally:
    if 'conexao' in locals():
        conecta.close()
