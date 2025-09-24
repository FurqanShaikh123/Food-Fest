# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, MenuItem, Order
import json

app = Flask(__name__)
CORS(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize DB manually (replaces before_first_request)
with app.app_context():
    db.create_all()

    # Add default menu items if table is empty
    if MenuItem.query.count() == 0:
        items = [
            MenuItem(name="Crispy Spring Rolls", description="Fresh vegetables and savory fillings", price=5.0),
            MenuItem(name="Spicy Chicken Wings", description="Marinated chicken wings with a spicy kick", price=7.0),
            MenuItem(name="Grilled Salmon", description="Freshly grilled salmon with asparagus", price=12.0),
            MenuItem(name="Vegetable Stir-Fry", description="Fresh vegetables stir-fried in light sauce", price=6.0),
            MenuItem(name="Chocolate Lava Cake", description="Warm chocolate cake with molten center", price=4.0),
            MenuItem(name="Fruit Tart", description="Sweet tart with seasonal fruits", price=4.5),
        ]
        db.session.add_all(items)
        db.session.commit()

# -----------------------------
# Routes for Customer
# -----------------------------

@app.get("/menu")
def get_menu():
    items = MenuItem.query.all()
    return jsonify([item.to_dict() for item in items])

@app.post("/order")
def place_order():
    data = request.get_json()
    username = data.get("username")
    payment_method = data.get("payment_method")
    items = data.get("items", [])

    if not username or not payment_method or not items:
        return jsonify({"error": "username, payment_method, and items are required"}), 400

    order = Order(username=username, payment_method=payment_method, items=json.dumps(items), status="Placed")
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully", "order_id": order.id})

# -----------------------------
# Routes for Manager
# -----------------------------

@app.get("/orders")
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.put("/order/<int:order_id>/status")
def update_order_status(order_id):
    data = request.get_json()
    status = data.get("status")
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.status = status
    db.session.commit()
    return jsonify({"message": f"Order {order_id} status updated to {status}"})

@app.post("/menu")
def add_menu_item():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    if not name or not price:
        return jsonify({"error": "name and price are required"}), 400

    item = MenuItem(name=name, description=description, price=price)
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Menu item added", "item": item.to_dict()})

@app.put("/menu/<int:item_id>")
def edit_menu_item(item_id):
    data = request.get_json()
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Menu item not found"}), 404

    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    item.price = data.get("price", item.price)
    db.session.commit()
    return jsonify({"message": "Menu item updated", "item": item.to_dict()})

@app.delete("/menu/<int:item_id>")
def remove_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Menu item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Menu item removed"})

# -----------------------------
# Run the server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
