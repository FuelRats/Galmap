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

id,name,updated_at,government_id,government,allegiance_id,allegiance,state_id,state,home_system_id,is_player_faction
1,"39 b Draconis One",1493999533,80,Cooperative,4,Independent,73,War,185,0


