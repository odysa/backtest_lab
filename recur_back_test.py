import math
from dataclasses import dataclass
from enum import Enum

import pandas as pd
from backtesting import Backtest, Strategy
from matplotlib import pyplot as plt

NORM = 1000000


class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class RecurConfig:
    frequency: Frequency
    amount: int
    day: int | None = None


class RecurBackTest:
    def __init__(self, ticker: str, data: pd.DataFrame, config: RecurConfig):
        if (
            config.frequency in [Frequency.WEEKLY, Frequency.MONTHLY]
            and config.day is None
        ):
            raise ValueError(
                "Day of week/month must be specified for weekly/monthly frequency."
            )
        self.data = self.prepare_data(data)
        self.ticker = ticker
        self.frequency = config.frequency
        self.amount = config.amount
        self.day = config.day
        self.strategy = self.get_strategy()
        self.bt = Backtest(
            self.data,
            self.strategy,
            commission=0,
            exclusive_orders=True,
            trade_on_close=True,
            cash=2000000,
        )

    def prepare_data(self, data:pd.DataFrame):
        # 2010-09-09 00:00:00-04:00
        # data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
        # data.index = pd.to_datetime(data["Date"])
        data.reset_index(inplace=True)
        data.index =  pd.to_datetime(data["Date"], utc=True)

        return self.normalize(data)

    def normalize(self, data):
        data["Close"] /= NORM
        data["Open"] /= NORM
        data["High"] /= NORM
        data["Low"] /= NORM
        return data

    def get_strategy(self):
        if self.frequency == Frequency.DAILY:
            self.DailyInvestmentStrategy.amount_to_invest = self.amount
            return self.DailyInvestmentStrategy
        elif self.frequency == Frequency.WEEKLY:
            self.WeeklyInvestmentStrategy.amount_to_invest = self.amount
            self.WeeklyInvestmentStrategy.day_of_week = self.day
            return self.WeeklyInvestmentStrategy
        elif self.frequency == Frequency.MONTHLY:
            self.MonthlyInvestmentStrategy.amount_to_invest = self.amount
            self.MonthlyInvestmentStrategy.day_of_month = self.day
            return self.MonthlyInvestmentStrategy
        else:
            raise ValueError(
                "Invalid frequency. Choose from 'daily', 'weekly', or 'monthly'."
            )

    class DailyInvestmentStrategy(Strategy):
        amount_to_invest: int

        def init(self):
            pass

        def next(self):
            self.buy(size=math.floor(self.amount_to_invest / self.data.Close[-1]))

    class WeeklyInvestmentStrategy(Strategy):
        amount_to_invest: int
        day_of_month: int

        def init(self):
            self.current_day_of_week = self.I(
                lambda x: x, self.data.Close.s.index.dayofweek
            )

        def next(self):
            if self.current_day_of_week[-1] == self.day_of_week:
                self.buy(size=math.floor(self.amount_to_invest / self.data.Close[-1]))

    class MonthlyInvestmentStrategy(Strategy):
        amount_to_invest: int
        day_of_month: int

        def init(self):
            self.current_day_of_month = self.I(lambda x: x, self.data.Close.s.index.day)

        def next(self):
            if self.current_day_of_month[-1] == self.day_of_month:
                self.buy(size=math.floor(self.amount_to_invest / self.data.Close[-1]))

    def print_stats(self, stats):
        trades = stats["_trades"]
        price_paid = trades["Size"] * trades["EntryPrice"]
        total_invested = price_paid.sum()

        current_shares = trades["Size"].sum()
        current_equity = current_shares * self.data["Close"].iloc[-1]
        average_price = total_invested / current_shares
        print("Rucurring Investment Backtest for", self.ticker.upper())
        print("Date Range: ", self.data.index[0], " - ", self.data.index[-1])
        print(f"Number of Trades: {trades.shape[0]}")
        print(f"Average Price: {average_price * NORM}")
        print(f"Current Price: {self.data['Close'].iloc[-1] * NORM}")
        print(f"Total Invested: {total_invested}")
        print(f"Current Value: {current_equity}")
        print(f"Current Shares: {current_shares / NORM}")
        print(f"Total Return: {current_equity - total_invested}")
        print(
            f"Total Return %: {((current_equity - total_invested) / total_invested) * 100}"
        )
        print("---------------------------------------------")

    def print_equity_curve(self, stats):
        trades = stats["_trades"]
        cum_shares = trades["Size"].cumsum()
        cum_investment = cum_shares * trades["EntryPrice"]

        plt.figure(0)
        plt.plot(trades["EntryTime"], cum_investment, label="Equity")
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Equity")
        plt.title("Equity Curve")
        plt.savefig("equity.png")

    def run(self):
        stats = self.bt.run()
        return stats
