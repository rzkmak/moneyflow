from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import io
import csv
from uuid import UUID
from datetime import datetime

from src.infrastructure.database import get_db
from src.infrastructure.repositories import TransactionRepository
from src.infrastructure.parsers import get_parser
from src.domain.schemas import (
    TransactionRead,
    TransactionUpdate,
    UploadSummary,
    DashboardStats,
    CategoryRuleCreate,
    CategoryRuleRead
)

router = APIRouter()

@router.post("/upload", response_model=UploadSummary)
async def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()
        filename = file.filename or "unknown.csv"
        
        parser = get_parser(filename, content)
        transactions = parser.parse(content, filename)
        
        imported_count = 0
        skipped_count = 0
        
        for t in transactions:
            # Check duplicate
            existing = TransactionRepository.get_by_hash(db, t.record_hash)
            if existing:
                skipped_count += 1
            else:
                # Apply auto-categorization before saving
                TransactionRepository.apply_auto_categorization(db, t)
                TransactionRepository.create(db, t)
                imported_count += 1
                
        return UploadSummary(
            imported=imported_count,
            skipped=skipped_count,
            message=f"Processing complete. {imported_count} imported, {skipped_count} skipped."
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return TransactionRepository.get_all(db, skip=skip, limit=limit)

@router.get("/template")
def download_template():
    # date,amount,description,category
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['date', 'amount', 'description', 'category'])
    writer.writerow(['2026-01-01', '1000', 'Lunch', 'Food'])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=template.csv"}
    )

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics formatted for charts."""

    # Get weekly spending trends by category
    weekly_trends_data = TransactionRepository.get_weekly_spending_by_category(db, start_date, end_date)

    # Get source breakdown
    source_data = TransactionRepository.get_source_breakdown(db, start_date, end_date)
    source_breakdown = [
        {
            "source": item["source"],
            "amount": item["amount"],
            "percentage": item["percentage"]
        }
        for item in source_data
    ]

    # Get top merchants
    merchant_data = TransactionRepository.get_top_merchants(db, start_date=start_date, end_date=end_date)
    top_merchants = [
        {
            "merchant": item.merchant or "Unknown",
            "amount": int(item.amount),
            "count": item.count
        }
        for item in merchant_data
    ]

    # Get category spending
    category_data = TransactionRepository.get_category_spending(db, start_date, end_date)
    category_spending = [
        {
            "category": item["category"],
            "amount": item["amount"],
            "percentage": item["percentage"]
        }
        for item in category_data
    ]

    return DashboardStats(
        weekly_trends=weekly_trends_data,
        source_breakdown=source_breakdown,
        top_merchants=top_merchants,
        category_spending=category_spending
    )

# Category Rules endpoints
@router.get("/category-rules", response_model=list[CategoryRuleRead])
def get_category_rules(db: Session = Depends(get_db)):
    """Get all category rules."""
    rules = TransactionRepository.get_all_category_rules(db)
    return rules

@router.post("/category-rules", response_model=CategoryRuleRead)
def create_category_rule(
    rule: CategoryRuleCreate,
    db: Session = Depends(get_db)
):
    """Create a new category rule."""
    return TransactionRepository.create_category_rule(db, rule.keyword, rule.category)

@router.delete("/category-rules/{rule_id}")
def delete_category_rule(
    rule_id: str,
    db: Session = Depends(get_db)
):
    """Delete a category rule."""
    success = TransactionRepository.delete_category_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category rule not found")
    return {"message": "Category rule deleted successfully"}

@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: str,
    update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update a transaction's category."""
    from src.infrastructure.models import Transaction

    # Find the transaction
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update the category
    transaction.category = update.category

    db.commit()
    db.refresh(transaction)

    return transaction
