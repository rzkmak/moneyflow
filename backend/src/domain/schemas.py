from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
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
