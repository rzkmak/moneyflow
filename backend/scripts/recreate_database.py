#!/usr/bin/env python3
"""
Script to recreate the MoneyFlow database with fresh schema.
"""

import os
import sys
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from infrastructure.models import Base, Transaction, CategoryRule, SourceType

def recreate_database():
    # Get the database path from the configuration
    db_path = os.path.join(os.path.dirname(__file__), '..', 'moneyflow.db')

    print(f"Database path: {db_path}")

    # Delete existing database if it exists
    if os.path.exists(db_path):
        print("Deleting existing database...")
        os.remove(db_path)
        print("Database deleted successfully!")
    else:
        print("No existing database found.")

    # Create new database and tables
    print("Creating new database...")
    engine = create_engine("sqlite:///./moneyflow.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print("Database created successfully!")

    # Verify tables were created
    print("\nVerifying database structure...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if tables exist
        tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        print("Tables in database:")
        for table in tables:
            table_name = table[0]
            count = db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
            print(f"  - {table_name}: {count} rows")

        if len(tables) == 0:
            print("ERROR: No tables were created!")
            return False

        print("\nDatabase recreation completed successfully!")
        return True

    except Exception as e:
        print(f"Error verifying database: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = recreate_database()
    sys.exit(0 if success else 1)