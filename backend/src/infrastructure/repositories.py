from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from sqlalchemy.sql import text
from .models import Transaction, CategoryRule
from ..domain.schemas import MonthlyWeeklyTrend, WeeklyTrendData

class TransactionRepository:
    @staticmethod
    def create(session: Session, transaction: Transaction) -> Transaction:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_hash(session: Session, record_hash: str) -> Transaction | None:
        return session.query(Transaction).filter(Transaction.record_hash == record_hash).first()

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> list[Transaction]:
        return (
            session.query(Transaction)
            .order_by(Transaction.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_weekly_spending_by_category(session: Session, start_date: str = None, end_date: str = None) -> list[MonthlyWeeklyTrend]:
        """Get total spending per week, broken down by category, grouped by month."""
        query = session.query(
            func.strftime("%Y-%m", Transaction.date).label("month"),
            func.strftime("%Y-%W", Transaction.date).label("week"),
            Transaction.category,
            func.sum(Transaction.amount).label("amount")
        )

        # Apply date filter if provided
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        # Group by month, week, and category
        weekly_data = (
            query
            .group_by(
                func.strftime("%Y-%m", Transaction.date),
                func.strftime("%Y-%W", Transaction.date),
                Transaction.category
            )
            .order_by(text("month ASC, week ASC"))
            .all()
        )

        # Transform to format expected by frontend
        result = {}
        for month, week, category, amount in weekly_data:
            if month not in result:
                result[month] = {}
            if week not in result[month]:
                result[month][week] = {}
            result[month][week][category] = int(amount)

        # Convert to list with month-week grouping
        output = []
        for month in sorted(result.keys()):
            month_weeks = []
            for week in sorted(result[month].keys()):
                # Format week label (e.g., "W1", "W2", etc.)
                week_num = int(week.split("-")[1])  # Week number (0-based)
                week_label = f"W{week_num + 1}"  # Convert to 1-based for display

                week_data = WeeklyTrendData(
                    week=week,
                    week_label=week_label,
                    categories=result[month][week]
                )
                month_weeks.append(week_data)

            month_data = MonthlyWeeklyTrend(
                month=month,
                weeks=month_weeks
            )
            output.append(month_data)

        return output

    @staticmethod
    def get_source_breakdown(session: Session, start_date: str = None, end_date: str = None) -> list[dict]:
        """Get spending breakdown by source with percentages."""
        # Get total amount by source
        query = session.query(
            Transaction.source,
            func.sum(Transaction.amount).label("amount")
        )

        # Apply date filter if provided
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        source_totals = query.group_by(Transaction.source).all()

        # Calculate total for percentages
        grand_total = sum(total.amount for total in source_totals) or 1

        return [
            {
                "source": total.source,
                "amount": int(total.amount),
                "percentage": round((total.amount / grand_total) * 100, 2)
            }
            for total in source_totals
        ]

    @staticmethod
    def get_top_merchants(session: Session, limit: int = 10, start_date: str = None, end_date: str = None) -> list[dict]:
        """Get top merchants by total spending."""
        query = session.query(
            Transaction.merchant,
            func.sum(Transaction.amount).label("amount"),
            func.count(Transaction.id).label("count")
        ).filter(Transaction.merchant.isnot(None))

        # Apply date filter if provided
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        return (
            query
            .group_by(Transaction.merchant)
            .order_by(text("amount DESC"))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_category_spending(session: Session, start_date: str = None, end_date: str = None) -> list[dict]:
        """Get spending breakdown by category."""
        # Get totals by category
        query = session.query(
            Transaction.category,
            func.sum(Transaction.amount).label("amount")
        )

        # Apply date filter if provided
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        category_totals = query.group_by(Transaction.category).order_by(text("amount DESC")).all()

        # Calculate total for percentages
        grand_total = sum(total.amount for total in category_totals) or 1

        return [
            {
                "category": total.category,
                "amount": int(total.amount),
                "percentage": round((total.amount / grand_total) * 100, 2)
            }
            for total in category_totals
        ]

    @staticmethod
    def apply_auto_categorization(session: Session, transaction: Transaction) -> Transaction:
        """Apply auto-categorization to a transaction based on rules."""
        if not transaction.merchant:
            return transaction

        # Get all rules and find matches
        merchant = str(transaction.merchant).lower()

        # Convert full-width ASCII to half-width ASCII for better matching
        def normalize_string(s):
            # Convert full-width ASCII to half-width ASCII
            result = ''
            for char in s:
                # Full-width ASCII range (FF01-FF5E)
                if 0xFF01 <= ord(char) <= 0xFF5E:
                    # Convert to half-width
                    result += chr(ord(char) - 0xFEE0)
                else:
                    result += char
            return result

        merchant_normalized = normalize_string(merchant)

        # Query all rules
        all_rules = session.query(CategoryRule).all()

        # Find all rules where the keyword is contained in the merchant name
        matching_rules = []
        for rule in all_rules:
            if not rule.keyword:
                continue

            rule_kw = normalize_string(rule.keyword.lower())

            # Remove all spaces (including full-width) for comparison
            merchant_no_spaces = merchant_normalized.replace(' ', '').replace('\u3000', '')
            rule_no_spaces = rule_kw.replace(' ', '').replace('\u3000', '')

            # Check if rule matches anywhere in merchant name
            if (rule_kw in merchant_normalized or
                rule_no_spaces in merchant_no_spaces or
                merchant_no_spaces.find(rule_no_spaces) >= 0):
                matching_rules.append(rule)

        if matching_rules:
            # Find the rule with the longest keyword (highest precedence)
            best_rule = max(matching_rules, key=lambda r: len(r.keyword))
            transaction.category = best_rule.category

        return transaction

    # Category Rule methods
    @staticmethod
    def create_category_rule(session: Session, keyword: str, category: str) -> CategoryRule:
        """Create a new category rule."""
        rule = CategoryRule(
            keyword=keyword,
            category=category
        )
        session.add(rule)
        session.commit()
        session.refresh(rule)
        return rule

    @staticmethod
    def get_all_category_rules(session: Session) -> list[CategoryRule]:
        """Get all category rules, ordered by keyword length (longest first)."""
        return (
            session.query(CategoryRule)
            .order_by(func.length(CategoryRule.keyword).desc())
            .all()
        )

    @staticmethod
    def delete_category_rule(session: Session, rule_id: str) -> bool:
        """Delete a category rule by ID."""
        rule = session.query(CategoryRule).filter(CategoryRule.id == rule_id).first()
        if rule:
            session.delete(rule)
            session.commit()
            return True
        return False
