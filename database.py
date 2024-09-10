# scripts/database.py

from sqlalchemy import create_engine, text

def get_engine():
    return create_engine('postgresql+psycopg2://postgres:root@localhost:5433/demo_db')

def get_connection():
    return get_engine().connect()

def create_table():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ticker_data (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP NOT NULL,
            instrument VARCHAR(255) NOT NULL,
            open DECIMAL NOT NULL,
            high DECIMAL NOT NULL,
            low DECIMAL NOT NULL,
            close DECIMAL NOT NULL,
            volume INTEGER NOT NULL
        );
        """))

if __name__ == "__main__":
    create_table()
