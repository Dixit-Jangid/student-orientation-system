"""Fix admin password"""
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
    print(f"Password: admin")
    print("\nYou can now login with:")
    print("  Username: admin")
    print("  Password: admin")
else:
    # Create admin if doesn't exist
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
        ('admin', 'admin@admin.com', admin_password_hash)
    )
    conn.commit()
    print("[SUCCESS] Admin user created!")
    print("\nYou can now login with:")
    print("  Username: admin")
    print("  Password: admin")

conn.close()

