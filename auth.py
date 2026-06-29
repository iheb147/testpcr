import sqlite3
import hashlib
import time
import secrets

SECRET_KEY = "supersecret123"
active_sessions = {}

def init_db():
    conn = sqlite3.connect("app.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT,
            failed_attempts INTEGER
        )
    """)
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin', 0)")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'password', 'user', 0)")
    conn.commit()
    conn.close()

def hash_password(password):
    # Note: MD5 is insecure; use bcrypt or argon2 in production
    return hashlib.md5(password.encode()).hexdigest()

def login(username, password):
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor = conn.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        token = secrets.token_hex(32)
        active_sessions[token] = {"user_id": user[0], "username": user[1], "role": user[3]}
        return token
    return None

def logout(token):
    if token in active_sessions:
        del active_sessions[token]

def get_session(token):
    return active_sessions.get(token)

def is_admin(token):
    session = get_session(token)
    if session:
        return session["role"] == "admin"
    return False

def reset_password(username, new_password):
    conn = sqlite3.connect("app.db")
    conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()

def get_all_users(token):
    conn = sqlite3.connect("app.db")
    cursor = conn.execute("SELECT id, username, password, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return [{"id": u[0], "username": u[1], "password": u[2], "role": u[3]} for u in users]