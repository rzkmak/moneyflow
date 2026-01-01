# Implementation Plan: Expense Visualization and Categorization

**Branch**: `002-visualization-and-categorization` | **Date**: 2026-01-01 | **Spec**: `/specs/002-visualization-and-categorization/spec.md`

## Summary
Implement a visual expense dashboard and an auto-categorization engine based on merchant names. The backend will use SQLAlchemy and Pandas for data aggregation and rule matching, while the frontend will use Recharts for visualization.

## Technical Context
**Language/Version**: Python 3.14 (Backend), TypeScript/React 19 (Frontend)
**Primary Dependencies**: FastAPI, SQLAlchemy, Pandas, Recharts (UI), TanStack Query
**Storage**: SQLite (`moneyflow.db`)
**Testing**: pytest
**Target Platform**: Web (Vite/Uvicorn)
**Performance Goals**: Dashboard rendering in < 500ms
**Constraints**: Must handle Japanese character encodings (Shift-JIS) for SMBC matching.

## Constitution Check
- **Library-First**: Categorization logic should be in a standalone module in `backend/src/infrastructure/parsers.py` or a new `services` module.
- **Test-First**: Unit tests for rule matching logic must precede implementation.
- **Simplicity**: Use Recharts (React-based) for simplicity in the frontend.

## Project Structure

### Documentation
```text
specs/002-visualization-and-categorization/
├── plan.md              # This file
├── spec.md              # Feature specification
└── data-model.md        # Data model changes (categories & rules)
```

### Source Code
```text
backend/
├── src/
│   ├── api/
│   │   └── transactions.py   # New endpoints for stats and rules
│   ├── domain/
│   │   └── schemas.py        # Pydantic schemas for Categories/Rules
│   ├── infrastructure/
│   │   ├── models.py         # DB model updates
│   │   ├── parsers.py        # Update parsers to apply rules
│   │   └── repositories.py   # Repository methods for aggregation
│   └── scripts/
│       └── seed_rules.py     # Script to seed default rules

frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/        # New Dashboard components
│   │   │   ├── SpendingChart.tsx
│   │   │   ├── SourcePieChart.tsx
│   │   │   └── MerchantList.tsx
│   │   └── TransactionList.tsx # Updated to allow category editing
│   ├── api/
│   │   └── client.ts         # New API hooks for stats
```

## Phases

### Phase 0: Data Model & Seeding
1.  **DB Migration**: Add `category` to `Transaction` table.
2.  **New Table**: Create `category_rules` table.
3.  **Seed Data**: Create `backend/src/scripts/seed_rules.py` with common Japanese merchants.

### Phase 1: Backend Aggregation & Auto-Categorization
1.  **Aggregation API**: Implement `GET /api/transactions/stats` to return data formatted for charts.
2.  **Rule Engine**: Update `CSVParser` to check `category_rules` during import.
3.  **Rule API**: Implement `POST /api/category-rules` to allow users to create new rules.

### Phase 2: Frontend Dashboard & Category UI
1.  **Dashboard Page**: Create a new layout with charts using `recharts`.
2.  **Category Selector**: Add a dropdown to `TransactionList.tsx` to edit categories.
3.  **Rule Prompt**: Implement the "Always apply this category to [Merchant]?" confirmation dialog.
