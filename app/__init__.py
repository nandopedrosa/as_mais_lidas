from flask import Flask
from flask.ext.mail import Mail
import config

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)

from app import views
