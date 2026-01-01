import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
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
    category = Column(String, nullable=False, default="Uncategorized")
    created_at = Column(DateTime, default=datetime.utcnow)


class CategoryRule(Base):
    __tablename__ = "category_rules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    keyword = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
