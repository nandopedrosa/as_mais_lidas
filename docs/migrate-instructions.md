Flask-Migrate instructions:

Initialize the DB:

    $ python migrate.py db init

Migrate the changes (remember to import your app models):

    $ python migrate.py db migrate

Update (apply) the changes to DB:

    $ python migrate.py db upgrade

Note: it was not straightforward to install Postgres + psycopg and use Flask-Migrate.
Things to bear in mind:

1. Export the Postgres Libraries to the system PATH (.bash_profile):

export PATH=$PATH:/Library/PostgreSQL/9.5/bin/
export PATH=$PATH=/Library/PostgreSQL/9.5/lib

2. Update libpq.5.dylib:

$ sudo mv /usr/lib/libpq.5.dylib /usr/lib/libpq.5.dylib.old
$ sudo ln -s /Library/PostgreSQL/9.4/lib/libpq.5.dylib /usr/lib

TO RUN SCRIPT ON HEROKU:

heroku run python  migrate.py db upgrade





