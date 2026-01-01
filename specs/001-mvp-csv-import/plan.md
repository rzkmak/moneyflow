# Implementation Plan: MVP Money Tracking & CSV Import

**Branch**: `001-mvp-csv-import` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-mvp-csv-import/spec.md`

## Summary

Build a local full-stack web application (React + FastAPI) to track personal finances. The system will ingest CSV exports from PayPay and SMBC, normalize them, and strictly prevent duplicates using record hashing. Data will be stored in a local SQLite database.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), Node.js 20+ / TypeScript 5 (Frontend)
**Primary Dependencies**: 
  - Backend: FastAPI, Pandas (for robust CSV/Data processing), Pydantic, SQLAlchemy (or SQLModel).
  - Frontend: React, Vite, Tailwind CSS, TanStack Query.
**Storage**: SQLite (Local file-based).
**Testing**: Pytest (Backend), Vitest (Frontend).
**Target Platform**: Localhost Web Application.
**Project Type**: Web Application (Monorepo-style).
**Performance Goals**: Parse and deduplicate 500 records in < 1 second.
**Constraints**: Must handle Japanese character encodings (Shift-JIS/CP932) correctly.
**Scale/Scope**: Single user, thousands of transactions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Library-First**: Core logic (CSV Parsing, Normalization, Deduplication) will be implemented as isolated Python modules/services, independent of the API layer.
- [x] **CLI Interface**: A management CLI will be provided to trigger imports and check stats via terminal.
- [x] **Test-First**: TDD will be enforced for the parser and deduplication logic.
- [x] **Integration Testing**: End-to-end tests will verify the full upload-to-database flow.

## Project Structure

### Documentation (this feature)

```text
specs/001-mvp-csv-import/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── core/              # Config, Logging
│   ├── domain/            # Business Logic (Transactions, Deduplication)
│   ├── infrastructure/    # Database, CSV Parsers
│   ├── api/               # FastAPI Routes
│   └── cli.py             # CLI Entrypoint
├── tests/
└── pyproject.toml

frontend/
├── src/
│   ├── components/
│   ├── features/          # Dashboard, Upload
│   ├── api/               # Generated Client
│   └── App.tsx
├── tests/
└── package.json
```

**Structure Decision**: Standard "Frontend/Backend" split for clear separation of concerns, facilitating future migration (e.g., to a cloud DB) if needed.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Pandas Dependency | Robust CSV parsing and Shift-JIS handling | Python stdlib `csv` can be brittle with malformed financial exports and encoding edge cases. |