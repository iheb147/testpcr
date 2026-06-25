import sqlite3

current_user = None


def login(username, password):
    global current_user

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"""
    SELECT * FROM users
    WHERE username='{username}'
    AND password='{password}'
    """

    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        current_user = username
        print("Login successful")
        return True

    return False


def register(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO users VALUES ('{username}','{password}')"
    )

    conn.commit()

    print("User created")


def logout():
    global current_user

    print(current_user + " disconnected")

    current_user = None
