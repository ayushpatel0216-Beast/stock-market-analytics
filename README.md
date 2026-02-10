# Stock Market Analytics Platform

A backend-driven financial analytics platform built with Python and FastAPI that
fetches real stock market data, stores it persistently, and generates technical
indicators and trading signals.

## Features
- Fetch real-time and historical stock market data
- Store data using SQLite for persistence
- Compute SMA-44 and SMA-200 technical indicators
- Generate buy/sell signals using moving average crossovers
- Visualize stock trends with automated charts
- RESTful API built with FastAPI

## Tech Stack
- Python
- FastAPI
- SQLite
- Pandas
- yFinance
- Matplotlib

## API Endpoints
- `POST /fetch/{symbol}` – Fetch and store stock data
- `GET /stocks/{symbol}` – Retrieve stored stock prices
- `GET /indicators/{symbol}` – View SMA-44 and SMA-200 indicators
- `GET /signals/{symbol}` – Get buy/sell crossover signals
- `GET /chart/{symbol}` – Generate price & SMA chart

## How to Run Locally
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
