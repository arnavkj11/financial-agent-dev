from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from enum import Enum

class TimeRange(str, Enum):
    LAST_24H = "1d"
    LAST_7D = "7d"
    LAST_30D = "30d"
    LAST_3M = "3m"
    LAST_6M = "6m"
    LAST_1Y = "1y"
    ALL_TIME = "all"

class CategoryStat(BaseModel):
    category: str
    amount: float
    percentage: float

class TrendPoint(BaseModel):
    period: str # "2024-01-01" or "2024-01" depending on granularity
    amount: float

class DashboardStats(BaseModel):
    total_spent: float
    top_category: Optional[str] = None
    category_breakdown: List[CategoryStat]
    monthly_trend: List[TrendPoint]
