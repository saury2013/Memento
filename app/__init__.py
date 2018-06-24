# -*- coding: utf-8 -*-

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskext.markdown import Markdown
from flask_wtf.csrf import CSRFProtect


from app.config_default import Config as DefaultConfig
from app.models.user import User
from app.models import db


base_dir = path.abspath(path.dirname(__file__))

csrf = CSRFProtect()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)

    app.config.from_object(DefaultConfig)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    Markdown(app)

    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth,url_prefix='/auth/')

    from app.api import api
    app.register_blueprint(api,url_prefix='/api/')

    login_manager.login_view = "auth.login"
    login_manager.login_message = "please login..."



    return app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

