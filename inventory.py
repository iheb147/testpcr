import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

inventory = []
FILE = "data.json"

def load_items():
    global inventory
    try:
        with open(FILE, "r") as f:
            data = f.read()
            inventory = json.loads(data)
    except FileNotFoundError:
        logger.warning(f"File {FILE} not found. Starting with empty inventory.")
        inventory = []
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {FILE}: {e}")
        inventory = []
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