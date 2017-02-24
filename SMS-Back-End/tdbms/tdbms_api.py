# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask import abort, make_response
from flask import request
import jsonpickle
import logging
from logging.handlers import RotatingFileHandler
from dbapi.entities_manager import EntitiesManager
from dbapi.GestorCredencialesSQL import GestorCredenciales

import datetime

import json
from termcolor import colored


app = Flask(__name__)


#file_handler = logging.FileHandler('app.log', 'rw')
#app.logger.addHandler(file_handler)
#app.logger.setLevel(logging.INFO)


# Activating verbose mode
v = 1

# Activating scms connection.
c = 0

microservice_name = '\n ## dbms Data Base mService ##'


class MyEncoder(json.JSONEncoder):
    """
    Class to provide a personal way to adapt specific objects to json
    when the default isn't enough for us.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            # We can select between two formats, is some places people prefer iso.
            #return obj.ctime()  # Example: Sun Oct 16 08:23:29 2016
            return obj.isoformat()  # Example: '2016-10-16T08:23:02

        return json.JSONEncoder.default(self, obj)


def process_response(response):
    """
    Function that process the response of entites manager
    to adjust to APIRest communications, reading the error
    messages and adjust this to the standard REST, and in
    case of error adding this in body of response becasue
    the user maybe want to be informed.

    :param response: a list with three params: status, data and log.
    :return:
    """

    print 'In process response'
    print response

    """
    Function to build a response with sense.
    :param self:
    :param response:
    :return:

    MySQL error standard codes that is processed.
        1452: Cannot add or update a child row: a foreign key constraint fails
        1054 unknown column, is when a value isn't a column in database
        1062: Duplicate entry
        1065: Query was empty
        1644: Some attribute fault.
        1146: Table x doesn't exist.
        1048: Column can't be null.
        -1:   When don't exists result, as a in a retrieved "related" data when there aren't related info.

    """

    if response['status'] == 1:
        # return json.dumps(response['data'], cls=MyEncoder)
        #app.logger.info('informing')
        # If there aren't data to return, it not needed json.dumps and use make_response.
        if response.get('data', None) == None:
            return ''
        elif len(response.get('data')) == 0:
            return ('', 204)
        else:
            return make_response(Response(json.dumps(response['data'], cls=MyEncoder), mimetype='application/json'))

    elif response['status'] == -1:
        # The element that it searched doesn't exists.
        abort(404)  # Is returned standard "Not found" error.

    elif response['status'] == 1054 or response['status'] == 1048:
        abort(400, response['log']) # Bad request

    elif response['status'] in [1452, 1146]:
        if response['log']:
            abort(404, response['log'])  # The same plus log.
        else:
            abort(404) # Not found

    elif response['status'] == 1062:

        # 409 Conflict because the item already exists in database and the user can't create another.
        # resource with the same values.
        abort(409, response['log'])

    elif response['status'] == 1644:
        if 'is required' in response['log']:
            abort(400, response['log']) # 400: Bad request.
        elif '404' in response['log']:
            abort(404) # 404 Not found
        else:
            abort(409, response['log']) # Conflict

    else:
        # Another problem that we don't have identified.
        abort(500)

#####################################################
#  Definition of Data Base micro Service REST API   #
#####################################################


@app.route('/test',methods=['GET'])
def test():
    """
    Test resource.

    Example of use:
        curl -i -X GET localhost:8002/test
    """
    return json.dumps({'dbms_api_test_status': 'ok'})


@app.route('/test_mysql',methods=['GET'])
def test_mysql():
    """
    Test resource.

    Example of use:
        curl -i -X GET localhost:8002/test
    """
    return json.dumps(EntitiesManager.test().get('data'))

#################################
#   Resources about entities    #
#################################


@app.route('/entities/<string:kind>', methods=['POST'])
def post_entity(kind):
    """
    INSERT a entity in the database, with a special input format:

    Input:

        Json payload:
        dict,  {}, with pairs: key (name of value in database), value (value to save in this key in database)


    Json return:

    Return:
        A json with the entire entity which is saved in database (with all extra control values) or error status code.

    Example of use:
        curl -H "Content-Type: application/json" -X POST -d '{"name": "María"}' localhost:8002/entities/student
        curl -H "Content-Type: application/json" -X POST -d '{"course": 1, "word": "B", "level": "ESO"}' localhost:8002/entities/class

    Example of return:
        {"createdBy": 1, "course": 5, "createdAt": "Thu Sep 22 16:09:36 2016", "word": "B", "level": "Primary", "classId": 19}

    If we want to use a file instead of:
        curl -H "Content-Type: application/json" -X POST -d @entityData.json localhost:8002/entidades

    Another example:
     curl -H "Content-Type: application/json" -X POST -d '{"associationId": 16, "studentId": 1}' localhost:8002/entities/enrollment
    {"createdBy": 1, "associationId": 16, "enrollmentId": 16, "createdAt": "2017-01-13T10:10:17", "studentId": 1}


    Use "| python -mjson.tool" after curl to see better the return to call on terminal.



    Special cases in entity CLASS:





    """

    received_json = request.get_json()

    print colored('mSDBapi.postEntity', 'green')
    print colored(received_json, 'green')

    if received_json is None:
        abort(400)  # Bad request.

    else:
        for key, value in received_json.iteritems():
            if type(value) is not int and type(value) is not list: # Because we accept a list of associationIds in enrollment resource.
                received_json[key] = value.encode('utf-8')

    # When are really saved data in database


    # Special multiple enrollment checking:
    if 'associationsIds' in received_json:
        return process_response(EntitiesManager.multiple_enrollment(kind, received_json))
    else:
        return process_response(EntitiesManager.post(kind, received_json))


@app.route('/entities/<string:kind>', methods=['GET']) #Si pedimos todas las entidades de un tipo
@app.route('/entities/<string:kind>/<int:entity_id>', methods=['GET']) #Si pedimos una entidad concreta de un tipo
def get_entities(kind, entity_id=None):
    """
    Retrieve info about entities, a list of all of them with all info or specific params or all data from one.

    Example of use:
    Mode 1: all
    curl  -i -X GET localhost:8002/entities/student  -> All items of student list with all data
    Mode 2: all with params:
    curl  -i -X GET localhost:8002/entities/student?params=name, surname  -> Only params sent from all students
    Mode 3: only one
    curl  -i -X GET  localhost:8002/entities/student/1  -> All data from student with id = 1
    """
    return process_response(EntitiesManager.get(kind, entity_id, request.args.get('params', None)))


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['PUT'])
def put_entities(kind, entity_id):
    """
    UPDATE an entity in the data base of microService.

    curl -H "Content-Type: application/json" -X PUT -d '{ "name": "NombreModificado" }' localhost:8002/entities/teacher/1



    When we put a item on tdbms there are a metadata params that are saved too, in all cases in the inserction it are:
    itemId, createdAt and createdBy.

    We pass data into a dict

    """

    raw_data = request.get_json()

    print colored('dbms.apigms_api.update_entities', 'green')
    print colored(request.headers, 'green')

    app.logger.info('hi')

    print colored(raw_data, 'red')

    if raw_data is None:
        abort(400) # Bad request.
    else:
        for key, value in raw_data.iteritems():
            if type(value) is not int:
                raw_data[key] = value.encode('utf-8')

    return process_response(EntitiesManager.update(kind, entity_id, raw_data))


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
@app.route('/entities/<string:kind>/<int:entity_id>/<string:optional_nested_kind>/<int:onk_entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id, optional_nested_kind = None, onk_entity_id = None):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    curl  -i -X  DELETE localhost:8002/entities/subject/1?action=dd
    """

    # When we want delete a student from a all class in which is enrollment or in all subjects.
    if kind in ['class', 'subject'] and optional_nested_kind is not None and onk_entity_id is not None:
        response = EntitiesManager.nested_delete(kind, entity_id, optional_nested_kind, onk_entity_id)
    else:
        response = EntitiesManager.delete(kind, entity_id, request.args.get('action', None))

    if response.get('log',None) and 'not found element to del' in response.get('log', None):
        abort(404)
    else:
        return process_response(response)


@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>/<int:rk_entity_id>/<string:subrelated_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind, rk_entity_id=None, subrelated_kind=None):

    """
    curl -i -X GET localhost:8002/entities/student/1/teacher

    Mode 2: all with params:
    curl  -i -X GET localhost:8002/entities/class/2/student?params=name, surname  -> Only params sent from all students

    curl -X GET localhost:8002/entities/teacher/4/imparts | python -mjson.tool

    """
    print locals()

    #from time import sleep
    #sleep(4)
    return process_response(EntitiesManager.get_related(kind=kind,
                                                        entity_id=entity_id,
                                                        related_kind=related_kind,
                                                        rk_entity_id=rk_entity_id,
                                                        subrelated_kind=subrelated_kind,
                                                        params=request.args.get('params', None)))




@app.route('/entities/<string:kind>/<int:entity_id>/report', methods=['GET'])
def get_report(kind, entity_id):
    """
    curl -i -X GET localhost:8002/entities/class/1/report
    """
    return process_response(EntitiesManager.get_report(kind, entity_id))

if __name__ == '__main__':
    handler = RotatingFileHandler('dbms_api_log.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)

