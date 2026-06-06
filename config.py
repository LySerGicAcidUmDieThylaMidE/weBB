import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")
    
    # Сначала проверяем переменную DATABASE_URL от Render. 
    # Если её нет — включается ваша локальная база.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://root:1111@localhost/luderezone'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
