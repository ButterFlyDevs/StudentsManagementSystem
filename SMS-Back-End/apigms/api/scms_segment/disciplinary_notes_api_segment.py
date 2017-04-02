################################
# Disciplinary Notes Resources #
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

disciplinary_notes_api = Blueprint('disciplinary_notes_api', __name__)


@disciplinary_notes_api.route('/disciplinarynote/schema', methods=['GET', 'PUT'])
def CRU_disciplinary_note_schema():
    """
    It call to SCmS to get a schema with options to ve showed in UI form to do a disciplinary note.
    :return: A dict
    """
    if request.method == 'GET':
        return CRUD.get(service='scms', resource='disciplinarynote/schema')

    if request.method == 'PUT':
        return CRUD.put(service='scms', resource='disciplinarynote/schema', id=None, json=request.get_json())


@disciplinary_notes_api.route('/disciplinarynote', methods=['GET'])
@disciplinary_notes_api.route('/disciplinarynote/<int:dn_id>', methods=['GET'])
def get_disciplinary_note(dn_id=None):
    """
    It call to SCmS to get a minimal content list of all items of this kind or all info about specific one.

    :param ac_id: id of the item or None if the request is about all.
    :return: A dict with info about one or a list with dicts inside with info for each one.
    """
    return CRUD.get(service='scms', resource='disciplinarynote', id=dn_id)


@disciplinary_notes_api.route('/disciplinarynote', methods=['POST'])
def post_disciplinary_note():
    """
    It call to SCmS to post a item of this kind.

    :return: Dict with id saved {'dnId': <int>} in the body and specific HTTP status code in the header.
    """
    return CRUD.post(service='scms', resource='disciplinarynote', json=request.get_json())


@disciplinary_notes_api.route('/disciplinarynote/<int:dn_id>', methods=['PUT'])
def update_disciplinary_note(dn_id):
    """
    It call to SCmS to update a item ot this kind.

    :param dn_id: id of item to update.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.put(service='scms', resource='disciplinarynote', id=dn_id, json=request.get_json())


@disciplinary_notes_api.route('/disciplinarynote/<int:dn_id>', methods=['DELETE'])
def delete_disciplinary_note(dn_id):
    """
    It call to SCmS to do a logic deletion of this kind of item in their data store.

    :param dn_id: dn id in data store.
    :return: Nothing in the body. Specific HTTP status code in the header.
    """
    return CRUD.delete(service='scms', resource='disciplinarynote', id=dn_id)
