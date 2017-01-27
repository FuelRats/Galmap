from pyramid.config import Configurator

from sqlalchemy import engine_from_config
from .models import DBSession, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(name='textures', path='static/ED3D-Galaxy-Map/textures')
    config.add_static_view(name='data', path='static/ED3D-Galaxy-Map/data')
    config.add_static_view('deform_static', 'deform:static/')
    config.add_route('home', '/')
    config.add_route('galmap', '/galmap')
    config.add_route('rats', '/rats')
    config.add_route('view_rat', '/view_rat')
    config.add_route('view_today', '/view_today')
    config.add_route('view_api', '/api')
    config.scan()
    return config.make_wsgi_app()
