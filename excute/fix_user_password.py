"""
Script to fix or create a user with correct password hash
"""
import sqlite3
import hashlib
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "specialization_prediction.db")

def create_or_update_user(username, password, email=None):
    """Create or update user with correct password hash"""
    print(f"\n{'='*60}")
    print(f"Creating/Updating user: {username}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(DATABASE_PATH):
        print(f"[ERROR] Database not found at: {DATABASE_PATH}")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Hash password
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"Password: '{password}'")
    print(f"Hash: {password_hash}")
    
    # Check if user exists
    cursor.execute("SELECT id, username, email, hashed_password FROM users WHERE username = ?", (username,))
    existing = cursor.fetchone()
    
    if existing:
        user_id, old_username, old_email, old_hash = existing
        print(f"\n[WARNING] User already exists:")
        print(f"   ID: {user_id}")
        print(f"   Old hash: {old_hash[:50]}...")
        print(f"   New hash: {password_hash[:50]}...")
        
        # Update password
        if email:
            cursor.execute(
                "UPDATE users SET hashed_password = ?, email = ? WHERE username = ?",
                (password_hash, email, username)
            )
        else:
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE username = ?",
                (password_hash, username)
            )
        conn.commit()
        print(f"[OK] Password updated successfully!")
    else:
        # Create new user
        if not email:
            email = f"{username}@example.com"
        
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, "user")
        )
        conn.commit()
        print(f"[OK] User created successfully!")
    
    # Verify
    cursor.execute("SELECT id, username, email, hashed_password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        user_id, db_username, db_email, db_hash = user
        print(f"\n[OK] Verification:")
        print(f"   ID: {user_id}")
        print(f"   Username: '{db_username}'")
        print(f"   Email: '{db_email}'")
        print(f"   Hash: {db_hash}")
        
        # Test password
        test_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if test_hash == db_hash:
            print(f"   [OK] Password verification: CORRECT")
        else:
            print(f"   [ERROR] Password verification: INCORRECT")
    
    conn.close()
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python fix_user_password.py <username> <password> [email]")
        print("\nExample: python fix_user_password.py ibrahim test123 ibrahim@example.com")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    email = sys.argv[3] if len(sys.argv) > 3 else None
    
    create_or_update_user(username, password, email)

