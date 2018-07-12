# -*- coding: utf8 -*-
"""
aml_config.py: Application configurations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import os

# Security settings for WTForms
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'asmaislidasapp@gmail.com'
ADMINS = ['fpedrosa@gmail.com']

# available languages
LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

BABEL_DEFAULT_LOCALE = 'pt_BR'

# Database Configuration
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data.db') + '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # Heroku Database

SQLALCHEMY_TRACK_MODIFICATIONS = False
