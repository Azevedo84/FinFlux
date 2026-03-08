import yfinance as yf
import pandas as pd

TICKERS = [
    "PETR4.SA","VALE3.SA","ITUB4.SA","BBDC4.SA","BBAS3.SA",
    "SANB11.SA","CPFE3.SA","EQTL3.SA","TAEE11.SA",
    "WEGE3.SA","RADL3.SA","LREN3.SA","GGBR4.SA",
    "CSNA3.SA","RAIL3.SA","HAPV3.SA","RDOR3.SA",
    "VIVT3.SA","SBSP3.SA","B3SA3.SA"
]

STOP = 0.08
ALVO = 0.12

resultados_por_ticker = {}

for ticker in TICKERS:

    print(f"Rodando {ticker}...")
    df = yf.download(ticker, period="5y", interval="1d", progress=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty or len(df) < 200:
        continue

    df["MM21"] = df["Close"].rolling(21).mean()
    df["MM200"] = df["Close"].rolling(200).mean()
    df["Vol_Media"] = df["Volume"].rolling(21).mean()

    df = df.dropna()

    ganhos = 0
    perdas = 0
    total_trades = 0

    for i in range(200, len(df)-1):

        preco = float(df["Close"].iloc[i])
        mm21 = float(df["MM21"].iloc[i])
        mm200 = float(df["MM200"].iloc[i])
        volume = float(df["Volume"].iloc[i])
        vol_media = float(df["Vol_Media"].iloc[i])
        preco_5 = float(df["Close"].iloc[i - 5])
        queda = (preco_5 - preco) / preco_5

        tendencia = (preco > mm200) and (mm21 > mm200)
        queda_ok = 0.05 <= queda <= 0.10
        volume_ok = volume > vol_media

        if tendencia and queda_ok and volume_ok:

            entrada = float(df["Close"].iloc[i+1])
            stop = entrada * (1 - STOP)
            alvo = entrada * (1 + ALVO)

            for j in range(i+1, len(df)):

                preco_saida = float(df["Close"].iloc[j])

                if preco_saida >= alvo:
                    ganhos += 1
                    total_trades += 1
                    break

                elif preco_saida <= stop:
                    perdas += 1
                    total_trades += 1
                    break

    if total_trades > 0:

        taxa_acerto = ganhos / total_trades
        expectativa = (taxa_acerto * ALVO) - ((1 - taxa_acerto) * STOP)

        resultados_por_ticker[ticker] = {
            "Trades": total_trades,
            "Taxa_Acerto": round(taxa_acerto * 100, 2),
            "Expectativa_%": round(expectativa * 100, 2)
        }

print("\n===== RESULTADO POR TICKER =====\n")

for ticker, dados in sorted(resultados_por_ticker.items(),
                             key=lambda x: x[1]["Expectativa_%"],
                             reverse=True):

    print(f"{ticker} | Trades: {dados['Trades']} | "
          f"Acerto: {dados['Taxa_Acerto']}% | "
          f"Expectativa: {dados['Expectativa_%']}%")