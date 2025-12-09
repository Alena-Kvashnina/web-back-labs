import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///hr_db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
