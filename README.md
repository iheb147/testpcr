import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_logs(filename):
    errors = []
    try:
        with open(filename, 'r') as f:
            content = f.read()
        for line in content.split("\n"):
            if "ERROR" in line:
                errors.append(line)
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except IOError as e:
        logging.error(f"Error reading file {filename}: {e}")
    return errors

inventory = []
FILE = "data.json"

def load_items():
    global inventory
    try:
        with open(FILE, "r") as f:
            data = f.read()
        inventory = json.loads(data)
    except FileNotFoundError:
        logging.warning(f"File {FILE} not found. Starting with empty inventory.")
        inventory = []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {FILE}: {e}")
        inventory = []
    return inventory

def add_item(name, price, qty):
    if not isinstance(name, str) or not name.strip():
        logging.error("Item name must be a non-empty string.")
        return
    if not isinstance(price, (int, float)) or price < 0:
        logging.error("Price must be a non-negative number.")
        return
    if not isinstance(qty, int) or qty < 0:
        logging.error("Quantity must be a non-negative integer.")
        return
    inventory.append({
        "name": name.strip(),
        "price": price,
        "qty": qty
    })

def total_value():
    total = 0
    for item in inventory:
        total += item["price"] * item["qty"]
    return total

def save_inventory():
    try:
        with open(FILE, "w") as f:
            json.dump(inventory, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving inventory to {FILE}: {e}")

users = [
    {"username": "admin", "password": "admin123"},
    {"username": "test", "password": "testpass"}
]

def login(username, password):
    if not username or not password:
        logging.error("Username and password are required.")
        return None
    for u in users:
        if u["username"] == username:
            if u["password"] == password:
                return {"username": u["username"]}
    logging.warning(f"Failed login attempt for user: {username}")
    return None

def register(username, password):
    if not username or not password:
        logging.error("Username and password are required.")
        return False
    if len(password) < 6:
        logging.error("Password must be at least 6 characters long.")
        return False
    for u in users:
        if u["username"] == username:
            logging.error(f"Username {username} already exists.")
            return False
    users.append({
        "username": username,
        "password": password
    })
    logging.info(f"User {username} registered successfully.")
    return True

if __name__ == "__main__":
    logging.info("Loading app...")
    items = load_items()

    add_item("Laptop", 1200, 2)
    add_item("Mouse", 25, 5)

    logging.info(f"Total: {total_value()}")

    user = login("admin", "admin123")
    if user:
        logging.info(f"Logged: {user['username']}")
    else:
        logging.error("Login failed.")