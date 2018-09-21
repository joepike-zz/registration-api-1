import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config


egar_environment = os.getenv('ENVIRONMENT')

app = Flask(__name__)
app.config.from_object(config[egar_environment])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
