from flask import Response
from models import Order
import csv
import json

def export_orders_csv():
    orders = Order.query.all()
    def generate():
        header = ['ID', 'Customer Name', 'Items', 'Total', 'Payment Method', 'Status', 'Created At']
        yield ','.join(header) + '\n'
        for o in orders:
            row = [
                str(o.id),
                o.customer_name,
                json.dumps(json.loads(o.items)),
                str(o.total),
                o.payment_method,
                o.status,
                str(o.created_at)
            ]
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=orders.csv"})
