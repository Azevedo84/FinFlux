import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# ==============================
# CONFIGURAÇÃO DO FUNDO
# ==============================

TICKERS = [
    # Energia / Commodities
    "PETR4.SA",
    "VALE3.SA",

    # Bancos
    "ITUB4.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "SANB11.SA",

    # Energia Elétrica
    "CPFE3.SA",
    "EQTL3.SA",
    "TAEE11.SA",

    # Consumo Forte
    "WEGE3.SA",
    "RADL3.SA",
    "LREN3.SA",

    # Indústria / Infra
    "GGBR4.SA",
    "CSNA3.SA",
    "RAIL3.SA",

    # Saúde
    "HAPV3.SA",
    "RDOR3.SA",

    # Telecom
    "VIVT3.SA",

    # Saneamento
    "SBSP3.SA",

    # Bolsa
    "B3SA3.SA"
]

ARQUIVO_LOG = "registro_operacoes.csv"

STOP_PERCENTUAL = 0.08
ALVO_PERCENTUAL = 0.12


# ==============================
# FUNÇÃO FILTRO MACRO (IBOV)
# ==============================

def mercado_favoravel():
    ibov = yf.download("^BVSP", period="1y", interval="1d", progress=False)

    if ibov.empty or len(ibov) < 200:
        return False

    ibov["MM200"] = ibov["Close"].rolling(200).mean()
    ibov = ibov.dropna()

    hoje = ibov.iloc[-1]

    preco = hoje["Close"].item()
    mm200 = hoje["MM200"].item()

    return preco > mm200


# ==============================
# FUNÇÃO REGISTRO
# ==============================

def registrar_operacao(ticker, preco):

    stop = round(preco * (1 - STOP_PERCENTUAL), 2)
    alvo = round(preco * (1 + ALVO_PERCENTUAL), 2)
    data = datetime.now().strftime("%Y-%m-%d")

    nova_linha = {
        "Data": data,
        "Ticker": ticker,
        "Entrada": preco,
        "Stop": stop,
        "Alvo": alvo,
        "Status": "ABERTA"
    }

    df_novo = pd.DataFrame([nova_linha])

    if os.path.exists(ARQUIVO_LOG):
        df_existente = pd.read_csv(ARQUIVO_LOG)

        # Evita duplicar operação aberta
        abertas = df_existente[
            (df_existente["Ticker"] == ticker) &
            (df_existente["Status"] == "ABERTA")
        ]

        if not abertas.empty:
            print(f"⚠ Já existe operação aberta em {ticker}")
            return

        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = df_novo

    df_final.to_csv(ARQUIVO_LOG, index=False)

    print(f"📁 Operação registrada: {ticker}")
    print(f"Entrada: {preco} | Stop: {stop} | Alvo: {alvo}")


# ==============================
# FUNÇÃO SCANNER
# ==============================

def verificar_hoje(ticker):

    df = yf.download(ticker, period="1y", interval="1d", progress=False)

    if df.empty or len(df) < 200:
        return

    df["MM21"] = df["Close"].rolling(21).mean()
    df["MM200"] = df["Close"].rolling(200).mean()
    df["Vol_Media"] = df["Volume"].rolling(21).mean()

    df = df.dropna()

    hoje = df.iloc[-1]
    cinco_dias_atras = df.iloc[-6]

    preco = hoje["Close"].item()
    mm21 = hoje["MM21"].item()
    mm200 = hoje["MM200"].item()
    volume = hoje["Volume"].item()
    vol_media = hoje["Vol_Media"].item()

    preco_5 = cinco_dias_atras["Close"].item()
    queda = (preco_5 - preco) / preco_5

    tendencia = (preco > mm200) and (mm21 > mm200)
    queda_ok = 0.05 <= queda <= 0.10
    volume_ok = volume > vol_media

    if tendencia and queda_ok and volume_ok:
        print(f"\n✅ SINAL ENCONTRADO EM {ticker}")
        print(f"Preço atual: {round(preco,2)}")
        print(f"Queda 5 dias: {round(queda*100,2)}%")

        registrar_operacao(ticker, round(preco, 2))


# ==============================
# EXECUÇÃO
# ==============================

print("\n🔎 MINI FUNDO - VERIFICAÇÃO DIÁRIA\n")

if not mercado_favoravel():
    print("🚫 IBOV abaixo da MM200. Sistema BLOQUEADO.")
else:
    print("✅ IBOV acima da MM200. Mercado favorável.\n")

    for ticker in TICKERS:
        verificar_hoje(ticker)

print("\n🏁 Fim da execução.\n")