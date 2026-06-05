import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root@localhost/my_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
