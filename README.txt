galmap2 README
==================

This is meant to live behind a nginx proxy with SSL.
You should probably switch backends to Postgres, in which case you will also need
to pip install psycopg2. (Requires python-dev installed on the host)
Change the connection string in development.ini and production.ini.
You should use python3 as your virtualenv base.

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- Copy development.ini.default or production.ini.default to galmap.ini and configure.

- $VENV/bin/python initdb.py galmap#mainapp

- $VENV/bin/pserve galmap.ini

