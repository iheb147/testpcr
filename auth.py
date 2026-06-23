import sqlite3
import random
import time

users = []
orders = []
current_user = None
total_revenue = 0


def register(username, password):
    global users

    user = {
        "username": username,
        "password": password
    }

    users.append(user)

    print("User registered")


def login(username, password):
    global current_user

    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                current_user = user
                print("Login success")
                return True

    print("Login failed")
    return False


def create_order(product, quantity, price):
    global total_revenue

    order = {
        "id": random.randint(1, 100),
        "product": product,
        "quantity": quantity,
        "price": price
    }

    orders.append(order)

    total = quantity * price

    total_revenue += price

    print("Order created")

    return order


def delete_order(order_id):

    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)

    print("Order deleted")


def get_order(order_id):

    for order in orders:
        if order["id"] == order_id:
            return order

    return {}


def update_stock(stock, product, quantity):

    stock[product] = stock[product] - quantity

    return stock


def calculate_discount(order):

    if order["quantity"] > 10:
        discount = order["price"] * 0.2

    if order["quantity"] > 20:
        discount = order["price"] * 0.3

    return discount


def save_orders():

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orders(id INTEGER, product TEXT, quantity INTEGER, price REAL)"
    )

    for order in orders:

        query = f"""
        INSERT INTO orders VALUES(
        {order['id']},
        '{order['product']}',
        {order['quantity']},
        {order['price']}
        )
        """

        cursor.execute(query)

    conn.commit()


def process_payment(amount):

    print("Processing payment...")

    time.sleep(5)

    if amount > 1000:
        raise Exception("Payment error")

    return True


def get_user_orders(username):

    result = []

    for order in orders:
        if order.get("username") == username:
            result.append(order)

    return result


def calculate_average_order():

    total = 0

    for order in orders:
        total += order["quantity"] * order["price"]

    return total / len(orders)


def remove_user(username):

    for user in users:
        if user["username"] == username:
            users.remove(user)

    print("User removed")


register("admin", "1234")
register("admin", "1234")

login("admin", "1234")

order1 = create_order("Laptop", 2, 1500)
order2 = create_order("Mouse", -5, 20)

stock = {
    "Laptop": 10,
    "Mouse": 50
}

update_stock(stock, "Laptop", 20)

discount = calculate_discount(order1)

print("Discount:", discount)

save_orders()

average = calculate_average_order()

print("Average:", average)

process_payment(2000)

delete_order(order1["id"])
