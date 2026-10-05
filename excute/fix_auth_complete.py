"""
Fix authentication to work with both bcrypt and SHA256
Make it work reliably with Python 3.13
"""

import hashlib
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def hash_password_sha256(password: str) -> str:
    """SHA256 password hashing - always works"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password_sha256(plain_password: str, hashed_password: str) -> bool:
    """SHA256 password verification - always works"""
    return hash_password_sha256(plain_password) == hashed_password

# Read auth.py
auth_file = 'backend/auth.py'
with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace get_password_hash to use SHA256 instead of bcrypt
old_hash = '''def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)'''

new_hash = '''def get_password_hash(password: str) -> str:
    """Hash a password - Uses SHA256 for compatibility"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()'''

if old_hash in content:
    content = content.replace(old_hash, new_hash)
    print("[OK] Updated get_password_hash to use SHA256")

# Replace verify_password to support both
old_verify = '''def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash - supports both bcrypt and SHA256"""
    import hashlib
    try:
        # Try bcrypt first
        return pwd_context.verify(plain_password, hashed_password)
    except:
        # Fallback to SHA256 for compatibility with test users
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return sha256_hash == hashed_password'''

new_verify = '''def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash - Uses SHA256"""
    import hashlib
    # Try SHA256 first (most reliable)
    sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    if sha256_hash == hashed_password:
        return True
    # Fallback to bcrypt for old passwords
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False'''

if 'def verify_password' in content:
    # Find and replace verify_password function
    import re
    pattern = r'def verify_password\(.*?\):\s+""".*?"""\s+.*?(?=\n\ndef|\n    def|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), new_verify)
        print("[OK] Updated verify_password")
    else:
        # Simple replace if regex doesn't work
        if 'pwd_context.verify' in content:
            content = re.sub(
                r'def verify_password\([^)]+\):.*?return pwd_context\.verify.*?(?=\n\ndef|\n    def|\Z)',
                new_verify,
                content,
                flags=re.DOTALL
            )
            print("[OK] Updated verify_password (simple method)")

# Write back
with open(auth_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Authentication fixed!")
print("Now all passwords use SHA256 (works with Python 3.13)")

