
import pandas as pd
from sqlalchemy import create_engine, text

def insert_data():
    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5433/demo_db')
    url = 'https://docs.google.com/spreadsheets/d/1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8/export?format=csv'
    data = pd.read_csv(url)

    # Ensure correct data types
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['open'] = pd.to_numeric(data['open'], errors='coerce')
    data['high'] = pd.to_numeric(data['high'], errors='coerce')
    data['low'] = pd.to_numeric(data['low'], errors='coerce')
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['volume'] = pd.to_numeric(data['volume'], errors='coerce')

    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
            INSERT INTO ticker_data (datetime, instrument, open, high, low, close, volume)
            VALUES (:datetime, :instrument, :open, :high, :low, :close, :volume)
            """),
            {
                'datetime': row['datetime'],
                'instrument': row['instrument'],
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            })

if __name__ == "__main__":
    insert_data()
