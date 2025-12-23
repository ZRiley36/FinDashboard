"""Configuration settings for the market data pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "market_data.duckdb"
DATABASE_DIR.mkdir(exist_ok=True)

# Logging configuration
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "pipeline.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# API configuration
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise ValueError("FINNHUB_API_KEY environment variable is not set.")

# API rate limits (Finnhub free tier: 60 calls/minute)
API_RATE_LIMIT_CALLS = 60
API_RATE_LIMIT_PERIOD = 60  # seconds
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 1  # seconds

# Data retention settings (in days)
DATA_RETENTION_DAYS = 365

# Scheduler configuration
SCHEDULER_TIMEZONE = "America/New_York"

# Job intervals (in minutes)
QUOTE_UPDATE_INTERVAL = 5  # Update quotes every 5 minutes
PROFILE_UPDATE_INTERVAL = 60  # Update company profiles hourly
FINANCIALS_UPDATE_INTERVAL = 1440  # Update financials daily

# Symbols to track (can be overridden)
DEFAULT_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

