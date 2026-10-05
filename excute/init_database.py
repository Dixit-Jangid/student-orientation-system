"""
Database Initialization Script
Creates and initializes the database with necessary tables
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import Base, engine, init_db, User, TestResult, PredictionHistory
from auth import get_password_hash

def create_database():
    """Create database tables"""
    print("="*60)
    print("DATABASE INITIALIZATION")
    print("="*60)
    
    # Create all tables
    print("\n[1/2] Creating database tables...")
    init_db()
    print("[OK] Tables created successfully")
    
    # Create a test user (optional)
    print("\n[2/2] Creating test user...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    existing_user = None
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.username == "test_user").first()
        if existing_user:
            print("[OK] Test user already exists (username: test_user, password: test123)")
        else:
            # Create test user
            test_user = User(
                username="test_user",
                email="test@example.com",
                hashed_password=get_password_hash("test123")
            )
            db.add(test_user)
            db.commit()
            print("[OK] Test user created successfully")
            print("  Username: test_user")
            print("  Password: test123")
            print("  Email: test@example.com")
            existing_user = test_user
    except Exception as e:
        print(f"[WARNING] Could not create test user: {e}")
        print("You can create a user manually through the API or frontend")
        db.rollback()
    finally:
        db.close()
    
    print("\n" + "="*60)
    print("DATABASE INITIALIZED SUCCESSFULLY!")
    print("="*60)
    print("\nDatabase file: specialization_prediction.db")
    print("\nYou can now:")
    print("  1. Start the backend server: cd backend && uvicorn main:app --reload")
    if existing_user:
        print("  2. Use the test user to login: test_user / test123")
    print("  3. Or register a new user through the API/Frontend")

if __name__ == "__main__":
    create_database()

