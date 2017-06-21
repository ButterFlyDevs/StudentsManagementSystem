###############################################################
# Teaching DataBase micro Service (TDmS) Resources Connection #
###############################################################


from flask import Blueprint
from termcolor import colored
from google.appengine.api import modules
import requests
from flask import make_response, request
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

tdbms_segment_api = Blueprint('tdbms_segment_api', __name__)

microservice_name = '\n ## tdbms Data Base mService ##'

@tdbms_segment_api.route('/testdbms', methods=['GET'])
def test():
    """
     Test resource.

    :return:

     Example of use:
        curl -i -X GET localhost:8001/test
    """

    response = requests.get("http://%s/test" % modules.get_hostname(module='tdbms'))
    return make_response(response.content, response.status_code)

@tdbms_segment_api.route('/entities/<string:kind>', methods=['POST'])
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
    response = requests.post(url='http://' + str(modules.get_hostname(module='tdbms')) + '/entities/' + str(kind),
                             json=request.get_json())
    response.headers['Access-Control-Allow-Origin'] = "*"
    return make_response(response.content, response.status_code)


@tdbms_segment_api.route('/entities/<string:kind>', methods=['GET'])
@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>', methods=['GET'])
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


    url = 'http://' + str(modules.get_hostname(module='tdbms')) + '/' + 'entities/' + str(kind)
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


@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>', methods=['PUT'])
def update_entities(kind, entity_id):

    """
    Data Base micro Service Resource connector, to update all kind of entities in this mService.
    More details in tdbms.

    :param kind: Type of element to modify.
    :param entity_id: Id of entity to modify.
    :param payload:

        A json dict with any elements to change.

    :return: The element modified or error status code if any problem.

    Exampe of use:
     # curl -H "Content-Type: application/json" -X PUT -d '{ "name": "nameModified", "surname": "surnameModified"} ' localhost:8001/entities/teacher/1

    """

    response = requests.put(url='http://' + str(modules.get_hostname(module='tdbms')) + '/entities/' + str(kind) + '/' + str(entity_id),
                            json=request.get_json())

    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>/<string:optional_nested_kind>/<int:onk_entity_id>', methods=['DELETE'])
@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id, optional_nested_kind = None, onk_entity_id = None):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    curl  -i -X  DELETE localhost:8002/entities/subject/1?action=dd
    """


    url = 'http://' + modules.get_hostname(module='tdbms') + '/entities/' + str(kind) + '/' + str(entity_id)

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


@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
@tdbms_segment_api.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>/<int:rk_entity_id>/<string:subrelated_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind, rk_entity_id=None, subrelated_kind=None):
    """

    :param kind:
    :param entity_id:
    :param related_kind:
    :return:

     Example of use:
       curl -i -X GET localhost:8001/entities/student/1/teacher
    """

    url = 'http://{}/entities/{}/{}/{}'.format(modules.get_hostname(module='tdbms'),kind,entity_id, related_kind)

    if rk_entity_id and subrelated_kind:
        url += '/{}/{}'.format(rk_entity_id, subrelated_kind)

    response = requests.get(url)
    response = make_response(response.content, response.status_code)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
