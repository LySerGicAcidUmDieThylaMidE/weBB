import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://3r2eCYwycnYB3x1.root:I5I10um2rA3CLot2@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/sys"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
