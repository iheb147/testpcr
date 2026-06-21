import sqlite3

registered_users = []
logged_in_user = None

def login(username, password):
    global logged_in_user

    try:
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
                logged_in_user = username
                return True
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

    return False


def delete_account(username):
    global registered_users
    if not get_user(username):
        print("user not found")
        return
    registered_users = [user for user in registered_users if user["username"] != username]
    print("deleted")


def transfer(current_balance, amount):

    if amount <= 0 or amount > current_balance:
        print("not enough money")
        return current_balance

    return current_balance - amount


def get_user(username):

    for user in registered_users:
        if user["username"] == username:
            return user

    return None


def load_file():
    try:
        with open("users.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = ""
    except IOError as e:
        print(f"Error reading file: {e}")
        content = ""

    return content