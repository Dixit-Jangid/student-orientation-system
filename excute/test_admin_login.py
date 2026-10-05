"""Test admin login directly"""
import hashlib
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password, hashed_password):
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return sha256_hash == hashed_password

# Connect to database
conn = sqlite3.connect('specialization_prediction.db')
cursor = conn.cursor()

# Get admin user
cursor.execute("SELECT username, hashed_password FROM users WHERE username = 'admin'")
result = cursor.fetchone()

if result:
    username, stored_hash = result
    print(f"Username: {username}")
    print(f"Stored hash: {stored_hash}")
    
    # Test password
    test_password = "admin"
    test_hash = hash_password(test_password)
    print(f"\nTest password: {test_password}")
    print(f"Test hash: {test_hash}")
    print(f"Hash match: {test_hash == stored_hash}")
    
    # Verify
    is_valid = verify_password(test_password, stored_hash)
    print(f"\nPassword verification: {is_valid}")
    
    if not is_valid:
        print("\n[FIXING] Updating password...")
        new_hash = hash_password("admin")
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE username = ?",
            (new_hash, 'admin')
        )
        conn.commit()
        print(f"[SUCCESS] Password updated to: {new_hash}")
        print(f"Now verification should work: {verify_password('admin', new_hash)}")
else:
    print("[ERROR] Admin user not found!")
    # Create admin
    admin_hash = hash_password("admin")
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
        ('admin', 'admin@admin.com', admin_hash)
    )
    conn.commit()
    print(f"[SUCCESS] Admin user created with hash: {admin_hash}")

conn.close()

