"""Main entry point for the market data pipeline with APScheduler."""

import signal
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz
from src.pipeline.data_pipeline import DataPipeline
from src.utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class PipelineScheduler:
    """Manages scheduled pipeline jobs."""
    
    def __init__(self):
        """Initialize the scheduler and pipeline."""
        self.scheduler = BlockingScheduler(timezone=pytz.timezone(config.SCHEDULER_TIMEZONE))
        self.pipeline = DataPipeline()
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(sig, frame):
            logger.info("Shutdown signal received, stopping scheduler...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _job_quotes(self):
        """Job function to ingest quotes."""
        try:
            logger.info("Starting scheduled quotes ingestion job")
            self.pipeline.ingest_quotes()
            logger.info("Scheduled quotes ingestion job completed")
        except Exception as e:
            logger.error(f"Error in scheduled quotes ingestion job: {e}")
    
    def _job_company_profiles(self):
        """Job function to ingest company profiles."""
        try:
            logger.info("Starting scheduled company profiles ingestion job")
            self.pipeline.ingest_company_profiles()
            logger.info("Scheduled company profiles ingestion job completed")
        except Exception as e:
            logger.error(f"Error in scheduled company profiles ingestion job: {e}")
    
    def _job_financials(self):
        """Job function to ingest financials."""
        try:
            logger.info("Starting scheduled financials ingestion job")
            self.pipeline.ingest_basic_financials()
            self.pipeline.ingest_financials_reported()
            logger.info("Scheduled financials ingestion job completed")
        except Exception as e:
            logger.error(f"Error in scheduled financials ingestion job: {e}")
    
    def start(self):
        """Start the scheduler with configured jobs."""
        # Add jobs
        self.scheduler.add_job(
            self._job_quotes,
            trigger=IntervalTrigger(minutes=config.QUOTE_UPDATE_INTERVAL),
            id="quotes_job",
            name="Quotes Ingestion",
            replace_existing=True
        )
        
        self.scheduler.add_job(
            self._job_company_profiles,
            trigger=IntervalTrigger(minutes=config.PROFILE_UPDATE_INTERVAL),
            id="profiles_job",
            name="Company Profiles Ingestion",
            replace_existing=True
        )
        
        self.scheduler.add_job(
            self._job_financials,
            trigger=IntervalTrigger(minutes=config.FINANCIALS_UPDATE_INTERVAL),
            id="financials_job",
            name="Financials Ingestion",
            replace_existing=True
        )
        
        logger.info("Scheduler started with the following jobs:")
        logger.info(f"  - Quotes: every {config.QUOTE_UPDATE_INTERVAL} minutes")
        logger.info(f"  - Company Profiles: every {config.PROFILE_UPDATE_INTERVAL} minutes")
        logger.info(f"  - Financials: every {config.FINANCIALS_UPDATE_INTERVAL} minutes")
        
        # Run initial ingestion
        logger.info("Running initial data ingestion...")
        try:
            self.pipeline.run_full_pipeline()
            logger.info("Initial data ingestion completed")
        except Exception as e:
            logger.error(f"Error in initial data ingestion: {e}")
        
        # Start scheduler
        logger.info("Starting scheduler...")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler interrupted")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the scheduler and close connections."""
        logger.info("Shutting down scheduler...")
        self.scheduler.shutdown()
        self.pipeline.close()
        logger.info("Shutdown complete")


def main():
    """Main entry point."""
    logger.info("Starting Market Data Pipeline")
    
    scheduler = PipelineScheduler()
    try:
        scheduler.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        scheduler.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    main()

