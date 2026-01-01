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
from src.api.transactions import router as transactions_router
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
import sys

# Create test database
@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# Create test app
@pytest.fixture
def client(test_db):
    app = FastAPI()
    app.include_router(transactions_router, prefix="/api/transactions", tags=["transactions"])

    # Override the get_db dependency
    def override_get_db():
        return test_db

    from src.api.dependencies import get_db
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

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

    for i in range(1000):  # Create 1000 transactions
        date = base_date + timedelta(days=i % 365)
        merchant_index = i % 50  # Cycle through 50 different merchants

        merchants = [
            "スターバックス銀座店", "マクドナルド新宿店", "セブン-イレブン渋谷店",
            "ローソン原宿店", "PayPay決済", "FamilyMart池袋店", "AM PMタワーマンション店",
            "イオン銀座店", "サンマルクカフェ", "ドトールコーヒー銀座",
            "モスバーガー新宿", "ケンタッキー銀座", "SUBWAY渋谷",
            "マクdonalds", "スタバ", "セブン", "ローソンストアー",
            "ミニストップ", "ファミリーマート", "サークルK",
        ]

        transaction = Transaction(
            date=date.date(),
            amount=1000 + (i % 9000),  # Amounts between 1000-10000
            merchant=merchants[merchant_index],
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

    def test_dashboard_stats_response_time(self, client, sample_transactions):
        """Test that /api/transactions/stats responds within 500ms."""

        # Measure response time
        start_time = time.time()
        response = client.get("/api/transactions/stats")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nDashboard stats response time: {response_time_ms:.2f}ms")

        # Assert response time is under 500ms
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Assert response is successful
        assert response.status_code == 200

        # Assert response contains expected data structure
        data = response.json()
        assert "monthly_trends" in data
        assert "source_breakdown" in data
        assert "top_merchants" in data
        assert "category_spending" in data

        # Assert data is not empty (we added 1000 transactions)
        assert len(data["monthly_trends"]) > 0
        assert len(data["source_breakdown"]) > 0
        assert len(data["top_merchants"]) > 0
        assert len(data["category_spending"]) > 0

        # Assert reasonable data sizes
        assert len(data["monthly_trends"]) <= 12  # Max 12 months
        assert len(data["top_merchants"]) <= 10    # Max 10 merchants
        assert len(data["category_spending"]) <= 20 # Max 20 categories

    def test_transactions_list_response_time(self, client, sample_transactions):
        """Test that /api/transactions responds within 500ms with pagination."""

        # Test with page 1, 20 items per page (default)
        start_time = time.time()
        response = client.get("/api/transactions")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nTransactions list response time: {response_time_ms:.2f}ms")

        # Assert response time is under 500ms
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Assert response is successful
        assert response.status_code == 200

        # Assert we get transactions back
        data = response.json()
        assert len(data) > 0
        assert len(data) <= 20  # Should not exceed page size

    def test_transactions_query_with_filters_performance(self, client, sample_transactions):
        """Test that filtered transactions query performs within 500ms."""

        # Test search filter performance
        start_time = time.time()
        response = client.get("/api/transactions?search=スターバックス")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        print(f"\nFiltered transactions response time: {response_time_ms:.2f}ms")

        # Assert response time is under 500ms
        assert response_time_ms < 500, f"Response time {response_time_ms:.2f}ms exceeds 500ms limit"

        # Assert response is successful
        assert response.status_code == 200

        # Verify we get Starbucks transactions
        data = response.json()
        for transaction in data:
            assert "スターバックス" in transaction.get("merchant", "")

    def test_database_query_performance(self, sample_transactions):
        """Test raw database query performance for dashboard stats."""

        # Test monthly spending query
        start_time = time.time()
        monthly_stats = TransactionRepository.get_monthly_spending(sample_transactions)
        end_time = time.time()

        query_time_ms = (end_time - start_time) * 1000

        print(f"\nMonthly spending query time: {query_time_ms:.2f}ms")

        # Assert query time is under 100ms (much stricter than API)
        assert query_time_ms < 100, f"Database query time {query_time_ms:.2f}ms exceeds 100ms limit"

        # Test source breakdown query
        start_time = time.time()
        source_stats = TransactionRepository.get_source_breakdown(sample_transactions)
        end_time = time.time()

        query_time_ms = (end_time - start_time) * 1000

        print(f"Source breakdown query time: {query_time_ms:.2f}ms")

        # Assert query time is under 100ms
        assert query_time_ms < 100, f"Database query time {query_time_ms:.2f}ms exceeds 100ms limit"

        # Test category spending query
        start_time = time.time()
        category_stats = TransactionRepository.get_category_spending(sample_transactions)
        end_time = time.time()

        query_time_ms = (end_time - start_time) * 1000

        print(f"Category spending query time: {query_time_ms:.2f}ms")

        # Assert query time is under 100ms
        assert query_time_ms < 100, f"Database query time {query_time_ms:.2f}ms exceeds 100ms limit"

    def test_concurrent_requests_performance(self, client, sample_transactions):
        """Test performance under concurrent requests."""
        import concurrent.futures
        import threading

        def make_request():
            return client.get("/api/transactions/stats")

        # Make 5 concurrent requests
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [future.result() for future in futures]
        end_time = time.time()

        total_time_ms = (end_time - start_time) * 1000
        avg_response_time_ms = total_time_ms / 5

        print(f"\nConcurrent requests total time: {total_time_ms:.2f}ms")
        print(f"Average response time: {avg_response_time_ms:.2f}ms")

        # Each request should still be under 500ms even under load
        assert avg_response_time_ms < 500, f"Average response time {avg_response_time_ms:.2f}ms exceeds 500ms limit"

        # All requests should be successful
        for response in responses:
            assert response.status_code == 200

