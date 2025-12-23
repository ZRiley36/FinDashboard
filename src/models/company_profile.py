"""Pydantic model for company profiles."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompanyProfile(BaseModel):
    """Model for company profile information."""
    
    symbol: str = Field(..., description="Stock symbol")
    company_name: Optional[str] = Field(None, alias="name", description="Company name")
    country: Optional[str] = Field(None, description="Country")
    currency: Optional[str] = Field(None, description="Currency")
    exchange: Optional[str] = Field(None, description="Exchange")
    ipo: Optional[str] = Field(None, description="IPO date")
    market_capitalization: Optional[float] = Field(None, alias="marketCapitalization", description="Market cap")
    share_outstanding: Optional[float] = Field(None, alias="shareOutstanding", description="Shares outstanding")
    website: Optional[str] = Field(None, description="Company website")
    phone: Optional[str] = Field(None, description="Phone number")
    industry: Optional[str] = Field(None, description="Industry")
    logo: Optional[str] = Field(None, description="Logo URL")
    finnhub_industry: Optional[str] = Field(None, alias="finnhubIndustry", description="Finnhub industry")
    ticker: Optional[str] = Field(None, description="Ticker symbol")
    ingested_at: datetime = Field(default_factory=datetime.now, description="When data was ingested")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

