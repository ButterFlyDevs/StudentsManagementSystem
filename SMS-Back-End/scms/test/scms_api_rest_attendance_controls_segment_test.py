"""
##########################################################
### SCmS attendance controls api segment test suite    ###
##########################################################
"""
import requests
import json
from time import sleep


def pytest_generate_tests(metafunc):
    """
    Config function to make the test to several scenarios.
    """
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

scenario1 = ('calling mService directly', {'port': '8003'})
scenario2 = ('calling mService through APIG', {'port': '8001'})


class TestClass(object):

    scenarios = [scenario1, scenario2]

    def test_empty_ac_items_in_data_store(self, port):

        url_base = 'http://localhost:{}/ac'.format(port)

        result = requests.get(url_base)
        assert result.status_code == 204

        # Item doesn't exist.
        result = requests.get(url_base+'/2239')
        assert result.status_code == 404

    def test_post_and_delete(self, port):

        url_base = 'http://localhost:{}/ac'.format(port)

        # Open JSON from file
        with open('test/AC_example_1.json') as data_file:
            data = json.load(data_file)
        response = requests.post(url=url_base, json=data)
        assert response.status_code == 200

        # Because the Asynchrony of the server.
        sleep(0.5)  # Time in seconds.

        result = requests.get(url_base)
        assert result.status_code == 200
        assert len(result.json()) == 1

        response = requests.delete(url='{}/{}'.format(url_base, response.json()['acId']))
        assert response.status_code == 200

        sleep(0.5)

        result = requests.get(url_base)
        assert result.status_code == 204

    def test_update(self, port):

        url_base = 'http://localhost:{}/ac'.format(port)

        with open('test/AC_example_1.json') as data_file:
            data = json.load(data_file)
        response = requests.post(url=url_base, json=data)
        assert response.status_code == 200
        ac_id = response.json()['acId']

        sleep(0.5)
        # A part of data is modified.
        data['students'][0]['control']['delay'] = 15

        response = requests.put(url='{}/{}'.format(url_base,ac_id), json=data)
        assert response.status_code == 200

        sleep(0.5)

        # Check the update
        response = requests.get(url='{}/{}'.format(url_base, ac_id))
        assert response.status_code == 200
        ac = response.json()
        assert ac['students'][0]['control']['delay'] == 15

        response = requests.delete(url='{}/{}'.format(url_base, ac_id))
        assert response.status_code == 200

        sleep(0.5)
