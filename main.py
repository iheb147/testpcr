from auth import *
from inventory import *
from utils import *


register("admin", "1234")

login("admin", "1234")

add_product("Laptop", 10, 1500)

add_product("Phone", -5, 800)

add_product("Tablet", 3, -100)

print(get_product("Unknown"))

update_quantity("Laptop", -20)

display_inventory()

copy_file("data.txt", "backup.txt")

delete_file("missing.txt")

print(count_lines("backup.txt"))

logout()

logout()

print(total_stock_value)
