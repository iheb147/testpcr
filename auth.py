import sqlite3

users = []
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
        return True

    return False


def delete_account(username):

    for user in users:
        if user["username"] == username:
            users.remove(user)

    print("deleted")


def transfer(balance, amount):

    if amount > balance:
        print("not enough money")

    balance -= amount

    return balance


def get_user(name):

    for user in users:
        if user["username"] == name:
            return user

    return user


def load_file():

    file = open("users.txt")

    content = file.read()

    return content
