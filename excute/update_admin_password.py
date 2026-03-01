"""Update admin password to use SHA256"""
import sqlite3
import hashlib

def hash_password(password):
    """SHA256 password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

# Update admin password in database
conn = sqlite3.connect('specialization_prediction.db')
cursor = conn.cursor()

# Update admin password
admin_password_hash = hash_password('admin')
cursor.execute(
    "UPDATE users SET hashed_password = ? WHERE username = ?",
    (admin_password_hash, 'admin')
)

conn.commit()

# Verify
cursor.execute("SELECT username, hashed_password FROM users WHERE username = 'admin'")
result = cursor.fetchone()
if result:
    print(f"[SUCCESS] Admin password updated!")
    print(f"Username: {result[0]}")
    print(f"Password hash: {result[1]}")
    print("\nYou can now login with:")
    print("  Username: admin")
    print("  Password: admin")
else:
    print("[ERROR] Admin user not found")

conn.close()

