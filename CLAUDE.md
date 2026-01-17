# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Development Protocol

**Before executing any commands or making code changes:**
1. **DO NOT execute anything without explicit user permission**
2. **ALWAYS create a plan** and share it with the user for approval
3. **WAIT for user confirmation** before proceeding with any implementation

### This means:
- No running `npm install`, `git commit`, `uvicorn`, or any commands without asking first
- No creating, editing, or deleting files without user approval
- No making assumptions about what the user wants - clarify first
- Always present a clear plan with steps before implementing anything

### Exception: Read-only operations
- Reading files (`Read`, `Glob`, `Grep`)
- Viewing documentation (`WebFetch`, `WebSearch`)
- Analyzing code structure
- These can be done without explicit permission but should still be purposeful

## Project Overview

MoneyFlow is a comprehensive personal finance tracking web application that aggregates financial transactions from multiple sources including PayPay Balance, SMBC Credit Cards, and manual CSV entries. The application uses a clean architecture with a Python/FastAPI backend and React/TypeScript frontend.

## ✅ Status: MVP Implementation Complete

The MoneyFlow MVP has been fully implemented and is ready for use. Both backend and frontend are complete with all core functionality working.

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI with automatic API documentation
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas for CSV parsing and normalization
- **Validation**: Pydantic for data validation

#### Backend Structure
```
backend/
├── src/
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   └── transactions.py     # Transaction endpoints
│   ├── core/                   # Core functionality
│   │   └── __init__.py
│   ├── domain/                 # Domain models
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas
│   └── infrastructure/         # Infrastructure layer
│       ├── __init__.py
│       ├── database.py        # Database connection and models
│       ├── models.py          # SQLAlchemy models
│       ├── parsers.py         # CSV parsers for different sources
│       └── repositories.py    # Repository pattern implementation
├── scripts/
│   └── init_db.py             # Database initialization script
├── tests/
│   └── test_parser_manual.py  # Manual parser tests
└── requirements.txt           # Python dependencies
```

#### Key Backend Components

1. **Database Models** (`backend/src/infrastructure/models.py`)
   - `Transaction`: Core entity with fields for id, date, amount, merchant, description, source, source_type, record_hash, created_at
   - `SourceType`: Enum for paypay, smbc, manual
   - Uses UUID for primary keys
   - Unique index on record_hash for deduplication

2. **API Endpoints** (`backend/src/api/transactions.py`)
   - `POST /api/transactions/upload`: Upload CSV files
   - `GET /api/transactions/`: List transactions with pagination
   - `GET /api/transactions/template`: Download CSV template for manual entries

3. **CSV Parsers** (`backend/src/infrastructure/parsers.py`)
   - Abstract base class for consistent interface
   - PayPayParser: Handles UTF-8 CSV with transaction IDs
   - SMBCParser: Handles Shift-JIS (CP932) Japanese encoding
   - ManualParser: For user-entered transactions

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and builds
- **State Management**: React hooks with TanStack Query for server state
- **Styling**: Tailwind CSS for utility-first styling

#### Frontend Structure
```
frontend/
├── src/
│   ├── api/                   # API client layer
│   │   ├── client.ts         # HTTP client implementation
│   │   └── index.ts          # API exports
│   ├── components/           # React components
│   │   ├── UploadSection.tsx # Drag & drop file upload
│   │   ├── TransactionList.tsx # Transaction table display
│   │   └── TemplateDownloader.tsx # Download template button
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── package.json            # Node.js dependencies
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
└── eslint.config.js       # ESLint configuration
```

## 🔧 Development Setup

### Prerequisites
- Python 3.8+ for backend
- Node.js 16+ for frontend

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python scripts/init_db.py  # Initialize database
uvicorn src.api.main:app --reload  # Start development server
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Start development server
```

### Access Points
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📊 Database Schema

### Transactions Table
- `id`: UUID string (Primary Key)
- `date`: Date (YYYY-MM-DD format)
- `amount`: Integer (amount in yen/cents)
- `merchant`: String (nullable)
- `description`: String (nullable)
- `source`: String (account/credit card name)
- `source_type`: Enum ('paypay', 'smbc', 'manual')
- `record_hash`: String (SHA-256 hash for deduplication)
- `created_at`: DateTime (auto-generated)

## 🧪 Testing

### Backend Tests
- Manual parser tests in `backend/tests/test_parser_manual.py`
- Sample data available in `sanitized-samples/`
- Run tests: `python backend/tests/test_parser_manual.py`

### Frontend Tests
- No automated tests currently implemented
- Manual testing with sample CSV files

## 📁 Data Import Formats

### PayPay CSV (UTF-8)
- Headers: Date & Time, Amount Outgoing (Yen), Amount Incoming (Yen), Transaction ID, Method, Business Name
- Uses Transaction ID for deduplication
- Amount normalized to integer (yen)

### SMBC Credit Card (Shift-JIS/CP932)
- Japanese character encoding support
- Includes credit card name in source field
- Amount in yen with debit/credit indicators

### Manual Template (UTF-8)
- Standard format for cash transactions
- Downloadable from API endpoint

## 🚀 Common Development Commands

### Backend
```bash
# Start development server
uvicorn src.api.main:app --reload

