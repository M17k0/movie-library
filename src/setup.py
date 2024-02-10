from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "very secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    app.template_folder = 'templates'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # type: ignore
    login_manager.login_message = ""
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app

def create_database(app: Flask) -> None:
    db_path = path.join("..", "instance", DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Database Created")
        return
    print("Database already exists")