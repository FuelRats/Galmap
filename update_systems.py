import os, sys, csv
from datetime import time, datetime, timedelta

import transaction
from odo import odo, dshape

import requests
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from sqlalchemy import engine_from_config

from galmap2.models import (
    DBSession,
    System,
    Body,
    Base,
)


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini.default")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    spinner = spinning_cursor()
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    if os.path.isfile('systems_recently.csv'):
        if datetime.fromtimestamp(os.path.getmtime('systems.csv')) > datetime.today()-timedelta(days=7):
            print("Updated systems file is less than 7 days old, skipping...")
    else:
        print("Downloading systems_recently.csv from EDDB.io...")
        r = requests.get("https://eddb.io/archive/v5/systems_recently.csv", stream=True)
        with open('systems_recently.csv', 'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
        print("Saved systems_recently.csv. Converting CSV to SQL.")
        # Do update on all systems that have changed.

        f = open('systems_recently.csv')
        counter = 0
        for item in csv.DictReader(f):
            counter += 1
            if counter % 100000 == 0:
                print("\r [" + next(spinner) + "] " + str(counter), end="", flush=True)
            elif counter % 10000 == 0:
                print('\r [' + next(spinner) + ']', end="", flush=True)
        with transaction.manager:
            model = System(id=item["id"], edsm_id=item["edsm_id"], name=item["name"],
                           x=item["x"], y=item["y"], z=item["z"], poulation=item["population"],
                           government_id=item["government_id"], government=item["government"],
                           allegiance_id=item["allegiance_id"], allegiance=item["allegiance"],
                           state_id=item["state_id"], state=item["state"], security_id=item["security_id"],
                           primary_economy_id=item["primary_economy_id"], primary_economy=item["primary_economy"],
                           power=item["power"], power_state=item["power_state"],
                           power_state_id=item["power_state_id"], needs_permit=item["needs_permit"],
                           updated_at=item["updated_at"], simbad_ref=item["simbad_ref"],
                           controlling_minor_faction_id=item["controlling_minor_faction_id"],
                           controlling_minor_faction=item["controlling_minor_faction"],
                           reserve_type_id=item["reserve_type_id"], reserve_type=item["reserve_type"])
            DBSession.merge(model)
