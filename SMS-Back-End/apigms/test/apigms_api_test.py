# -*- coding: utf-8 -*-
import requests
import os
from termcolor import colored
import datetime

"""
### Testing using pytests library. ###

Use: pytest or py.test in the same folder
Use:  fab run_apigms_api_tes in main proyect folder

To show details:  py.test --cov-report html --cov . --verbose

# How check code quality: pylint dbms_api.py
"""

urlBase = 'http://localhost:8001'


class TestClass:

    def setup(self):

        print '\nReset Database'

        dir = os.getcwd().split('/')[-1]

        sentence = 'mysql -u root -p\'root\' <'
        if dir == 'pytest':
            sentence += ' ../../../dbms/dbapi/DBCreator.sql'
        elif dir == 'StudentsManagementSystem':
            sentence += ' SMS-Back-End/dbms/dbapi/DBCreator.sql'

        os.system(sentence)

    def test_dbms_api_test(self):
        """
        Run the most simple test.
        pytest -s dbms_api_test.py::TestClass::test_dbms_api_test
        """
        url = urlBase+'/test'
        assert requests.get(url).json().get('dbms_api_test_status', None) == 'ok'

    def test_get_entities(self):
        url = urlBase + '/entities'

        # We define a block with entity tests:

        # Insert n students
        n = 10
        for a in range(0, n):
            response = requests.post(url + '/student', json={'data': {'name': 'student' + unicode(a)}})
            assert response.status_code == 200

        # Checking all features about get methods.

        # Check if all students have been inserted
        response = requests.get(url + '/student')

        # And the response have all data that it expected
        response_data = response.json()
        assert n == len(response_data)
        for item in response_data:
            assert item.get('createdBy', None) != None
            assert item.get('name', None) != None
            assert item.get('createdAt', None) != None
            assert item.get('studentId', None) != None

        # When we call to specific item:
        response = requests.get(url + '/student' + '/3')
        response_data = response.json()
        assert response_data.get('createdBy', None) != None
        assert response_data.get('name', None) != None
        assert response_data.get('studentId', None) != None
        assert response_data.get('createdAt', None) != None


    def test_post_entities(self):
        url = urlBase + '/entities'

        # We define a block with entity tests:
        tests = [
            {'kind': 'student',
             'data': {'name': u'súperNombre'}
             },
            {'kind': 'student',
             'data': {'name': u'Juan'}
             },
            {'kind': 'teacher',
             'data': {'name': u'súperNombre'}
             },
            {'kind': 'subject',
             'data': {'name': u'Francés'}
             },
            {'kind': 'class',
             'data': {'course': 1, 'word': u'B', 'level': u'ESO'}
             }
        ]

        date_time_now = datetime.datetime.now()

        for item in tests:

            response = requests.post(url + '/' + item['kind'], json={'data': item['data']})

            if response.json():
                json_response = response.json()

            # Particular attributes. Check if the retrieve data is exactly to sent data.
            for key, value in item['data'].iteritems():
                assert json_response.get(key) == value  # entity.get(key) is unicode but value is string.

            # Control attributes.
            # Transform the ctime format to datetime to best management.
            date_entity = datetime.datetime.strptime(json_response.get('createdAt', None), "%a %b %d %H:%M:%S %Y")

            # Check if the hours and minutes both are the same.
            assert date_entity.strftime("%H:%M") == date_time_now.strftime("%H:%M")
            # And if the date also it's the same.
            assert date_entity.date() == date_time_now.date()

            # Check status code:
            assert response.status_code == 200



        # Now check the possible errors:
        response = requests.post(url + '/class', json={'data': {'course': 1, 'word': u'B', 'level': u'ESO'}})
        assert response.status_code == 409  # 409 Conflict: this resource already exists and can't be create again.

        response = requests.post(url + '/class', json={'data': {'coursera': 1, 'word': u'B', 'level': u'ESO'}})
        assert response.status_code == 404
        # 404 Not found: this resource can't be created because any of element don't exists. ("coursera")

        response = requests.post(url + '/classes', json={'data': {'course': 1, 'word': u'B', 'level': u'ESO'}})
        assert response.status_code == 404
        # 404 Not found: this resource can't be created because the resource "classes" doesn't exists.




