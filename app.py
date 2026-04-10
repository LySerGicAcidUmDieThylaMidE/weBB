from flask import Flask
from config import Config
from models import db

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



