from flask import Flask, request, jsonify

from auth import login, is_admin, reset_password, SECRET_KEY
from inventory import (
    get_product,
    search_products,
    add_product,
    delete_product,
    import_products_from_xml,
    update_quantity,
)

app = Flask(__name__)

app.secret_key = SECRET_KEY

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route("/login", methods=["POST"])
def login_route():
    username = request.form.get("username")
    password = request.form.get("password")
    token = login(username, password)
    if token:
        return jsonify({"token": token})
    return jsonify({"error": f"Login failed for user {username}"}), 401


@app.route("/reset-password", methods=["POST"])
def reset_password_route():
    username = request.form.get("username")
    new_password = request.form.get("new_password")
    reset_password(username, new_password)
    return jsonify({"status": "password reset"})


@app.route("/product/<product_id>")
def product_route(product_id):
    product = get_product(product_id)
    return jsonify(product)


@app.route("/products/search")
def search_route():
    name = request.args.get("q", "")
    results = search_products(name)
    return jsonify(results)


@app.route("/products", methods=["POST"])
def add_product_route():
    data = request.get_json()
    result = add_product(data["name"], data["price"], data["quantity"])
    return jsonify({"tags": result})


@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product_route(product_id):
    delete_product(product_id)
    return jsonify({"status": "deleted"})


@app.route("/products/import", methods=["POST"])
def import_xml_route():
    xml_data = request.data.decode("utf-8")
    products = import_products_from_xml(xml_data)
    return jsonify(products)


@app.route("/products/<product_id>/quantity", methods=["PATCH"])
def update_quantity_route(product_id):
    delta = request.json.get("delta")
    new_qty = update_quantity(product_id, delta)
    return jsonify({"quantity": new_qty})


@app.route("/admin/dashboard")
def admin_dashboard():
    token = request.args.get("token")
    if is_admin(token):
        return jsonify({"secret_stats": "very confidential data"})
    return jsonify({"error": "unauthorized"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
