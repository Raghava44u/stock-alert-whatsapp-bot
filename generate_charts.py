import yfinance as yf
import matplotlib.pyplot as plt
import os

# Folder to store charts
CHART_DIR = "charts"

def generate_chart(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="5m")  # 1-day chart, 5-min intervals

    if hist.empty:
        return None

    plt.figure(figsize=(8, 4))
    plt.plot(hist.index, hist["Close"], label=f"{ticker} Price", color="blue")
    plt.title(f"{ticker} Price Chart - Today")
    plt.xlabel("Time")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.legend()

    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)

    filepath = os.path.join(CHART_DIR, f"{ticker}.png")
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return filepath
