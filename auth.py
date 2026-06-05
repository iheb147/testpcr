import hashlib
import os

users = [
    {"username": "admin", "password": hashlib.sha256("1234".encode()).hexdigest()},
    {"username": "test", "password": hashlib.sha256("password".encode()).hexdigest()}
]

def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for u in users:
        if u["username"] == username:
            if u["password"] == hashed_password:
                return u
    return None

def register(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users.append({
        "username": username,
        "password": hashed_password
    })