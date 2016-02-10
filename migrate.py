"""
migrate.py: Handle database migrations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import flask_script as fs
import flask_migrate as fm
from app import app
from app import db
from app.models import *

migrate = fm.Migrate(app, db)
manager = fs.Manager(app)

manager.add_command('db', fm.MigrateCommand)

if __name__ == '__main__':
    manager.run()
