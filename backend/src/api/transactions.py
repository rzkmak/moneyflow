from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io
import csv

from src.infrastructure.database import get_db
from src.infrastructure.repositories import TransactionRepository
from src.infrastructure.parsers import get_parser
from src.domain.schemas import TransactionRead, UploadSummary

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
