"""
##########################################################
###         SCmS marks api segment TEST SUITE          ###
##########################################################
"""
import requests
from time import sleep
import json

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

    @classmethod
    def check_mark_with_original(cls, mark, mark2):

        # In the get a Mark returned must have all values from original mark plus
        # the metadata 'createdBy', 'createdAt' and 'markId'
        assert mark.get('createdBy', None)
        assert mark.get('createdAt', None)
        assert mark.get('markId', None)

        # And the rest of values of the mark saved:
        for k, v in mark2.items():
            assert mark[k] == v

    def test_empty_mark_items_in_data_store(self, port):

        url = 'http://localhost:{}/mark'.format(port)

        result = requests.get(url)
        assert result.status_code == 204

        # Item doesn't exist.
        result = requests.get(url+'/2239')
        assert result.status_code == 404

        # Item searched with enrollmentId doesn't exists.
        result = requests.get(url + '?enrollmentId=423')
        assert result.status_code == 404

    def test_post_and_delete(self, port):

        url = 'http://localhost:{}/mark'.format(port)

        # Open JSON from file
        with open('test/mark_example_1.json') as data_file:
            data = json.load(data_file)
        response = requests.post(url=url, json=data)
        assert response.status_code == 200

        # Because the Asynchronously of the server.
        sleep(0.5)  # Time in seconds.

        result = requests.get(url)
        assert result.status_code == 200
        assert len(result.json()) == 1

        # Item searched with enrollmentId exists.
        result = requests.get(url='{}{}{}'.format(url,'?enrollmentId=',data['enrollment']['enrollmentId']))
        assert result.status_code == 200

        response = requests.delete(url='{}/{}'.format(url, response.json()['markId']))
        assert response.status_code == 200

        sleep(0.5)

        result = requests.get(url)
        assert result.status_code == 204

    def test_update(self, port):

        url = 'http://localhost:{}/mark'.format(port)

        with open('test/mark_example_1.json') as data_file:
            data = json.load(data_file)
        response = requests.post(url=url, json=data)
        assert response.status_code == 200
        ac_id = response.json()['markId']

        sleep(0.5)
        # A part of data is modified.
        data['marks']['preFirstEv'] = 7.6

        response = requests.put(url='{}/{}'.format(url,ac_id), json=data)
        assert response.status_code == 200

        sleep(0.5)

        # Check the update
        response = requests.get(url='{}/{}'.format(url, ac_id))
        assert response.status_code == 200
        ac = response.json()
        assert data['marks']['preFirstEv'] == 7.6

        response = requests.delete(url='{}/{}'.format(url, ac_id))
        assert response.status_code == 200

        sleep(0.5)
