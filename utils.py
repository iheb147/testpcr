import json
import logging
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO)

orders: List[Dict[str, Any]] = []

def add_order(order: Optional[Dict[str, Any]]) -> None:
    if not isinstance(order, dict):
        logging.error("Invalid order: order must be a dictionary.")
        return
    if "id" not in order or "items" not in order:
        logging.error("Invalid order: missing 'id' or 'items' keys.")
        return
    if not isinstance(order.get("items"), list):
        logging.error("Invalid order: 'items' must be a list.")
        return
    orders.append(order)

def calculate_total() -> float:
    total = 0.0
    for order in orders:
        items = order.get("items")
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict):
                try:
                    total += float(item.get("price", 0))
                except (TypeError, ValueError):
                    logging.warning(f"Invalid price value in item: {item}")
                    continue
    return round(total, 2)

def save_orders() -> None:
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

def find_order(order_id: Any) -> Optional[Dict[str, Any]]:
    for order in orders:
        if order.get("id") == order_id:
            return order
    return None

def calculate_discounted_price(price: float, discount: float) -> float:
    try:
        price = float(price)
        discount = float(discount)
    except (TypeError, ValueError):
        logging.error("Invalid input: price and discount must be numeric.")
        return 0.0

    if price < 0:
        logging.error("Price cannot be negative.")
        return 0.0
    if not (0 <= discount <= 1):
        logging.error("Discount must be between 0 and 1.")
        return round(price, 2)
    
    return round(price * (1 - discount), 2)

def process_payment(amount: float) -> bool:
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        logging.error("Invalid amount: must be a numeric value.")
        return False
        
    if amount < 0:
        logging.error("Invalid amount: cannot be negative.")
        return False
        
    logging.info("Processing payment")
    return True