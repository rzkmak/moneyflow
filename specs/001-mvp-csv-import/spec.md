# Feature Specification: MVP Money Tracking & CSV Import

**Feature Branch**: `001-mvp-csv-import`
**Created**: 2026-01-01
**Status**: ✅ Implementation Complete
**Updated**: 2025-01-01
**Input**: MVP Money Tracking Web App. Supports importing PayPay and SMBC Credit CSVs, plus a generic template CSV. Includes strict duplicate detection by hashing individual transaction records.

## User Scenarios & Testing

### User Story 1 - Import Financial CSVs (Priority: P1)

As a user, I want to upload my transaction history from PayPay and SMBC credit cards so that I can see all my expenses in one place without manual entry.

**Why this priority**: Core value proposition of the MVP.

**Independent Test**: Can be tested by uploading sample CSVs from both sources and verifying the data appears in the UI.

**Acceptance Scenarios**:

1. **Given** a valid PayPay CSV export file, **When** I upload it via the web interface, **Then** the system parses the data and displays the transactions in a unified list with correct dates, amounts, and merchant names.
2. **Given** a valid SMBC Credit Card CSV export file (Shift-JIS encoded), **When** I upload it, **Then** the system correctly decodes the text and imports the transactions.
3. **Given** a malformed or unrecognized file, **When** I attempt to upload it, **Then** the system displays a clear error message.

---

### User Story 2 - Duplicate Prevention (Priority: P1)

As a user, I want the system to automatically reject duplicate transactions so that my financial records remain accurate even if I upload overlapping CSV files.

**Why this priority**: Essential for data integrity; without this, the app is unusable for ongoing tracking.

**Independent Test**: Upload a file, then upload the same file (or a file containing a subset of the same rows) and verify count of new records is 0.

**Acceptance Scenarios**:

1. **Given** a CSV file has already been imported, **When** I upload the exact same file again, **Then** the system reports that 0 new transactions were added and all rows were skipped.
2. **Given** a CSV file containing a mix of new transactions and previously imported ones, **When** I upload it, **Then** the system only imports the new transactions and skips the duplicates based on a unique hash of the record data.

---

### User Story 3 - Manual Entry via Template (Priority: P2)

As a user, I want to download a standard CSV template, fill it with cash or other expenses, and upload it, so that I can track transactions not covered by automatic exports.

**Why this priority**: Handles the "gap" in digital tracking (cash, unformatted sources).

**Independent Test**: Download template, add a row, upload, verify row exists.

**Acceptance Scenarios**:

1. **Given** I am on the dashboard, **When** I click "Download Template", **Then** I receive a CSV file with columns: `date`, `amount`, `description`, `category`.
2. **Given** a filled-out template CSV, **When** I upload it, **Then** the manual transactions are added to my unified list.

### Edge Cases

- **Encoding Issues**: Uploading a Shift-JIS file when the system expects UTF-8 (System must handle or auto-detect).
- **Date Formats**: Different CSVs using different date formats (e.g., `YYYY/MM/DD` vs `YYYY-MM-DD`).
- **Negative Values**: Handling refunds or income (positive vs negative amounts) consistently across different source formats.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a web interface for file upload (Drag & Drop or File Selector).
- **FR-002**: System MUST support parsing of **PayPay** transaction history CSVs.
- **FR-003**: System MUST support parsing of **SMBC Credit Card** transaction CSVs (handling Shift-JIS encoding).
- **FR-004**: System MUST support parsing of a **Standard/Custom** CSV format (`date`, `amount`, `description`, `category`).
- **FR-005**: System MUST normalize all imports into a unified `Transaction` structure.
- **FR-006**: System MUST extract and persist the "Source of Funds" (e.g., "PayPay Balance", "Olive Gold Card") for each transaction.
    - For **PayPay**: Extract from the `Method` column.
    - For **SMBC**: Extract from the file header (Line 1), capturing Card Name and Masked Number.
