"""
Add test data to the database (Simple version - direct SQL)
Creates sample users and test results without bcrypt issues
"""

import sqlite3
from datetime import datetime, timedelta
import random
import hashlib

def hash_password(password):
    """Simple password hashing for test data"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_test_data():
    """Add test users and sample test results"""
    print("="*60)
    print("ADDING TEST DATA TO DATABASE")
    print("="*60)
    
    conn = sqlite3.connect('specialization_prediction.db')
    cursor = conn.cursor()
    
    try:
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) FROM users")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"\n[INFO] Database already has {existing_count} users")
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
        
        created_user_ids = []
        for user_data in test_users:
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_data["username"],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"  [SKIP] User '{user_data['username']}' already exists")
                created_user_ids.append(existing[0])
            else:
                hashed_pwd = hash_password(user_data["password"])
                cursor.execute(
                    "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
                    (user_data["username"], user_data["email"], hashed_pwd)
                )
                user_id = cursor.lastrowid
                created_user_ids.append(user_id)
                print(f"  [OK] Created user: {user_data['username']} / {user_data['password']}")
        
        conn.commit()
        
        # Create sample test results
        print("\n[2] Creating sample test results...")
        
        specializations = [
            "Machine Learning Engineer",
            "Data Scientist",
            "Full-Stack Developer",
            "Cybersecurity Analyst",
            "Backend Developer",
            "Frontend Developer",
            "DevOps Engineer",
            "Data Engineer"
        ]
        
        filieres = [
            "Intelligence Artificielle & Sciences des Données",
            "Cybersécurité & Infrastructures Réseaux",
            "Développement Digital & Systèmes d'Information"
        ]
        
        total_results = 0
        for user_id in created_user_ids:
            # Get username for display
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            username = cursor.fetchone()[0]
            
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
                
                cursor.execute("""
                    INSERT INTO test_results 
                    (user_id, filiere, predicted_specialization, confidence, 
                     practical_test_score, logical_reasoning_score, problem_solving_score,
                     time_spent_minutes, previous_level, current_level, improvement_rate, test_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    filiere,
                    specialization,
                    round(random.uniform(0.65, 0.95), 4),
                    round(random.uniform(60, 95), 2),
                    round(random.uniform(55, 90), 2),
                    round(random.uniform(58, 92), 2),
                    round(random.uniform(25, 60), 2),
                    random.randint(1, 4),
                    random.randint(2, 5),
                    round(random.uniform(-0.2, 0.4), 4),
                    test_date
                ))
                
                test_result_id = cursor.lastrowid
                
                # Create prediction history
                cursor.execute("""
                    INSERT INTO prediction_history
                    (user_id, test_result_id, predicted_specialization, confidence, prediction_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    test_result_id,
                    specialization,
                    round(random.uniform(0.65, 0.95), 4),
                    test_date
                ))
                
                total_results += 1
                print(f"  [OK] Created test result for {username}: {specialization}")
        
        conn.commit()
        
        # Get final counts
        cursor.execute("SELECT COUNT(*) FROM test_results")
        total_tests = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM prediction_history")
        total_predictions = cursor.fetchone()[0]
        
        print("\n" + "="*60)
        print("[SUCCESS] Test data added successfully!")
        print("="*60)
        print(f"\nTotal users: {len(created_user_ids)}")
        print(f"Total test results: {total_tests}")
        print(f"Total predictions: {total_predictions}")
        print("\nTest users (password: test123):")
        for user_id in created_user_ids:
            cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            username = cursor.fetchone()[0]
            print(f"  - {username}")
        print("\nYou can now view the database with: python view_database.py")
        
    except Exception as e:
        print(f"\n[ERROR] Could not add test data: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    add_test_data()

