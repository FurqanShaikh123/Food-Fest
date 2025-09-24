from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "price": self.price}

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    items = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Placed")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "payment_method": self.payment_method,
            "items": json.loads(self.items),
            "status": self.status
        }
