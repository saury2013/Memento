# -*- coding: utf-8 -*-

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from app.config_default import Config as DefaultConfig
from app.models.user import User
from app.models import db

base_dir = path.abspath(path.dirname(__file__))


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DefaultConfig)
    db.init_app(app)
    login_manager.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth,url_prefix='/auth')

    login_manager.login_view = "auth.login"
    login_manager.login_message = "please login..."

    return app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
