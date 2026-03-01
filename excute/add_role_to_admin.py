"""Add role column to users table and set admin role"""
import sqlite3

# Connect to database
conn = sqlite3.connect('specialization_prediction.db')
cursor = conn.cursor()

# Add role column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    conn.commit()
    print("[SUCCESS] Added 'role' column to users table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("[INFO] 'role' column already exists")
    else:
        print(f"[WARNING] Error adding role column: {e}")

# Update admin user to have admin role
cursor.execute(
    "UPDATE users SET role = 'admin' WHERE username = 'admin'"
)
conn.commit()

# Verify
cursor.execute("SELECT id, username, role FROM users WHERE username = 'admin'")
result = cursor.fetchone()

if result:
    user_id, username, role = result
    print(f"\n[VERIFICATION]")
    print(f"ID: {user_id}")
    print(f"Username: {username}")
    print(f"Role: {role}")
    
    if role == 'admin':
        print("\n[SUCCESS] Admin user has admin role!")
    else:
        print("\n[ERROR] Admin user does not have admin role!")
else:
    print("[ERROR] Admin user not found!")

# Show all users with roles
cursor.execute("SELECT id, username, role FROM users")
all_users = cursor.fetchall()
print(f"\n[ALL USERS]")
print(f"Total users: {len(all_users)}")
for user_id, username, role in all_users:
    role_display = role if role else 'user (default)'
    print(f"  ID: {user_id}, Username: {username}, Role: {role_display}")

conn.close()

print("\n" + "="*60)
print("ROLE SYSTEM UPDATED")
print("="*60)
print("\nIMPORTANT: Restart the backend server!")
print("  cd backend")
print("  uvicorn main:app --reload")

