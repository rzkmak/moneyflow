from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import transactions

app = FastAPI(title="MoneyFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For MVP local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "MoneyFlow API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