- **FR-007**: System MUST generate a unique cryptographic hash for every imported transaction record based on its core data fields (Date, Amount, Merchant/Description).
- **FR-008**: System MUST check the generated hash against existing records before insertion. If the hash exists, the record MUST be skipped.
- **FR-009**: System MUST display a summary after upload: "X records imported, Y duplicates skipped".
- **FR-010**: System MUST allow users to download the Standard CSV template.
- **FR-011**: System MUST display the unified list of transactions sorted by date (newest first).

### Key Entities

- **Transaction**:
    - `id` (System UUID)
    - `transaction_date` (Date)
    - `amount` (Integer/Decimal - standardized currency)
    - `merchant` (String - description or shop name)
    - `category` (String - optional)
    - `source` (String - e.g. "PayPay Balance", "Olive Gold - ****1234")
    - `source_type` (Enum: PayPay, SMBC, Manual)
    - `record_hash` (String - Unique Index for deduplication)
    - `original_data` (JSON/String - optional, for debugging)

## Success Criteria

### Measurable Outcomes

- **SC-001**: User can successfully import 3 different valid CSV files (PayPay, SMBC, Custom) without server errors.
- **SC-002**: Re-uploading a file with 100 transactions results in exactly 0 new database records.
- **SC-003**: Transactions from Shift-JIS encoded files display correct Japanese characters in the UI.
- **SC-004**: Import process for a typical monthly file (<500 rows) completes in under 2 seconds.

## Implementation Status ✅ COMPLETE

### Completed Components

**Backend (Python/FastAPI) - Phase 1: 100% Complete**
- ✅ FastAPI application with CORS middleware
- ✅ SQLAlchemy database models with `Transaction` entity
- ✅ SQLite database (`moneyflow.db`) already created
- ✅ Repository pattern for CRUD operations
- ✅ Base parser architecture with concrete parsers:
  - `PayPayParser` - Handles UTF-8 PayPay CSVs
  - `SMBCParser` - Handles Shift-JIS (CP932) SMBC CSVs
- ✅ API endpoints:
  - `POST /api/transactions/upload` - File upload with duplicate detection
  - `GET /api/transactions` - List transactions with pagination
  - `GET /api/transactions/template` - Download CSV template
- ✅ Cryptographic hash-based duplicate prevention
- ✅ Support for multiple data sources (PayPay Balance, Credit Cards)

**Frontend (React/Vite) - Phase 2: 100% Complete**
- ✅ React/Vite setup with TypeScript
- ✅ Main layout with header and grid system
- ✅ `UploadSection` component with drag-and-drop functionality
- ✅ `TransactionList` component with table view
- ✅ `TemplateDownloader` component
- ✅ API client integration
- ✅ Upload progress feedback and error handling
- ✅ Responsive design

### Technology Stack Implemented

- **Backend**: Python, FastAPI, SQLAlchemy, Pandas, SQLite
- **Frontend**: React, Vite, TypeScript, Tailwind CSS
- **Database**: SQLite
- **CSV Processing**: pandas with custom parsers

### Database Schema (Actual Implementation)

```sql
Transaction {
  id (UUID, Primary Key)
  date (Date)
  amount (Integer - yen)
  merchant (String)
  description (String)
  source (String - e.g., "PayPay Balance")
  source_type (Enum: paypay, smbc, manual)
  record_hash (String - Unique Index)
  created_at (DateTime)
}
```

### Sample Data Integration
- **PayPay CSV**: 131K file with real transaction data (Aug-Nov 2025)
- **SMBC CSV**: Small sample demonstrating Shift-JIS encoding
- Both files are being used to test the parsers

### Next Steps (Future Enhancements)
1. Comprehensive error handling and logging
2. Unit tests for all components
3. Authentication and user management
4. Transaction categorization and analytics
5. Search/filter functionality in transaction list
6. Data export capabilities