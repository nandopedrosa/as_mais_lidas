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

# Database Configuration
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data.db') + '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # Heroku Database

SQLALCHEMY_TRACK_MODIFICATIONS = False
