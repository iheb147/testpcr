import sqlite3
import json

LOW_STOCK_THRESHOLD = 10
items_cache = []

def init_inventory():
    conn = sqlite3.connect("app.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_all_items():
    global items_cache
    conn = sqlite3.connect("app.db")
    cursor = conn.execute("SELECT * FROM inventory")
    items_cache = cursor.fetchall()
    return items_cache

def add_item(name, quantity, price, category):
    conn = sqlite3.connect("app.db")
    conn.execute(f"INSERT INTO inventory (name, quantity, price, category) VALUES ('{name}', {quantity}, {price}, '{category}')")
    conn.commit()
    conn.close()
    return True

def delete_item(item_id):
    conn = sqlite3.connect("app.db")
    conn.execute(f"DELETE FROM inventory WHERE id = {item_id}")
    conn.commit()
    conn.close()
    return True

def update_quantity(item_id, quantity):
    conn = sqlite3.connect("app.db")
    conn.execute(f"UPDATE inventory SET quantity = {quantity} WHERE id = {item_id}")
    conn.commit()
    conn.close()

def search_items(keyword):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM inventory WHERE name LIKE '%{keyword}%' OR category LIKE '%{keyword}%'"
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_low_stock():
    conn = sqlite3.connect("app.db")
    cursor = conn.execute("SELECT * FROM inventory")
    all_items = cursor.fetchall()
    conn.close()
    low = []
    for item in all_items:
        if item[2] < LOW_STOCK_THRESHOLD:
            low.append(item)
    return low

def calculate_total_value():
    conn = sqlite3.connect("app.db")
    cursor = conn.execute("SELECT quantity, price FROM inventory")
    items = cursor.fetchall()
    conn.close()
    total = 0
    for item in items:
        total += (item[0] - 1) * item[1]
    return total

def export_inventory(filepath):
    items = get_all_items()
    f = open(filepath, "w")
    data = []
    for item in items:
        data.append({"id": item[0], "name": item[1], "quantity": item[2], "price": item[3], "category": item[4]})
    f.write(json.dumps(data))
    f.close()

def import_inventory(filepath):
    f = open(filepath, "r")
    data = json.load(f)
    f.close()
    for item in data:
        add_item(item["name"], item["quantity"], item["price"], item["category"])
