"""
Script to generate large amounts of test data for visualization
- Creates 2000+ students
- Generates 2000+ initial tests
- Generates 500 improvement tests (retests)
- All with random data
"""

import sqlite3
import hashlib
import random
import os
from datetime import datetime, timedelta
import numpy as np

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "specialization_prediction.db")

# Filières and their specializations
FILIERES = [
    "Intelligence Artificielle & Sciences des Données",
    "Cybersécurité & Infrastructures Réseaux",
    "Développement Digital & Systèmes d'Information"
]

SPECIALIZATIONS = {
    "Intelligence Artificielle & Sciences des Données": [
        "Machine Learning Engineer",
        "Data Scientist",
        "Deep Learning Specialist",
        "NLP Engineer",
        "Computer Vision Engineer"
    ],
    "Cybersécurité & Infrastructures Réseaux": [
        "Cybersecurity Analyst",
        "Network Security Engineer",
        "Penetration Tester",
        "Security Architect",
        "Incident Response Specialist"
    ],
    "Développement Digital & Systèmes d'Information": [
        "Full-Stack Developer",
        "Backend Developer",
        "Frontend Developer",
        "DevOps Engineer",
        "Mobile App Developer"
    ]
}

ALL_SPECIALIZATIONS = []
for specs in SPECIALIZATIONS.values():
    ALL_SPECIALIZATIONS.extend(specs)

def get_password_hash(password: str) -> str:
    """Hash password using SHA256"""
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_random_answers(num_questions=25):
    """Generate random answers (0-3) for questions"""
    # Generate question IDs like the backend expects (e.g., "ml_1", "ds_2", etc.)
    # For simplicity, we'll use generic IDs that match the pattern
    answers = {}
    for i in range(1, num_questions + 1):
        # Use a pattern that matches what the backend expects
        question_id = f'q{i}'
        answers[question_id] = random.randint(0, 3)
    return answers

def calculate_scores(answers):
    """Calculate test scores based on answers"""
    total_questions = len(answers)
    avg_answer = sum(answers.values()) / total_questions if total_questions > 0 else 0
    
    # Convert to 0-100 scale
    practical_score = (avg_answer / 3) * 100
    logical_score = min(100, practical_score + random.uniform(-10, 15))
    problem_score = min(100, practical_score + random.uniform(-10, 15))
    
    return practical_score, logical_score, problem_score

