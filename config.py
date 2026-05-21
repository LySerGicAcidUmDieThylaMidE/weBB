import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1111@localhost/luderezone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
