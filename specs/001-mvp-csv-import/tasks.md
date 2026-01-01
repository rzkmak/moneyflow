# Tasks: MVP Money Tracking & CSV Import

## Phase 1: Backend Infrastructure (Python/FastAPI) ✅ COMPLETED

- [x] **Task 1.1**: Initialize Python project with `poetry` or `venv` and install dependencies (`fastapi`, `uvicorn`, `pandas`, `sqlalchemy`, `pydantic`).
- [x] **Task 1.2**: Define SQLAlchemy models based on `data-model.md`.
- [x] **Task 1.3**: Implement `TransactionRepository` for CRUD operations and duplicate check (by `record_hash`).
- [x] **Task 1.4**: Implement `BaseParser` and concrete parsers:
    - `PayPayParser`: Handle UTF-8, extract `Transaction ID` for hash.
    - `SMBCParser`: Handle `cp932` (Shift-JIS), extract header info for source, generate synthetic hash.
- [x] **Task 1.5**: Create API endpoints:
    - `POST /api/transactions/upload`: Handle file upload, parse, and save new records.
    - `GET /api/transactions`: List transactions with filtering/sorting.
    - `GET /api/template`: Download the standard CSV template.

## Phase 2: Frontend Implementation (React/Vite) ✅ COMPLETED

- [x] **Task 2.1**: Scaffold React project with Vite, TypeScript, and Tailwind CSS.
- [x] **Task 2.2**: Create API client service to interact with FastAPI.
- [x] **Task 2.3**: Build `UploadSection` component with drag-and-drop and progress/status feedback.
- [x] **Task 2.4**: Build `TransactionList` component with a table view.
- [x] **Task 2.5**: Add "Download Template" button and responsive design.

## Phase 3: Integration & Testing 🔄 IN PROGRESS

- [x] **Task 3.1**: Run integration tests using `sanitized-samples/`.
- [x] **Task 3.2**: Verify deduplication logic works across multiple uploads.
- [ ] **Task 3.3**: Final UI polish and verification against Success Criteria.

## Phase 4: Production Preparation (Upcoming)

- [ ] **Task 4.1**: Add comprehensive error handling and logging
- [ ] **Task 4.2**: Implement unit tests for all components
- [ ] **Task 4.3**: Add authentication and user management
- [ ] **Task 4.4**: Implement transaction categorization and analytics
