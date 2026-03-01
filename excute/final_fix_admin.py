"""Final fix for admin login - ensure everything is correct"""
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password, hashed_password):
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return sha256_hash == hashed_password

# Connect to database
conn = sqlite3.connect('specialization_prediction.db')
cursor = conn.cursor()

# Delete existing admin if exists
cursor.execute("DELETE FROM users WHERE username = 'admin'")
conn.commit()

# Create fresh admin user
admin_hash = hash_password('admin')
cursor.execute(
    "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
    ('admin', 'admin@admin.com', admin_hash)
)
conn.commit()

# Verify
cursor.execute("SELECT username, hashed_password FROM users WHERE username = 'admin'")
result = cursor.fetchone()

if result:
    username, stored_hash = result
    is_valid = verify_password('admin', stored_hash)
    
    print("="*60)
    print("ADMIN USER SETUP")
    print("="*60)
    print(f"Username: {username}")
    print(f"Password: admin")
    print(f"Hash: {stored_hash}")
    print(f"Verification: {'[PASS]' if is_valid else '[FAIL]'}")
    print("="*60)
    print("\nYou can now login with:")
    print("  Username: admin")
    print("  Password: admin")
    print("\nIMPORTANT: Restart the backend server after this fix!")
    print("  cd backend")
    print("  uvicorn main:app --reload")
else:
    print("[ERROR] Failed to create admin user!")

conn.close()

