from fastapi import FastAPI
from backend.services import (
    create_table,
    fetch_and_store_stock,
    get_stock_data,
    get_stock_indicators,
    get_trade_signals,
    generate_stock_chart
)


app = FastAPI(title="Stock Market Analytics Platform")

@app.on_event("startup")
def startup():
    create_table()

@app.get("/")
def home():
    return {"message": "API is running successfully"}

@app.post("/fetch/{symbol}")
def fetch_stock(symbol: str):
    fetch_and_store_stock(symbol)
    return {"status": "Data fetched", "symbol": symbol}
from backend.services import get_stock_data

@app.get("/stocks/{symbol}")
def read_stock(symbol: str):
    return get_stock_data(symbol)

@app.get("/indicators/{symbol}")
def indicators(symbol: str):
    return get_stock_indicators(symbol)

@app.get("/signals/{symbol}")
def signals(symbol: str):
    return get_trade_signals(symbol)

@app.get("/chart/{symbol}")
def chart(symbol: str):
    return generate_stock_chart(symbol)



