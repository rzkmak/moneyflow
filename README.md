# MoneyFlow - Personal Finance Tracker

A comprehensive money tracking web application that aggregates financial transactions from multiple sources including PayPay Balance, SMBC Credit Cards, and manual entries.

## 🎯 Project Purpose

This project serves as a learning platform to demonstrate how to effectively utilize AI tools for software development. The main goal is to showcase a modern development workflow using AI assistants at different stages of the project lifecycle.

### AI Tools Utilized

1. **Gemini CLI** (for spec-kit analysis)
   - Used for analyzing and structuring specification documents
   - Helps break down complex requirements into actionable tasks

2. **Spec-kit** (for specification documentation)
   - Comprehensive specification system for project planning
   - Generates detailed feature specifications, data models, and implementation plans
   - Maintains project consistency and documentation quality

3. **Claude Code** (for implementation)
   - Handles actual code implementation and development tasks
   - Follows the development protocol specified in CLAUDE.md
   - Executes tasks only with explicit user permission and clear planning

### Development Workflow

This project demonstrates a collaborative AI-assisted development approach:
1. **Specification Phase**: Use Gemini CLI to analyze and create detailed specs
2. **Planning Phase**: Use Spec-kit to generate implementation plans and task lists
3. **Implementation Phase**: Use Claude Code with strict protocol for safe, controlled development
4. **Quality Assurance**: Continuous verification against specifications and requirements

## ✅ Status: MVP Implementation Complete

The MoneyFlow MVP has been fully implemented and is ready for use. Both backend and frontend are complete with all core functionality working.

### 🎯 Key Features
- **Multi-Source CSV Import**: Import transactions from PayPay, SMBC Credit Cards, and manual CSV entries
- **Automatic Deduplication**: Prevents duplicate transactions using SHA-256 hashing
- **Encoding Support**: Handles both UTF-8 and Shift-JIS (Japanese) character encodings
- **Real-time Feedback**: Upload progress tracking and status updates
- **Responsive UI**: Modern interface that works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (backend)
- Node.js 16+ (frontend)

### Installation & Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.api.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Usage
1. Open http://localhost:5173 in your browser
2. Drag and drop CSV files to upload transactions
3. View all transactions in a unified list sorted by date
4. Download CSV templates for manual entry

## 📂 Project Structure

```
moneyflow/
├── backend/                    # Python/FastAPI backend
│   ├── src/
│   │   ├── api/              # API endpoints
│   │   ├── core/              # Core functionality
│   │   ├── models/            # Database models
│   │   ├── repositories/      # Data access layer
│   │   └── parsers/           # CSV parsers
│   └── scripts/               # Utility scripts
├── frontend/                  # React/Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── types/            # TypeScript definitions
│   └── public/               # Static assets
├── sanitized-samples/         # Sanitized CSV samples for testing
└── specs/                     # Project specifications
    └── 001-mvp-csv-import/
        ├── README.md          # Detailed overview
        ├── spec.md            # Feature specification
        ├── completion-checklist.md  # Implementation verification
        └── quickstart.md       # Setup instructions
```

## 📋 Supported File Formats

| Source | Encoding | Features |
|--------|----------|----------|
| PayPay CSV | UTF-8 | Transaction IDs, amount normalization |
| SMBC Credit Card | Shift-JIS (CP932) | Japanese characters, header parsing |
| Manual Template | UTF-8 | Standard format for cash transactions |

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Data Processing**: Pandas
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks

## 🧪 Testing

Sample data included for testing:
- `sanitized-samples/`: Mock PayPay and SMBC CSV files for testing

## 📚 Documentation

For detailed specifications and technical documentation, see:
- [**Complete Documentation**](./specs/001-mvp-csv-import/README.md) - Comprehensive project overview
- [**Feature Specification**](./specs/001-mvp-csv-import/spec.md) - Detailed requirements
- [**Implementation Checklist**](./specs/001-mvp-csv-import/completion-checklist.md) - Verification status
- [**Quickstart Guide**](./specs/001-mvp-csv-import/quickstart.md) - Setup instructions

## 🎯 Current Status

The MVP implementation is **100% complete** with:
- ✅ Full backend API implementation
- ✅ Complete React frontend
- ✅ Multi-format CSV parsing
- ✅ Duplicate detection system
- ✅ Responsive UI design
- ✅ Database integration
- ✅ Real sample data testing

## 🚀 Future Enhancements

### Phase 2: Dashboard & Analytics
- **Transaction Visualization Dashboard**
  - Interactive charts and graphs for expense analysis
  - Monthly/weekly spending trends
  - Category-based transaction grouping and filtering
  - Source-based spending breakdowns
  - Budget tracking and alerts

### Phase 3: Quality Assurance
- **End-to-End Automated UI Testing**
  - Cypress or Playwright for comprehensive UI automation
  - Test critical user flows: upload, import, view transactions
  - Cross-browser testing (Chrome, Firefox, Safari)
  - Visual regression testing for UI consistency

### Phase 4: Cloud Integration
- **Backup Storage Functionality**
  - Google Drive integration for automatic database backups
  - Microsoft OneDrive support as alternative storage option
  - Version history for transaction data
  - Secure authentication with OAuth2
  - Automatic scheduled backups
  - Manual backup triggers and restore functionality

### Phase 5: Advanced Features
- User authentication and multi-user support
- Transaction categorization with machine learning
- Advanced search and filtering capabilities
- Data export to multiple formats (CSV, PDF, Excel)
- Mobile application development
- Budget tracking and spending alerts
- Recurring transaction management
- Investment portfolio tracking

## 🤝 Contributing

The MVP is complete and functional. The project structure supports easy extension of new features. For detailed implementation information, see the specifications in the `specs/` directory.

## 📄 License

[MIT License](LICENSE)

---

**Development Status**: ✅ MVP Complete
**Branch**: `001-mvp-csv-import`
**Last Updated**: January 2025