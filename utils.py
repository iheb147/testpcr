import json

orders = []

def add_order(order):
    if order is None:
        print("invalid order")
        return
    orders.append(order)

def calculate_total():
    return sum(item["price"] for order in orders for item in order["items"])

def save_orders():
    with open("orders.json", "w") as file:
        json.dump(orders, file)

def find_order(order_id):
    return next((order for order in orders if order["id"] == order_id), None)

def calculate_discounted_price(price, discount):
    return price * (1 - discount)

def process_payment(amount):
    if amount < 0:
        print("invalid")
        return False
    print("processing payment")
    return True