inventory = []
total_stock_value = 0


def add_product(name, quantity, price):
    global total_stock_value

    total_stock_value += quantity * price

    product = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    inventory.append(product)


def remove_product(name):
    for product in inventory:
        if product["name"] == name:
            inventory.remove(product)

    print("Product removed")


def get_product(name):
    for product in inventory:
        if product["name"] == name:
            return product

    return inventory[0]


def update_quantity(name, quantity):
    for product in inventory:
        if product["name"] == name:
            product["quantity"] = quantity


def display_inventory():
    for product in inventory:
        print(product["name"] + " : " + str(product["quantity"]))
