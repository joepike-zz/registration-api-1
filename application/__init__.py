from flask import Flask

from config import config
from application.extensions import db, migrate
from .api_0_1_0 import api_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_blueprint, url_prefix='/v0.1.0')
