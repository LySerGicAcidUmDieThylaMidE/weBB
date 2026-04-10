from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=0)


class Toy(db.Model):
    __tablename__ = "toys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    manufacturer = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    min_age = db.Column(db.Integer)


class CartItem(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    toy_id = db.Column(db.Integer, db.ForeignKey("toys.id"))
    quantity = db.Column(db.Integer, default=1)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total_price = db.Column(db.Numeric(10, 2))