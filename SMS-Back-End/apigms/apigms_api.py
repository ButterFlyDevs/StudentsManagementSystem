# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, Response, make_response
import json
from google.appengine.api import modules
import urllib2
from termcolor import colored

app = Flask(__name__)

# Activating verbose mode
v = 1

microservice_name = '\n ## dbms Data Base mService ##'

module = modules.get_current_module_name()
instance = modules.get_current_instance_id()

# Test method.
@app.route('/test',methods=['GET'])
def test():
    """
    Test resource.

    Example of use:
    curl -i -X GET localhost:8002/test
    """

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'test'
    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

    return response


@app.route('/entities/<string:kind>', methods=['POST'])
def put_entity(kind):

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'entities/' + str(kind)

    req = urllib2.Request(url, request.get_data(), {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

    return response


@app.route('/entities/<string:kind>', methods=['GET'])
@app.route('/entities/<string:kind>/<int:entity_id>', methods=['GET'])
def get_entities(kind, entity_id=None):
    # curl -i -X GET localhost:8080/entities/teacher

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'entities/' + str(kind)

    if entity_id is not None:
        url += '/' + str(entity_id)

    print url

    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    response = f.read()

    print type(response)
    response = json.dumps(response)
    print type(response)

    f.close()

    """
    res = Response(json.dumps(response), mimetype='application/json')

    rews = make_response(res)

    rews.headers['Access-Control-Allow-Origin'] = "*"
    """

    return response

    #return Response(json.dumps(list), mimetype='application/json')
    #return  jsonify(r)
    #return response


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['PUT'])
def update_entities(kind, entity_id):
    # curl -H "Content-Type: application/json" -X PUT -d '{ "data": {"name": "NombreModificado"} }' localhost:8001/entities/teacher/1

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'entities/' + str(kind) + '/' + str(entity_id)

    print url

    req = urllib2.Request(url, request.get_data(), {'Content-Type': 'application/json'})
    req.get_method = lambda: "PUT"
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

    return response


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    """

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'entities/' + str(kind) + '/' + str(entity_id)

    req = urllib2.Request(url)
    req.get_method = lambda: "DELETE"
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

    return response


@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind):
#    """
#    curl -i -X GET localhost:8001/entities/student/1/teacher
#    ""

    url = "http://%s/" % modules.get_hostname(module='dbms')
    url += 'entities/' + str(kind) + '/' + str(entity_id) + '/' + str(related_kind)

    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

    return response


if __name__ == '__main__':
    app.run(debug=True)


