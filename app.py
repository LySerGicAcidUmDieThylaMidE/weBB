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



