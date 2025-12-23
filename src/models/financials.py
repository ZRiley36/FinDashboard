"""Pydantic model for company financials."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class FinancialMetric(BaseModel):
    """Model for individual financial metrics."""
    
    value: Optional[float] = None
    period: Optional[str] = None


class BasicFinancials(BaseModel):
    """Model for basic financials data."""
    
    symbol: str = Field(..., description="Stock symbol")
    metric_type: str = Field(..., alias="metricType", description="Type of metric")
    series: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Financial series data")
    metric: Optional[Dict[str, Any]] = Field(None, description="Current metrics")
    ingested_at: datetime = Field(default_factory=datetime.now, description="When data was ingested")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class FinancialsReported(BaseModel):
    """Model for reported financials."""
    
    symbol: str = Field(..., description="Stock symbol")
    cik: Optional[str] = Field(None, description="CIK identifier")
    data: Optional[list] = Field(None, description="Financial data array")
    ingested_at: datetime = Field(default_factory=datetime.now, description="When data was ingested")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

