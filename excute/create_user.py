"""Create a user in the database"""
import sys
import os
import hashlib
import sqlite3

def hash_password(password):
    """Simple password hashing - must match backend"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    """Create a user in the database"""
    conn = sqlite3.connect('specialization_prediction.db')
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"[INFO] User '{username}' already exists!")
            print("Use this password to login:")
            return False
        
        # Create user
        hashed_pwd = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
            (username, email, hashed_pwd)
        )
        conn.commit()
        
        print(f"[SUCCESS] User '{username}' created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not create user: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        password = sys.argv[2] if len(sys.argv) > 2 else "test123"
        email = sys.argv[3] if len(sys.argv) > 3 else f"{username}@example.com"
    else:
        username = "DRHAG"
        password = "test123"
        email = "drhag@example.com"
    
    print("="*60)
    print("CREATE USER")
    print("="*60)
    create_user(username, email, password)
    print("\nYou can now login with:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")

