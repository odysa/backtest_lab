import os

import pandas as pd
import yfinance as yf


def fetch_ticker_data(ticker: str) -> pd.DataFrame:
    data_path = f"data/{ticker}.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    ticker: yf.Ticker = yf.Ticker(ticker)
    ticker_data = ticker.history(period="10y")
    ticker_data.to_csv(data_path)
    return ticker_data