"""Create admin user with proper encoding"""
import sqlite3
import hashlib
import sys

def hash_password(password):
    """Hash password with SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_admin():
    """Create admin user in database"""
    conn = sqlite3.connect('specialization_prediction.db')
    cursor = conn.cursor()
    
    # Delete existing admin if exists
    cursor.execute("DELETE FROM users WHERE username = 'admin'")
    conn.commit()
    
    # Create new admin user
    admin_hash = hash_password('admin')
    try:
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
            ('admin', 'admin@admin.com', admin_hash)
        )
        conn.commit()
        print(f"[SUCCESS] Admin user created!")
        print(f"Username: admin")
        print(f"Password: admin")
        print(f"Hash: {admin_hash}")
    except sqlite3.IntegrityError as e:
        print(f"[ERROR] Integrity error: {e}")
        # Try to update instead
        cursor.execute(
            "UPDATE users SET hashed_password = ?, email = ? WHERE username = ?",
            (admin_hash, 'admin@admin.com', 'admin')
        )
        conn.commit()
        print(f"[SUCCESS] Admin user updated!")
    
    # Verify
    cursor.execute("SELECT id, username, email, hashed_password FROM users WHERE username = 'admin'")
    result = cursor.fetchone()
    
    if result:
        user_id, username, email, stored_hash = result
        print(f"\n[VERIFICATION]")
        print(f"ID: {user_id}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Hash: {stored_hash}")
        
        # Test password verification
        test_hash = hash_password('admin')
        is_valid = test_hash == stored_hash
        print(f"Password verification: {'[PASS]' if is_valid else '[FAIL]'}")
        print(f"Expected hash: {test_hash}")
        print(f"Stored hash: {stored_hash}")
        print(f"Match: {is_valid}")
        
        return True
    else:
        print("[ERROR] Admin user not found after creation!")
        return False
    
    conn.close()

if __name__ == "__main__":
    success = create_admin()
    if success:
        print("\n" + "="*60)
        print("ADMIN USER CREATED SUCCESSFULLY")
        print("="*60)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin")
        print("\nIMPORTANT: Restart the backend server!")
        print("  cd backend")
        print("  uvicorn main:app --reload")
    else:
        print("\n[ERROR] Failed to create admin user!")
        sys.exit(1)

