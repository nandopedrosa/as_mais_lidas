"""
config.py: Application initialization

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.facade import get_most_read

"""
=================================================== App Initilization ====================================
"""

app = Flask(__name__)

# Load Configurations
app.config.from_pyfile('aml_config.py')

# Database
from app.models import db
db.init_app(app)

DEFAULT_NS = "uol"

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page with the default News Source
    :return: The rendered index page
    """
    news, header = get_most_read(DEFAULT_NS)
    current_year = datetime.now().year    
    return render_template("ns.html",
                           title='Home Page',
                           year=current_year,
                           news=news,
                           header=header,
                           )

from app import views           


