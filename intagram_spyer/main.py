# -*- encoding: utf-8 -*-
__author__ = 'pahaz'

from bottle import route, run, template, response
import requests as r


@route('/inst/<lat>/<lng>/')
def inst(lat, lng):
    url = 'https://api.instagram.com/v1/media/search?lat={lat:0.6f}&lng={lng:0.6f}&client_id=3d56e75ea0ae4b96aa459aa22530a519' \
        .format(lng=float(lng), lat=float(lat))
    rez = r.get(url)

    response.content_type = 'application/json; charset=utf-8'
    return rez.content


@route('/')
def index():
    a = open('index.html')
    return a.read()


run(host='localhost', port=80)
