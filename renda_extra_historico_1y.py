import yfinance as yf
import pandas as pd
import numpy as np

# =============================
# CONFIGURAÇÃO
# =============================

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

STOP = -0.08
ALVO = 0.12

# =============================
# FUNÇÃO BACKTEST
# =============================

def backtest(ticker):
    df = yf.download(ticker, period="1y", interval="1d", progress=False)

    if df.empty or len(df) < 250:
        return None

    df["MM21"] = df["Close"].rolling(21).mean()
    df["MM200"] = df["Close"].rolling(200).mean()
    df["Vol_Media"] = df["Volume"].rolling(21).mean()

    df = df.dropna()

    trades = []

    for i in range(200, len(df) - 1):

        preco = df["Close"].iloc[i].item()
        mm21 = df["MM21"].iloc[i].item()
        mm200 = df["MM200"].iloc[i].item()
        volume = df["Volume"].iloc[i].item()
        vol_media = df["Vol_Media"].iloc[i].item()

        preco_5_dias = df["Close"].iloc[i - 5].item()
        queda = (preco_5_dias - preco) / preco_5_dias

        tendencia = (preco > mm200) and (mm21 > mm200)
        queda_ok = 0.05 <= queda <= 0.10
        volume_ok = volume > vol_media

        if tendencia and queda_ok and volume_ok:

            entrada = df["Close"].iloc[i + 1].item()

            for j in range(i + 1, len(df)):
                preco_saida = df["Close"].iloc[j].item()
                variacao = (preco_saida - entrada) / entrada

                if variacao >= ALVO:
                    trades.append(ALVO)
                    break
                elif variacao <= STOP:
                    trades.append(STOP)
                    break

    return trades

# =============================
# EXECUÇÃO
# =============================

todos_trades = []

for ticker in TICKERS:
    print(f"Rodando {ticker}...")
    resultado = backtest(ticker)
    if resultado:
        todos_trades.extend(resultado)

if len(todos_trades) > 0:
    trades = np.array(todos_trades)
    taxa_acerto = len(trades[trades > 0]) / len(trades)
    retorno_total = trades.sum()
    ganho_medio = trades[trades > 0].mean() if len(trades[trades > 0]) > 0 else 0
    perda_media = trades[trades < 0].mean() if len(trades[trades < 0]) > 0 else 0

    print("\n===== RESULTADO BACKTEST =====")
    print("Total de Trades:", len(trades))
    print("Taxa de Acerto:", round(taxa_acerto * 100, 2), "%")
    print("Retorno Total (soma simples):", round(retorno_total * 100, 2), "%")
    print("Ganho Médio:", round(ganho_medio * 100, 2), "%")
    print("Perda Média:", round(perda_media * 100, 2), "%")
else:
    print("Nenhum trade encontrado.")