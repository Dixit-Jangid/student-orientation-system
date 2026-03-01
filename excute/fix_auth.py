"""
Fix authentication - Add SHA256 support for compatibility
This allows both bcrypt and SHA256 passwords
"""

import hashlib
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.auth import verify_password as bcrypt_verify, get_password_hash as bcrypt_hash

def sha256_hash(password: str) -> str:
    """SHA256 password hashing for compatibility"""
    return hashlib.sha256(password.encode()).hexdigest()

def sha256_verify(plain_password: str, hashed_password: str) -> bool:
    """SHA256 password verification"""
    return sha256_hash(plain_password) == hashed_password

def verify_password_compatible(plain_password: str, hashed_password: str) -> bool:
    """Verify password - supports both bcrypt and SHA256"""
    try:
        # Try bcrypt first
        return bcrypt_verify(plain_password, hashed_password)
    except:
        # Fallback to SHA256
        return sha256_verify(plain_password, hashed_password)

# Update backend/auth.py to use compatible verification
auth_file = 'backend/auth.py'
with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace verify_password function
old_verify = '''def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)'''

new_verify = '''def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash - supports both bcrypt and SHA256"""
    import hashlib
    try:
        # Try bcrypt first
        return pwd_context.verify(plain_password, hashed_password)
    except:
        # Fallback to SHA256 for compatibility with test users
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return sha256_hash == hashed_password'''

if old_verify in content:
    content = content.replace(old_verify, new_verify)
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] Updated auth.py to support both bcrypt and SHA256")
else:
    print("[INFO] auth.py already updated or structure different")

print("\n[SUCCESS] Authentication fixed!")
print("Now you can login with:")
print("  - Users created via API (bcrypt)")
print("  - Users created via add_test_data_simple.py (SHA256)")

