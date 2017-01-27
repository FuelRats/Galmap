import os
import sys
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
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    # Add all the systems!

    print("Downloading systems.csv from EDDB.io...")
    r = requests.get("https://eddb.io/archive/v5/systems.csv", stream=True)
    with open('systems.csv', 'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
    print("Saved systems.csv. Converting CSV to SQL.")
    ds = dshape("var *{  id: ?int64,  edsm_id: ?int64,  name: ?string,  x: ?float64,  y: ?float64,  "
                "z: ?float64,  population: ?int64,  is_populated: ?int64,  government_id: ?int64,  "
                "government: ?string,  allegiance_id: ?int64,  allegiance: ?string,  "
                "state_id: ?int64,  state: ?string,  security_id: ?float64,  security: ?string,  "
                "primary_economy_id: ?float64,  primary_economy: ?string,  power: ?string,  "
                "power_state: ?string,  power_state_id: ?string,  needs_permit: ?int64,  "
                "updated_at: ?int64,  simbad_ref: ?string,  controlling_minor_faction_id: ?string,  "
                "controlling_minor_faction: ?string,  reserve_type_id: ?float64,  reserve_type: ?string  }")
    url = str(engine.url) + "::" + System.__tablename__
    t = odo('systems.csv', url, dshape=ds)
    print("Uppercasing system names...")
    DBSession.execute("UPDATE systems set name = UPPER(name)")
    print("Creating indexes...")
    DBSession.execute("CREATE INDEX systems_idx on systems(name)")
    print("Done!")


main()
