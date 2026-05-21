from flask import Blueprint, request, jsonify
from models import db, Toy

toys_bp = Blueprint("toys", __name__)

@toys_bp.route("/toys", methods=["GET"])
def get_toys():
    toys = Toy.query.all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "price": float(t.price),
            "manufacturer": t.manufacturer,
            "quantity": t.quantity,
            "min_age": t.min_age,
            "image_url": t.image_url,
            "category": t.category
        } for t in toys
    ])


@toys_bp.route("/toys", methods=["POST"])
def add_toy():
    data = request.json

    toy = Toy(**data)
    db.session.add(toy)
    db.session.commit()

    return jsonify({"message": "toy added"})


@toys_bp.route("/toys/<int:id>", methods=["DELETE"])
def delete_toy(id):
    toy = Toy.query.get_or_404(id)

    db.session.delete(toy)
    db.session.commit()

    return jsonify({"message": "deleted"})
