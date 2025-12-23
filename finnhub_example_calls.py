import finnhub
import os
from dotenv import load_dotenv

load_dotenv()

# Setup client
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise ValueError("FINNHUB_API_KEY environment variable is not set. Please create a .env file with your API key.")

finnhub_client = finnhub.Client(api_key=API_KEY)

# Real-time quote (High Usage, available)
print('Quote:', finnhub_client.quote('AAPL'))

# Company profile (free version) and peers/basic financials/earnings
print('Company profile2:', finnhub_client.company_profile2(symbol='AAPL'))
print('Peers:', finnhub_client.company_peers('AAPL'))
print('Basic financials:', finnhub_client.company_basic_financials('AAPL', 'all'))
print('Earnings (surprises):', finnhub_client.company_earnings('TSLA', limit=5))
print('Company news (1y):', finnhub_client.company_news('AAPL', _from="2024-12-01", to="2025-12-01"))

# Market & news
print('General news:', finnhub_client.general_news('general', min_id=0))
print('Earnings calendar (1 month):', finnhub_client.earnings_calendar(_from="2020-06-10", to="2020-06-30", symbol="", international=False))

# Symbols & lookup
print('Stock symbols sample:', finnhub_client.stock_symbols('US')[0:5])
print('Symbol lookup:', finnhub_client.symbol_lookup('apple'))

# Crypto & Forex basic lists
print('Crypto exchanges:', finnhub_client.crypto_exchanges())
print('Crypto symbols sample:', finnhub_client.crypto_symbols('BINANCE')[0:5])
print('Forex exchanges:', finnhub_client.forex_exchanges())
print('Forex symbols sample:', finnhub_client.forex_symbols('OANDA')[0:5])

# Country, covid and economic metadata
print('Country list sample:', finnhub_client.country()[0:5])
print('COVID-19 summary:', finnhub_client.covid19())

# Financials as reported (new) and recommendation trends
print('Financials reported:', finnhub_client.financials_reported(symbol='AAPL', freq='annual'))
print('Recommendation trends:', finnhub_client.recommendation_trends('AAPL'))

# Market status / holiday
print('Market status:', finnhub_client.market_status(exchange='US'))
print('Market holidays:', finnhub_client.market_holiday(exchange='US'))

