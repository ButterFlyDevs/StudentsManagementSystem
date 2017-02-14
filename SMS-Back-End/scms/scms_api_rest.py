# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask import abort, make_response
from flask import request
import logging
from logging.handlers import RotatingFileHandler

import datetime

import json
from termcolor import colored

from scm.scm import Association_Manager
from scm.scm import Attendance_Controls_Manager as ACM
from das.das import *


app = Flask(__name__)

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

# Activating verbose mode
v = 1


microservice_name = '\n ## scms Students Control micro Service ##'


def process_response(response):
    """
    Process the response of Association_Manager to adapt to a api rest response, with
    HTTP status code instead of library status code.
    :param response:
    :return:
    """


    if response.get('status', None) == 1: # 200: OK STATUS.

        if response.get('data', None) is not None:
            if len(response.get('data')) == 0:
                return ('', 204)
            else:
                return make_response(Response(json.dumps(response['data'],  cls=MyEncoder), mimetype='application/json'))
        else:
            return ''

    elif response.get('log', None) is not None:
        abort(400, response['log'])  # 400: Bad request.

    elif response.get('status', None) == -1:
        # The element that it searched doesn't exists.
        abort(404)  # Is returned standard "Not found" error.



#####################################################
#  Definition of Data Base micro Service REST API   #
#####################################################

@app.route('/test',methods=['GET'])
def test():
    """
    Test resource.

    Example of use:
        curl -i -X GET localhost:8003/test
    """
    return json.dumps({'scms_api_rest_test_status': 'ok'})

#########################
# Association Resources #
#########################


@app.route('/association', methods=['POST'])
def post_association():
    """
    curl -H "Content-Type: application/json" -X POST -d '{"name": "María"}' localhost:8003/association

    Post with example file:
    curl -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/ADB_example_1.json localhost:8003/association

    :return:
    """

    # return Association_Manager.post2(request.get_json())
    return process_response(Association_Manager.post(request.get_json()))


@app.route('/association', methods=['GET'])
@app.route('/association/<int:entity_id>', methods=['GET'])
@app.route('/association/teacher/<int:teacher_id>', methods=['GET'])
def get_association(entity_id = None, teacher_id = None):
    """
    curl -i -X GET localhost:8003/association

    curl -i -X GET localhost:8003/association/teacher/1

    curl -X GET localhost:8003/association | python -mjson.tool

    :return:
    """

    return process_response(Association_Manager.get(entity_id, teacher_id))


@app.route('/association/<int:entity_id>', methods=['DELETE'])
def delete_association(entity_id):
    """
    Do a logic deletion of an association in the database of microservice.
    :param entity_id: association identification
    :return: A 200 OK Status Code or 404 Not Found if the item doesn't exists.

    Example of use:
        curl  -i -X  DELETE localhost:8003/association/<associationId>
        like: .../association/5629499534213120

    """

    return process_response(Association_Manager.delete(entity_id))


@app.route('/association/<int:entity_id>', methods=['PUT'])
def put_association(entity_id):
    """
    curl -H "Content-Type: application/json" -X PUT -d @test/ADB_example_2.json localhost:8003/association/5629499534213120
    :param entity_id:
    :return:
    """

    return process_response(Association_Manager.put(entity_id, request.get_json()))

################################
# Attendance Control Resources #
################################


@app.route('/ac', methods=['GET'])
@app.route('/ac/<int:ac_id>', methods=['GET'])
def get_ac(ac_id=None):
    """
    > curl -i -X GET localhost:8003/ac

    Get a list of acs or a specific ac from datastore.
    :param ac_id:
    :return:
    """
    return process_response(ACM.get_ac(ac_id))


@app.route('/acbase/<int:association_id>', methods=['GET'])
def get_ac_base(association_id):
    """
    Get the Attendance Control Base to the association with id passed in url.
    :param association_id:
    :return:

    curl -i -X GET localhost:8003/acbase/<id>
    curl -i -X GET localhost:8003/acbase/5629499534213120
    """

    return process_response(ACM.get_ac_base(association_id))


@app.route('/ac', methods=['POST'])
def post_ac():
    """
    curl -H "Content-Type: application/json" -X POST -d '...' localhost:8003/association

    Post with example file:
    curl -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/AC_example_1.json localhost:8003/ac

    :return:
    """

    # return Association_Manager.post2(request.get_json())
    return process_response(ACM.post_ac(request.get_json()))



##################################
# Data Analysis System Resources #
##################################


@app.route('/das/attendances/general', methods=['GET'])
def get_attendances_general():
    """
    curl -i -X GET localhost:8003/das/attendances/general

    :return:
    """
    return process_response(get_general_attendance_report())

if __name__ == '__main__':
    app.run(debug=True)

