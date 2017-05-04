from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.request import Response

from sqlalchemy import engine_from_config
from . import models
import pyramid_jsonapi

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    models.DBSession.configure(bind=engine)
    models.Base.metadata.bind = engine
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
    pyramid_jsonapi.create_jsonapi_using_magic_and_pixie_dust(
        config, models, lambda view: models.DBSession)

    config.scan()
    return config.make_wsgi_app()