########################
# SCMS Marks Resources #
########################


from flask import Blueprint, request
from termcolor import colored
from google.appengine.api import modules
import requests
from flask import make_response, request
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

marks_api = Blueprint('marks_api', __name__)

import sys
sys.path.insert(0, 'api')

from services import CRUD


@marks_api.route('/mark', methods=['GET'])
@marks_api.route('/mark/<int:mark_id>', methods=['GET'])
def get_mark(mark_id=None):
    """
    It call to SCmS to get a minimal content list of all items of this kind or all info about specific one.

    Also in this case is possible get the item using enrollmentId as param in /mark url (/mark?enrollmentId=<int>).

    :param ac_id: id of the item or None if the request is about all.
    :return: A dict with info about one or a list with dicts inside with info for each one.
    """
    return CRUD.get(service='scms', resource='mark', id=mark_id, args=request.args)


@marks_api.route('/mark', methods=['POST'])
def post_mark():
    """
    It call to SCmS to post a item of this kind.

    :return: Dict with id saved {'markId': <int>} in the body and specific HTTP status code in the header.
    """
    return CRUD.post(service='scms', resource='mark', json=request.get_json())


@marks_api.route('/mark/<int:mark_id>', methods=['PUT'])
def update_mark(mark_id):
    """
    It call to SCmS to update a item ot this kind.

    :param mark_id: id of item to update.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.put(service='scms', resource='mark', id=mark_id, json=request.get_json())


@marks_api.route('/mark/<int:mark_id>', methods=['DELETE'])
def delete_mark(mark_id):
    """
    It call to SCmS to do a logic deletion of this kind of item in their data store.

    :param mark_id: mark id in data store.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.delete(service='scms', resource='mark', id=mark_id)