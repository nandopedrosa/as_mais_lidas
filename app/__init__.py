"""
config.py: Application initialization

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from flask import Flask
from flask.ext.babel import Babel
from flask.json import JSONEncoder as BaseEncoder
from speaklater import _LazyString
import logging
import logging.handlers
from flask.ext.sqlalchemy import SQLAlchemy

"""
=================================================== Custom Config Classes ====================================
"""


class JSONEncoder(BaseEncoder):
    """
    Subclass of BaseEncoder. Allows Flask-Babel lazy_gettext to render error messages on WTForms.
    """

    def default(self, o):
        if isinstance(o, _LazyString):
            return str(o)
        return BaseEncoder.default(self, o)

"""
=================================================== App Initilization ====================================
"""

app = Flask(__name__)

# Load Configurations
app.config.from_pyfile('aml_config.py')

# Flask-Babel
babel = Babel(app)

# Database
db = SQLAlchemy(app)

# Custom JSON Serializer (necessary for Flask-Babel lazy_gettext to work)
app.json_encoder = JSONEncoder

from app import views
