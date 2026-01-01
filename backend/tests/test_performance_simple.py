import pytest
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Import from the src module
sys.path.append('src')
from infrastructure.models import Base, Transaction, CategoryRule, SourceType
from infrastructure.repositories import TransactionRepository

# Create test database
@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_transactions(test_db):
    """Create sample transactions for performance testing."""

    # Add category rules
    rules = [
        CategoryRule(keyword="スターバックス", category="Coffee"),
        CategoryRule(keyword="マクドナルド", category="Fast Food"),
        CategoryRule(keyword="セブン-イレブン", category="Convenience Store"),
        CategoryRule(keyword="ローソン", category="Convenience Store"),
        CategoryRule(keyword="PayPay", category="Payment"),
    ]

    for rule in rules:
        test_db.add(rule)

    # Create transactions spanning multiple months
    transactions = []
    base_date = datetime(2023, 1, 1)

    merchants = [
        "スターバックス銀座店", "マクドナルド新宿店", "セブン-イレブン渋谷店",
        "ローソン原宿店", "PayPay決済", "FamilyMart池袋店", "AM PMタワーマンション店",
        "イオン銀座店", "サンマルクカフェ", "ドトールコーヒー銀座",
        "モスバーガー新宿", "ケンタッキー銀座", "SUBWAY渋谷",
        "マクdonalds", "スタバ", "セブン", "ローソンストアー",
        "ミニストップ", "ファミリーマート", "サークルK",
    ]

    for i in range(1000):  # Create 1000 transactions
        date = base_date + timedelta(days=i % 365)
        merchant_index = i % len(merchants)
        merchant = merchants[merchant_index]

        transaction = Transaction(
            date=date.date(),
            amount=1000 + (i % 9000),  # Amounts between 1000-10000
            merchant=merchant,
            source="PayPay" if i % 4 == 0 else "SMBC",
            source_type=SourceType.paypay if i % 4 == 0 else SourceType.smbc,
            record_hash=f"hash_{i}",
            category="Uncategorized"
        )
        transactions.append(transaction)

    # Add transactions in batches
    for i in range(0, len(transactions), 100):
        batch = transactions[i:i+100]
        for transaction in batch:
            # Apply auto-categorization
            categorized = TransactionRepository.apply_auto_categorization(test_db, transaction)
            categorized.category = categorized.category  # Ensure categorization is applied
            test_db.add(categorized)
        test_db.commit()

    return test_db

