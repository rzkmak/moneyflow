# Data Model: Expense Visualization and Categorization

## Entity: Transaction (Modified)

| Field | Type | Description |
|-------|------|-------------|
| id | UUID (PK) | Unique identifier |
| date | Date | Transaction date |
| amount | Integer | Amount in Yen |
| merchant | String (Nullable) | Name of merchant |
| description| String (Nullable) | Additional info |
| source | String | Account/Card name |
| source_type| Enum | paypay, smbc, manual |
| record_hash| String (Unique) | For deduplication |
| category | String | **NEW**: Assigned category (e.g., "Food", "Transport") |
| created_at | DateTime | Timestamp |

## Entity: CategoryRule

Matches a merchant name substring to a category.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID (PK) | Unique identifier |
| keyword | String | Substring to look for in `merchant` |
| category | String | Category to assign (e.g., "Convenience Store") |
| created_at | DateTime | Timestamp |

### Rule Matching Logic
1.  System retrieves all `CategoryRules`.
2.  For a given transaction, it checks if any `rule.keyword` is contained within `transaction.merchant`.
3.  If multiple matches occur, the rule with the longest `keyword` takes precedence (to handle cases like "Amazon" vs "Amazon Music").
4.  If no match is found, category defaults to "Uncategorized".
