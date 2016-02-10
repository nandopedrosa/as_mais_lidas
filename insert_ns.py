from app import app
from app import db
from app.models import *
from app.aml_utils import friendly_names, urls


def main():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/as-mais-lidas'
    for key in urls.keys():
        name = friendly_names[key]
        url = urls[key]
        ns = NewsSource(name, key, url)
        db.session.add(ns)
        db.session.commit()


if __name__ == '__main__':
    main()
