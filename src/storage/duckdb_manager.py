"""DuckDB storage manager for market data."""

import duckdb
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import polars as pl
from src.utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class DuckDBManager:
    """Manages DuckDB database operations."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize DuckDB connection.
        
        Args:
            db_path: Path to DuckDB database file. Defaults to config.DATABASE_PATH
        """
        self.db_path = db_path or config.DATABASE_PATH
        self.conn = duckdb.connect(str(self.db_path))
        self._initialize_schema()
        logger.info(f"Initialized DuckDB connection: {self.db_path}")
    
    def _initialize_schema(self):
        """Create database tables if they don't exist."""
        # Quotes table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                symbol VARCHAR NOT NULL,
                current_price DOUBLE,
                change_amount DOUBLE,
                percent_change DOUBLE,
                high_price DOUBLE,
                low_price DOUBLE,
                open_price DOUBLE,
                previous_close DOUBLE,
                timestamp BIGINT,
                ingested_at TIMESTAMP NOT NULL,
                PRIMARY KEY (symbol, timestamp)
            )
        """)
        
        # Company profiles table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS company_profiles (
                symbol VARCHAR PRIMARY KEY,
                company_name VARCHAR,
                country VARCHAR,
                currency VARCHAR,
                exchange VARCHAR,
                ipo VARCHAR,
                market_capitalization DOUBLE,
                share_outstanding DOUBLE,
                website VARCHAR,
                phone VARCHAR,
                industry VARCHAR,
                logo VARCHAR,
                finnhub_industry VARCHAR,
                ticker VARCHAR,
                ingested_at TIMESTAMP NOT NULL
            )
        """)
        
        # Basic financials table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS basic_financials (
                symbol VARCHAR NOT NULL,
                metric_type VARCHAR,
                metric_data JSON,
                series_data JSON,
                ingested_at TIMESTAMP NOT NULL,
                PRIMARY KEY (symbol, ingested_at)
            )
        """)
        
        # Financials reported table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS financials_reported (
                symbol VARCHAR NOT NULL,
                cik VARCHAR,
                data JSON,
                ingested_at TIMESTAMP NOT NULL,
                PRIMARY KEY (symbol, ingested_at)
            )
        """)
        
        logger.info("Database schema initialized")
    
    def insert_quote(self, quote_data: Dict[str, Any]) -> None:
        """
        Insert or update a quote record.
        
        Args:
            quote_data: Dictionary containing quote data
        """
        try:
            self.conn.execute("""
                INSERT INTO quotes (
                    symbol, current_price, change_amount, percent_change,
                    high_price, low_price, open_price, previous_close,
                    timestamp, ingested_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                quote_data.get("symbol"),
                quote_data.get("current_price"),
                quote_data.get("change_amount"),
                quote_data.get("percent_change"),
                quote_data.get("high_price"),
                quote_data.get("low_price"),
                quote_data.get("open_price"),
                quote_data.get("previous_close"),
                quote_data.get("timestamp"),
                quote_data.get("ingested_at", datetime.now())
            ])
            logger.debug(f"Inserted quote for {quote_data.get('symbol')}")
        except Exception as e:
            logger.error(f"Error inserting quote: {e}")
            raise
    
    def insert_company_profile(self, profile_data: Dict[str, Any]) -> None:
        """
        Insert or update a company profile.
        
        Args:
            profile_data: Dictionary containing company profile data
        """
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO company_profiles (
                    symbol, company_name, country, currency, exchange,
                    ipo, market_capitalization, share_outstanding,
                    website, phone, industry, logo, finnhub_industry,
                    ticker, ingested_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                profile_data.get("symbol"),
                profile_data.get("company_name"),
                profile_data.get("country"),
                profile_data.get("currency"),
                profile_data.get("exchange"),
                profile_data.get("ipo"),
                profile_data.get("market_capitalization"),
                profile_data.get("share_outstanding"),
                profile_data.get("website"),
                profile_data.get("phone"),
                profile_data.get("industry"),
                profile_data.get("logo"),
                profile_data.get("finnhub_industry"),
                profile_data.get("ticker"),
                profile_data.get("ingested_at", datetime.now())
            ])
            logger.debug(f"Inserted/updated company profile for {profile_data.get('symbol')}")
        except Exception as e:
            logger.error(f"Error inserting company profile: {e}")
            raise
    
    def insert_basic_financials(self, financials_data: Dict[str, Any]) -> None:
        """
        Insert basic financials data.
        
        Args:
            financials_data: Dictionary containing financials data
        """
        try:
            import json
            self.conn.execute("""
                INSERT INTO basic_financials (
                    symbol, metric_type, metric_data, series_data, ingested_at
                ) VALUES (?, ?, ?, ?, ?)
            """, [
                financials_data.get("symbol"),
                financials_data.get("metric_type"),
                json.dumps(financials_data.get("metric_data")) if financials_data.get("metric_data") else None,
                json.dumps(financials_data.get("series_data")) if financials_data.get("series_data") else None,
                financials_data.get("ingested_at", datetime.now())
            ])
            logger.debug(f"Inserted basic financials for {financials_data.get('symbol')}")
        except Exception as e:
            logger.error(f"Error inserting basic financials: {e}")
            raise
    
    def insert_financials_reported(self, financials_data: Dict[str, Any]) -> None:
        """
        Insert reported financials data.
        
        Args:
            financials_data: Dictionary containing reported financials data
        """
        try:
            import json
            self.conn.execute("""
                INSERT INTO financials_reported (
                    symbol, cik, data, ingested_at
                ) VALUES (?, ?, ?, ?)
            """, [
                financials_data.get("symbol"),
                financials_data.get("cik"),
                json.dumps(financials_data.get("data")) if financials_data.get("data") else None,
                financials_data.get("ingested_at", datetime.now())
            ])
            logger.debug(f"Inserted reported financials for {financials_data.get('symbol')}")
        except Exception as e:
            logger.error(f"Error inserting reported financials: {e}")
            raise
    
    def query(self, sql: str) -> pl.DataFrame:
        """
        Execute a SQL query and return results as Polars DataFrame.
        
        Args:
            sql: SQL query string
            
        Returns:
            Polars DataFrame with query results
        """
        try:
            result = self.conn.execute(sql).fetchdf()
            return pl.from_pandas(result)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def get_latest_quotes(self, symbol: Optional[str] = None) -> pl.DataFrame:
        """
        Get the latest quotes for a symbol or all symbols.
        
        Args:
            symbol: Stock symbol (optional)
            
        Returns:
            Polars DataFrame with latest quotes
        """
        if symbol:
            sql = f"""
                SELECT * FROM quotes
                WHERE symbol = '{symbol}'
                ORDER BY timestamp DESC
                LIMIT 1
            """
        else:
            sql = """
                SELECT * FROM (
                    SELECT *,
                           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp DESC) as rn
                    FROM quotes
                ) WHERE rn = 1
            """
        return self.query(sql)
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
        logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