def generate_students_and_tests(num_students=2000, num_improvements=500):
    """Generate students and their test data"""
    print(f"\n{'='*60}")
    print(f"GENERATION DE DONNÉES DE TEST")
    print(f"{'='*60}\n")
    print(f"Étudiants à créer: {num_students}")
    print(f"Tests initiaux: {num_students}")
    print(f"Tests d'amélioration: {num_improvements}")
    print(f"Total tests: {num_students + num_improvements}\n")
    
    if not os.path.exists(DATABASE_PATH):
        print(f"[ERROR] Database not found at: {DATABASE_PATH}")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filiere TEXT NOT NULL,
            predicted_specialization TEXT NOT NULL,
            confidence REAL NOT NULL,
            practical_test_score REAL NOT NULL,
            logical_reasoning_score REAL NOT NULL,
            problem_solving_score REAL NOT NULL,
            time_spent_minutes REAL NOT NULL,
            previous_level INTEGER NOT NULL,
            current_level INTEGER NOT NULL,
            improvement_rate REAL NOT NULL,
            test_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_result_id INTEGER NOT NULL,
            predicted_specialization TEXT NOT NULL,
            confidence REAL NOT NULL,
            prediction_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (test_result_id) REFERENCES test_results(id)
        )
    ''')
    
    conn.commit()
    
    # Generate students
    print("[INFO] Creation des etudiants...")
    student_ids = []
    base_date = datetime.now() - timedelta(days=180)  # Tests over last 6 months
    
    for i in range(1, num_students + 1):
        username = f"student_{i:04d}"
        email = f"student_{i:04d}@test.com"
        password_hash = get_password_hash("test123")
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, "user")
            )
            user_id = cursor.lastrowid
            student_ids.append(user_id)
            
            if i % 100 == 0:
                print(f"  [OK] {i}/{num_students} etudiants crees")
        except sqlite3.IntegrityError:
            # User already exists, get existing ID
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                student_ids.append(result[0])
    
    conn.commit()
    print(f"[OK] {len(student_ids)} etudiants crees/recuperes\n")
    
    # Generate initial tests
    print("[INFO] Generation des tests initiaux...")
    test_count = 0
    
    for i, user_id in enumerate(student_ids):
        # Random filiere
        filiere = random.choice(FILIERES)
        
        # Random specialization for this filiere
        specialization = random.choice(SPECIALIZATIONS[filiere])
        
        # Get actual question IDs for this filiere/specialization
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from questions_bank import get_questions_for_specialization
            
            questions = get_questions_for_specialization(specialization, num_questions=25)
            if questions and len(questions) > 0:
                question_ids = [q['id'] for q in questions]
            else:
                # Fallback: use generic IDs based on specialization prefix
                prefix = specialization.lower().replace(' ', '_').replace('-', '_')[:2]
                question_ids = [f'{prefix}_{i}' for i in range(1, 26)]
        except Exception as e:
            # Fallback: use generic IDs based on specialization prefix
            prefix = specialization.lower().replace(' ', '_').replace('-', '_')[:2]
            question_ids = [f'{prefix}_{i}' for i in range(1, 26)]
        
        # Generate random answers with actual question IDs
        answers = {qid: random.randint(0, 3) for qid in question_ids}
        
        # Calculate scores
        practical_score, logical_score, problem_score = calculate_scores(answers)
        
        # Random test date (within last 6 months)
        days_ago = random.randint(0, 180)
        test_date = (base_date + timedelta(days=days_ago, hours=random.randint(0, 23))).isoformat()
        
        # Levels
        previous_level = 1
        current_level = random.randint(1, 5)
        improvement_rate = (current_level - previous_level) / 5.0
        
        # Confidence (0.3 to 0.95)
        confidence = random.uniform(0.3, 0.95)
        
        # Time spent (15 to 60 minutes)
        time_spent = random.uniform(15, 60)
        
        try:
            cursor.execute('''
                INSERT INTO test_results 
                (user_id, filiere, predicted_specialization, confidence, 
                 practical_test_score, logical_reasoning_score, problem_solving_score,
                 time_spent_minutes, previous_level, current_level, improvement_rate, test_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, filiere, specialization, confidence,
                practical_score, logical_score, problem_score,
                time_spent, previous_level, current_level, improvement_rate, test_date
            ))
            
            test_result_id = cursor.lastrowid
            
            # Add to prediction history
            cursor.execute('''
                INSERT INTO prediction_history 
                (user_id, test_result_id, predicted_specialization, confidence, prediction_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, test_result_id, specialization, confidence, test_date))
            
            test_count += 1
            
            if test_count % 200 == 0:
                conn.commit()
                print(f"  [OK] {test_count}/{num_students} tests crees")
        except Exception as e:
            print(f"  [ERROR] Erreur pour user_id {user_id}: {e}")
            continue
    
    conn.commit()
    print(f"[OK] {test_count} tests initiaux crees\n")
    
    # Generate improvement tests (retests)
    print("[INFO] Generation des tests d'amelioration...")
    improvement_count = 0
    
    # Select random students for improvements
    students_for_improvement = random.sample(student_ids, min(num_improvements, len(student_ids)))
    
    for user_id in students_for_improvement:
        # Get previous test
        cursor.execute('''
            SELECT current_level, filiere, predicted_specialization, test_date
            FROM test_results 
            WHERE user_id = ? 
            ORDER BY test_date DESC 
            LIMIT 1
        ''', (user_id,))
        
        prev_test = cursor.fetchone()
        if not prev_test:
            continue
        
        prev_level, prev_filiere, prev_spec, prev_date = prev_test
        
        # Improvement: new level should be higher or equal
        new_level = min(5, prev_level + random.randint(0, 2))
        improvement_rate = (new_level - prev_level) / 5.0
        
        # Same filiere or random (70% same, 30% different)
        if random.random() < 0.7:
            filiere = prev_filiere
        else:
            filiere = random.choice(FILIERES)
        
        specialization = random.choice(SPECIALIZATIONS[filiere])
        
        # Generate new answers (usually better)
        answers = generate_random_answers(25)
        
        # Calculate scores (usually better than before)
        practical_score, logical_score, problem_score = calculate_scores(answers)
        # Boost scores for improvement
        practical_score = min(100, practical_score + random.uniform(5, 20))
        logical_score = min(100, logical_score + random.uniform(5, 20))
        problem_score = min(100, problem_score + random.uniform(5, 20))
        
        # Test date after previous test
        days_after = random.randint(1, 90)
        if isinstance(prev_date, str):
            prev_date_obj = datetime.fromisoformat(prev_date.replace('Z', '+00:00') if 'Z' in prev_date else prev_date)
        else:
            prev_date_obj = prev_date
        test_date = (prev_date_obj + timedelta(days=days_after)).isoformat()
        
        # Higher confidence for improvements
        confidence = random.uniform(0.5, 0.98)
        
        # Time spent (usually less, more experienced)
        time_spent = random.uniform(10, 45)
        
        try:
            cursor.execute('''
                INSERT INTO test_results 
                (user_id, filiere, predicted_specialization, confidence, 
                 practical_test_score, logical_reasoning_score, problem_solving_score,
                 time_spent_minutes, previous_level, current_level, improvement_rate, test_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, filiere, specialization, confidence,
                practical_score, logical_score, problem_score,
                time_spent, prev_level, new_level, improvement_rate, test_date.isoformat()
            ))
            
            test_result_id = cursor.lastrowid
            
            # Add to prediction history
            cursor.execute('''
                INSERT INTO prediction_history 
                (user_id, test_result_id, predicted_specialization, confidence, prediction_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, test_result_id, specialization, confidence, test_date.isoformat()))
            
            improvement_count += 1
            
            if improvement_count % 100 == 0:
                conn.commit()
                print(f"  [OK] {improvement_count}/{num_improvements} ameliorations creees")
        except Exception as e:
            print(f"  [ERROR] Erreur pour amelioration user_id {user_id}: {e}")
            continue
    
    conn.commit()
    print(f"[OK] {improvement_count} tests d'amelioration crees\n")
    
    # Statistics
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM test_results")
    total_tests = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT filiere) FROM test_results")
    filiere_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT predicted_specialization) FROM test_results")
    spec_count = cursor.fetchone()[0]
    
    print(f"{'='*60}")
    print(f"STATISTIQUES FINALES")
    print(f"{'='*60}")
    print(f"Total utilisateurs: {total_users}")
    print(f"Total tests: {total_tests}")
    print(f"Filieres: {filiere_count}")
    print(f"Specialisations: {spec_count}")
    print(f"{'='*60}\n")
    
    conn.close()
    print("[OK] Generation terminee avec succes!")

if __name__ == "__main__":
    import sys
    
    num_students = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    num_improvements = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    
    generate_students_and_tests(num_students, num_improvements)

