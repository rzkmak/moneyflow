# Money Flow MVP - CSV Import System

A complete money tracking web application that allows users to import financial transactions from multiple sources including PayPay Balance, SMBC Credit Cards, and manual CSV entries.

## ✅ Status: IMPLEMENTATION COMPLETE

The MVP has been fully implemented with all core functionality working. Both backend and frontend are complete and ready for use.

## 🎯 Features Delivered

### Core Functionality
- **Multi-Source CSV Import**: PayPay, SMBC Credit Cards, and Manual entries
- **Duplicate Prevention**: SHA-256 hash-based automatic rejection of duplicates
- **Encoding Support**: UTF-8 and Shift-JIS (CP932) for Japanese characters
- **Real-time Feedback**: Upload progress and status updates
- **Transaction Management**: View and manage all transactions in one place

### User Interface
- **Drag & Drop**: Intuitive file upload interface
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Progress Indicators**: Real-time feedback during uploads
- **Clean UI**: Modern interface built with Tailwind CSS

### Data Integrity
- **Cryptographic Hashing**: Each transaction gets a unique hash for deduplication
- **Database Indexing**: Optimized for fast duplicate checking
- **Encoding Detection**: Automatic handling of different file encodings
- **Source Tracking**: Records which account/credit card each transaction came from

## 🏗️ Architecture

### Backend (Python/FastAPI)
```
backend/
├── src/
│   ├── api/
│   │   └── main.py           # FastAPI application
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── database.py      # Database connection
│   ├── models/
│   │   └── transaction.py   # SQLAlchemy model
│   ├── repositories/
│   │   └── transaction.py   # Repository pattern
│   └── parsers/
│       ├── base.py          # Abstract base parser
│       ├── paypay.py        # PayPay CSV parser
│       └── smbc.py          # SMBC CSV parser
├── scripts/
│   └── init_db.py           # Database initialization
└── requirements.txt         # Dependencies
```

### Frontend (React/Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadSection.tsx    # Drag & drop upload
│   │   ├── TransactionList.tsx  # Transaction table
│   │   └── TemplateDownloader.tsx # Template download
│   ├── services/
│   │   └── api.ts             # API client
│   ├── types/
│   │   └── index.ts           # TypeScript interfaces
│   └── App.tsx                # Main application
└── package.json              # Dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ for backend
- Node.js 16+ for frontend
- npm or yarn for package management

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd moneyflow
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.api.main:app --reload
   ```

3. **Setup Frontend**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📊 Data Models

### Transaction Entity
```typescript
interface Transaction {
  id: string;                    // UUID
  date: Date;                   // Transaction date
  amount: number;                // Amount in yen (positive = expense, negative = income)
  merchant: string;              // Merchant name
  description: string;          // Description
  source: string;               // Source account/credit card
  sourceType: 'paypay' | 'smbc' | 'manual';
  recordHash: string;            // SHA-256 hash for deduplication
  createdAt: Date;              // Record creation timestamp
}
```

## 🧪 Testing

### Sample Data Included
- `sanitized-samples/`: Mock PayPay and SMBC CSV files for testing (UTF-8 and Shift-JIS)

### Test Coverage
- Integration tests with real CSV files
- Deduplication verification
- Encoding handling validation
- API endpoint testing

## 📋 Features in Detail

### CSV Import
- **PayPay Parser**: Handles UTF-8 encoded CSV files with transaction IDs
- **SMBC Parser**: Handles Shift-JIS (CP932) encoded credit card statements
- **Manual Template**: Standard CSV format for cash and other transactions

### Duplicate Prevention
- Uses SHA-256 hash based on date, amount, and merchant
- Automatic detection and rejection of duplicates
- Works across different file uploads

### User Experience
- Drag and drop file upload
- Progress indicators during import
- Clear success/error messages
- Responsive design for all devices

## 🔧 Technical Implementation

### Backend Technologies
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: ORM for database operations
- **Pandas**: CSV parsing and data manipulation
- **SQLite**: Lightweight database
- **Pydantic**: Data validation and serialization

### Frontend Technologies
- **React**: Component-based UI framework
- **Vite**: Fast build tool and development server
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Fetch API**: HTTP client for backend communication

### Performance Optimizations
- Database indexing on record_hash field
- Efficient CSV parsing with pandas
- Frontend code splitting
- Lazy loading of transaction data

## 🎯 Success Criteria

All original MVP requirements have been met:
- ✅ Import PayPay, SMBC, and Custom CSV files
- ✅ Prevent duplicate transactions
- ✅ Handle Japanese character encoding
- ✅ Complete imports in under 2 seconds
- ✅ Provide intuitive user interface
- ✅ Support responsive design

## 📈 Future Enhancements

The MVP is complete, but future improvements could include:
1. **User Management**: Authentication and multi-user support
2. **Categorization**: Automatic or manual transaction categorization
3. **Analytics**: Financial insights and reporting
4. **Search/Filter**: Advanced transaction filtering
5. **Export**: Data export to various formats
6. **Mobile Apps**: iOS and Android applications
7. **Cloud Storage**: Integration with cloud services
8. **Bank Integration**: Direct bank API connections

## 📄 Documentation

- [Feature Specification](./spec.md) - Detailed requirements and design
- [Data Model](./data-model.md) - Database schema and entity relationships
- [Implementation Plan](./plan.md) - Technical architecture and approach
- [Research Documentation](./research.md) - Technical research and decisions
- [Task Breakdown](./tasks.md) - Completed and remaining tasks
- [Completion Checklist](./completion-checklist.md) - Detailed implementation verification
- [Quickstart Guide](./quickstart.md) - Getting started instructions

## 🤝 Contributing

The MVP implementation is complete and functional. The project structure supports easy extension for future features.

## 📞 Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.

---

**Status**: ✅ MVP Implementation Complete
**Created**: 2026-01-01
**Updated**: 2025-01-01
**Branch**: `001-mvp-csv-import`