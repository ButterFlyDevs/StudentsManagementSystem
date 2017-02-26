# -*- coding: utf-8 -*-
"""
##########################################################
### Students Control micro Service Api Rest Test Suite ###
##########################################################

"""
import requests
import os
from termcolor import colored
import datetime

urlBase = 'http://localhost:8003/association'


class TestClass:

    def test_empty_data_store_and_schema(self):
        result = requests.get(urlBase)
        assert result.status_code == 204

        result = requests.get(urlBase+'/schema')

        print result

    """
    def test_post_association(self):

        url = urlBase + '/association'

        association = {
            'association': {
                'associationId': 13,
                'class': {'classId': 283, 'classWord': 'A', 'classCourse': 2, 'classLevel': 'Elementary'},
                'subject': {'subjectId': 24, 'subjectName': 'Pruebas'}
            },
            'teacher': {'teacherId': 213,
                        'teacherName': 'asdk',
                        'teacherSurname': 'sdlkfjs',
                        'teacherImgProfile': 'www.google.es'},

            'students': [{'studentId': 213,
                          'studentName': 'asdk',
                          'studentSurname': 'sdlkfjs',
                          'studentImgProfile': 'www.google.es'},

                         {'studentId': 213,
                          'studentName': 'asdk',
                          'studentSurname': 'sdlkfjs',
                          'studentImgProfile': 'www.google.es'}
                         ]
        }

        response = requests.post(url=url, json=association)

        assert response.status_code == 200  # Success but without content.
    """


