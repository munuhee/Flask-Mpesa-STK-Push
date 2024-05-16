"""Initialize Flask app with SQLAlchemy and Flask-Migrate.

Creates a Flask app instance, configures it using 'config.py',
sets up SQLAlchemy for database operations, and configures Flask-Migrate.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Initialize CSRF protection
csrf = CSRFProtect(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, services, forms
