"""
Test script to verify user registration and login
"""
import requests
import hashlib

BASE_URL = "http://127.0.0.1:8000"

def test_register_and_login():
    """Test user registration and login"""
    username = "test_user_" + str(hashlib.md5(str(hashlib.sha256(b"test").hexdigest()).encode()).hexdigest()[:8])
    email = f"{username}@test.com"
    password = "test123"
    
    print(f"\n{'='*60}")
    print("TEST: User Registration and Login")
    print(f"{'='*60}\n")
    
    # 1. Register user
    print(f"1. Registering user: {username}")
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Registration successful")
            print(f"   User ID: {response.json().get('id')}")
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error during registration: {e}")
        return
    
    # 2. Login with registered user
    print(f"\n2. Logging in with: {username}")
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        # OAuth2PasswordRequestForm expects form data
        response = requests.post(
            f"{BASE_URL}/api/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful")
            print(f"   Token: {data.get('access_token', '')[:50]}...")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Has completed test: {data.get('has_completed_test')}")
            print(f"   Redirect to: {data.get('redirect_to')}")
        else:
            print(f"   ❌ Login failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error during login: {e}")
    
    # 3. Test password hash
    print(f"\n3. Testing password hash")
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(f"   Password: {password}")
    print(f"   SHA256 Hash: {password_hash}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    test_register_and_login()

