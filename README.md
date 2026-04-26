# Stock Market Analytics Platform

A backend-driven financial analytics platform built with Python and FastAPI that fetches real stock market data, stores it persistently, and generates technical indicators and trading signals. This project was created to strengthen my backend development, API design, and financial data processing skills through a practical real-world application. It allows users to retrieve historical stock data, store it in SQLite, and analyze trends using indicators such as SMA-44 and SMA-200. I built the project using Python, FastAPI, SQLite, Pandas, yFinance, and Matplotlib. While developing it, I worked through backend routing, database design, API testing, and data visualization, which helped improve my understanding of scalable backend systems and technical problem solving.

## Features
- Fetch real-time and historical stock market data
- Store data using SQLite for persistence
- Compute SMA-44 and SMA-200 technical indicators
- Generate buy/sell signals using moving average crossovers
- Visualize stock trends with automated charts
- Build RESTful API endpoints using FastAPI

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
- `GET /chart/{symbol}` – Generate a price and SMA chart

## How to Run Locally
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload

video demo: 
https://youtu.be/neeOaTlEjLY
