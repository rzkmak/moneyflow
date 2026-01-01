# Research: CSV Formats & Deduplication Strategy

**Feature**: MVP CSV Import
**Date**: 2026-01-01

## Decisions

### 1. CSV Parsing Strategy
- **Decision**: Use Python's `pandas` library with `encoding='cp932'` (extended Shift-JIS).
- **Rationale**: Japanese financial institutions (SMBC) overwhelmingly use Shift-JIS. `cp932` is the robust variant that handles special Microsoft characters often found in these files. Pandas provides high-performance parsing and easy column mapping.

### 2. PayPay Import Strategy
- **Format**: PayPay CSV exports include a unique `取引番号` (Transaction ID).
- **Deduplication**: Use `取引番号` directly as the unique key.
- **Source of Funds**: Map directly from the `Method` column (e.g., "PayPay Balance", "Credit VISA 1691").
- **Mapping**:
    - `取引日` -> `transaction_date`
    - `出金金額（円）` -> `amount` (if present, else check `入金金額（円）` for refunds/income)
    - `取引先` -> `merchant`
    - `取引内容` -> `description`

### 3. SMBC Import Strategy
- **Format**: Standard Vpass export (`利用日`, `利用店名・商品名`, `利用金額`, etc.).
- **Header Data**: Line 0 contains card info.
    - Index 1: Masked Number (e.g., `4980-00**-****-****`)
    - Index 2: Card Name (e.g., `Ｏｌｉｖｅゴールド／クレジット`)
- **Source of Funds**: Combine Card Name and Masked Number (e.g., "Olive Gold / Credit (****-****)") and apply to all rows in the file.
- **Deduplication**: No unique ID provided in CSV.
- **Strategy**: Generate a synthetic hash: `SHA256(YYYYMMDD + MerchantName + Amount)`.
- **Constraint**: If a user has two identical transactions (same shop, same day, same amount), they will be treated as duplicates. *Mitigation*: This is rare enough to accept for MVP; can add "Row Number" to hash if strictly necessary, but file re-uploads would break that. *Decision*: Accept strict content deduplication.

### 4. Database Schema (Draft)
- **Table**: `transactions`
    - `id`: UUID (Primary Key)
    - `source_id`: String (The PayPay ID or the Synthetic Hash) - *Unique Index*
    - `source_type`: Enum (`paypay`, `smbc`, `manual`)
    - ... other fields per spec.

## Open Questions Resolved
- **Shift-JIS Support**: Confirmed requirement.
- **Duplicate Detection**: Hybrid approach (ID for PayPay, Hash for SMBC).
