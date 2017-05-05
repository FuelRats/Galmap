import json
import logging
import requests
from datetime import date, datetime, timedelta

from pyramid.settings import aslist
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
    settings = request.registry.settings()
    bearer_token = settings['bearer_token']
    response = requests.get("https://api.fuelrats.com/rats?bearer=" +
                            bearer_token + "&limit=2000", verify=False)
    response.encoding = 'utf-8'
    tempjson = response.json()
    rats = []
    # log.debug("Got rats:"+str(tempjson))
    for CMDRName in tempjson['data']:
        rats.append(CMDRName['CMDRname'])
    jrats = json.dumps(rats)
    return {'project': 'galmap2',
            'rats': jrats}


@view_config(route_name='view_today', renderer='templates/galmap.pt')
def view_today(request):
    settings = request.registry.settings()
    bearer_token = settings['bearer_token']
    today = datetime.now() - timedelta(days=1)
    url = "https://api.fuelrats.com/rescues?bearer=" + \
          bearer_token + "&createdAtAfter=" + str(today)
    log.debug("Hitting URL: " + url)
    response = requests.get(url, verify=False)
    tempjson = response.json()
    systems = []
    for rescue in tempjson['data']:
        log.debug("Fetching system " + rescue['system'])
        sysupper = rescue['system'].upper()
        sysreq = DBSession.query(System).filter(System.name.like(sysupper)).limit(10).first()
        if not sysreq:
            continue;
        log.debug("Query return: " + sysreq.name)
        coords = {"x": sysreq.x, "y": sysreq.y, "z": sysreq.z}
        syscoords = coords
        systems.append({"name": rescue['system'],
                        "coords": syscoords,
                        "infos": "<h2><center>Rescue data:</center></h2><br>" +
                                 "<b>Date</b>: " + rescue['createdAt'] + "<br><b>Platform: </b>" +
                                 rescue['platform'] + "<br><b>Epic:</b> " + str(rescue['epic']) +
                                 "<br><b>Code Red:</b> " + str(rescue['codeRed'])
                        })
    return {'project': 'galmap2',
            'title': 'Rescues for ' + str(today),
            'json': json.dumps(systems)}


# @view_config(route_name='view_rat', renderer='templates/galmap.pt')
@view_config(request_method='POST', route_name='view_rat', renderer='templates/galmap.pt')
def view_rat_view(request):
    settings = request.registry.settings()
    bearer_token = settings['bearer_token']
    fields = {}
    if not request.params:
        fields = {"error", "No parameters provided."}
        return fields
    if 'rat' not in request.params:
        fields = {"error", "No rat provided."}
        return fields
    log.debug("Params: " + str(request.params))
    rat = request.params['rat']
    # rat = "e8fc095a-4561-4237-a890-83b859e85156"
    url = "https://api.fuelrats.com/rats?bearer=" + bearer_token + "CMDRname=" + rat
    response = requests.get(url, verify=False)
    tempjson = response.json()
    log.debug("Got rat response: " + str(tempjson) + " type " + str(type(tempjson)))
    ratid = tempjson['data'][0]['id']
    log.debug("RatID:" + ratid)
    url = "https://api.fuelrats.com/rescues?bearer=" + bearer_token + \
          "limit=500&firstLimpet=" + str(ratid)
    rescueres = requests.get(url, verify=False)
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
                        "coords": syscoords,
                        "infos": "<h2><center>Rescue data:</center></h2><br>" +
                                 "<b>Date</b>: " + rescue['createdAt'] + "<br><b>Platform: </b>" +
                                 rescue['platform'] + "<br><b>Epic:</b> " + str(rescue['epic']) +
                                 "<br><b>Code Red:</b> " + str(rescue['codeRed'])
                        })
    rescues.append({"systems": systems})
    return {'project': 'galmap2',
            'title': 'Rescues for ' + rat,
            'json': json.dumps(systems)}


@view_config(route_name='view_api', request_method='OPTIONS')
def view_api(request):
    request.response.headerlist.extend(
        (
            ('Access-Control-Allow-Origin', '*'),
            ('Content-Type', 'application/json')
        ))
    return request


@view_config(route_name='view_api', renderer='json')
def view_api(request):
    settings = request.registry.settings()
    bearer_token = settings['bearer_token']
    fields = {}
    if not request.params:
        fields["error"] = "No parameters provided."
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
            fields[field] = data
        except TypeError:
            fields[field] = None
    return fields
