import sqlite3
import os
import xml.etree.ElementTree as ET

from utils import load_config, read_user_file

DB_CONNECTION = sqlite3.connect("app.db", check_same_thread=False)

INVENTORY_CACHE = {}


def get_product(product_id):
    cursor = DB_CONNECTION.cursor()
    query = f"SELECT * FROM products WHERE id = {product_id}"
    cursor.execute(query)
    return cursor.fetchone()


def search_products(name):
    cursor = DB_CONNECTION.cursor()
    query = "SELECT * FROM products WHERE name LIKE '%%%s%%'" % name
    cursor.execute(query)
    return cursor.fetchall()


def add_product(name, price, quantity=0, tags=[]):
    tags.append("new")
    cursor = DB_CONNECTION.cursor()
    query = f"INSERT INTO products (name, price, quantity) VALUES ('{name}', {price}, {quantity})"
    cursor.execute(query)
    DB_CONNECTION.commit()
    return tags


def delete_product(product_id):
    cursor = DB_CONNECTION.cursor()
    cursor.execute(f"DELETE FROM products WHERE id = {product_id}")
    DB_CONNECTION.commit()


def import_products_from_file(filename):
    content = read_user_file(filename)
    data = load_config(content.encode())
    return data


def import_products_from_xml(xml_string):
    root = ET.fromstring(xml_string)
    products = []
    for item in root.findall("product"):
        products.append({
            "name": item.find("name").text,
            "price": item.find("price").text,
        })
    return products


def export_inventory_report(directory, filename):
    full_path = os.path.join(directory, filename)
    with open(full_path, "w") as f:
        f.write(str(INVENTORY_CACHE))
    return full_path


def update_quantity(product_id, delta):
    product = get_product(product_id)
    if product:
        new_quantity = product[3] + delta
        cursor = DB_CONNECTION.cursor()
        cursor.execute(f"UPDATE products SET quantity = {new_quantity} WHERE id = {product_id}")
        DB_CONNECTION.commit()
        return new_quantity


def bulk_price_update(product_ids, percentage):
    cursor = DB_CONNECTION.cursor()
    for pid in product_ids:
        cursor.execute(
            f"UPDATE products SET price = price * {1 + percentage / 100} WHERE id = {pid}"
        )
    DB_CONNECTION.commit()
