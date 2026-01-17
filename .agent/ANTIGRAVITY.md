# MoneyFlow - Antigravity Project Context

## Project Overview

MoneyFlow is a full-stack personal finance tracker designed to aggregate financial transactions from various sources (PayPay, SMBC, manual entries). Beyond its functional purpose, it serves as a showcase for an **AI-first development workflow** utilizing Antigravity, Claude Code, and Spec-kit.

**Status:** MVP is 100% complete and fully functional.

**Feature Status:**
*   ✅ MVP (CSV Import, Deduplication) - Spec 001
*   ✅ Expense Visualization & Auto-Categorization - Spec 002
*   🚧 Antigravity + Claude Tooling Migration - Spec 003 (In Progress)

## Architecture & Tech Stack

### Backend (`/backend`)
*   **Framework:** FastAPI
*   **Database:** SQLite with SQLAlchemy ORM
*   **Data Processing:** Pandas (for CSV parsing and normalization)
*   **Validation:** Pydantic
*   **Key Components:**
    *   `src/api/`: FastAPI routers and endpoints
    *   `src/domain/`: Pydantic schemas for data validation
    *   `src/infrastructure/`: Database models (`Transaction`, `CategoryRule`), repository patterns, and specialized CSV parsers
    *   `src/core/`: Internal utility and configuration

### Frontend (`/frontend`)
*   **Framework:** React 19 (Vite 7)
*   **Language:** TypeScript
*   **State Management:** TanStack Query (React Query)
*   **Styling:** Tailwind CSS
*   **Visualization:** Recharts
*   **Key Components:**
    *   `src/components/Dashboard/`: Charts for spending trends and breakdown
    *   `src/components/TransactionList.tsx`: Transaction management with categorization UI
    *   `src/api/`: API client and service layer

### Specification & Workflow (`/specs`, `.specify`, `.agent`)
*   **Spec-kit:** A comprehensive specification system used for project planning and documentation
*   **Antigravity:** For planning, specification review, UI verification (browser agent), and project coordination
*   **Claude Code:** For implementation following established specifications
*   **Workflow:** Planning (Antigravity) → Specification (Spec-kit) → Implementation (Claude Code) → Verification (Antigravity)

## AI-Assisted Development Workflow

### 1. Planning & Specification Phase (Antigravity)
- Analyze requirements and create initial plans
- Review and validate spec-kit generated specifications
- Use `/sync-with-specs` to catch up with current project state
- Use `/review-spec` to validate specification completeness

### 2. Documentation Phase (Spec-kit)
- Generate structured specification documents
- Create implementation plans and task breakdowns
- Define data models and acceptance criteria
- Maintain project constitution and principles

### 3. Implementation Phase (Claude Code)
- Receive handoff via `/handoff-to-claude` workflow
- Follow strict development protocol (plan → approval → implementation)
- Implement features according to specifications
- Adhere to CLAUDE.md guidelines

### 4. Verification Phase (Antigravity)
- Use `/verify-implementation` to check code quality
- Use `/verify-ui` to test UI changes with browser agent
- Create visual verification reports with screenshots
- Validate against acceptance criteria

## Documentation Synchronization

To ensure consistent project context across different agents and for human developers:

1.  **ANTIGRAVITY.md:** Primary context for Antigravity agent. Focuses on technical architecture, workflows, and task-specific state.
2.  **CLAUDE.md:** Primary context for Claude Code agent. Mirrors technical architecture and development protocol.
3.  **README.md:** Human-centric overview. High-level goals, setup, and usage.

**Sync Process:**
*   When project architecture or major dependencies change, update `README.md` first
*   Propagate those changes to `ANTIGRAVITY.md` and `CLAUDE.md`
*   Maintain the **Agent Interaction Guidelines** consistently across both agent-specific files

## Agent Interaction Guidelines

*   **Consent:** Never execute any commands, scripts, or code modifications without explicit user consent
*   **Planning:** Always define a clear, step-by-step plan before starting any task
*   **Review:** Present the plan to the user and request a review/approval before proceeding with implementation
*   **Transparency:** Clearly communicate what you're doing and why
*   **Collaboration:** Work with Claude Code through handoff workflows, not in parallel

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

### Quick Start Both Servers
```bash
make start
```

## Workflows

Antigravity has access to predefined workflows in `.agent/workflows/`:

- **start_feature.md** - Start a new feature with spec-kit
- **sync_with_specs.md** - Catch up with current project specifications
- **review_spec.md** - Review spec-kit generated specifications
- **handoff_to_claude.md** - Hand off implementation to Claude Code
- **verify_implementation.md** - Verify Claude's implementation
- **verify_ui.md** - Verify UI changes using browser agent

Invoke workflows using slash commands (e.g., `/sync-with-specs`) or reference them directly.

## Key Files & Directories

*   `backend/moneyflow.db`: SQLite database
*   `backend/src/infrastructure/parsers.py`: Logic for different CSV formats (PayPay, SMBC, Manual)
*   `frontend/src/components/`: React components for UI
*   `specs/`: Detailed feature specifications and implementation plans
*   `.specify/memory/constitution.md`: Core engineering principles
*   `.agent/workflows/`: Workflow definitions for common tasks
*   `CLAUDE.md`: Development protocol for Claude Code
*   `Makefile`: Convenient commands for development workflow

## Current State

### Completed Features
- ✅ Multi-source CSV import (PayPay, SMBC, Manual)
- ✅ Automatic deduplication using SHA-256 hashing
- ✅ Transaction list with sorting and filtering
- ✅ Dashboard with spending visualizations
- ✅ Auto-categorization with custom rules
- ✅ Category management UI

### In Progress
- 🚧 Tooling migration from Gemini CLI to Antigravity + Claude Code

### Pending
- See `specs/` directory for planned features

## Browser-Based UI Verification

Antigravity has browser agent capabilities for UI verification:

1. **Start servers**: `make start`
2. **Navigate to**: http://localhost:5173
3. **Test flows**: Upload CSV, view transactions, check dashboard
4. **Capture screenshots**: Document key states and flows
5. **Verify responsiveness**: Test mobile, tablet, desktop views
6. **Check functionality**: Filtering, sorting, categorization
7. **Create report**: Visual verification with screenshots

Use the `/verify-ui` workflow for structured UI testing.

## Spec-kit Integration

Spec-kit is used for structured specification documentation:

- **Location**: `.specify/` directory
- **Constitution**: `.specify/memory/constitution.md`
- **Specifications**: `specs/00X-feature-name/`
- **Files**: spec.md, plan.md, tasks.md, data-model.md, completion-checklist.md

Always verify specifications against the project constitution before implementation.

## Notes

- Always work on feature branches (e.g., `003-feature-name`)
- Use Makefile targets for common tasks
- Follow the established workflow: Plan → Spec → Implement → Verify
- Leverage browser agent for UI verification
- Keep documentation synchronized across all three files
- Respect the development protocol: no execution without consent
