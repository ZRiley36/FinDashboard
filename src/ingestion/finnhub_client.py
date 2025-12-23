"""Finnhub API client wrapper."""

import finnhub
import time
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class FinnhubClient:
    """Wrapper around Finnhub SDK with error handling and rate limiting."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Finnhub client.
        
        Args:
            api_key: Finnhub API key. Defaults to config.FINNHUB_API_KEY
        """
        self.api_key = api_key or config.FINNHUB_API_KEY
        if not self.api_key:
            raise ValueError("Finnhub API key is required")
        
        self.client = finnhub.Client(api_key=self.api_key)
        self.last_call_time = 0
        self.min_call_interval = config.API_RATE_LIMIT_PERIOD / config.API_RATE_LIMIT_CALLS
        logger.info("Finnhub client initialized")
    
    def _rate_limit(self):
        """Enforce rate limiting."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_call_interval:
            sleep_time = self.min_call_interval - time_since_last_call
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def _retry_request(self, func, *args, **kwargs):
        """
        Execute a request with retry logic.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
        """
        for attempt in range(config.API_RETRY_ATTEMPTS):
            try:
                self._rate_limit()
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < config.API_RETRY_ATTEMPTS - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}/{config.API_RETRY_ATTEMPTS}): {e}")
                    time.sleep(config.API_RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"Request failed after {config.API_RETRY_ATTEMPTS} attempts: {e}")
                    raise
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary containing quote data
        """
        logger.debug(f"Fetching quote for {symbol}")
        try:
            quote_data = self._retry_request(self.client.quote, symbol)
            quote_data["symbol"] = symbol
            return quote_data
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            raise
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary containing company profile data
        """
        logger.debug(f"Fetching company profile for {symbol}")
        try:
            profile_data = self._retry_request(self.client.company_profile2, symbol=symbol)
            if profile_data:
                profile_data["symbol"] = symbol
            return profile_data or {}
        except Exception as e:
            logger.error(f"Error fetching company profile for {symbol}: {e}")
            raise
    
    def get_basic_financials(self, symbol: str, metric: str = "all") -> Dict[str, Any]:
        """
        Get basic financials for a symbol.
        
        Args:
            symbol: Stock symbol
            metric: Metric type (default: "all")
            
        Returns:
            Dictionary containing basic financials data
        """
        logger.debug(f"Fetching basic financials for {symbol}")
        try:
            financials_data = self._retry_request(
                self.client.company_basic_financials,
                symbol=symbol,
                metric=metric
            )
            if financials_data:
                financials_data["symbol"] = symbol
                financials_data["metric_type"] = metric
            return financials_data or {}
        except Exception as e:
            logger.error(f"Error fetching basic financials for {symbol}: {e}")
            raise
    
    def get_financials_reported(self, symbol: str, freq: str = "annual") -> Dict[str, Any]:
        """
        Get reported financials for a symbol.
        
        Args:
            symbol: Stock symbol
            freq: Frequency (annual or quarterly)
            
        Returns:
            Dictionary containing reported financials data
        """
        logger.debug(f"Fetching reported financials for {symbol}")
        try:
            financials_data = self._retry_request(
                self.client.financials_reported,
                symbol=symbol,
                freq=freq
            )
            if financials_data:
                financials_data["symbol"] = symbol
            return financials_data or {}
        except Exception as e:
            logger.error(f"Error fetching reported financials for {symbol}: {e}")
            raise
    
    def get_quotes_batch(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get quotes for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary mapping symbols to quote data
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.get_quote(symbol)
            except Exception as e:
                logger.error(f"Failed to fetch quote for {symbol}: {e}")
                results[symbol] = None
        return results
    
    def get_company_profiles_batch(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get company profiles for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary mapping symbols to profile data
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.get_company_profile(symbol)
            except Exception as e:
                logger.error(f"Failed to fetch profile for {symbol}: {e}")
                results[symbol] = None
        return results

