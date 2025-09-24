from flask import Blueprint, request, jsonify
from models import db, MenuItem

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'description': i.description,
        'price': i.price,
        'category': i.category,
        'image_url': i.image_url
    } for i in items])

@menu_bp.route('/add', methods=['POST'])
def add_menu_item():
    data = request.get_json()
    item = MenuItem(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Menu item added successfully'}), 201

@menu_bp.route('/update/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify({'message': 'Menu item updated successfully'})

@menu_bp.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Menu item deleted successfully'})
