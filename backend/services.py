import yfinance as yf
from backend.database import get_db_connection

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT,
            open_price REAL,
            close_price REAL,
            high_price REAL,
            low_price REAL,
            volume INTEGER
        )
    """)

    conn.commit()
    conn.close()

def fetch_and_store_stock(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1y")

    conn = get_db_connection()
    cursor = conn.cursor()

    for date, row in data.iterrows():
        cursor.execute("""
            INSERT INTO stocks 
            (symbol, date, open_price, close_price, high_price, low_price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            str(date.date()),
            float(row["Open"]),
            float(row["Close"]),
            float(row["High"]),
            float(row["Low"]),
            int(row["Volume"])
        ))

    conn.commit()
    conn.close()
def get_stock_data(symbol: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, open_price, close_price, high_price, low_price, volume
        FROM stocks
        WHERE symbol = ?
        ORDER BY date DESC
        LIMIT 10
    """, (symbol,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


import pandas as pd

def get_stock_indicators(symbol: str):
    conn = get_db_connection()

    df = pd.read_sql(
        """
        SELECT date, close_price
        FROM stocks
        WHERE symbol = ?
        ORDER BY date
        """,
        conn,
        params=(symbol,)
    )

    conn.close()

    if df.empty:
        return {"error": "No data found for symbol"}

    df["SMA_44"] = df["close_price"].rolling(window=44).mean()
    df["SMA_200"] = df["close_price"].rolling(window=200).mean()


    return df.tail(10).to_dict(orient="records")

def get_trade_signals(symbol: str):
    conn = get_db_connection()

    df = pd.read_sql(
        """
        SELECT date, close_price
        FROM stocks
        WHERE symbol = ?
        ORDER BY date
        """,
        conn,
        params=(symbol,)
    )

    conn.close()

    if len(df) < 200:
        return {"error": "Not enough data for SMA-200"}

    df["SMA_44"] = df["close_price"].rolling(window=44).mean()
    df["SMA_200"] = df["close_price"].rolling(window=200).mean()

    df["signal"] = "HOLD"

    for i in range(1, len(df)):
        if (
            df.loc[i, "SMA_44"] > df.loc[i, "SMA_200"]
            and df.loc[i - 1, "SMA_44"] <= df.loc[i - 1, "SMA_200"]
        ):
            df.loc[i, "signal"] = "BUY"

        elif (
            df.loc[i, "SMA_44"] < df.loc[i, "SMA_200"]
            and df.loc[i - 1, "SMA_44"] >= df.loc[i - 1, "SMA_200"]
        ):
            df.loc[i, "signal"] = "SELL"

    return df.tail(10)[
        ["date", "close_price", "SMA_44", "SMA_200", "signal"]
    ].to_dict(orient="records")

import matplotlib.pyplot as plt
import os

def generate_stock_chart(symbol: str):
    conn = get_db_connection()

    df = pd.read_sql(
        """
        SELECT date, close_price
        FROM stocks
        WHERE symbol = ?
        ORDER BY date
        """,
        conn,
        params=(symbol,)
    )

    conn.close()

    if len(df) < 200:
        return {"error": "Not enough data for SMA-200 chart"}

    df["SMA_44"] = df["close_price"].rolling(window=44).mean()
    df["SMA_200"] = df["close_price"].rolling(window=200).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["close_price"], label="Close Price")
    plt.plot(df["date"], df["SMA_44"], label="SMA 44")
    plt.plot(df["date"], df["SMA_200"], label="SMA 200")

    plt.title(f"{symbol} Price with SMA 44 & SMA 200")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs("charts", exist_ok=True)
    file_path = f"charts/{symbol}_chart.png"
    plt.savefig(file_path)
    plt.close()

    return {"message": "Chart generated", "file": file_path}
