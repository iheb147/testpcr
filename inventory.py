import json

inventory = []
FILE = "data.json"

def load_items():
    f = open(FILE, "r")
    data = f.read()
    inventory = json.loads(data)
    return inventory

def add_item(name, price, qty):
    inventory.append({
        "name": name,
        "price": price,
        "qty": qty
    })

def total_value():
    total = 0
    for item in inventory:
        total += item["price"]
    return total
