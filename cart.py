from flask import Blueprint, request, jsonify
from models import db, CartItem

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.json

    item = CartItem(**data)
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "added to cart"})


@cart_bp.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "toy_id": i.toy_id,
            "quantity": i.quantity
        } for i in items
    ])