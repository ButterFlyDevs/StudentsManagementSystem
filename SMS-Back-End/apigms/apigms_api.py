# -*- coding: utf-8 -*-

from flask import Flask, request, Response, make_response
from flask.ext.cors import CORS, cross_origin
import json
from google.appengine.api import modules
import urllib2
from termcolor import colored

import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "localhost"}})



# Activating verbose mode
v = 1

# DEFAULT PORT TO THIS microService in local: 8001

microservice_name = '\n ## dbms Data Base mService ##'

module = modules.get_current_module_name()
instance = modules.get_current_instance_id()


def ping(url, payload=None, method=None):
    """
    Method that isolates the way to do the request front all microservices and how processes the response.

    :param url:
    :param payload:
    :param method:
    :return:
    """

    if payload is None:
        request = urllib2.Request(url)
        if method == 'DELETE':
            request.get_method = lambda: "DELETE"

    else:
        # We need send data with json format and by default is POST
        request = urllib2.Request(url, data=json.dumps(payload.get_json()),
                                  headers={'Content-Type': 'application/json'})
        # We can force to PUT if is the method that we need
        if method is 'PUT':
            request.get_method = lambda: "PUT"

    response = make_response(Response(urllib2.urlopen(request), mimetype='application/json'))
    response.headers['Access-Control-Allow-Origin'] = "*"

    return response


@app.route('/test', methods=['GET'])
def test():
    """
     Test resource.

    :return:

     Example of use:
        curl -i -X GET localhost:8001/test
    """
    response = requests.get("http://%s/test" % modules.get_hostname(module='dbms'))
    return make_response(response.content, response.status_code)


@app.route('/entities/<string:kind>', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type'])
def post_entity(kind):
    """
    Data Base micro Service Resource connector, put all kind of entities in this mService.

    :param kind:
    :payload json:
    :return:

     Example of use:
      curl -i -H "Content-Type: application/json" -X POST -d '{ "data": {"name": "María"} }' localhost:8001/entities/student
      curl -i -H "Content-Type: application/json" -X POST -d '{ "data": {"course": 1, "word": "B", "level": "ESO"} }' localhost:8001/entities/class

    """
    response = requests.post(url='http://' + str(modules.get_hostname(module='dbms')) + '/entities/' + str(kind),
                             json=request.get_json())
    response.headers['Access-Control-Allow-Origin'] = "*"
    return make_response(response.content, response.status_code)



@app.route('/entities/<string:kind>', methods=['GET'])
@app.route('/entities/<string:kind>/<int:entity_id>', methods=['GET'])
def get_entities(kind, entity_id=None):
    """
    Data Base micro Service Resource connector, to get info about all kind of entities in this mService.

    :param kind: Type of entity to get info.
    :param entity_id:
    :return: Exactly the response which is received from service.

    Example of use:

         curl -i -X GET localhost:8001/entities/teacher

    See more info in dbms_apy.py
    """

    url = 'http://' + str(modules.get_hostname(module='dbms')) + '/' + 'entities/' + str(kind)
    if entity_id is not None:
        url += '/' + str(entity_id)

    params = request.args.get('params', None)
    if params != None:
        print params
        url += '?params='+str(params)

    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response



@app.route('/entities/<string:kind>/<int:entity_id>', methods=['PUT'])
def update_entities(kind, entity_id):
    """
    Data Base micro Service Resource connector, to update all kind of entities in this mService.

    :param kind:
    :param entity_id:
    :return:

    Exampe of use:
     # curl -H "Content-Type: application/json" -X PUT -d '{ "data": {"name": "nameModified", "surname": "surnameModified"} }' localhost:8001/entities/teacher/1
    """

    url = 'http://' + modules.get_hostname(module='dbms') + '/entities/' + str(kind) + '/' + str(entity_id)
    return ping(url=url, payload=request, method='PUT')


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    """

    url = 'http://' + modules.get_hostname(module='dbms') + '/entities/' + str(kind) + '/' + str(entity_id)

    return ping(url=url, method='DELETE')


@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind):
    """

    :param kind:
    :param entity_id:
    :param related_kind:
    :return:

     Example of use:
       curl -i -X GET localhost:8001/entities/student/1/teacher
    """

    url = 'http://' + modules.get_hostname(module='dbms') + '/entities/' + str(kind) + '/' + str(entity_id) + '/' + str(related_kind)

    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response




if __name__ == '__main__':
    app.run(debug=True)