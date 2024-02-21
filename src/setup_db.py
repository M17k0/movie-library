"""
Set up database
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def init_database(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)    
    
def create_database(app: Flask) -> None:
    db_path = path.join("..", "instance", DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database Created")
        return
    print("Database already exists")