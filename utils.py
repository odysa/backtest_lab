import os
from dataclasses import dataclass

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
@dataclass
class TestStatistics:
    num_trades: int
    avg_price: float
    current_price: float
    total_invested: float
    current_equity: float
    current_shares: int
    total_return: float
    total_return_pct: float

    def print(self):
        print(f"Number of trades: {self.num_trades}")
        print(f"Average price: {self.avg_price}")
        print(f"Current price: {self.current_price}")
        print(f"Total invested: {self.total_invested}")
        print(f"Current equity: {self.current_equity}")
        print(f"Current shares: {self.current_shares}")
        print(f"Total return: {self.total_return}")
        print(f"Total return %: {self.total_return_pct}")

