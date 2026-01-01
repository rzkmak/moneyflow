# MoneyFlow - Gemini Project Context

## Project Overview
MoneyFlow is a full-stack personal finance tracker designed to aggregate financial transactions from various sources (PayPay, SMBC, manual entries). Beyond its functional purpose, it serves as a showcase for an **AI-first development workflow** utilizing Gemini, Claude, and Spec-kit.

**Status:** MVP is 100% complete and fully functional.
**Feature Status:**
*   ✅ MVP (CSV Import, Deduplication)
*   ✅ Expense Visualization & Auto-Categorization (Spec 002)

## Architecture & Tech Stack

### Backend (`/backend`)
*   **Framework:** FastAPI
*   **Database:** SQLite with SQLAlchemy ORM
*   **Data Processing:** Pandas (for CSV parsing and normalization)
*   **Validation:** Pydantic
*   **Key Components:**
    *   `src/api/`: FastAPI routers and endpoints.
    *   `src/domain/`: Pydantic schemas for data validation.
    *   `src/infrastructure/`: Database models (`Transaction`, `CategoryRule`), repository patterns, and specialized CSV parsers.
    *   `src/core/`: Internal utility and configuration.

### Frontend (`/frontend`)
*   **Framework:** React 19 (Vite 7)
*   **Language:** TypeScript
*   **State Management:** TanStack Query (React Query)
*   **Styling:** Tailwind CSS
*   **Visualization:** Recharts
*   **Key Components:**
    *   `src/components/Dashboard/`: Charts for spending trends and breakdown.
    *   `src/components/TransactionList.tsx`: Transaction management with categorization UI.
    *   `src/api/`: API client and service layer.

### Specification & Workflow (`/specs`, `.specify`, `.claude`)
*   **Spec-kit:** A comprehensive specification system used for project planning.
*   **Workflow:** Specification (Gemini) → Planning (Spec-kit) → Implementation (Claude Code).

## Documentation Synchronization
To ensure consistent project context across different agents and for human developers:
1.  **GEMINI.md:** Primary context for the Gemini agent. Focuses on technical architecture, agent rules, and task-specific state.
2.  **CLAUDE.md:** Primary context for the Claude agent. Mirrors the technical architecture and "Constitution" principles.
3.  **README.md:** Human-centric overview. High-level goals, setup, and usage.

**Sync Process:**
*   When the project architecture or major dependencies change, update `README.md` first.
*   Propagate those changes to `GEMINI.md` and `CLAUDE.md`.
*   Maintain the **Agent Interaction Guidelines** and **Constitution** consistently across both agent-specific files.

## Agent Interaction Guidelines
*   **Consent:** Never execute any commands, scripts, or code modifications without explicit user consent.
*   **Planning:** Always define a clear, step-by-step plan before starting any task.
*   **Review:** Present the plan to the user and request a review/approval before proceeding with implementation.

## Development Commands

### Backend
```bash
cd backend
# Setup environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run development server (Port 8000)
uvicorn src.api.main:app --reload
```

### Frontend
```bash
cd frontend
# Install dependencies
npm install

# Run development server (Port 5173)
npm run dev
```

## Key Files & Directories
*   `backend/moneyflow.db`: SQLite database.
*   `backend/src/infrastructure/parsers.py`: Logic for different CSV formats.
*   `specs/`: Detailed feature specifications and implementation plans.
*   `.specify/memory/constitution.md`: Core engineering principles.
*   `server.log`: Backend runtime logs.
