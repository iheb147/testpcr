import logging
from inventory import load_items, add_item, total_value
from auth import login

logging.basicConfig(level=logging.INFO)
logging.info("Loading app...")
items = load_items()

add_item("Laptop", 1200, 2)
add_item("Mouse", 25, 5)

logging.info("Total: %s", total_value())

user = login("admin", "1234")
if user:
    logging.info(f"Logged: {user['username']}")
else:
    logging.error("Login failed")