import os, sys
from datetime import time, datetime, timedelta

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # Add all the systems!
    if datetime.fromtimestamp(os.path.getmtime('systems.csv')) > datetime.today()-timedelta(days=7):
        print("Using cached systems.csv")
    else:
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
    if datetime.fromtimestamp(os.path.getmtime('bodies.jsonl')) >  datetime.today()-timedelta(days=7):
        print("Using cached bodies.jsonl")
    else:
        print("Downloading bodies.jsonl from EDDB.io...")
        r = requests.get("https://eddb.io.archive/v5/bodies.jsonl", stream=True)
        with open('bodies.jsonl', 'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
    print("Saved bodies.jsonl. Converting JSONL to SQL.")
    ds = dshape("var *{ id: ?int64, created_at: ?int64, updated_at: ?int64, name: ?string, "
                "system_id: ?int64, group_id: ?int64, group_name: ?string, type_id: ?int64, "
                "type_name: ?string, distance_to_arrival: ?int64, full_spectral_class: ?string, "
                "spectral_class: ?string, spectral_sub_class: ?string, luminosity_class: ?string, "
                "luminosity_sub_class: ?string, surface_temperature: ?int64, is_main_star: ?bool, "
                "age: ?int64, solar_masses: ?float64, solar_radius: ?float64, catalogue_gliese_id : ?int64, "
                "catalogue_hipp_id: ?int64, catalogue_hd_id: ?int64, volcanism_type_id: ?int64, "
                "volcanism_type_name: ?string, atmosphere_type_id: ?int64, atmosphere_type_name: ?string, "
                "terraforming_state_id: ?int64, terraforming_state_name: ?string, earth_masses: ?float64, "
                "radius: ?int64, gravity: ?float64, surface_pressure: ?int64, orbital_period: ?float64, "
                "semi_major_axis: ?float64, orbital_eccentricity: ?float64, orbital_inclination: ?float64, "
                "arg_of_periapsis: ?float64, rotational_period: ?float64, "
                "is_rotational_period_tidally_locked: ?bool, axis_tilt: ?float64, eg_id: ?int64, "
                "belt_moon_masses: ?float64, ring_type_id: ?int64, ring_type_name: ?string, "
                "ring_mass: ?int64, ring_inner_radius: ?float64, ring_outer_radius: ?float64, "
                "rings: ?json, atmosphere_composition: ?json, solid_composition: ?json, "
                "materials: ?json, is_landable: ?int64}")
    url = str(engine.url) + "::" + Body.__tablename__
    t = odo('bodies.jsonl', url, dshape=ds)
    print("Creating indexes...")
    DBSession.execute("CREATE INDEX bodies_idx on bodies(name)")
    print("Done!")
main()
