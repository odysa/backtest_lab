import recur_back_test
import utils

if __name__ == "__main__":
    tickers = ["voo", "qqq", "spy", "upro"]
    for ticker in tickers:
        data = utils.fetch_ticker_data(ticker)
        recur_test = recur_back_test.RecurBackTest(
            ticker,
            data,
            recur_back_test.RecurConfig(
                frequency=recur_back_test.Frequency.WEEKLY,
                amount=1000,
                day=0,
            ),
        )
        stats = recur_test.run()
        recur_test.print_stats(stats)