

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text


def get_connection():
    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5433/demo_db')
    return engine.connect()


def analyze_data():
    conn = get_connection()
    query = "SELECT * FROM ticker_data ORDER BY datetime"
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Compute RSI
    def compute_rsi(series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Compute MACD
    def compute_macd(series, short_window=12, long_window=26, signal_window=9):
        short_ema = series.ewm(span=short_window, adjust=False).mean()
        long_ema = series.ewm(span=long_window, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    # Calculate RSI
    data['RSI'] = compute_rsi(data['close'])

    # Calculate MACD
    data['MACD_Line'], data['Signal_Line'], data['Histogram'] = compute_macd(data['close'])

    # Define buy and sell signals
    data['Buy_Signal'] = ((data['RSI'] < 30) & (data['MACD_Line'] > data['Signal_Line'])).astype(int)
    data['Sell_Signal'] = ((data['RSI'] > 70) & (data['MACD_Line'] < data['Signal_Line'])).astype(int)

    buy_signals = data[data['Buy_Signal'] == 1]
    sell_signals = data[data['Sell_Signal'] == 1]

    print(f"Number of Buy Signals: {len(buy_signals)}")
    print(f"Number of Sell Signals: {len(sell_signals)}")

    # Optionally, you can also print the buy and sell signals for verification
    print("\nBuy Signals:")
    print(buy_signals[['datetime', 'close', 'RSI', 'MACD_Line', 'Signal_Line']])

    print("\nSell Signals:")
    print(sell_signals[['datetime', 'close', 'RSI', 'MACD_Line', 'Signal_Line']])


if __name__ == "__main__":
    analyze_data()
