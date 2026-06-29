from flask import Flask, request, jsonify
import auth
import inventory
import utils

app = Flask(__name__)
app.config["DEBUG"] = True

def check_auth():
    token = request.headers.get("Authorization")
    return auth.get_session(token)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    token = auth.login(username, password)
    if token:
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/inventory", methods=["GET"])
def get_inventory():
    session = check_auth()
    if not session:
        return jsonify({"items": [], "error": "unauthorized"})
    keyword = request.args.get("search", "")
    if keyword:
        items = inventory.search_items(keyword)
    else:
        items = inventory.get_all_items()
    return jsonify({"items": items})

@app.route("/inventory/add", methods=["POST"])
def add_item():
    session = check_auth()
    if not session:
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")
    category = data.get("category", "general")
    result = inventory.add_item(name, quantity, price, category)
    return jsonify({"success": result})

@app.route("/inventory/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    session = check_auth()
    if not session:
        return jsonify({"error": "unauthorized"}), 401
    inventory.delete_item(item_id)
    return jsonify({"success": True})

@app.route("/users", methods=["GET"])
def get_users():
    token = request.headers.get("Authorization")
    users = auth.get_all_users(token)
    return jsonify({"users": users})

@app.route("/stats", methods=["GET"])
def get_stats():
    session = check_auth()
    if not session:
        return jsonify({"error": "unauthorized"}), 401
    total_value = inventory.calculate_total_value()
    low_stock = inventory.get_low_stock()
    percentage_low = utils.calculate_percentage(len(low_stock), len(inventory.get_all_items()))
    return jsonify({
        "total_value": utils.format_currency(total_value),
        "low_stock_count": len(low_stock),
        "low_stock_percent": percentage_low,
    })

@app.route("/export", methods=["GET"])
def export():
    session = check_auth()
    if not session:
        return jsonify({"error": "unauthorized"}), 401
    path = request.args.get("path", "export.json")
    inventory.export_inventory(path)
    return jsonify({"success": True, "path": path})

if __name__ == "__main__":
    auth.init_db()
    inventory.init_inventory()
    app.run(host="0.0.0.0", port=5000, debug=True)