class TestDashboardPerformance:
    """Test dashboard performance metrics."""

    def test_dashboard_stats_response_time(self, sample_transactions):
        """Test that dashboard stats query responds within 500ms."""

        # Test monthly spending query
        start_time = time.time()
        monthly_stats = TransactionRepository.get_monthly_spending(sample_transactions)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nMonthly spending query time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Test source breakdown query
        start_time = time.time()
        source_stats = TransactionRepository.get_source_breakdown(sample_transactions)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"Source breakdown query time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Test category spending query
        start_time = time.time()
        category_stats = TransactionRepository.get_category_spending(sample_transactions)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"Category spending query time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Test top merchants query
        start_time = time.time()
        top_merchants = TransactionRepository.get_top_merchants(sample_transactions)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"Top merchants query time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Verify data integrity
        assert len(monthly_stats) > 0
        assert len(source_stats) > 0
        assert len(category_stats) > 0
        assert len(top_merchants) > 0

        # Verify expected data structures
        # Monthly spending returns Row objects
        for stat in monthly_stats:
            assert hasattr(stat, '__getitem__')
            assert len(stat) == 2
            assert isinstance(stat[0], str)  # month
            assert isinstance(stat[1], (int, float))  # total_amount

        # Source breakdown returns dicts
        for stat in source_stats:
            assert isinstance(stat, dict)
            assert 'source' in stat
            assert 'amount' in stat
            assert 'percentage' in stat

        # Category spending returns dicts
        for stat in category_stats:
            assert isinstance(stat, dict)
            assert 'category' in stat
            assert 'amount' in stat
            assert 'percentage' in stat

        # Top merchants returns Row objects (merchant, amount, count)
        for merchant in top_merchants:
            assert hasattr(merchant, '__getitem__')
            assert len(merchant) == 3
            assert isinstance(merchant[0], str)  # merchant
            assert isinstance(merchant[1], (int, float))  # amount
            assert isinstance(merchant[2], int)  # count

    def test_auto_categorization_performance(self, sample_transactions):
        """Test that auto-categorization performs within 500ms."""

        # Create a new transaction to categorize
        test_transaction = Transaction(
            date=datetime(2023, 12, 15).date(),
            amount=1500,
            merchant="スターバックス新宿店",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="perf_test_hash",
            category="Uncategorized"
        )

        # Test auto-categorization performance
        start_time = time.time()
        categorized = TransactionRepository.apply_auto_categorization(sample_transactions, test_transaction)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nAuto-categorization time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Verify categorization worked correctly
        assert categorized.category == "Coffee"

    def test_rule_retrieval_performance(self, sample_transactions):
        """Test that category rule retrieval performs within 500ms."""

        # Test retrieving all rules
        start_time = time.time()
        rules = TransactionRepository.get_all_category_rules(sample_transactions)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nRule retrieval time: {response_time_ms:.2f}ms")
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Verify rules are ordered by length
        for i in range(len(rules) - 1):
            assert len(rules[i].keyword) >= len(rules[i + 1].keyword)

        # Verify we have the expected rules
        rule_keywords = [rule.keyword for rule in rules]
        assert "スターバックス" in rule_keywords
        assert "マクドナルド" in rule_keywords
        assert "セブン-イレブン" in rule_keywords

    def test_database_query_scalability(self):
        """Test performance with larger datasets."""
        # Create a database with more transactions
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Add rules
        rules = [
            CategoryRule(keyword="スターバックス", category="Coffee"),
            CategoryRule(keyword="マクドナルド", category="Fast Food"),
        ]
        for rule in rules:
            session.add(rule)
        session.commit()

        # Create 5000 transactions for scalability test
        print("\nCreating 5000 transactions for scalability test...")
        base_date = datetime(2023, 1, 1)

        merchants = [
            "スターバックス銀座店", "マクドナルド新宿店", "セブン-イレブン渋谷店",
            "ローソン原宿店", "PayPay決済", "FamilyMart池袋店", "AM PMタワーマンション店",
            "イオン銀座店", "サンマルクカフェ", "ドトールコーヒー銀座",
        ]

        for i in range(5000):
            date = base_date + timedelta(days=i % 365)
            merchant_index = i % len(merchants)

            merchant = merchants[merchant_index]

            transaction = Transaction(
                date=date.date(),
                amount=1000 + (i % 9000),
                merchant=merchant,
                source="PayPay",
                source_type=SourceType.paypay,
                record_hash=f"hash_large_{i}",
                category="Uncategorized"
            )

            categorized = TransactionRepository.apply_auto_categorization(session, transaction)
            categorized.category = categorized.category
            session.add(categorized)

            if i % 1000 == 0:
                session.commit()

        session.commit()

        # Test performance with larger dataset
        print("Testing performance with 5000 transactions...")

        start_time = time.time()
        monthly_stats = TransactionRepository.get_monthly_spending(session)
        source_stats = TransactionRepository.get_source_breakdown(session)
        category_stats = TransactionRepository.get_category_spending(session)
        top_merchants = TransactionRepository.get_top_merchants(session)
        end_time = time.time()

        total_time_ms = (end_time - start_time) * 1000

        print(f"All dashboard queries time with 5000 transactions: {total_time_ms:.2f}ms")
        assert total_time_ms < 500, f"Total query time {total_time_ms:.2f}ms exceeds 500ms limit"

        # Verify we got expected data
        assert len(monthly_stats) > 0
        assert len(source_stats) > 0
        assert len(category_stats) > 0
        assert len(top_merchants) > 0

        session.close()