# -*- coding: utf-8 -*-
"""
Extensions module.

Each extension is initialized in the app factory located in __init__.py
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()