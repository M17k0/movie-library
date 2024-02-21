"""
Set up the flask web application and database
"""
from flask import Flask
from os import path
from flask_login import LoginManager

from .setup_db import init_database, create_database
from .views import views
from .auth import auth
from . import models

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "very secret key"
    init_database(app)

    app.template_folder = "templates"

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # type: ignore
    login_manager.login_message = ""
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get((id))

    return app
