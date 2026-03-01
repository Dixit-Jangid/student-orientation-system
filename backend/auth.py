"""
Authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db, User
import hashlib

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash - Uses SHA256"""
    if not plain_password or not hashed_password:
        print(f"[AUTH] Missing password or hash - plain: {bool(plain_password)}, hash: {bool(hashed_password)}")
        return False
    
    # Try SHA256 first (most reliable)
    try:
        sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        print(f"[AUTH] Comparing hashes - provided: {sha256_hash[:20]}..., stored: {hashed_password[:20]}...")
        if sha256_hash == hashed_password:
            print("[AUTH] Password verified successfully")
            return True
        else:
            print("[AUTH] Password hash mismatch")
    except Exception as e:
        print(f"[AUTH ERROR] Error hashing password: {e}")
        return False
    
    # Fallback: try direct comparison for old bcrypt passwords
    return False

def get_password_hash(password: str) -> str:
    """Hash a password - Uses SHA256 for compatibility with Python 3.13"""
    # Use utf-8 encoding to match verify_password
    hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"[AUTH] Hashing password - result: {hash_value[:20]}...")
    return hash_value

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
