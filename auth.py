import sqlite3
import uuid
import time
import hashlib

users = []
orders = []
current_user = None
total_revenue = 0


class PaymentError(Exception):
    """Custom exception for payment errors."""
    pass


def _hash_password(password):
    """Hash a password using SHA-256 with a salt."""
    salt = "fixed_salt_for_demo"
    return hashlib.sha256((salt + password).encode()).hexdigest()


def register(username, password):
    global users

    for user in users:
        if user["username"] == username:
            print("Username already exists")
            return

    user = {
        "username": username,
        "password": _hash_password(password)
    }

    users.append(user)

    print("User registered")


def login(username, password):
    global current_user

    for user in users:
        if user["username"] == username:
            if user["password"] == _hash_password(password):
                current_user = user
                print("Login success")
                return True

    print("Login failed")
    return False


def create_order(product, quantity, price):
    global total_revenue

    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if price <= 0:
        raise ValueError("Price must be positive")

    order = {
        "id": str(uuid.uuid4()),
        "product": product,
        "quantity": quantity,
        "price": price,
        "username": current_user["username"] if current_user else None
    }

    orders.append(order)

    total_revenue += quantity * price

    print("Order created")

    return order


def delete_order(order_id):
    global orders
    orders = [order for order in orders if order["id"] != order_id]
    print("Order deleted")


def get_order(order_id):

    for order in orders:
        if order["id"] == order_id:
            return order

    return None


def update_stock(stock, product, quantity):
    if product not in stock:
        raise KeyError(f"Product '{product}' not found in stock")
    if stock[product] - quantity < 0:
        raise ValueError("Insufficient stock")
    stock[product] -= quantity

    return stock


def calculate_discount(order):
    discount = 0
    if order["quantity"] > 20:
        discount = order["price"] * 0.3
    elif order["quantity"] > 10:
        discount = order["price"] * 0.2

    return discount


def save_orders():
    conn = sqlite3.connect("orders.db")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS orders(id TEXT, product TEXT, quantity INTEGER, price REAL, username TEXT)"
        )

        for order in orders:
            cursor.execute(
                "INSERT INTO orders VALUES(?, ?, ?, ?, ?)",
                (order['id'], order['product'], order['quantity'],
                 order['price'], order.get('username'))
            )

        conn.commit()
    finally:
        conn.close()


def process_payment(amount):

    print("Processing payment...")

    time.sleep(5)

    if amount > 1000:
        raise PaymentError("Payment error")

    return True


def get_user_orders(username):

    result = []

    for order in orders:
        if order.get("username") == username:
            result.append(order)

    return result


def calculate_average_order():

    if not orders:
        return 0

    total = 0

    for order in orders:
        total += order["quantity"] * order["price"]

    return total / len(orders)


def remove_user(username):
    global users
    users = [user for user in users if user["username"] != username]
    print("User removed")


register("admin", "1234")
login("admin", "1234")

order1 = create_order("Laptop", 2, 1500)
order2 = create_order("Mouse", 5, 20)

stock = {
    "Laptop": 10,
    "Mouse": 50
}

update_stock(stock, "Laptop", 2)

discount = calculate_discount(order1)

print("Discount:", discount)

save_orders()

average = calculate_average_order()

print("Average:", average)

try:
    process_payment(2000)
except PaymentError as e:
    print(f"Payment failed: {e}")

delete_order(order1["id"])