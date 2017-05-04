from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Text,
    Float,
    Boolean,
    JSON,
    ForeignKey)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Body(Base):
    __tablename__ = 'bodies'
    id = Column(Integer, primary_key=True)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    name = Column(Text)
    system_id = Column(BigInteger, ForeignKey('system.id'))
    group_id = Column(Integer)
    group_name = Column(Text)
    type_id = Column(BigInteger)
    type_name = Column(Text)
    distance_to_arrival = Column(BigInteger)
    full_spectral_class = Column(Text)
    spectral_class = Column(Text)
    spectral_sub_class = Column(Text)
    luminosity_class = Column(Text)
    luminosity_sub_class = Column(Text)
    surface_temperature = Column(BigInteger)
    is_main_star = Column(Boolean)
    age = Column(BigInteger)
    solar_masses = Column(Float)
    solar_radius = Column(Float)
    catalogue_gliese_id = Column(Text)
    catalogue_hipp_id = Column(Text)
    catalogue_hd_id = Column(Text)
    volcanism_type_id = Column(BigInteger)
    volcanism_type_name = Column(Text)
    atmosphere_type_id = Column(BigInteger)
    atmosphere_type_name = Column(Text)
    terraforming_state_id = Column(BigInteger)
    terraforming_state_name = Column(Text)
    earth_masses = Column(Float)
    radius = Column(BigInteger)
    gravity = Column(Float)
    surface_pressure = Column(BigInteger)
    orbital_period = Column(Float)
    semi_major_axis = Column(Float)
    orbital_eccentricity = Column(Float)
    orbital_inclination = Column(Float)
    arg_of_periapsis = Column(Float)
    rotational_period = Column(Float)
    is_rotational_period_tidally_locked = Column(Boolean)
    axis_tilt = Column(Float)
    eg_id = Column(BigInteger)
    belt_moon_masses = Column(Float)
    ring_type_id = Column(BigInteger)
    ring_type_name = Column(Text)
    ring_mass = Column(BigInteger)
    ring_inner_radius = Column(Float)
    ring_outer_radius = Column(Float)
    rings = Column(JSON)                    # FUCK YOU
    atmosphere_composition = Column(JSON)   # NESTED JSON
    solid_composition = Column(JSON)        # I AM NOT
    materials = Column(JSON)                # DEALING WITH YOU
    is_landable = Column(BigInteger)

class System(Base):
    __tablename__ = 'systems'
    id = Column(Integer, primary_key=True)
    edsm_id = Column(Integer)
    name = Column(Text)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    population = Column(BigInteger)
    is_populated = Column(Integer)
    government_id = Column(Integer)
    government = Column(Text)
    allegiance_id = Column(Integer)
    allegiance = Column(Text)
    state_id = Column(Integer)
    state = Column(Text)
    security_id = Column(Integer)
    security = Column(Text)
    primary_economy_id = Column(Integer)
    primary_economy = Column(Text)
    power = Column(Text)
    power_state = Column(Text)
    power_state_id = Column(Integer)
    needs_permit = Column(Integer)
    updated_at = Column(Integer)
    simbad_ref = Column(Text)
    controlling_minor_faction_id = Column(Integer)
    controlling_minor_faction = Column(Text)
    reserve_type_id = Column(Integer)
    reserve_type = Column(Text)
    bodies = relationship("Body")

class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass