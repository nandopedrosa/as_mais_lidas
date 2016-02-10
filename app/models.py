"""
models.py: Business classes for the Model Layer

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from app import app, db


class NewsSource(db.Model):
    id_news_source = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128), unique=True, nullable=False)
    url = db.Column(db.String(128), nullable=False)

    def __init__(self, name, key, url):
        self.name = name
        self.key = key
        self.url = url

    def __repr__(self):
        return 'Name: ' + name + ', Key: ' + key + ', URL: ' + url
