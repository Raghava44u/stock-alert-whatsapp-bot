import yfinance as yf
import pandas as pd
import json

def load_config():
    with open("config.json") as f:
        return json.load(f)

def get_top_stocks():
    config = load_config()
    tickers = config["tracked_stocks"]
    
    data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="1m")

        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            open_price = hist['Open'].iloc[0]
            percent_change = ((current_price - open_price) / open_price) * 100

            data.append({
                "symbol": ticker,
                "current": round(current_price, 2),
                "open": round(open_price, 2),
                "percent_change": round(percent_change, 2)
            })

    df = pd.DataFrame(data)
    top = df.sort_values(by="percent_change", ascending=False).head(5)
    return top
if __name__ == "__main__":
    top_stocks = get_top_stocks()
    print("🔥 Top 5 Performing US Stocks Today:\n")
    print(top_stocks.to_string(index=False))
