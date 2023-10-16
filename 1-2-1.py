"""Utility functions"""

import os
import pandas as pd

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # Read CSV file for the symbol
        path = symbol_to_path(symbol)
        df_temp = pd.read_csv(path, index_col='Date',
                              parse_dates=True,
                              usecols=['Date', 'Adj Close'],
                              na_values=['nan'])

        # Rename the 'Adj Close' column to the symbol name
        df_temp = df_temp.rename(columns={'Adj Close': symbol})

        # Join the data for the symbol with the main DataFrame
        df = df.join(df_temp)

        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=['SPY'])

    return df


def test_run():
    # Define a Date range
    dates = pd.date_range('2022-10-17', '2023-10-13')

    # Choose stock symbols to read
    symbols = ['IBM', 'TSLA']

    # Get stock data
    df = get_data(symbols, dates)
    print(df)


if __name__ == "__main__":
    test_run()