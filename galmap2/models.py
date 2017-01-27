from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class System(Base):
    __tablename__ = 'systems'
    id = Column(Integer, primary_key=True)
    edsm_id = Column(Integer)
    name = Column(Text)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    population = Column(Integer)
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
    simbad_ref = Column(Integer)
    controlling_minor_faction_id = Column(Integer)
    controlling_minor_faction = Column(Text)
    reserve_type_id = Column(Integer)
    reserve_type = Column(Text)


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass