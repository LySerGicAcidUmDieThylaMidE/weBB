from flask import Blueprint, request, jsonify
from models import db, Order

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.json

    order = Order(**data)
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "order created"})