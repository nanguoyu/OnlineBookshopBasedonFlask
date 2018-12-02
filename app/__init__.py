import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NANGUOYU'
    bootstrap.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

