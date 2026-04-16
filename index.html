from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = "secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1111@localhost/luderezone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# модели

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, nullable=False)


# апи

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    print("REGISTER DATA:", data)
    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        return jsonify({"error": "Заполните все поля"}), 400

    if User.query.filter_by(login=login).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    user = User(
        login=login,
        password_hash=generate_password_hash(password),
        role=0
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    login = data.get("login")
    password = data.get("password")

    user = User.query.filter_by(login=login).first()

    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["role"] = user.role
        return jsonify({"message": "success"})
    else:
        return jsonify({"error": "Неверный логин или пароль"}), 401


@app.route("/api/me")
def me():
    if "user_id" not in session:
        return jsonify({"user": None})

    return jsonify({
        "user": {
            "id": session["user_id"],
            "role": session["role"]
        }
    })


@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "logged out"})


# фронт

@app.route("/")
def index():
    return send_from_directory("static", "index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
