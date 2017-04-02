from google.appengine.api import modules
import requests
from flask import make_response, request
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()


class CRUD(object):
    """
    Important:
    The mainly goal of this class is unify the way to call all services form this. So, if in the future
    the way have any changes it will be for all connectors, simplify the maintenance.
    """

    @classmethod
    def get(cls, service, resource, id=None, args=None):
        """
        Do a GET request over a micro service in the backend using the params given.

        :param service: The name of the service (used for google services auto discovering).
        :param resource: The url segment of the service.
        :param id: The id of the request item.
        :param args: Args to put in the url (?paramA=<>&...)
        :return: Exactly the same response of the service.
        """

        url = 'http://{}/{}'.format(modules.get_hostname(module=service), resource)

        if id:
            url += '/{}'.format(id)

        if args:
            url += '?'
            for arg in args:
                url += '{}={}&'.format(arg, args.get(arg))
            url = url[:-1]

        response = requests.get(url, timeout=10)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return make_response(response.content, response.status_code)

    @classmethod
    def post(cls, service, resource, json):
        """
        Do a POST request over a micro service in the backend using the params given.

        :param service: The name of the service (used for google services auto discovering).
        :param resource: The url segment of the service.
        :param json: The payload where are the data to put in a dict format.
        :return: Exactly the same response of the service.
        """

        response = requests.post(url='http://{}/{}'.format(modules.get_hostname(module=service), resource), json=json)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return make_response(response.content, response.status_code)

    @classmethod
    def put(cls, service, resource, id, json):
        """
        Do a PUT request over a micro service in the backend using the params given.

        :param service: The name of the service (used for google services auto discovering).
        :param resource: The url segment of the service.
        :param id: The id of the request item. **CAN BE NONE TO SINGLETON RESOURCES**
        :param json: The payload where are the data to put in a dict format.
        :return: Exactly the same response of the service.
        """

        # For singleton resources.
        url = 'http://{}/{}'.format(modules.get_hostname(module=service), resource)

        if id:
            url += '/{}'.format(id)

        response = requests.put(url=url, json=json)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return make_response(response.content, response.status_code)

    @classmethod
    def delete(cls, service, resource, id):
        """
        Do a DELETE request over a micro service in the backend using the params given.

        :param service: The name of the service (used for google services auto discovering).
        :param resource: The url segment of the service.
        :param id: The id of the request item.
        :return: Exactly the same response of the service.
        """

        response = requests.delete('http://{}/{}/{}'.format(modules.get_hostname(module=service), resource, id))
        response.headers['Access-Control-Allow-Origin'] = "*"
        return  make_response(response.content, response.status_code)
