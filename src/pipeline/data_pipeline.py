"""Main data pipeline orchestration."""

from typing import List, Optional
from src.ingestion.finnhub_client import FinnhubClient
from src.storage.duckdb_manager import DuckDBManager
from src.transformation.transformers import DataTransformer
from src.utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class DataPipeline:
    """Orchestrates the data pipeline: ingest → transform → store."""
    
    def __init__(self):
        """Initialize the pipeline with clients and transformers."""
        self.finnhub_client = FinnhubClient()
        self.db_manager = DuckDBManager()
        self.transformer = DataTransformer()
        logger.info("Data pipeline initialized")
    
    def ingest_quotes(self, symbols: Optional[List[str]] = None) -> None:
        """
        Ingest quotes data for given symbols.
        
        Args:
            symbols: List of stock symbols. Defaults to config.DEFAULT_SYMBOLS
        """
        symbols = symbols or config.DEFAULT_SYMBOLS
        logger.info(f"Starting quotes ingestion for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                # Ingest
                raw_data = self.finnhub_client.get_quote(symbol)
                
                # Transform
                transformed_data = self.transformer.transform_quote_data(raw_data)
                
                if transformed_data:
                    # Store
                    self.db_manager.insert_quote(transformed_data)
                    logger.info(f"Successfully ingested quote for {symbol}")
                else:
                    logger.warning(f"No data returned for quote {symbol}")
                    
            except Exception as e:
                logger.error(f"Error ingesting quote for {symbol}: {e}")
                continue
        
        logger.info("Quotes ingestion completed")
    
    def ingest_company_profiles(self, symbols: Optional[List[str]] = None) -> None:
        """
        Ingest company profiles for given symbols.
        
        Args:
            symbols: List of stock symbols. Defaults to config.DEFAULT_SYMBOLS
        """
        symbols = symbols or config.DEFAULT_SYMBOLS
        logger.info(f"Starting company profiles ingestion for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                # Ingest
                raw_data = self.finnhub_client.get_company_profile(symbol)
                
                # Transform
                transformed_data = self.transformer.transform_company_profile_data(raw_data)
                
                if transformed_data:
                    # Store
                    self.db_manager.insert_company_profile(transformed_data)
                    logger.info(f"Successfully ingested company profile for {symbol}")
                else:
                    logger.warning(f"No data returned for company profile {symbol}")
                    
            except Exception as e:
                logger.error(f"Error ingesting company profile for {symbol}: {e}")
                continue
        
        logger.info("Company profiles ingestion completed")
    
    def ingest_basic_financials(self, symbols: Optional[List[str]] = None) -> None:
        """
        Ingest basic financials for given symbols.
        
        Args:
            symbols: List of stock symbols. Defaults to config.DEFAULT_SYMBOLS
        """
        symbols = symbols or config.DEFAULT_SYMBOLS
        logger.info(f"Starting basic financials ingestion for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                # Ingest
                raw_data = self.finnhub_client.get_basic_financials(symbol)
                
                # Transform
                transformed_data = self.transformer.transform_basic_financials_data(raw_data)
                
                if transformed_data:
                    # Store
                    self.db_manager.insert_basic_financials(transformed_data)
                    logger.info(f"Successfully ingested basic financials for {symbol}")
                else:
                    logger.warning(f"No data returned for basic financials {symbol}")
                    
            except Exception as e:
                logger.error(f"Error ingesting basic financials for {symbol}: {e}")
                continue
        
        logger.info("Basic financials ingestion completed")
    
    def ingest_financials_reported(self, symbols: Optional[List[str]] = None, freq: str = "annual") -> None:
        """
        Ingest reported financials for given symbols.
        
        Args:
            symbols: List of stock symbols. Defaults to config.DEFAULT_SYMBOLS
            freq: Frequency (annual or quarterly)
        """
        symbols = symbols or config.DEFAULT_SYMBOLS
        logger.info(f"Starting reported financials ingestion for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                # Ingest
                raw_data = self.finnhub_client.get_financials_reported(symbol, freq=freq)
                
                # Transform
                transformed_data = self.transformer.transform_financials_reported_data(raw_data)
                
                if transformed_data:
                    # Store
                    self.db_manager.insert_financials_reported(transformed_data)
                    logger.info(f"Successfully ingested reported financials for {symbol}")
                else:
                    logger.warning(f"No data returned for reported financials {symbol}")
                    
            except Exception as e:
                logger.error(f"Error ingesting reported financials for {symbol}: {e}")
                continue
        
        logger.info("Reported financials ingestion completed")
    
    def run_full_pipeline(self, symbols: Optional[List[str]] = None) -> None:
        """
        Run the complete pipeline for all data types.
        
        Args:
            symbols: List of stock symbols. Defaults to config.DEFAULT_SYMBOLS
        """
        symbols = symbols or config.DEFAULT_SYMBOLS
        logger.info(f"Running full pipeline for {len(symbols)} symbols")
        
        try:
            self.ingest_quotes(symbols)
            self.ingest_company_profiles(symbols)
            self.ingest_basic_financials(symbols)
            self.ingest_financials_reported(symbols)
            logger.info("Full pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error in full pipeline execution: {e}")
            raise
    
    def close(self):
        """Close database connections."""
        self.db_manager.close()
        logger.info("Pipeline closed")

