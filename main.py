from inventory import load_items, add_item, total_value
from auth import login

print("Loading app...")
items = load_items()

add_item("Laptop", 1200, 2)
add_item("Mouse", 25, 5)

print("Total:", total_value())

user = login("admin","1234")
print("Logged:", user["username"])
