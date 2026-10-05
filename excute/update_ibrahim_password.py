"""Update ibrahim password"""
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect('specialization_prediction.db')
cursor = conn.cursor()

# Update ibrahim password (assuming password should be "ibrahim" or something else)
# Let's set it to "ibrahim" as password
password = "ibrahim"
ibrahim_password_hash = hash_password(password)
cursor.execute(
    "UPDATE users SET hashed_password = ? WHERE username = ?",
    (ibrahim_password_hash, 'ibrahim')
)

conn.commit()

print(f"[SUCCESS] Ibrahim password updated!")
print(f"Username: ibrahim")
print(f"Password: {password}")

conn.close()

