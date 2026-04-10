from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash



auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(login=data["login"]).first():
        return jsonify({"error": "User exists"}), 400

    user = User(
        login=data["login"],
        password_hash=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(login=data["login"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "success",
        "user_id": user.id,
        "role": user.role
    })


