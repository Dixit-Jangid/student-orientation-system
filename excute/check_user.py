"""
Script to check user in database and test password verification
"""
import sqlite3
import hashlib
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "specialization_prediction.db")

def check_user(username, password):
    """Check if user exists and verify password"""
    print(f"\n{'='*60}")
    print(f"Checking user: {username}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(DATABASE_PATH):
        print(f"[ERROR] Database not found at: {DATABASE_PATH}")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT id, username, email, hashed_password, role FROM users")
    all_users = cursor.fetchall()
    
    print(f"Total users in database: {len(all_users)}\n")
    
    if len(all_users) == 0:
        print("[ERROR] No users found in database!")
        conn.close()
        return
    
    # Print all users
    print("All users in database:")
    for user in all_users:
        user_id, db_username, email, hashed_pwd, role = user
        print(f"  - ID: {user_id}, Username: '{db_username}', Email: '{email}', Role: '{role}'")
        print(f"    Password hash: {hashed_pwd[:50]}...")
    
    # Find specific user
    print(f"\n{'='*60}")
    print(f"Looking for user: '{username}'")
    print(f"{'='*60}\n")
    
    cursor.execute("SELECT id, username, email, hashed_password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"[ERROR] User '{username}' NOT FOUND in database!")
        print("\nAvailable usernames:")
        for u in all_users:
            print(f"  - '{u[1]}'")
        conn.close()
        return
    
    user_id, db_username, email, hashed_pwd, role = user
    print(f"[OK] User found!")
    print(f"   ID: {user_id}")
    print(f"   Username: '{db_username}'")
    print(f"   Email: '{email}'")
    print(f"   Role: '{role}'")
    print(f"   Stored hash: {hashed_pwd}")
    print(f"   Hash length: {len(hashed_pwd)}")
    
    # Test password
    print(f"\n{'='*60}")
    print(f"Testing password verification")
    print(f"{'='*60}\n")
    
    # Hash the provided password
    provided_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"Provided password: '{password}'")
    print(f"Provided hash: {provided_hash}")
    print(f"Stored hash:      {hashed_pwd}")
    print(f"\nHash match: {provided_hash == hashed_pwd}")
    
    if provided_hash == hashed_pwd:
        print("[OK] Password is CORRECT!")
    else:
        print("[ERROR] Password is INCORRECT!")
        print("\nTrying different encodings...")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'ascii']
        for enc in encodings:
            try:
                test_hash = hashlib.sha256(password.encode(enc)).hexdigest()
                if test_hash == hashed_pwd:
                    print(f"[OK] Match found with encoding: {enc}")
                    break
            except:
                pass
    
    conn.close()
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else "ibrahim"
    password = sys.argv[2] if len(sys.argv) > 2 else "test123"
    check_user(username, password)

