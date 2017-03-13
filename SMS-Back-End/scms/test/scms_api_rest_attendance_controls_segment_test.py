"""
##########################################################
### SCmS attendance controls api segment test suite    ###
##########################################################
"""
import requests
import json
from time import sleep

url_base = 'http://localhost:8003/ac'


class TestClass(object):

    def test_empty_ac_items_in_data_store(self):
        result = requests.get(url_base)
        assert result.status_code == 204

        # Item doesn't exist.
        result = requests.get(url_base+'/2239')
        assert result.status_code == 404

    def test_post_and_delete(self):

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

    def test_update(self):

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
