#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.infrastructure.database import engine
from src.infrastructure.models import CategoryRule

def seed_category_rules():
    """Seed default category rules for common Japanese merchants."""

    print("Seeding category rules...")

    # Common Japanese merchant categorization rules
    # Keywords are ordered by specificity (longest matches first)
    default_rules = [
        # Convenience Stores
        {"keyword": "セブン-イレブン", "category": "Convenience Store"},
        {"keyword": "ファミリーマート", "category": "Convenience Store"},
        {"keyword": "ローソン", "category": "Convenience Store"},
        {"keyword": "ミニストップ", "category": "Convenience Store"},
        {"keyword": "デイリーヤマザキ", "category": "Convenience Store"},
        {"keyword": "セブン", "category": "Convenience Store"},  # Short form
        {"keyword": "ローソン", "category": "Convenience Store"},  # Already covered but explicit

        # Supermarkets
        {"keyword": "イトーヨーカドー", "category": "Groceries"},
        {"keyword": "イオン", "category": "Groceries"},
        {"keyword": "ヤマザキデイリーストア", "category": "Groceries"},
        {"keyword": "マルエツ", "category": "Groceries"},
        {"keyword": "ジョイフル", "category": "Groceries"},
        {"keyword": "ビッグエー", "category": "Groceries"},
        {"keyword": "スーパー", "category": "Groceries"},
        {"keyword": "スーパーマーケット", "category": "Groceries"},
        {"keyword": "ディスカウント", "category": "Groceries"},

        # Restaurants & Food
        {"keyword": "マクドナルド", "category": "Fast Food"},
        {"keyword": "バーガーキング", "category": "Fast Food"},
        {"keyword": "KFC", "category": "Fast Food"},
        {"keyword": "ケンタッキー", "category": "Fast Food"},
        {"keyword": "サブウェイ", "category": "Fast Food"},
        {"keyword": "モスバーガー", "category": "Fast Food"},
        {"keyword": "ファーストフード", "category": "Fast Food"},

        # Coffee Shops
        {"keyword": "スターバックス", "category": "Coffee"},
        {"keyword": "コーヒー", "category": "Coffee"},
        {"keyword": "スタバ", "category": "Coffee"},
        {"keyword": "ドトール", "category": "Coffee"},
        {"keyword": "エフエムコーヒー", "category": "Coffee"},
        {"keyword": "ブルーマウンテン", "category": "Coffee"},

        # Convenience Store Food
        {"keyword": "弁当", "category": "Prepared Food"},
        {"keyword": "おにぎり", "category": "Prepared Food"},
        {"keyword": "サンドイッチ", "category": "Prepared Food"},
        {"keyword": "パン", "category": "Prepared Food"},
        {"keyword": "スイーツ", "category": "Prepared Food"},
        {"keyword": "デザート", "category": "Prepared Food"},
        {"keyword": "お菓子", "category": "Snacks"},

        # Transportation
        {"keyword": "JR", "category": "Transportation"},
        {"keyword": "東海道", "category": "Transportation"},
        {"keyword": "山手線", "category": "Transportation"},
        {"keyword": "メトロ", "category": "Transportation"},
        {"keyword": "バス", "category": "Transportation"},
        {"keyword": "タクシー", "category": "Transportation"},
        {"keyword": "タクシー", "category": "Transportation"},
        {"keyword": "ガソリン", "category": "Transportation"},
        {"keyword": "エネオス", "category": "Transportation"},
        {"keyword": "出光", "category": "Transportation"},
        {"keyword": "IDEMITSU", "category": "Transportation"},
        {"keyword": "エッソ", "category": "Transportation"},
        {"keyword": "モービル", "category": "Transportation"},

        # Department Stores
        {"keyword": "伊勢丹", "category": "Department Store"},
        {"keyword": "三越", "category": "Department Store"},
        {"keyword": "高島屋", "category": "Department Store"},
        {"keyword": "大丸", "category": "Department Store"},
        {"keyword": "阪急", "category": "Department Store"},
        {"keyword": "丸井", "category": "Department Store"},
        {"keyword": "パルコ", "category": "Department Store"},
        {"keyword": "ルミネ", "category": "Department Store"},
        {"keyword": "そごう", "category": "Department Store"},

        # Electronics
        {"keyword": "ビックカメラ", "category": "Electronics"},
        {"keyword": "ヨドバシカメラ", "category": "Electronics"},
        {"keyword": "ヤマダ電機", "category": "Electronics"},
        {"keyword": "エディオン", "category": "Electronics"},
        {"keyword": "家電", "category": "Electronics"},
        {"keyword": "電気", "category": "Electronics"},
        {"keyword": "スマホ", "category": "Electronics"},
        {"keyword": "携帯", "category": "Electronics"},

        # Pharmacies
        {"keyword": "マツモトキヨシ", "category": "Pharmacy"},
        {"keyword": "ココカラファイン", "category": "Pharmacy"},
        {"keyword": "ドラッグストア", "category": "Pharmacy"},
        {"keyword": "薬局", "category": "Pharmacy"},
        {"keyword": "クリニック", "category": "Healthcare"},
        {"keyword": "病院", "category": "Healthcare"},

        # Entertainment
        {"keyword": "映画", "category": "Entertainment"},
        {"keyword": "シネマ", "category": "Entertainment"},
        {"keyword": "劇場", "category": "Entertainment"},
        {"keyword": "コンサート", "category": "Entertainment"},
        {"keyword": "ライブ", "category": "Entertainment"},
        {"keyword": "カラオケ", "category": "Entertainment"},
        {"keyword": "ゲーム", "category": "Entertainment"},
        {"keyword": "アミューズメント", "category": "Entertainment"},

        # Online Shopping
        {"keyword": "Amazon", "category": "Online Shopping"},
        {"keyword": "楽天", "category": "Online Shopping"},
        {"keyword": "Yahoo", "category": "Online Shopping"},
        {"keyword": "PayPay", "category": "Payment"},  # PayPay Balance/Shopping
        {"keyword": "LINE", "category": "Online Shopping"},
        {"keyword": "Mercari", "category": "Online Shopping"},
        {"keyword": "ラクマ", "category": "Online Shopping"},
        {"keyword": "モバイル決済", "category": "Payment"},
        {"keyword": "コンビニ決済", "category": "Payment"},

        # General Japanese Keywords
        {"keyword": "コンビニ", "category": "Convenience Store"},
        {"keyword": "コンビニエンスストア", "category": "Convenience Store"},
        {"keyword": "スーパー", "category": "Groceries"},
        {"keyword": "食料品", "category": "Groceries"},
        {"keyword": "飲料", "category": "Groceries"},
        {"keyword": "文房具", "category": "Office Supplies"},
        {"keyword": "書店", "category": "Books"},
        {"keyword": "本屋", "category": "Books"},
        {"keyword": "ファッション", "category": "Clothing"},
        {"keyword": "衣服", "category": "Clothing"},
        {"keyword": "靴", "category": "Clothing"},
        {"keyword": "銀行", "category": "Banking"},
        {"keyword": "ATM", "category": "Banking"},
        {"keyword": "振込", "category": "Banking"},
        {"keyword": "公共料金", "category": "Bills"},
        {"keyword": "水道", "category": "Bills"},
        {"keyword": "電気", "category": "Bills"},
        {"keyword": "ガス", "category": "Bills"},
        {"keyword": "電話", "category": "Bills"},
    ]

    # Create database session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Clear existing rules
        existing_count = session.query(CategoryRule).count()
        if existing_count > 0:
            print(f"Clearing {existing_count} existing rules...")
            session.query(CategoryRule).delete()

        # Add new rules
        added_count = 0
        for rule_data in default_rules:
            # Check if rule already exists
            existing = session.query(CategoryRule).filter(
                CategoryRule.keyword == rule_data["keyword"]
            ).first()

            if not existing:
                rule = CategoryRule(
                    keyword=rule_data["keyword"],
                    category=rule_data["category"],
                    created_at=datetime.utcnow()
                )
                session.add(rule)
                added_count += 1

        session.commit()
        print(f"Successfully seeded {added_count} category rules")

        # Show categories summary
        categories = session.query(CategoryRule.category).distinct().all()
        print(f"Categories: {', '.join([c.category for c in categories])}")

    except Exception as e:
        session.rollback()
        print(f"Error seeding rules: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_category_rules()