################################
# Attendance Control Resources #
################################

from flask import Blueprint
from termcolor import colored
from google.appengine.api import modules
import requests
from flask import make_response, request
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()


import sys
sys.path.insert(0, 'api')

from services import CRUD

attendance_controls_api = Blueprint('attendance_controls_api', __name__)


@attendance_controls_api.route('/ac', methods=['GET'])
@attendance_controls_api.route('/ac/<int:ac_id>', methods=['GET'])
def get_ac(ac_id=None):
    """
    It call to SCmS to get a minimal content list of all items of this kind or all info about specific one.

    :param ac_id: id of the item or None if the request is about all.
    :return: A dict with info about one or a list with dicts inside with info for each one.
    """
    return CRUD.get(service='scms', resource='ac', id=ac_id)


@attendance_controls_api.route('/ac/base/<int:ac_id>', methods=['GET'])
def get_ac_base(ac_id):
    """
    It call to SCmS to request a item (base type).

    :param ac_id: The id of the item in the service.
    :return: A dict with data.
    """
    return CRUD.get(service='scms', resource='ac/base', id=ac_id)


@attendance_controls_api.route('/ac', methods=['POST'])
def post_ac():
    """
    It call to SCmS to post a item of this kind.

    :return: Dict with id saved {'acId': <int>} in the body and specific HTTP status code in the header.
    """
    return CRUD.post(service='scms', resource='ac', json=request.get_json())


@attendance_controls_api.route('/ac/<int:ac_id>', methods=['PUT'])
def update_ac(ac_id):
    """
    It call to SCmS to update a item ot this kind.

    :param ac_id: id of item to update.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.put(service='scms', resource='ac', id=ac_id, json=request.get_json())


@attendance_controls_api.route('/ac/<int:ac_id>', methods=['DELETE'])
def delete_ac(ac_id):
    """
    It call to SCmS to do a logic deletion of this kind of item in their data store.

    :param ac_id: ac id in data store.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.delete(service='scms', resource='ac', id=ac_id)