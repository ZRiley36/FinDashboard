"""Pydantic model for stock quotes."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Quote(BaseModel):
    """Model for real-time stock quotes."""
    
    symbol: str = Field(..., description="Stock symbol")
    current_price: float = Field(..., alias="c", description="Current price")
    change: float = Field(..., alias="d", description="Change amount")
    percent_change: float = Field(..., alias="dp", description="Percent change")
    high_price: float = Field(..., alias="h", description="High price of the day")
    low_price: float = Field(..., alias="l", description="Low price of the day")
    open_price: float = Field(..., alias="o", description="Open price of the day")
    previous_close: float = Field(..., alias="pc", description="Previous close price")
    timestamp: Optional[int] = Field(None, alias="t", description="Unix timestamp")
    ingested_at: datetime = Field(default_factory=datetime.now, description="When data was ingested")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

