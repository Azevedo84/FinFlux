from banco_dados.conexao_nuvem import conectar_banco_nuvem
from datetime import datetime, timedelta
import calendar

conecta = conectar_banco_nuvem()

try:
    lista_final = []

    # Obtendo a data atual para a fatura
    data_atual = datetime.now()
    fatura_atual = data_atual.strftime("%m/%Y")
    # Obtendo o ano e mês atuais
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    primeiro_dia_mes = datetime(ano_atual, mes_atual, 1)
    ultimo_dia_mes_numero = calendar.monthrange(ano_atual, mes_atual)[1]
    ultimo_dia_atual = datetime(ano_atual, mes_atual, ultimo_dia_mes_numero)

    # Formatando as datas para o formato 'YYYY-MM-DD'
    ini_atual = primeiro_dia_mes.strftime('%Y-%m-%d')
    fim_atual = ultimo_dia_atual.strftime('%Y-%m-%d')

    # Descobre o próximo mês e ano
    if data_atual.month == 12:  # se for dezembro
        prox_mes = 1
        ano = data_atual.year + 1
    else:
        prox_mes = data_atual.month + 1
        ano = data_atual.year

    ini_prox = datetime(ano, prox_mes, 1)
    ultimo_dia = calendar.monthrange(ano, prox_mes)[1]
    fim_prox = datetime(ano, prox_mes, ultimo_dia) + timedelta(days=1)  # fim exclusivo

    cursor = conecta.cursor()
    cursor.execute(f"SELECT mov.data, mov.qtde_ent "
                   f"FROM movimentacao AS mov "
                   f"WHERE mov.DATA >= '{ini_atual}' "
                   f"AND mov.DATA < '{fim_atual}' "
                   f"and mov.id_categoria = 4 or mov.id_categoria = 3;")
    lista_pagamentos_atual = cursor.fetchall()

    if not lista_pagamentos_atual:
        dados = (mes_atual + 1, f"Pagamento", f"05/{mes_atual}/2025", 2300, "")
        lista_final.append(dados)

    cursor = conecta.cursor()
    cursor.execute(f"SELECT mov.data, mov.qtde_ent "
                   f"FROM movimentacao AS mov "
                   f"WHERE mov.DATA >= '{ini_atual}' "
                   f"AND mov.DATA < '{fim_atual}' "
                   f"and mov.id_categoria = 2;")
    lista_adiantamentos_atual = cursor.fetchall()

    if not lista_adiantamentos_atual:
        dados = (mes_atual, f"Adiantamento", f"21/{mes_atual}/2025", 1100, "")
        lista_final.append(dados)

    cursor = conecta.cursor()
    cursor.execute(f"""
        SELECT mov.data, mov.qtde_ent
        FROM movimentacao AS mov
        WHERE mov.DATA >= '{ini_prox .strftime("%Y-%m-%d")}'
          AND mov.DATA < '{fim_prox.strftime("%Y-%m-%d")}'
          AND (mov.id_categoria = 3 OR mov.id_categoria = 4);
    """)
    lista_pagamentos_proximo_mes = cursor.fetchall()

    if not lista_pagamentos_proximo_mes:
        dados = (mes_atual + 1, f"Pagamento", f"05/{mes_atual + 1}/2025", 2300, "")
        lista_final.append(dados)

    cursor = conecta.cursor()
    cursor.execute(f"""
            SELECT mov.data, mov.qtde_ent
            FROM movimentacao AS mov
            WHERE mov.DATA >= '{ini_prox.strftime("%Y-%m-%d")}'
              AND mov.DATA < '{fim_prox.strftime("%Y-%m-%d")}'
              AND (mov.id_categoria = 2);
        """)
    lista_adiantamentos_proximo_mes = cursor.fetchall()

    if not lista_adiantamentos_proximo_mes:
        dados = (mes_atual + 1, f"Adiantamento", f"21/{mes_atual + 1}/2025", 1100, "")
        lista_final.append(dados)

    # Conectando ao banco de dados e obtendo os dados de saldo bancário
    cursor = conecta.cursor()
    cursor.execute(f"SELECT sald.id, bc.descricao "
                   f"FROM saldo_banco as sald "
                   f"INNER JOIN cadastro_banco as bc ON sald.id_banco = bc.id "
                   f"WHERE sald.id_usuario = 1 "
                   f"AND sald.id_tipoconta = 1 "
                   f"ORDER BY bc.descricao;")
    dados_saldo = cursor.fetchall()
    # Processando os saldos e faturas
    if dados_saldo:
        for i in dados_saldo:
            id_saldo, nome_banco = i

            cursor = conecta.cursor()
            cursor.execute(f"SELECT id, mes, ano, DATE_FORMAT(vencimento, '%d/%m/%Y') "
                           f"FROM cadastro_fatura "
                           f"WHERE mes = {mes_atual} AND ano = {ano_atual} "
                           f"AND id_saldo = {id_saldo};")
            dados_faturas = cursor.fetchall()
            if dados_faturas:
                for ii in dados_faturas:
                    id_fatura, mes_fatura, ano_fatura, venc = ii

                    cursor = conecta.cursor()
                    cursor.execute(f"""
                        SELECT COALESCE(SUM(qtde_sai), 0) AS total_saida
                        FROM movimentacao
                        WHERE id_fatura = {id_fatura}
                          AND id_saldo = {id_saldo};
                    """)
                    total_saida = cursor.fetchone()[0]

                    dados = (mes_fatura, f"Fatura {nome_banco}", venc, "", total_saida)
                    lista_final.append(dados)

        if lista_final:
            # 🔽 aqui você insere a função e ordenação
            def chave_ordenacao(item):
                mes, tipo, data, entrada, saida = item
                data_convertida = datetime.strptime(data, "%d/%m/%Y") if isinstance(data, str) else data
                # Critério:
                # 1) ordenar pela data
                # 2) entradas primeiro (se entrada tem valor → prioridade 0, senão 1)
                prioridade = 0 if entrada else 1
                return data_convertida, prioridade

            lista_final.sort(key=chave_ordenacao)

            # Agora percorre a lista já ordenada
            for iii in lista_final:
                mes, tipo, data, entrada, saida = iii
                print(iii)

finally:
    if 'conexao' in locals():
        conecta.close()