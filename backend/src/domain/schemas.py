from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from src.infrastructure.models import SourceType

class TransactionRead(BaseModel):
    id: str
    date: date
    amount: int
    merchant: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    source: str
    source_type: SourceType
    created_at: datetime

    class Config:
        from_attributes = True

class UploadSummary(BaseModel):
    imported: int
    skipped: int
    message: str

class WeeklyTrendData(BaseModel):
    week: str
    week_label: str
    categories: Dict[str, int]

class MonthlyWeeklyTrend(BaseModel):
    month: str
    weeks: List[WeeklyTrendData]

class SourceBreakdown(BaseModel):
    source: str
    amount: int
    percentage: float

class TopMerchant(BaseModel):
    merchant: str
    amount: int
    count: int

class CategorySpending(BaseModel):
    category: str
    amount: int
    percentage: float

class DashboardStats(BaseModel):
    weekly_trends: List[MonthlyWeeklyTrend]
    source_breakdown: List[SourceBreakdown]
    top_merchants: List[TopMerchant]
    category_spending: List[CategorySpending]

class CategoryRuleCreate(BaseModel):
    keyword: str
    category: str

class TransactionUpdate(BaseModel):
    category: str

class CategoryRuleRead(BaseModel):
    id: str
    keyword: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True
