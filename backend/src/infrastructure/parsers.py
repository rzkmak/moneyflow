import pandas as pd
import hashlib
import io
import csv
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from .models import Transaction, SourceType

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_content: bytes, filename: str) -> List[Transaction]:
        pass

class PayPayParser(BaseParser):
    def parse(self, file_content: bytes, filename: str) -> List[Transaction]:
        # PayPay is UTF-8
        # Force all columns to string to prevent ID conversion
        df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8', dtype=str)
        
        transactions = []
        for _, row in df.iterrows():
            # Skip invalid rows if necessary
            if pd.isna(row.get('Transaction ID')):
                continue

            # Parse Date
            date_str = row['Date & Time']
            # Format: 2025/11/07 18:58:48
            try:
                dt = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
                date_obj = dt.date()
            except ValueError:
                continue

            # Amount Logic
            # Amount Outgoing (Yen) or Amount Incoming (Yen)
            amount = 0
            outgoing = row.get('Amount Outgoing (Yen)', '-')
            incoming = row.get('Amount Incoming (Yen)', '-')

            if outgoing != '-':
                # Remove commas
                amount = int(str(outgoing).replace(',', ''))
            elif incoming != '-':
                # Income is negative expense in our logic? Or separate? 
                # Spec: "positive for expense/outgoing, negative for income/refund"
                amount = -1 * int(str(incoming).replace(',', ''))
            
            # Merchant
            merchant = row.get('Business Name', '')
            description = row.get('Transaction Details', '')
            
            # Source
            source = row.get('Method', 'PayPay')
            
            # Hash
            # Use Transaction ID directly
            record_hash = str(row['Transaction ID'])

            t = Transaction(
                date=date_obj,
                amount=amount,
                merchant=merchant,
                description=description,
                source=source,
                source_type=SourceType.paypay,
                record_hash=record_hash
            )
            transactions.append(t)
            
        return transactions

class SMBCParser(BaseParser):
    def parse(self, file_content: bytes, filename: str) -> List[Transaction]:
        # SMBC is CP932 / Shift-JIS
        # Read first line for Source Info
        text_io = io.TextIOWrapper(io.BytesIO(file_content), encoding='cp932')
        header_line = text_io.readline()
        text_io.seek(0)
        
        # Parse Header Line manually
        # e.g., "User Name","4980-00**...","Olive Gold"
        # We can use csv reader for just the first line
        reader = csv.reader(io.StringIO(header_line))
        try:
            header_row = next(reader)
            masked_num = header_row[1]
            card_name = header_row[2]
            source_name = f"{card_name} ({masked_num})"
        except:
            source_name = "SMBC Card"

        # Read Data - No Header in file, columns by index
        # 0: Date, 1: Merchant, 5: Amount
        # Note: pandas read_csv with header=None
        # We need to skip row 0 (metadata)
        df = pd.read_csv(io.BytesIO(file_content), encoding='cp932', header=None, skiprows=1)
        
        transactions = []
        for _, row in df.iterrows():
            # row is a Series with integer index
            date_str = str(row[0])
            merchant = str(row[1])
            amount_raw = row[5]
            
            try:
                # Date format: 2025/11/28
                dt = datetime.strptime(date_str, '%Y/%m/%d')
                date_obj = dt.date()
            except ValueError:
                continue

            try:
                amount = int(str(amount_raw).replace(',', ''))
            except:
                amount = 0

            # Synthetic Hash
            # SHA256(YYYYMMDD + Merchant + Amount)
            hash_base = f"{date_str}{merchant}{amount}".encode('utf-8')
            record_hash = hashlib.sha256(hash_base).hexdigest()

            t = Transaction(
                date=date_obj,
                amount=amount,
                merchant=merchant,
                description="Credit Card Payment",
                source=source_name,
                source_type=SourceType.smbc,
                record_hash=record_hash
            )
            transactions.append(t)
            
        return transactions

class TemplateParser(BaseParser):
    def parse(self, file_content: bytes, filename: str) -> List[Transaction]:
        # Standard format: date,amount,description,category
        df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8')
        
        transactions = []
        for _, row in df.iterrows():
            date_str = row['date']
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                date_obj = dt.date()
            except:
                continue
                
            amount = int(row['amount'])
            desc = row.get('description', '')
            cat = row.get('category', '')
            
            # Hash
            hash_base = f"{date_str}{desc}{amount}".encode('utf-8')
            record_hash = hashlib.sha256(hash_base).hexdigest()
            
            t = Transaction(
                date=date_obj,
                amount=amount,
                merchant=desc, # Use description as merchant for manual
                description=desc,
                category=cat,
                source="Manual Entry",
                source_type=SourceType.manual,
                record_hash=record_hash
            )
            transactions.append(t)
        return transactions

def get_parser(filename: str, content: bytes) -> BaseParser:
    # Auto-detection logic
    # Try to decode first few bytes as UTF-8 vs Shift-JIS?
    # Or look for specific headers.
    
    # Simple Heuristic:
    # 1. Try decoding as UTF-8. If it contains "Transaction ID" -> PayPay.
    # 2. Try decoding as CP932. If it contains "SMBC" or similar -> SMBC.
    
    try:
        utf8_head = content[:1000].decode('utf-8')
        if "Transaction ID" in utf8_head or "取引番号" in utf8_head:
            return PayPayParser()
        if "date,amount,description" in utf8_head:
            return TemplateParser()
    except:
        pass
        
    try:
        # SMBC check
        cp932_head = content[:1000].decode('cp932')
        # Check for card number pattern or specific Japanese chars?
        # The sample had "Ｏｌｉｖｅゴールド"
        if "Ｏｌｉｖｅ" in cp932_head or "クレジット" in cp932_head or "Card" in cp932_head:
             return SMBCParser()
    except:
        pass
        
    # Default/Fallback? Raise Error
    raise ValueError("Unknown CSV format")
