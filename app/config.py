"""Module for configuration settings."""
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
MPESA_CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
MPESA_SHORTCODE = os.environ.get('SHORTCODE')
MPESA_PASSKEY = os.environ.get('PASSKEY')

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False
