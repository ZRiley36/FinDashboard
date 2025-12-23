"""Data transformation utilities using Polars."""

import polars as pl
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataTransformer:
    """Handles data transformations using Polars."""
    
    @staticmethod
    def transform_quote_data(quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform quote data from API format to database format.
        
        Args:
            quote_data: Raw quote data from API
            
        Returns:
            Transformed quote data dictionary
        """
        if not quote_data or quote_data.get("c") is None:
            return None
        
        return {
            "symbol": quote_data.get("symbol", ""),
            "current_price": float(quote_data.get("c", 0)),
            "change_amount": float(quote_data.get("d", 0)),
            "percent_change": float(quote_data.get("dp", 0)),
            "high_price": float(quote_data.get("h", 0)),
            "low_price": float(quote_data.get("l", 0)),
            "open_price": float(quote_data.get("o", 0)),
            "previous_close": float(quote_data.get("pc", 0)),
            "timestamp": quote_data.get("t"),
            "ingested_at": datetime.now()
        }
    
    @staticmethod
    def transform_company_profile_data(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform company profile data from API format to database format.
        
        Args:
            profile_data: Raw company profile data from API
            
        Returns:
            Transformed company profile data dictionary
        """
        if not profile_data:
            return None
        
        return {
            "symbol": profile_data.get("symbol", ""),
            "company_name": profile_data.get("name"),
            "country": profile_data.get("country"),
            "currency": profile_data.get("currency"),
            "exchange": profile_data.get("exchange"),
            "ipo": profile_data.get("ipo"),
            "market_capitalization": profile_data.get("marketCapitalization"),
            "share_outstanding": profile_data.get("shareOutstanding"),
            "website": profile_data.get("weburl"),
            "phone": profile_data.get("phone"),
            "industry": profile_data.get("industry"),
            "logo": profile_data.get("logo"),
            "finnhub_industry": profile_data.get("finnhubIndustry"),
            "ticker": profile_data.get("ticker"),
            "ingested_at": datetime.now()
        }
    
    @staticmethod
    def transform_basic_financials_data(financials_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform basic financials data from API format to database format.
        
        Args:
            financials_data: Raw basic financials data from API
            
        Returns:
            Transformed basic financials data dictionary
        """
        if not financials_data:
            return None
        
        return {
            "symbol": financials_data.get("symbol", ""),
            "metric_type": financials_data.get("metricType", "all"),
            "metric_data": financials_data.get("metric"),
            "series_data": financials_data.get("series"),
            "ingested_at": datetime.now()
        }
    
    @staticmethod
    def transform_financials_reported_data(financials_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform reported financials data from API format to database format.
        
        Args:
            financials_data: Raw reported financials data from API
            
        Returns:
            Transformed reported financials data dictionary
        """
        if not financials_data:
            return None
        
        return {
            "symbol": financials_data.get("symbol", ""),
            "cik": financials_data.get("cik"),
            "data": financials_data.get("data"),
            "ingested_at": datetime.now()
        }
    
    @staticmethod
    def clean_quotes_dataframe(df: pl.DataFrame) -> pl.DataFrame:
        """
        Clean and normalize a quotes Polars DataFrame.
        
        Args:
            df: Polars DataFrame with quote data
            
        Returns:
            Cleaned DataFrame
        """
        if df.is_empty():
            return df
        
        # Remove rows with null prices
        df = df.filter(pl.col("current_price").is_not_null())
        
        # Ensure numeric columns are properly typed
        numeric_cols = [
            "current_price", "change_amount", "percent_change",
            "high_price", "low_price", "open_price", "previous_close"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df = df.with_columns(pl.col(col).cast(pl.Float64))
        
        # Sort by timestamp
        if "timestamp" in df.columns:
            df = df.sort("timestamp", descending=True)
        
        return df
    
    @staticmethod
    def aggregate_quotes_by_symbol(df: pl.DataFrame) -> pl.DataFrame:
        """
        Aggregate quotes data by symbol, keeping the latest entry.
        
        Args:
            df: Polars DataFrame with quote data
            
        Returns:
            Aggregated DataFrame
        """
        if df.is_empty():
            return df
        
        return (
            df.sort("timestamp", descending=True)
            .group_by("symbol")
            .first()
        )
    
    @staticmethod
    def calculate_price_changes(df: pl.DataFrame) -> pl.DataFrame:
        """
        Calculate additional price change metrics.
        
        Args:
            df: Polars DataFrame with quote data
            
        Returns:
            DataFrame with additional calculated columns
        """
        if df.is_empty():
            return df
        
        return df.with_columns([
            (pl.col("current_price") - pl.col("previous_close")).alias("price_change_from_close"),
            ((pl.col("current_price") - pl.col("previous_close")) / pl.col("previous_close") * 100).alias("percent_change_from_close"),
            (pl.col("high_price") - pl.col("low_price")).alias("day_range")
        ])

