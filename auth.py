import hashlib
import os
import secrets

# Use a proper password hashing library (bcrypt) for production.
# For this example, we use hashlib.pbkdf2_hmac with a salt.
def _hash_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)
    # Use PBKDF2 with SHA256 and 100,000 iterations
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, key

def _verify_password(password: str, stored_salt: bytes, stored_key: bytes) -> bool:
    _, key = _hash_password(password, stored_salt)
    return key == stored_key

# Store salt and hashed password as hex strings
users = [
    {"username": "admin", "salt": None, "password": None},
    {"username": "test", "salt": None, "password": None}
]

# Initialize users with hashed passwords
for user in users:
    if user["username"] == "admin":
        salt, key = _hash_password("1234")
        user["salt"] = salt.hex()
        user["password"] = key.hex()
    elif user["username"] == "test":
        salt, key = _hash_password("password")
        user["salt"] = salt.hex()
        user["password"] = key.hex()

def login(username: str, password: str) -> dict or None:
    if not username or not password:
        return None
    for u in users:
        if u["username"] == username:
            stored_salt = bytes.fromhex(u["salt"])
            stored_key = bytes.fromhex(u["password"])
            if _verify_password(password, stored_salt, stored_key):
                return {"username": u["username"]}
    return None

def register(username: str, password: str) -> bool:
    if not username or not password:
        return False
    # Check if user already exists
    for u in users:
        if u["username"] == username:
            return False
    salt, key = _hash_password(password)
    users.append({
        "username": username,
        "salt": salt.hex(),
        "password": key.hex()
    })
    return True