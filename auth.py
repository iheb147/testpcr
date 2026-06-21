import sqlite3

users = []
current_user = None

def login(username, password):
    global current_user

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()

        query = """
        SELECT * FROM users
        WHERE username=?
        AND password=?
        """

        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        if result:
            current_user = username
            return True

    return False


def delete_account(username):
    global users
    users = [user for user in users if user["username"] != username]
    print("deleted")


def transfer(balance, amount):

    if amount <= 0 or amount > balance:
        print("not enough money")
        return balance

    return balance - amount


def get_user(name):

    for user in users:
        if user["username"] == name:
            return user

    return None


def load_file():

    with open("users.txt", "r") as file:
        content = file.read()

    return content