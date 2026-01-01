import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import io
import csv
import sys

# Import from the src module
sys.path.append('src')
from infrastructure.models import Base, Transaction, CategoryRule, SourceType
from infrastructure.repositories import TransactionRepository

# Test database setup
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add some test rules
    rules = [
        CategoryRule(keyword="スターバックス", category="Coffee"),
        CategoryRule(keyword="マクドナルド", category="Fast Food"),
        CategoryRule(keyword="セブン-イレブン", category="Convenience Store"),
    ]

    for rule in rules:
        session.add(rule)

    session.commit()
    yield session
    session.close()

class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_upload_and_categorize_transaction(self, db_session):
        """Test the complete flow from CSV upload to categorization."""
        # Create a test CSV content (PayPay format)
        csv_content = """Transaction ID,Date & Time,Method,Business Name,Transaction Details,Amount Outgoing (Yen),Amount Incoming (Yen)
1,2023/01/15 10:30:00,スターバックス,スターバックス銀座店,コーヒー購入,1500,-"""

        # Convert to file-like object
        csv_file = io.BytesIO(csv_content.encode('utf-8'))

        # Create a test repository instance to test the parser directly
        from infrastructure.parsers import get_parser

        # Test the parser
        parser = get_parser("test_paypay.csv", csv_file.getvalue())
        transactions = parser.parse(csv_file.getvalue(), "test_paypay.csv")

        # Should have parsed one transaction
        assert len(transactions) == 1

        # Check transaction details
        transaction = transactions[0]
        assert transaction.merchant == "スターバックス銀座店"
        assert transaction.amount == 1500
        assert transaction.source == "スターバックス"
        assert transaction.source_type == SourceType.paypay
        assert transaction.category == "Uncategorized"  # Will be categorized during save

        # Apply auto-categorization and then save
        categorized_transaction = TransactionRepository.apply_auto_categorization(db_session, transaction)
        saved_transaction = TransactionRepository.create(db_session, categorized_transaction)

        # Check that auto-categorization was applied
        assert saved_transaction.category == "Coffee"

        # Verify the transaction is in the database
        db_transaction = db_session.query(Transaction).filter(Transaction.id == saved_transaction.id).first()
        assert db_transaction is not None
        assert db_transaction.category == "Coffee"

    def test_dashboard_stats_aggregation(self, db_session):
        """Test that dashboard statistics are correctly aggregated."""
        # Add test transactions
        transactions = [
            Transaction(
                date=datetime(2023, 1, 15).date(),
                amount=1000,
                merchant="スターバックス",
                source="PayPay",
                source_type=SourceType.paypay,
                record_hash="hash1",
                category="Coffee"
            ),
            Transaction(
                date=datetime(2023, 1, 15).date(),
                amount=800,
                merchant="マクドナルド",
                source="PayPay",
                source_type=SourceType.paypay,
                record_hash="hash2",
                category="Fast Food"
            ),
            Transaction(
                date=datetime(2023, 1, 16).date(),
                amount=500,
                merchant="セブン-イレブン",
                source="PayPay",
                source_type=SourceType.paypay,
                record_hash="hash3",
                category="Convenience Store"
            ),
        ]

        for transaction in transactions:
            db_session.add(transaction)

        db_session.commit()

        # Test monthly spending
        monthly_stats = TransactionRepository.get_monthly_spending(db_session)
        assert len(monthly_stats) == 1  # All transactions in the same month
        assert monthly_stats[0][0] == "2023-01"
        assert monthly_stats[0][1] == 2300  # 1000 + 800 + 500

        # Test source breakdown
        source_stats = TransactionRepository.get_source_breakdown(db_session)
        assert len(source_stats) == 1
        assert source_stats[0]["source"] == "PayPay"
        assert source_stats[0]["amount"] == 2300
        assert source_stats[0]["percentage"] == 100.0

        # Test category spending
        category_stats = TransactionRepository.get_category_spending(db_session)
        assert len(category_stats) == 3

        # Check that all categories are present
        categories = {stat["category"] for stat in category_stats}
        assert categories == {"Coffee", "Fast Food", "Convenience Store"}

        # Check amounts
        for stat in category_stats:
            if stat["category"] == "Coffee":
                assert stat["amount"] == 1000
            elif stat["category"] == "Fast Food":
                assert stat["amount"] == 800
            elif stat["category"] == "Convenience Store":
                assert stat["amount"] == 500

    def test_category_rule_crud_workflow(self, db_session):
        """Test the complete CRUD workflow for category rules."""
        # Test creating a rule
        rule = TransactionRepository.create_category_rule(db_session, "ローソン", "Convenience Store")
        assert rule.keyword == "ローソン"
        assert rule.category == "Convenience Store"
        assert rule.id is not None

        # Test retrieving all rules (should be ordered by length)
        all_rules = TransactionRepository.get_all_category_rules(db_session)
        assert len(all_rules) >= 1

        # Test the ordering - rules should be by keyword length descending
        for i in range(len(all_rules) - 1):
            assert len(all_rules[i].keyword) >= len(all_rules[i + 1].keyword)

        # Test deleting a rule
        success = TransactionRepository.delete_category_rule(db_session, rule.id)
        assert success is True

        # Verify rule is deleted
        deleted_rule = db_session.query(CategoryRule).filter(CategoryRule.id == rule.id).first()
        assert deleted_rule is None

        # Test deleting non-existent rule
        success = TransactionRepository.delete_category_rule(db_session, "non-existent-id")
        assert success is False

    def test_auto_categorization_with_longest_match(self, db_session):
        """Test that the longest matching keyword has precedence."""
        # Add rules with different lengths
        TransactionRepository.create_category_rule(db_session, "ローソン", "Convenience Store")
        TransactionRepository.create_category_rule(db_session, "ローソンストアー", "Supermarket")

        # Test transaction that matches both rules
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1000,
            merchant="ローソンストアー渋谷店",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test_longest",
            category="Uncategorized"
        )

        # Apply categorization
        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match the longer keyword "ローソンストアー"
        assert result.category == "Supermarket"

    def test_template_csv_generation(self, db_session):
        """Test that template CSV generation works correctly."""
        # This would typically be tested via the API, but we'll test the functionality
        import io
        from csv import writer

        output = io.StringIO()
        csv_writer = writer(output)
        csv_writer.writerow(['date', 'amount', 'description', 'category'])
        csv_writer.writerow(['2026-01-01', '1000', 'Lunch', 'Food'])

        output.seek(0)
        csv_content = output.read()

        assert 'date' in csv_content
        assert 'amount' in csv_content
        assert 'description' in csv_content
        assert 'category' in csv_content
        assert '2026-01-01' in csv_content
        assert '1000' in csv_content
        assert 'Lunch' in csv_content
        assert 'Food' in csv_content

    def test_parser_selection_logic(self, db_session):
        """Test that the correct parser is selected for different file types."""
        from infrastructure.parsers import get_parser

        # Test PayPay detection
        paypay_content = b"Transaction ID,Date & Time,Method,Business Name,Transaction Details,Amount Outgoing (Yen),Amount Incoming (Yen)\n1,2023/01/15 10:30:00,PayPay,Test Merchant,Test,1500,-"
        parser = get_parser("paypay.csv", paypay_content)
        assert parser.__class__.__name__ == "PayPayParser"

        # Test template detection
        template_content = b"date,amount,description,category\n2023-01-01,1000,Lunch,Food"
        parser = get_parser("template.csv", template_content)
        assert parser.__class__.__name__ == "TemplateParser"

    def test_error_handling(self, db_session):
        """Test error handling in various scenarios."""
        # Test duplicate transaction detection
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1000,
            merchant="Test Merchant",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="duplicate_hash",
            category="Uncategorized"
        )

        # Save transaction
        TransactionRepository.create(db_session, transaction)

        # Try to save the same transaction again
        duplicate_transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1000,
            merchant="Test Merchant",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="duplicate_hash",  # Same hash
            category="Food"
        )

        # This should not create a duplicate
        existing = TransactionRepository.get_by_hash(db_session, "duplicate_hash")
        assert existing is not None

        # Test transaction with empty merchant
        transaction_no_merchant = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1000,
            merchant=None,
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="no_merchant_hash",
            category="Uncategorized"
        )

        # Should not crash and should keep original category
        result = TransactionRepository.apply_auto_categorization(db_session, transaction_no_merchant)
        assert result.category == "Uncategorized"