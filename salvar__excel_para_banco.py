import pandas as pd
import math
from conexao_nuvem import conectar_banco_nuvem


conecta = conectar_banco_nuvem()

arquivo_excel = 'Pasta1.xlsx'

dados = pd.read_excel(arquivo_excel)

lista_dados = dados.values.tolist()

for linha in lista_dados:
    data, banco, tipo_conta, grupo, categoria, entradas, saidas, estabelecimento, observacao = linha

    datas = pd.to_datetime(data).strftime('%Y-%m-%d')

    bancotete = banco.find(" - ")
    id_banco = banco[:bancotete]

    tipo_contatete = tipo_conta.find(" - ")
    id_tipo = tipo_conta[:tipo_contatete]

    grupotete = grupo.find(" - ")
    id_grupo = grupo[:grupotete]

    categoriatete = categoria.find(" - ")
    id_categoria = categoria[:categoriatete]

    if math.isnan(entradas):
        float_ent = 0.0
    else:
        float_ent = entradas

    if math.isnan(saidas):
        float_sai = 0.0
    else:
        float_sai = saidas

    estabelecimentotete = estabelecimento.find(" - ")
    id_estab = estabelecimento[:estabelecimentotete]

    if type(observacao) == float:
        obs_maiusculo = ""
    else:
        obs_maiusculo = observacao.upper()

    cursor = conecta.cursor()
    cursor.execute(f'SELECT id, id_estab '
                   f'FROM cadastro_banco '
                   f'where id = {id_banco};')
    lista_completa = cursor.fetchall()
    id_estab1 = lista_completa[0][1]

    cursor = conecta.cursor()
    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                   f"where id_usuario = 1 "
                   f"and id_banco = {id_banco} "
                   f"and id_tipoconta = {id_tipo};")
    saldo_conta = cursor.fetchall()
    id_saldo, saldo = saldo_conta[0]

    print(linha)

    cursor = conecta.cursor()
    cursor.execute(f'SELECT * FROM movimentacao '
                   f'where id_saldo = {id_saldo} '
                   f'and data = "{datas}" '
                   f'and qtde_ent = "{float_ent}" '
                   f'and qtde_sai = "{float_sai} '
                   f'and id_estab = {id_estab}";')
    lista_movimentacao = cursor.fetchall()

    if not lista_movimentacao:
        cursor = conecta.cursor()
        cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                       f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                       f'values ("{datas}", {id_saldo}, {id_categoria}, '
                       f'{float_ent}, {float_sai}, {id_estab}, 19, "{obs_maiusculo}");')
    
        if id_categoria == "7":
            cursor = conecta.cursor()
            cursor.execute(f'SELECT id, id_estab '
                           f'FROM cadastro_banco '
                           f'where id_estab = {id_estab};')
            lista_completa = cursor.fetchall()
            id_banco2 = lista_completa[0][0]

            cursor = conecta.cursor()
            cursor.execute(f"SELECT ID_BANCO, ID_TIPOCONTA FROM liga_banco_tipo "
                           f"where id_banco = {id_banco2} and ID_TIPOCONTA <> 1;")
            define_tipo = cursor.fetchall()
            if define_tipo:
                if len(define_tipo) == 1:
                    id_tipo2 = define_tipo[0][1]

                    cursor = conecta.cursor()
                    cursor.execute(f"SELECT id, saldo FROM saldo_banco "
                                   f"where id_usuario = 1 "
                                   f"and id_banco = {id_banco2} "
                                   f"and id_tipoconta = {id_tipo2};")
                    saldo_conta2 = cursor.fetchall()
                    id_saldo2, saldo2 = saldo_conta2[0]

                    cursor = conecta.cursor()
                    cursor.execute(f'SELECT * FROM movimentacao '
                                   f'where id_saldo = {id_saldo2} '
                                   f'and data = "{datas}" '
                                   f'and qtde_ent = "{float_sai}" '
                                   f'and qtde_sai = "{float_ent} '
                                   f'and id_estab = {id_estab1}";')
                    lista_movimentacao2 = cursor.fetchall()
                    if not lista_movimentacao2:
                        cursor = conecta.cursor()
                        cursor.execute(f'Insert into movimentacao (data, id_saldo, '
                                       f'id_categoria, qtde_ent, qtde_sai, id_estab, id_cidade, obs) '
                                       f'values ("{datas}", {id_saldo2}, {id_categoria}, '
                                       f'{float_sai}, {float_ent}, {id_estab1}, 19, "{obs_maiusculo}");')
                else:
                    print("DEFINIR QUAL O TIPOCONTA")
                    print(define_tipo)
                    break
    
        conecta.commit()
        print("LANÇADO", "\n\n")

if 'conexao' in locals():
    conecta.close()