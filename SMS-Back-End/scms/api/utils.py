
from flask import abort, make_response, Response
import datetime
import json


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