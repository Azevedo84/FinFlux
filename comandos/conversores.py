from comandos.notificacao import tratar_notificar_erros
import os
import inspect
import locale

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivo = os.path.basename(nome_arquivo_com_caminho)


def valores_para_float(string):
    try:
        if string is None:
            return 0.00

        string_certo = str(string)

        if "R$ " in string_certo:
            limpa_string = string_certo.replace("R$ ", '')
        elif "%" in string_certo:
            limpa_string = string_certo.replace("%", '')
        else:
            limpa_string = string_certo

        if limpa_string:
            if "," in limpa_string and "." in limpa_string:
                string_com_ponto = limpa_string.replace('.', '')
                string_com_ponto = string_com_ponto.replace(',', '.')
                valor_float = float(string_com_ponto)
            elif "," in limpa_string:
                string_com_ponto = limpa_string.replace(',', '.')
                valor_float = float(string_com_ponto)
            else:
                valor_float = float(limpa_string)
        else:
            valor_float = 0.00

        return valor_float

    except ValueError:
        # Se a conversão falhar, retornar 0.00 e logar o erro
        nome_funcao = inspect.currentframe().f_code.co_name
        print(f"Valor inválido para conversão: {string}", nome_funcao, nome_arquivo)
        return 0.00
    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)
        return 0.00

def valores_para_int(string):
    try:
        if string is None:
            return 0.00

        string_certo = str(string)

        if "R$ " in string_certo:
            limpa_string = string_certo.replace("R$ ", '')
        elif "%" in string_certo:
            limpa_string = string_certo.replace("%", '')
        else:
            limpa_string = string_certo

        if limpa_string:
            if "," in limpa_string and "." in limpa_string:
                string_com_ponto = limpa_string.replace('.', '')
                string_com_ponto = string_com_ponto.replace(',', '.')
                valor_float = float(string_com_ponto)
            elif "," in limpa_string:
                string_com_ponto = limpa_string.replace(',', '.')
                valor_float = float(string_com_ponto)
            else:
                valor_float = float(limpa_string)
        else:
            valor_float = 0.00

        valor_int = int(valor_float)

        return valor_int

    except ValueError:
        # Se a conversão falhar, retornar 0.00 e logar o erro
        nome_funcao = inspect.currentframe().f_code.co_name
        print(f"Valor inválido para conversão: {string}", nome_funcao, nome_arquivo)
        return 0.00
    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)
        return 0.00

def valores_para_virgula(string):
    try:
        string = str(string)
        if "R$ " in string:
            limpa_string = string.replace("R$ ", '')
        elif "%" in string:
            limpa_string = string.replace("%", '')
        else:
            limpa_string = string

        if limpa_string:
            if "." in limpa_string:
                string_com_virgula = limpa_string.replace('.', ',')
            else:
                string_com_virgula = limpa_string
        else:
            string_com_virgula = "0,00"

        # 🔹 Ajuste extra: se começar com vírgula, adicionar 0 na frente
        if string_com_virgula.startswith(","):
            string_com_virgula = "0" + string_com_virgula

        return string_com_virgula

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)

def float_para_virgula(valor_float):
    try:
        if valor_float:
            limpa_string = str(valor_float)
        else:
            limpa_string = "0"

        if limpa_string:
            if "." in limpa_string:
                string_com_virgula = limpa_string.replace('.', ',')
            else:
                string_com_virgula = limpa_string
        else:
            string_com_virgula = "0,00"

        return string_com_virgula

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)

def float_para_moeda_reais_com_4_casas(valor):
    try:
        valor_float = valores_para_float(valor)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Formata manualmente com 4 casas decimais e separadores locais
        valor_formatado = f"R$ {valor_float:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")

        return valor_formatado

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)

def float_para_moeda_reais(valor):
    try:
        valor_float = valores_para_float(valor)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        valor_final = locale.currency(valor_float, grouping=True, symbol=True)

        return valor_final

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)

def moeda_reais_para_float(valor_moeda):
    try:
        # Remove o símbolo da moeda e os separadores de milhar
        valor_moeda = valor_moeda.replace('R$', '').replace('.', '').replace(',', '.')

        # Converte a string para float
        valor_float = float(valor_moeda.strip())

        return valor_float

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)

def data_banco_para_brasileiro(data_banco):
    try:
        data_brasil = data_banco.strftime("%d/%m/%Y")

        return data_brasil

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)
