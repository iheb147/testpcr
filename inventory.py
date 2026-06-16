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
            inventory = json.load(f)
    except FileNotFoundError:
        logger.warning(f"File {FILE} not found. Starting with empty inventory.")
        inventory = []
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {FILE}: {e}")
        inventory = []
    return inventory

def add_item(name, price, qty):
    if not isinstance(name, str) or not name.strip():
        logger.error("Item name must be a non-empty string.")
        return
    if not isinstance(price, (int, float)) or price < 0:
        logger.error("Price must be a non-negative number.")
        return
    if not isinstance(qty, int) or qty < 0:
        logger.error("Quantity must be a non-negative integer.")
        return
    item = {
        "name": name.strip(),
        "price": price,
        "qty": qty
    }
    inventory.append(item)

def total_value():
    total = 0
    for item in inventory:
        total += item["price"] * item["qty"]
    return total