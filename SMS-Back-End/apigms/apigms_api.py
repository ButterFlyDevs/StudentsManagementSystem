# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask.ext.cors import CORS, cross_origin
import json
from google.appengine.api import modules
import urllib2
from termcolor import colored

import requests
import requests_toolbelt.adapters.appengine



from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)

# With this we get that the requests (in terminal) show the method DELETE instead of OPTIONS.
#CORS(app)
cors = CORS(app, resources={r"/entities/*": {"origins": "*"}})


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


@app.route('/testdbms', methods=['GET'])
def test():
    """
     Test resource.

    :return:

     Example of use:
        curl -i -X GET localhost:8001/test
    """

    response = requests.get("http://%s/test" % modules.get_hostname(module='dbms'))
    return make_response(response.content, response.status_code)


@app.route('/test', methods=['GET'])
def test2():
    """
     Test resource.

    :return:

     Example of use:
        curl -i -X GET localhost:8001/test
    """
    return ('OK')

###############################################################
# Teaching DataBase micro Service (TDmS) Resources Connection #
###############################################################

@app.route('/entities/<string:kind>', methods=['POST'])
def post_entity(kind):
    """
    Data Base micro Service Resource connector, put all kind of entities in this mService.

    :param kind:
    :payload json:
    :return:

     Example of use:
      curl -i -H "Content-Type: application/json" -X POST -d '{ "data": {"name": "new name"} }' localhost:8001/entities/student
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
    More details in dbms.

    :param kind: Type of element to modify.
    :param entity_id: Id of entity to modify.
    :param payload:

        A json dict with any elements to change.

    :return: The element modified or error status code if any problem.

    Exampe of use:
     # curl -H "Content-Type: application/json" -X PUT -d '{ "name": "nameModified", "surname": "surnameModified"} ' localhost:8001/entities/teacher/1

    """

    response = requests.put(url='http://' + str(modules.get_hostname(module='dbms')) + '/entities/' + str(kind) + '/' + str(entity_id),
                            json=request.get_json())

    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route('/entities/<string:kind>/<int:entity_id>/<string:optional_nested_kind>/<int:onk_entity_id>', methods=['DELETE'])
@app.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id, optional_nested_kind = None, onk_entity_id = None):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    curl  -i -X  DELETE localhost:8002/entities/subject/1?action=dd
    """


    url = 'http://' + modules.get_hostname(module='dbms') + '/entities/' + str(kind) + '/' + str(entity_id)

    if optional_nested_kind is not None and onk_entity_id is not None:
        url += '/{}/{}'.format(optional_nested_kind, onk_entity_id)

    action = request.args.get('action', None)
    if action:
        url += '?action=' + action


    print url

    #return ping(url=url, method='DELETE')
    response = requests.delete(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>/<int:rk_entity_id>/<string:subrelated_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind, rk_entity_id=None, subrelated_kind=None):
    """

    :param kind:
    :param entity_id:
    :param related_kind:
    :return:

     Example of use:
       curl -i -X GET localhost:8001/entities/student/1/teacher
    """

    url = 'http://{}/entities/{}/{}/{}'.format(modules.get_hostname(module='dbms'),kind,entity_id, related_kind)

    if rk_entity_id and subrelated_kind:
        url += '/{}/{}'.format(rk_entity_id, subrelated_kind)

    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


##############################################################
# Students Control micro Service (SCmS) Resources Connection #
##############################################################

@app.route('/association', methods=['POST'])
def post_association():
    """
    curl -H "Content-Type: application/json" -X POST -d '{"name": "María"}' localhost:8003/association

    Post with example file:
    curl -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/ADB_example_1.json localhost:8001/association

    :return:

    """

    response = requests.post(url = 'http://{}/{}'.format(modules.get_hostname(module='scms'), 'association'),
                             json=request.get_json())
    response.headers['Access-Control-Allow-Origin'] = "*"
    return make_response(response.content, response.status_code)


@app.route('/association', methods=['GET'])
@app.route('/association/<int:entity_id>', methods=['GET'])
@app.route('/association/teacher/<int:teacher_id>', methods=['GET'])
def get_association(entity_id = None, teacher_id = None):

    url = 'http://{}/{}'.format(modules.get_hostname(module='scms'), 'association')

    if entity_id is not None:
        url += '/{}'.format(entity_id)

    if teacher_id is not None:
        url += '/teacher/{}'.format(teacher_id)

    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

################################
# Attendance Control Resources #
################################

@app.route('/ac', methods=['GET'])
@app.route('/ac/<int:ac_id>', methods=['GET'])
def get_ac(ac_id=None):
    """
    Get a list of acs or a specific ac from datastore.
    :param ac_id:
    :return:
    """

    url = 'http://{}/{}'.format(modules.get_hostname(module='scms'), 'ac')
    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route('/acbase/<int:association_id>', methods=['GET'])
def get_ac_base(association_id):
    """
    Get the Attendance Control Base to the association with id passed in url.
    :param association_id:
    :return:

    curl -i -X GET localhost:8003/acbase/<id>
    curl -i -X GET localhost:8003/acbase/5629499534213120
    """

    url = 'http://{}/{}/{}'.format(modules.get_hostname(module='scms'), 'acbase', association_id)
    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == '__main__':
    app.run(debug=True)
