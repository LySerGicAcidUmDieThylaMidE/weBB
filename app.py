from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(
    __name__,
    static_folder="../static"
)

app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1111@localhost/luderezone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ models ------------------

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=0)


class Toy(db.Model):
    __tablename__ = "toys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    manufacturer = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))


class CartItem(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    toy_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    toy_id = db.Column(db.Integer)


# ------------------ auth ------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("login") or not data.get("password"):
        return jsonify({"error": "Заполните все поля"}), 400

    if User.query.filter_by(login=data["login"]).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    user = User(
        login=data["login"],
        password_hash=generate_password_hash(data["password"]),
        role=0
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(login=data.get("login")).first()

    if user and check_password_hash(user.password_hash, data.get("password")):
        session["user_id"] = user.id
        session["user"] = user.login
        session["role"] = user.role
        return jsonify({"message": "success"})

    return jsonify({"error": "Неверный логин или пароль"}), 401


@app.route("/api/me")
def me():
    if "user_id" not in session:
        return jsonify({"user": None})

    return jsonify({
        "user": {
            "id": session["user_id"],
            "role": session["role"],
            "login": session["user"]
        }
    })


@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "logged out"})

@app.route("/api/change-password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return jsonify({"error":"auth"}), 403

    data = request.json

    user = User.query.get(session["user_id"])

    if not check_password_hash(
        user.password_hash,
        data["old_password"]
    ):
        return jsonify({
            "error":"Старый пароль неверный"
        }), 400

    user.password_hash = generate_password_hash(
        data["new_password"]
    )

    db.session.commit()

    return jsonify({
        "message":"Пароль изменён"
    })

# ------------------ toys ------------------

@app.route("/api/toys")
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


@app.route("/api/toys/<int:id>")
def get_toy(id):

    toy = Toy.query.get_or_404(id)

    return jsonify({
        "id": toy.id,
        "name": toy.name,
        "description": toy.description,
        "price": float(toy.price),
        "manufacturer": toy.manufacturer,
        "quantity": toy.quantity,
        "min_age": toy.min_age,
        "image_url": toy.image_url,
        "category": toy.category
    })


@app.route("/api/toys/search")
def search_toys():
    q = request.args.get("q", "")

    toys = Toy.query.filter(Toy.name.contains(q)).all()

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


@app.route("/api/toys/age")
def toys_by_age():
    age = request.args.get("age", type=int)

    if age is None:
        return jsonify([])

    toys = Toy.query.filter(Toy.min_age <= age).all()

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








def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # регистрация роутов
    from routes.auth import auth_bp
    from routes.toys import toys_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(toys_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(orders_bp, url_prefix="/api")

    return app


app = create_app()

from flask import render_template
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