# Initialize database
python scripts/init_db.py

# Run parser tests
python backend/tests/test_parser_manual.py

# Install dependencies
pip install -r requirements.txt
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Install dependencies
npm install
```

## 🔒 Security & Data Handling

- **CORS**: Enabled for local development (allow_origins=["*"])
- **File Uploads**: No file size limits for MVP
- **Data Deduplication**: SHA-256 hash-based prevention
- **Encoding Support**: Automatic detection of UTF-8 and Shift-JIS
- **Database**: Local SQLite with unique constraints on record_hash

## 🎯 Key Features Implemented

1. **Multi-Source CSV Import**
   - PayPay Balance transactions
   - SMBC Credit Card statements
   - Manual entry via CSV template

2. **Data Integrity**
   - Automatic duplicate prevention
   - Encoding detection and conversion
   - Data validation and normalization

3. **User Experience**
   - Drag & drop file upload
   - Real-time progress feedback
   - Responsive design for mobile/desktop
   - Transaction list with sorting

## 📈 Performance Considerations

- SQLite database optimized for local use
- Pagination for transaction listing (default 100 records)
- Unique index on record_hash for fast duplicate checking
- Efficient CSV parsing with pandas

## 🔮 Future Enhancements (Post-MVP)

- User authentication and multi-user support
- Transaction categorization and analytics
- Advanced search and filtering
- Data export capabilities
- Mobile application development
- Cloud storage integration
- Budget tracking and alerts

## Documentation Synchronization

### Purpose
To ensure consistent project context across different AI agents and for human developers, maintaining a single source of truth for project state.

### Document Roles
1.  **README.md:** Human-centric overview. Includes high-level project goals, setup instructions, and quick start guide.
2.  **ANTIGRAVITY.md:** Primary context for Antigravity agent. Focuses on technical architecture, workflows, and task-specific state.
3.  **CLAUDE.md:** Primary context for Claude agent. Mirrors the technical architecture and development protocol.

### Sync Process

#### Step 1: Architecture/Dependency Changes
When project architecture or major dependencies change:
1.  Update **README.md** first (human-readable format)
2.  Propagate technical changes to **ANTIGRAVITY.md**
3.  Mirror **ANTIGRAVITY.md** in **CLAUDE.md**

#### Step 2: Constitution/Principles Updates
When project constitution or engineering principles change:
1.  Update in **ANTIGRAVITY.md** (primary source)
2.  Mirror exactly in **CLAUDE.md**
3.  Summarize key changes in **README.md**

#### Step 3: Agent Interaction Guidelines
- Keep **Agent Interaction Guidelines** identical across both agent-specific files
- Update both ANTIGRAVITY.md and CLAUDE.md simultaneously for guideline changes

#### Step 4: README Creation/Updates
If README.md doesn't exist:
1.  Create comprehensive README with:
    - Project overview and goals
    - Tech stack overview
    - Setup instructions
    - Development workflow
    - Key commands
2.  Extract technical details for ANTIGRAVITY.md and CLAUDE.md from README

### Best Practices
- Use README.md as the entry point for new developers
- Keep ANTIGRAVITY.md and CLAUDE.md technically precise
- Review all three documents quarterly for consistency
- Update documentation after major milestones or architectural changes

## 📚 Additional Resources

- Complete Documentation: `specs/001-mvp-csv-import/README.md`
- Feature Specification: `specs/001-mvp-csv-import/spec.md`
- Implementation Checklist: `specs/001-mvp-csv-import/completion-checklist.md`
- Quickstart Guide: `specs/001-mvp-csv-import/quickstart.md`

## 🤝 Contributing

The MVP is complete and functional. The project follows clean architecture principles with clear separation of concerns between:
- API layer (FastAPI endpoints)
- Domain layer (business logic)
- Infrastructure layer (data access, parsers, database)

For development, always test with real sample data from the sample directories to ensure parsers work correctly with actual bank export formats.