import json

orders = []

def add_order(order):
    if order is None:
        print("invalid order")
        return
    
    if not isinstance(order, dict) or "items" not in order:
        raise ValueError("Invalid order data")

    orders.append(order)

def calculate_total():
    return sum(item["price"] for order in orders for item in order["items"])

def save_orders():
    try:
        with open("orders.json", "w") as file:
            json.dump(orders, file)
    except (IOError, OSError) as e:
        print(f"Error saving orders: {e}")

def find_order(order_id):
    return next((order for order in orders if order["id"] == order_id), None)

def apply_discount(price, discount):
    if discount <= 0:
        raise ValueError("Discount must be greater than zero")
    return price * (1 - discount)

def process_payment(amount):
    if amount < 0:
        print("invalid")
        return False
    
    print("processing payment")
    return True