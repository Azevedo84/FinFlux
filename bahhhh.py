import re
import pandas as pd

# Dados copiados do PDF
dados = """
CLB DE
01/07/2022
01/07/2025
110,00
R$ 7.539,00
R$ 10.385,84
R$ 9.958,82
CLE
CDB PRE
07/07/2022
07/07/2025
14,48
R$ 262,46
R$ 367,63
R$ 351,86
PRE
CDB PRE
01/08/2022
02/08/2027
13,50
R$ 1.200,00
R$ 1.631,26
R$ 1.566,58
PRE
CDB DE
05/12/2022
05/12/2025
110,00
R$ 2.400,00
R$ 3.115,91
R$ 3.008,53
CDX
CDB DE
07/12/2022
08/12/2025
110,00
R$ 50,00
R$ 64,84
R$ 62,62
CDE
CDB DI
03/03/2023
03/03/2026
110,00
R$ 1.302,00
R$ 1.632,85
R$ 1.574,96
CDE
CDB DE
21/03/2023
21/03/2025
110,00
R$ 294,92
R$ 367,39
R$ 354,71
CLE
CDS DI
04/05/2023
04/05/2026
110,00
R$ 1.300,00
R$ 1.593,43
R$ 1.542,08
CDE
CDB DE
05/06/2023
05/06/2026
110,00
R$ 200,00
R$ 242,15
R$ 234,78
CDE
CDB DE
22/06/2023
22/06/2026
110,00
R$ 500,00
R$ 601,33
R$ 583,60
CDE
CLB PRE
05/07/2023
05/07/2028
11,00
R$ 200,00
R$ 233,98
R$ 228,04
PRE
CIB PRE
21/08/2023
21/08/2028
11,20
R$ 2.083,82
R$ 2,410,80
R$ 2.353,58
PRE
CDB PRE
06/09/2023
08/09/2026
11,30
R$ 1.320,00
R$ 1.521,24
R$ 1.486,03
PRE
CIB DI
06/11/2023
08/11/2027
113,00
R$ 150,00
R$ 172,11
R$ 168,25
CDE
CDB DI
22/11/2023
24/11/2025
115,00
R$ 1.354,77
R$ 1.549,34
R$ 1.515,30
CDE
CDB PRE
29/01/2024
29/01/2025
11,20
R$ 4.543,67
R$ 5,020,73
R$ 4.925,32
PRE
CDB PRE
01/02/2024
03/02/2025
11,20
R$ 1.384,43
R$ 1.527,85
R$ 1.499,17
PRE
CDB PRE
05/02/2024
05/02/2025
10,50
R$ 2.873,03
R$ 3.149,64
R$ 3.094,32
PRE
CDB PRE
06/03/2024
07/03/2029
11,40
R$ 1.412,00
R$ 1.546,24
R$ 1.519,40
PRE
CDB DE
11/03/2024
12/03/2027
110,00
R$ 1.438,36
R$ 1.578,46
R$ 1.550,44
CDE
CDB DE
01/04/2024
02/04/2027
110,00
R$ 55,85
R$ 60,90
R$ 59,89
CDE
CDS DE
03/04/2024
05/04/2027
110,00
R$ 2.792,49
R$ 3.042,42
R$ 2.992,44
CDE
CIB DE
05/04/2024
06/04/2027
110,00
R$ 1.461,07
R$ 1.590,43
R$ 1.564,56
CLE
CDB PRE
05/07/2024
21/06/2027
13,10
R$ 4.477,07
R$ 4.765,95
R$ 4.708,18
PRE
CDB PRE
23/07/2024
28/06/2029
12,80
R$ 250,96
R$ 265,26
R$ 262,05
PRE
CDB PRE
02/08/2024
19/07/2027
12,70
R$ 1.323,65
R$ 1.393,24
R$ 1.377,59
PRE
CDB IPCA
05/09/2024
23/08/2027
06,60
R$ 1.910,00
R$ 1.983,47
R$ 1.966,94
IPCA
CDB PRE
05/11/2024
06/11/2028
13,60
R$ 1.400,00
R$ 1.429,34
R$ 1.422,74
PRE
CDB PRE
11/11/2024
03/11/2026
13,00
R$ 165,20
R$ 168,19
R$ 167,52
PRE
CDB PRE
05/12/2024
05/12/2028
12,40
R$ 2.841,89
R$ 2.869,70
R$ 2.863,45
PRE
CLB PRE
09/12/2024
30/11/2026
13,90
R$ 600,00
R$ 605,91
R$ 604,45
PRE
СТВ ІРСА
02/01/2025
02/01/2026
06,50
R$ 3.000,00
R$ 3.004,82
R$ 3.000,64
IPCA
CDB PRE
02/01/2025
06/07/2026
14,90
R$ 3.000,00
R$ 3.004,96
R$ 3.000,66
PRE
"""  # Substitua pelo restante dos seus dados

# Dividir os dados em linhas
linhas = dados.split("\n")

# Variáveis auxiliares
registros = []
registro_atual = []

# Processar as linhas
for linha in linhas:
    linha = linha.strip()
    if not linha:
        continue  # Ignorar linhas vazias

    # Identificar início de um novo registro (supondo que comece com "CDB" ou algo similar)
    if re.match(r"^CDB|^COB|^CDS", linha):
        if registro_atual:
            registros.append(registro_atual)
        registro_atual = [linha]
    else:
        registro_atual.append(linha)

# Adicionar o último registro
if registro_atual:
    registros.append(registro_atual)

# Combinar os registros em uma estrutura tabular
tabela = []
for registro in registros:
    if len(registro) == 8:
        tabela.append(registro)

# Criar um DataFrame pandas
colunas = ["Produto", "Investido em", "Vencimento", "Taxa", "Valor Investido", "Valor Bruto", "Valor Líquido",
           "Indexador"]
df = pd.DataFrame(tabela, columns=colunas)

# Salvar como Excel (opcional)
df.to_excel("investimentos.xlsx", index=False)

# Mostrar o DataFrame
print(df)
