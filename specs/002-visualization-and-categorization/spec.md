# Feature Specification: Expense Visualization and Categorization

**Feature Branch**: `002-visualization-and-categorization`  
**Created**: 2026-01-01  
**Status**: Draft  
**Input**: Option B: Expense Dashboard + Auto-Categorization by Merchant Name

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Expense Dashboard (Priority: P1)

As a user, I want to see a visual overview of my spending so that I can understand my financial habits at a glance.

**Why this priority**: This is the core value proposition of the feature. Visualizing existing data (even without categorization) provides immediate insight.

**Independent Test**: User navigates to the "Dashboard" tab and sees charts for Monthly Spending Trends, Spending by Source, and Top Merchants by Spending.

**Acceptance Scenarios**:
1. **Given** transactions exist in the database, **When** I open the dashboard, **Then** I see a bar chart showing total spend per month.
2. **Given** transactions from PayPay and SMBC, **When** I view the Spending by Source section, **Then** I see a pie chart showing the percentage of spend per source.

---

### User Story 2 - Manual Categorization (Priority: P1)

As a user, I want to assign categories to my transactions so that I can track my spending by type (e.g., Food, Transport).

**Why this priority**: Manual categorization is the foundation for the auto-categorization system and more granular charts.

**Independent Test**: User clicks on a transaction in the list, selects a category from a dropdown, and the change is persisted.

**Acceptance Scenarios**:
1. **Given** an "Uncategorized" transaction, **When** I select "Food" from the category dropdown, **Then** the transaction's category is updated to "Food".

---

### User Story 3 - Auto-Categorization Rules (Priority: P2)

As a user, I want the system to automatically categorize transactions based on the merchant name so that I don't have to manually edit every single entry.

**Why this priority**: High convenience factor. It reduces the friction of maintaining the system.

**Independent Test**: User uploads a CSV containing "7-Eleven". If a rule for "7-Eleven" exists, the transaction is automatically labeled "Convenience Store".

**Acceptance Scenarios**:
1. **Given** a rule exists mapping "Starbucks" to "Coffee", **When** I upload a CSV with a Starbucks transaction, **Then** it is automatically saved with the "Coffee" category.
2. **Given** I manually change a merchant's category, **When** I check "Apply to all future transactions", **Then** a new rule is created in the system.

---

### User Story 4 - Spending by Category Chart (Priority: P2)

As a user, I want to see a chart of my spending broken down by category so that I can see where my money is going.

**Why this priority**: Dependent on User Story 2 & 3. Provides the most actionable insight for budgeting.

**Acceptance Scenarios**:
1. **Given** categorized transactions, **When** I view the dashboard, **Then** I see a chart showing spend per category (e.g., Food: 30%, Rent: 50%).

---

### User Story 5 - Dashboard Time Range Filter (Priority: P2)

As a user, I want to filter the dashboard data by a specific time range so that I can analyze my spending patterns over different periods (e.g., this month, last quarter, custom date range).

**Why this priority**: Provides temporal flexibility for financial analysis. Users often want to compare spending across different time periods.

**Independent Test**: User selects a custom date range from the calendar dropdown and sees all dashboard charts update to reflect the filtered time period.

**Acceptance Scenarios**:
1. **Given** I am on the dashboard, **When** I open the filter dropdown, **Then** I see the default option "Last 90 Days" and calendar options for custom date ranges.
2. **Given** I select "Last 30 Days", **When** the dashboard refreshes, **Then** all charts show data only from the last 30 days.
3. **Given** I select a custom date range (e.g., 2025-10-01 to 2025-12-31), **When** I apply the filter, **Then** all charts update to show data within that specific period.
4. **Given** I change the filter, **Then** all dashboard components (weekly spending trends, source breakdown, category spending) update consistently.

---

### User Story 6 - Weekly Spending Trends with Category Breakdown (Priority: P1)

As a user, I want to see a stacked bar chart of weekly spending categorized by category so that I can understand my spending patterns over time with detailed category insights.

**Why this priority**: Provides granular temporal insights with category breakdown, enabling better budgeting and spending analysis.

**Independent Test**: User views the dashboard and sees a stacked bar chart showing weekly spending with different colors representing categories.

**Acceptance Scenarios**:
1. **Given** transactions exist in the selected date range, **When** I view the weekly trends chart, **Then** I see a stacked bar chart with weeks on the x-axis (earliest first) and total amount on the y-axis.
2. **Given** transactions from multiple categories, **When** I view the weekly trends, **Then** each bar is divided by category with different colors.
3. **Given** I select a date range spanning multiple weeks, **When** I view the weekly trends, **Then** I see a bar for each week within the selected period.
4. **Given** I have no transactions for a particular week, **When** I view the weekly trends, **Then** that week shows as zero height with no categories displayed.

---

### Edge Cases
- **No Merchant Name:** How to categorize transactions with empty merchant fields (e.g., manual cash entries with just a description)?
- **Conflicting Rules:** If "Amazon" matches "Amazon Music" (Entertainment) and "Amazon" (Shopping), which rule takes precedence? (Plan: Longest keyword match wins).
- **Deleted Categories:** What happens to transactions if a category name is changed or deleted?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST store a `category` for each transaction in the database.
- **FR-002**: System MUST allow users to create and persist `CategoryRules` (Keyword -> Category).
- **FR-003**: System MUST provide a "Dashboard" view with chart types: Weekly Spending Trends (stacked by category), Source Breakdown, and Category Breakdown.
- **FR-004**: System MUST automatically categorize new transactions during the import process if a matching rule exists.
- **FR-005**: System MUST allow users to manually edit the category of any transaction.
- **FR-006**: System SHOULD seed a list of common Japanese merchant rules on initial setup.
- **FR-007**: System MUST provide a time range filter for the Dashboard view with the following features:
  - Default value: Last 90 days from current date
  - Calendar dropdown selector for custom date ranges (start and end date)
  - Filter MUST affect all dashboard charts and statistics (weekly spending trends, category breakdown, source breakdown)
  - Filter MUST update dashboard data in real-time when changed
  - Filter MUST persist for the user's session
- **FR-008**: System MUST provide weekly spending data aggregated by category for the selected date range.
- **FR-009**: System MUST return weekly data in chronological order (earliest week first).

### Key Entities
- **Transaction (Updated)**:
  - `category`: String (Default: "Uncategorized")
- **CategoryRule**:
  - `id`: UUID
  - `keyword`: String (The merchant name substring to match)
  - `category`: String (The category to assign)
  - `created_at`: DateTime

## UI Guidelines

### Language Requirements
- **SC-LANG-001**: All UI titles, labels, and tooltips must be in English
- **SC-LANG-002**: No Japanese text should appear in the user interface
- **SC-LANG-003**: Date formatting should follow YYYY-MM-DD format
- **SC-LANG-004**: Currency formatting should use JPY with proper Japanese locale formatting (¥ symbol)

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Users can categorize a transaction in 2 clicks.
- **SC-002**: At least 70% of common Japanese convenience store/transport transactions are auto-categorized correctly using the "Starter Pack" rules.
- **SC-003**: Dashboard charts load in under 500ms for up to 10,000 transactions.
- **SC-004**: All UI components display content in English language.
