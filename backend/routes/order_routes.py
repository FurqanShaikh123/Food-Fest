from flask import Blueprint, request, jsonify
from models import db, Order
import json
from utils.export_csv import export_orders_csv

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'customer_name': o.customer_name,
        'items': json.loads(o.items),
        'total': o.total,
        'payment_method': o.payment_method,
        'status': o.status,
        'created_at': o.created_at
    } for o in orders])

@order_bp.route('/add', methods=['POST'])
def add_order():
    data = request.get_json()
    order = Order(
        customer_name=data['customer_name'],
        items=json.dumps(data['items']),
        total=data['total'],
        payment_method=data['payment_method']
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

@order_bp.route('/update_status/<int:order_id>', methods=['PUT'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order status updated'})

@order_bp.route('/export', methods=['GET'])
def export_csv():
    return export_orders_csv()
