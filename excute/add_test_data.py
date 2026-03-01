"""
Add test data to the database
Creates sample users and test results for demonstration
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal, User, TestResult, PredictionHistory
from auth import get_password_hash

def add_test_data():
    """Add test users and sample test results"""
    print("="*60)
    print("ADDING TEST DATA TO DATABASE")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"\n[INFO] Database already has {existing_users} users")
            response = input("Do you want to add more test data? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        # Create test users
        print("\n[1] Creating test users...")
        test_users = [
            {"username": "student1", "email": "student1@example.com", "password": "test123"},
            {"username": "student2", "email": "student2@example.com", "password": "test123"},
            {"username": "student3", "email": "student3@example.com", "password": "test123"},
        ]
        
        created_users = []
        for user_data in test_users:
            # Check if user exists
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if existing:
                print(f"  [SKIP] User '{user_data['username']}' already exists")
                created_users.append(existing)
            else:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"])
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                created_users.append(user)
                print(f"  [OK] Created user: {user_data['username']} / {user_data['password']}")
        
        # Create sample test results
        print("\n[2] Creating sample test results...")
        
        specializations = [
            "Machine Learning Engineer",
            "Data Scientist",
            "Full-Stack Developer",
            "Cybersecurity Analyst",
            "Backend Developer",
            "Frontend Developer"
        ]
        
        filieres = [
            "Intelligence Artificielle & Sciences des Données",
            "Cybersécurité & Infrastructures Réseaux",
            "Développement Digital & Systèmes d'Information"
        ]
        
        for user in created_users:
            # Create 2-3 test results per user
            num_tests = random.randint(2, 3)
            
            for i in range(num_tests):
                # Random specialization
                specialization = random.choice(specializations)
                
                # Determine filiere based on specialization
                if "Machine Learning" in specialization or "Data" in specialization or "AI" in specialization:
                    filiere = filieres[0]
                elif "Security" in specialization or "Cyber" in specialization:
                    filiere = filieres[1]
                else:
                    filiere = filieres[2]
                
                # Create test result
                test_date = datetime.now() - timedelta(days=random.randint(0, 30))
                
                test_result = TestResult(
                    user_id=user.id,
                    filiere=filiere,
                    predicted_specialization=specialization,
                    confidence=random.uniform(0.65, 0.95),
                    practical_test_score=random.uniform(60, 95),
                    logical_reasoning_score=random.uniform(55, 90),
                    problem_solving_score=random.uniform(58, 92),
                    time_spent_minutes=random.uniform(25, 60),
                    previous_level=random.randint(1, 4),
                    current_level=random.randint(2, 5),
                    improvement_rate=random.uniform(-0.2, 0.4),
                    test_date=test_date
                )
                db.add(test_result)
                db.commit()
                db.refresh(test_result)
                
                # Create prediction history
                pred_history = PredictionHistory(
                    user_id=user.id,
                    test_result_id=test_result.id,
                    predicted_specialization=specialization,
                    confidence=test_result.confidence,
                    prediction_date=test_date
                )
                db.add(pred_history)
                db.commit()
                
                print(f"  [OK] Created test result for {user.username}: {specialization} (confidence: {test_result.confidence:.2f})")
        
        print("\n" + "="*60)
        print("[SUCCESS] Test data added successfully!")
        print("="*60)
        print("\nTest users created:")
        for user in created_users:
            print(f"  - Username: {user.username}, Password: test123")
        print(f"\nTotal test results created: {db.query(TestResult).count()}")
        print(f"Total predictions: {db.query(PredictionHistory).count()}")
        print("\nYou can now view the database with: python view_database.py")
        
    except Exception as e:
        print(f"\n[ERROR] Could not add test data: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_data()

