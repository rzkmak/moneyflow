import pytest
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import from the src module
sys.path.append('src')
from infrastructure.models import Transaction, CategoryRule, SourceType
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
        CategoryRule(keyword="セブン-イレブン", category="Convenience Store"),
        CategoryRule(keyword="スターバックス", category="Coffee"),
        CategoryRule(keyword="マクドナルド", category="Fast Food"),
        CategoryRule(keyword="ローソン", category="Convenience Store"),
        CategoryRule(keyword="FamilyMart", category="Convenience Store"),
        CategoryRule(keyword="AM PM", category="Convenience Store"),
        CategoryRule(keyword="PayPay", category="Payment"),
        CategoryRule(keyword="クレジットカード", category="Bills"),
        # Rule that should match longer keywords first
        CategoryRule(keyword="ローソン", category="Convenience Store"),
        CategoryRule(keyword="ローソンストアー", category="Supermarket"),
    ]

    for rule in rules:
        session.add(rule)

    session.commit()
    yield session
    session.close()

class TestAutoCategorization:
    """Test cases for auto-categorization rule matching."""

    def test_exact_match(self, db_session):
        """Test exact keyword matching."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1500,
            merchant="スターバックス銀座店",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test1",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        assert result.category == "Coffee"

    def test_partial_match(self, db_session):
        """Test partial keyword matching."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=500,
            merchant="セブン-イレブン新宿店",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test2",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        assert result.category == "Convenience Store"

    def test_no_merchant_name(self, db_session):
        """Test that transactions without merchant name are not categorized."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1000,
            merchant=None,
            source="Manual",
            source_type=SourceType.manual,
            record_hash="test3",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        assert result.category == "Uncategorized"

    def test_no_matching_rule(self, db_session):
        """Test that transactions without matching rules keep original category."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=2000,
            merchant="Unknown Shop",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test4",
            category="Food"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should keep original category if no rule matches
        assert result.category == "Food"

    def test_longest_keyword_match_precedence(self, db_session):
        """Test that longer keywords have higher precedence."""
        # We have both "ローソン" and "ローソンストアー" rules
        # "ローソンストアー" is longer and should match first
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=3000,
            merchant="ローソンストアー渋谷店",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test5",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match the longer keyword "ローソンストアー"
        assert result.category == "Supermarket"

    def case_insensitive_matching(self, db_session):
        """Test that matching is case insensitive."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=800,
            merchant="familymart shinjuku",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test6",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match "FamilyMart" rule
        assert result.category == "Convenience Store"

    def test_multiple_keyword_matches(self, db_session):
        """Test behavior when multiple keywords could match."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=1200,
            merchant="セブン-イレブン PayPoint",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test7",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match the first found rule (longest keyword among matches)
        # Both "セブン-イレブン" and "PayPoint" could match
        # "セブン-イレブン" is longer (6 chars vs 8 chars in Japanese)
        assert result.category == "Convenience Store"

    def test_japanese_character_matching(self, db_session):
        """Test matching of Japanese characters including full-width."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=700,
            merchant="ＡＭ　ＰＭ　タワーマンション店",  # Full-width AM PM
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test8",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match the "AM PM" rule
        assert result.category == "Convenience Store"

    def test_partial_word_matching(self, db_session):
        """Test that partial words within merchant name can match."""
        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=950,
            merchant="マクドナルドディーラックス銀座",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test9",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(db_session, transaction)

        # Should match "マクドナルド" rule
        assert result.category == "Fast Food"

    def test_rule_order_by_keyword_length(self, db_session):
        """Test that rules are ordered by keyword length (longest first)."""
        # This tests the database query ordering
        rules = TransactionRepository.get_all_category_rules(db_session)

        # Rules should be ordered by keyword length descending
        for i in range(len(rules) - 1):
            assert len(rules[i].keyword) >= len(rules[i + 1].keyword)

    def test_empty_database(self):
        """Test behavior with no rules in database."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        transaction = Transaction(
            date=datetime(2023, 1, 15).date(),
            amount=500,
            merchant="Some Shop",
            source="PayPay",
            source_type=SourceType.paypay,
            record_hash="test10",
            category="Uncategorized"
        )

        result = TransactionRepository.apply_auto_categorization(session, transaction)

        assert result.category == "Uncategorized"
        session.close()


class TestCategoryRuleCRUD:
    """Test CRUD operations for category rules."""

    def test_create_rule(self, db_session):
        """Test creating a new category rule."""
        rule = TransactionRepository.create_category_rule(db_session, "テスト店", "Test Category")

        assert rule.keyword == "テスト店"
        assert rule.category == "Test Category"
        assert rule.id is not None

    def test_get_all_rules_ordered(self, db_session):
        """Test getting all rules ordered by keyword length."""
        # Add rules with different lengths
        TransactionRepository.create_category_rule(db_session, "a", "Short")
        TransactionRepository.create_category_rule(db_session, "longer keyword", "Long")
        TransactionRepository.create_category_rule(db_session, "medium", "Medium")

        rules = TransactionRepository.get_all_category_rules(db_session)

        # Check ordering
        lengths = [len(rule.keyword) for rule in rules]
        assert lengths == sorted(lengths, reverse=True)

    def test_delete_rule(self, db_session):
        """Test deleting a category rule."""
        rule = TransactionRepository.create_category_rule(db_session, "ToDelete", "Category")
        rule_id = rule.id

        success = TransactionRepository.delete_category_rule(db_session, rule_id)

        assert success is True
        rule = db_session.query(CategoryRule).filter(CategoryRule.id == rule_id).first()
        assert rule is None

    def test_delete_nonexistent_rule(self, db_session):
        """Test deleting a non-existent rule."""
        success = TransactionRepository.delete_category_rule(db_session, "nonexistent-id")

        assert success is False


# Import Base for the test fixture
from infrastructure.models import Base