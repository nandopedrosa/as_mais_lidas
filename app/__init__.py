"""
config.py: Application initialization

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.babel import Babel
import config

app = Flask(__name__)

# For session security
app.secret_key = 'F12Zr47jyX R~X@H!jmM]Lwf/,?KT'

app.config.from_object('config')

# Flask-Mail
mail = Mail(app)

# Flask-Babel
babel = Babel(app)

from app import views
