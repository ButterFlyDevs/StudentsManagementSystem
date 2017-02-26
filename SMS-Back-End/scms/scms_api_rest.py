# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask import abort, make_response
from flask import request
import logging
from logging.handlers import RotatingFileHandler

import datetime

import json
from termcolor import colored

from scm.scm import AssociationManager
from scm.scm import AttendanceControlsManager as ACM
from scm.scm import MarksManager
from scm.scm import DisciplinaryNotesManager
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
    Process the response of AssociationManager to adapt to a api rest response, with
    HTTP status code instead of library status code.
    :param response:
    :return:
    """

    if response.get('status', None) == 400:
        if response.get('log', None):
            abort(400, response['log'])

    elif response.get('status', None) == 404:
        if response.get('log', None):
            abort(404, response['log'])
        else:
            abort(404)

    elif response.get('status', None) == 500:
        if response.get('log', None):
            abort(500, response['log'])

    elif response.get('status', None) == 204:
        if not response.get('log', None):
            return '', 204

    elif response.get('status', None) == 200:

        # Return 200 with content in boy with json format encoder.
        if response.get('data', None):
            return make_response(Response(json.dumps(response['data'], cls=MyEncoder), mimetype='application/json'))

        # Return 200 Ok Status Code without body.
        else:
            return '', 200

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

# TODO: Cambiar el nombre al adb para que no entre en conflicto con las association del tdbms
@app.route('/association/schema', methods=['GET'])
def get_association_datastore_schema():
    return process_response(AssociationManager.get_association_schema())

@app.route('/association', methods=['POST'])
def post_association():
    """
    curl -H "Content-Type: application/json" -X POST -d '{"name": "María"}' localhost:8003/association

    Post with example file:
    curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/ADB_example_1.json localhost:8003/association

    :return:
    """

    # return AssociationManager.post2(request.get_json())
    return process_response(AssociationManager.post(request.get_json()))


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

    return process_response(AssociationManager.get(entity_id, teacher_id))


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

    return process_response(AssociationManager.delete(entity_id))


@app.route('/association/<int:entity_id>', methods=['PUT'])
def put_association(entity_id):
    """
    curl -H "Content-Type: application/json" -X PUT -d @test/ADB_example_2.json localhost:8003/association/5629499534213120
    :param entity_id:
    :return:
    """

    return process_response(AssociationManager.put(entity_id, request.get_json()))

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


@app.route('/ac/base/<int:association_id>', methods=['GET'])
def get_ac_base(association_id):
    """
    Get the Attendance Control Base to the association with id passed in url.
    :param association_id: id of the association saved in TDBmS.
    :return:

    curl -i -X GET localhost:8003/ac/base/<id>
    curl -i -X GET localhost:8003/ac/base/5629499534213120
    """

    return process_response(ACM.get_ac_base(association_id))


@app.route('/ac', methods=['POST'])
def post_ac():
    """
    curl -H "Content-Type: application/json" -X POST -d '...' localhost:8003/association

    Post with example file:
    curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/AC_example_1.json localhost:8003/ac

    :return:
    """

    # return AssociationManager.post2(request.get_json())
    return process_response(ACM.post_ac(request.get_json()))


##################################
# Data Analysis System Resources #
##################################

"""
@app.route('/das/attendances/general', methods=['GET'])
def get_attendances_general():

    curl -i -X GET localhost:8003/das/attendances/general

    :return:

    return process_response(get_general_attendance_report())
"""

################################
#      Marks Resources         #
################################


@app.route('/mark', methods=['POST'])
def post_mark():
    """
    Save a mark in the database.

    Post with example file:
    curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/mark_example_1.json localhost:8003/mark

    :return: Return HTTP status code and the mark as is saved in the data store.
    """
    return process_response(MarksManager.post(request.get_json()))


@app.route('/mark', methods=['GET'])
@app.route('/mark/<int:mark_id>', methods=['GET'])
def get_mark(mark_id=None):
    """
    Example of use:

        curl -i -X GET localhost:8003/mark

    Get a list of marks or a specific mark from data store.
    :param mark_id:
    :return:
    """
    return process_response(MarksManager.get(mark_id))


@app.route('/mark/<int:mark_id>', methods=['DELETE'])
def delete_mark(mark_id):
    """
    Do a logic deletion of a mark in the data store.
    :param mark_id: mark id in data store
    :return: A 200 OK Status Code or 404 Not Found if the item doesn't exists.

    Example of use:
        curl  -i -X  DELETE localhost:8003/mark/<markId>
        curl  -i -X  DELETE localhost:8003/mark/5629499534213120

    """
    return process_response(MarksManager.delete(mark_id))


####################################
#   Disciplinary Notes Resources   #
####################################


@app.route('/disciplinarynote', methods=['POST'])
def post_disciplinary_note():
    """
    Save a Disciplinary Note in the database.

    Post with example file:
    curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/disciplinary_note_example_1.json localhost:8003/disciplinarynote

    :return: Return HTTP status code and the mark as is saved in the data store.
    """
    return process_response(DisciplinaryNotesManager.post(request.get_json()))


@app.route('/disciplinarynote', methods=['GET'])
@app.route('/disciplinarynote/<int:disciplinary_note_id>', methods=['GET'])
def get_disciplinary_note(disciplinary_note_id=None):
    """
    Example of use:

        curl -i -X GET localhost:8003/disciplinarynote

    Get a list of disciplinary_notes or a specific disciplinary note from data store.
    :param disciplinary_note_id:
    :return:
    """
    return process_response(DisciplinaryNotesManager.get(disciplinary_note_id))


@app.route('/disciplinarynote/<int:disciplinary_note_id>', methods=['DELETE'])
def delete_disciplinary_note(disciplinary_note_id):
    """
    Do a logic deletion of a disciplinary note in the data store.
    :param disciplinary_note_id: disciplinary note id in data store
    :return: A 200 OK Status Code or 404 Not Found if the item doesn't exists.

    Example of use:
        curl  -i -X  DELETE localhost:8003/disciplinarynote/<disciplinary_note_Id>
        curl  -i -X  DELETE localhost:8003/disciplinarynote/5629499534213120

    """
    return process_response(DisciplinaryNotesManager.delete(disciplinary_note_id))

if __name__ == '__main__':
    app.run(debug=True)

