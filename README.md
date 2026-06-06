# FinDashboard

A Python script that pulls real-time market data from the Finnhub API — quotes, company financials, news — and surfaces it as a single dashboard view.

## Stack
Python · Finnhub API · [Streamlit / Flask / Rich / whatever you're using]

## What it does
- Pulls live quotes for a watchlist of tickers
- Fetches company-level financials (earnings, revenue) on demand
- [add: what the user actually sees — terminal table? web page? CSV?]

## Run it
```bash
git clone https://github.com/ZRiley36/FinDashboard.git
cd FinDashboard
pip install -r requirements.txt
export FINNHUB_API_KEY=your_key  # see config.py
python main.py
```

## Status
Early-stage. Currently fetches and prints data; next milestone is a charted view of the watchlist over a 30-day window.
