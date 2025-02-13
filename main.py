import recur_back_test
import utils

if __name__ == "__main__":
    tickers = ["voo", "qqq", "spy", "brk-b", "ko", "gld", "upro", "BTC-USD"]
    stats_map = {}
    for ticker in tickers:
        data = utils.fetch_ticker_data(ticker)
        recur_test = recur_back_test.RecurBackTest(
            ticker,
            data,
            recur_back_test.RecurConfig(
                frequency=recur_back_test.Frequency.WEEKLY,
                amount=100,
                day=2,
            ),
        )
        stats = recur_test.run()
        stats_map[ticker] = stats
        recur_test.print_stats()
