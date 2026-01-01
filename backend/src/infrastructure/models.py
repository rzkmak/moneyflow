import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Integer, String
from .database import Base

class SourceType(enum.Enum):
    paypay = "paypay"
    smbc = "smbc"
    manual = "manual"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    merchant = Column(String, nullable=True)
    description = Column(String, nullable=True)
    source = Column(String, nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    record_hash = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
