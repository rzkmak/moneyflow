from sqlalchemy.orm import Session
from .models import Transaction

class TransactionRepository:
    @staticmethod
    def create(session: Session, transaction: Transaction) -> Transaction:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_hash(session: Session, record_hash: str) -> Transaction | None:
        return session.query(Transaction).filter(Transaction.record_hash == record_hash).first()

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> list[Transaction]:
        return (
            session.query(Transaction)
            .order_by(Transaction.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
