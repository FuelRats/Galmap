import json
import logging
from urllib.request import urlopen
import urllib.parse
import requests
from datetime import date, datetime, timedelta
import os
import sqlalchemy
from pyramid.view import view_config
from .models import DBSession, System

log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home_view(request):
    return {'project': 'galmap2'}


@view_config(route_name='galmap', renderer='templates/galmap.pt')
def galmap_view(request):
    return {'project': 'galmap2'}


@view_config(route_name='rats', renderer='templates/rats.pt')
def rats_view(request):
    response = urlopen("https://api.fuelrats.com/rats?limit=2000")
    tempjson = json.loads(response.read())
    rats = []
    for CMDRName in tempjson['data']:
        rats.append(CMDRName['CMDRname'])
    return {'project': 'galmap2',
            'rats': rats}


@view_config(route_name='view_today', renderer='templates/galmap.pt')
def view_today(request):
    today = datetime.now() - timedelta(days=1)
    url = "https://api.fuelrats.com/rescues?createdAtAfter=" + str(today)
    log.debug("Hitting URL: " + url)
    response = requests.get(url)
    tempjson = response.json()
    systems = []
    for rescue in tempjson['data']:
        log.debug("Fetching system " + rescue['system'])
        sysreq = requests.get("https://www.edsm.net/api-v1/system?systemName=" +
                              rescue['system'] + "&coords=1")
        log.debug("Got sysdata: " + sysreq.text)
        sysjson = sysreq.json()
        if not sysjson:
            log.debug("Null sysjson...")
            continue
        if sysjson['coords'] is not 'null':
            syscoords = sysjson['coords']
            systems.append({"name": rescue['system'],
                            "coords": syscoords
                            })
    return {'project': 'galmap2',
            'title': 'Rescues for ' + str(today),
            'json': json.dumps(systems)}


@view_config(route_name='view_rat', renderer='templates/galmap.pt')
# @view_config(request_method='POST', route_name='view_rat', renderer='templates/galmap.pt')
def view_rat_view(request):
    # rat = request.params['rat']
    rat = "e8fc095a-4561-4237-a890-83b859e85156"
    url = "https://api.fuelrats.com/rats?id=" + rat
    response = requests.get(url)
    tempjson = response.json()
    log.debug("Got rat response: " + str(tempjson))
    # temp2 = tempjson['data']
    # ratid = temp2[0]['id']
    url = "https://api.fuelrats.com/rescues?firstLimpet=" + rat
    # url = "https://api.fuelrats.com/rescues?firstLimpet=9a61520b-b069-4ece-8274-1230ce43f776"
    rescueres = requests.get(url)
    log.debug("Text version:" + rescueres.text)
    rescuejson = rescueres.json()
    log.debug("Fetched rescues: " + str(rescuejson))
    rescues = []
    systems = []
    for rescue in rescuejson['data']:
        log.debug("Fetching system " + rescue['system'])
        sysupper = rescue['system'].upper()
        sysreq = DBSession.query(System).filter(System.name.like(sysupper)).limit(10).first()
        if not sysreq:
            continue;
        log.debug("Query return: " + sysreq.name)
        coords = {"x": sysreq.x, "y": sysreq.y, "z": sysreq.z}
        syscoords = coords
        systems.append({"name": rescue['system'],
                        "coords": syscoords
                        })
    rescues.append({"systems": systems})
    return {'project': 'galmap2',
            'title': 'Rescues for Absolver',
            'json': json.dumps(systems)}

@view_config(route_name='view_api', renderer='json')
def view_api(request):
    fields = {}
    if not request.params:
        fields["error"]="No parameters provided."
        return fields
    if 'name' not in request.params:
        fields["error"] = "Missing system name parameter."
        return fields
    sysname = request.params['name'].upper()
    sysreq = DBSession.query(System).filter(System.name.like(sysname)).limit(10).first()
    fields = {}
    for field in [x for x in dir(sysreq) if not x.startswith('_') and x != 'metadata']:
        data = sysreq.__getattribute__(field)
        try:
            json.dumps(data)
            fields[field]=data
        except TypeError:
            fields[field]=None
    return fields