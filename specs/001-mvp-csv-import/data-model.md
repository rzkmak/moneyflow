# Data Model: MVP Money Tracking

## Entities

### Transaction
The core record representing a single financial movement.

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key (System generated) |
| `date` | Date | The date of the transaction |
| `amount` | Integer | Standardized amount in JPY (positive for expense/outgoing, negative for income/refund) |
| `merchant` | String | The shop name or counterparty |
| `description`| String | Detailed transaction content |
| `source` | String | Source of funds (e.g. "PayPay Balance", "Olive Gold") |
| `source_type`| Enum | `paypay`, `smbc`, `manual` |
| `record_hash`| String | Unique hash for deduplication (`SHA256`) |
| `created_at` | DateTime | System timestamp |

## Relationships
- Currently a single table system for MVP.

## Validation Rules
- `date` must be valid YYYY-MM-DD.
- `amount` must not be null.
- `record_hash` must be unique across the database.
