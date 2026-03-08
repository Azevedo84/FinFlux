import yfinance as yf
import pandas as pd

TICKERS = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "WEGE3.SA",
    "BBAS3.SA"
]

def verificar_hoje(ticker):
    df = yf.download(ticker, period="1y", interval="1d", progress=False)

    if df.empty or len(df) < 200:
        return None

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
        return {
            "Ticker": ticker,
            "Preço Atual": round(preco, 2),
            "Queda 5 dias (%)": round(queda * 100, 2)
        }

    return None


print("\n🔎 Verificando oportunidades HOJE...\n")

sinais = []

for ticker in TICKERS:
    resultado = verificar_hoje(ticker)
    if resultado:
        sinais.append(resultado)

if sinais:
    for s in sinais:
        print("✅ SINAL ENCONTRADO:")
        print(s)
else:
    print("❌ Nenhuma oportunidade hoje.")