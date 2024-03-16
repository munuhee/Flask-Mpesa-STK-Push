"""Module for configuration settings.
- loads environment variables using dotenv
- sets up various configuration parameters for the Flask app.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secret key for Flask sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

# Daraja API credentials
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
SHORTCODE = os.environ.get('SHORTCODE')
PASSKEY = os.environ.get('PASSKEY')

# Daraja API endpoints
AUTH_URL = os.environ.get('AUTH_URL')
STK_PUSH_URL = os.environ.get('STK_PUSH_URL')

# SQLite database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///daraja.db'

# Disable Flask-SQLAlchemy modification tracking
SQLALCHEMY_TRACK_MODIFICATIONS = False
