# -*- coding: utf-8 -*-
"""
##############################################
### Teaching Data Base Api Rest Test Suite ###
##############################################

# Testing using pytests library. Use: pytest or py.test in the same folder
# To show details

This Test Suite is a mix between UnitTest and functional test because we focus the
test in the the functionality of the Api and inside of this tst whe check a lot of times
the functions unitarian.


# py.test --cov-report html --cov . --verbose


# How check code quality: pylint dbms_api.py
"""
import requests
import os
from termcolor import colored
import datetime

urlBase = 'http://localhost:8002'
example_user = 1

class TestClass:

    def setup_method(self):
        # pytest test/dbms_api_test.py::TestClass::test_dbms_api_test -vv -s
        os.system('mysql -u root -p\'root\' < dbapi/DBCreator.sql >/dev/null 2>&1')

    def test_tdbms_api_rest_conection_test(self):
        url = urlBase + '/test'
        assert requests.get(url).json().get('dbms_api_test_status', None) == 'ok'

    def test_students_entities(self):
        """
        Test all possibilities with STUDENT kind entity.
        """
        url = urlBase + '/entities'

        # At first we don't have any student in the database.
        response = requests.get(url='{}/student'.format(url))
        assert response.status_code == 204  # Success but without content.

        """
        When we put a student in the database we receive as response the same item as is saved inside, with
        all attributes plus another to control.
        """

        # Check put a normal user with all their fields.
        user_data = {'name': u'Jessica', 'surname': u'Stewart',
                     'dni': 36178276,
                     'locality': u'Bithmonth', 'province': u'London',
                     'birthdate': '2000-12-03', 'phone': '4829172',
                     'profileImageUrl': 'http://www.iconsfind.com/wp-content/uploads/2015/10/20151012_561bae5f0713e.png',
                     'email': 'jessica.stewart@gmail.com',
                     'address': '4th floor, No 65, 25 Laleh street'}

        response = requests.post(url='{}/student'.format(url), json=user_data)
        assert response.status_code == 200  # Ok

        # Check if the values that we put are the same received:
        response = response.json()
        for key, value in user_data.iteritems():
            assert response.get(key) == user_data.get(key)

        # Check if all control values are ok:

        # Created METADATA:
        # The date when it was created without seconds:
        assert datetime.datetime.strptime(response.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert response.get('createdBy', None) == example_user
        assert response.get('studentId') == 1 # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert response.get('deletedBy', None) is None
        assert response.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert response.get('modifiedBy', None) is None
        assert response.get('modifiedAt', None) is None

        # When we insert a new student with fewer attributes:
        response = requests.post(url='{}/student'.format(url), json={'name': u'Jhon'})
        assert response.status_code == 200  # Ok

        # Only the attributes that was introduced more the basic control will be received:
        response = response.json()
        assert response.get('name') == u'Jhon'
        assert response.get('createdAt', None)
        assert response.get('createdBy') == 1
        assert response.get('studentId') == 2
        assert len(response) == 4  # One param and three metadata values.

        # Check if a bad request is correctly answered, because a required field like name in this case is missing value.
        response = requests.post(url='{}/student'.format(url), json={'surname': 'Edwards'})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered.  # With EMPTY DATA
        response = requests.post(url='{}/student'.format(url), json={})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a a bad resource is correctly answered with 404 Not found..
        assert requests.post(url='{}/studeesasd'.format(url), json=user_data).status_code == 404  # Not found

        # Check if a bad param name is detected like a bad request.
        assert requests.post(url='{}/student'.format(url), json={'namer': u'Jhon'}).status_code == 400

        # Check getter of arrays:
        response = requests.get(url='{}/student'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 2 # We only have an element inside array.

        # We check if all attributes of the item are correct.
        for key, value in user_data.iteritems():
            assert value == response_list[0].get(key)  # Compare with the original student.
            # Created metadata:
            # The date when it was created without seconds:
            assert datetime.datetime.strptime(response_list[0].get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
                   == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
            assert response_list[0].get('createdBy', None) == example_user
            assert response_list[0].get('studentId') == 1  # The id of item is returned correctly.

            # The deleted metadata values doesn't exists:
            assert response_list[0].get('deletedBy', None) is None
            assert response_list[0].get('deletedAt', None) is None

            # The modified metadata values doesn't exists:
            assert response_list[0].get('modifiedBy', None) is None
            assert response_list[0].get('modifiedAt', None) is None

        # Put 20 students more:
        for a in range(20):
            response = requests.post(url='{}/student'.format(url), json={'name': str(a), 'surname': str(a)})
            assert response.status_code == 200  # Ok

        # Check if all is inside:
        response = requests.get(url='{}/student'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 22  # We only have an element inside array.

        # Check the values of last inserted:
        for a in range(2, 22):
            assert response_list[a].get('name') == str(a-2)
            assert response_list[a].get('surname') == str(a-2)
            assert response_list[a].get('createdAt', None)
            assert response_list[a].get('createdBy') == 1
            assert response_list[a].get('studentId') == a+1
            assert len(response_list[a]) == 5 # More the surname

        # DELETIONS

        # We can't have two active items with the same dni because is the unique value in studient
        # table definition, but we can if these are "logically deleted" items.

        # We insert a nuew item
        response = requests.post(url='{}/student'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 200  # Ok
        last_item = response.json();

        # We can't insert the same item again.
        response = requests.post(url='{}/student'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 409  # Conflict

        # But if we deleted it:
        response = requests.delete('{}/student/{}'.format(url, last_item.get('studentId')))
        assert response.status_code == 200

        # We can.
        response = requests.post(url='{}/student'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 200  # Ok

        # We only have one item more that before.
        assert len(requests.get(url='{}/student'.format(url)).json()) == 23

        # Item's related that don't exists.
        response = requests.get('{}/student/{}/teacher'.format(url, 4))
        assert response.status_code == 204  #The resource exists but we can have items related.

        response = requests.get('{}/student/{}/teacher'.format(url, 44334))
        assert response.status_code == 404  #The item student with id 44334 doesn't exists.

        # UPDATES, specially with metadata:

        # Before:
        response = requests.get(url='{}/student/{}'.format(url, 1))
        assert response.status_code == 200  # Ok
        item = response.json()
        assert item.get('modifiedAt', None) is None
        assert item.get('modifiedBy', None) is None

        response = requests.put('{}/student/{}'.format(url, 1), json={'name': u'Eduard'})
        assert response.status_code == 200
        item = response.json()

        # After:
        assert item.get('name') == u'Eduard'
        assert datetime.datetime.strptime(item.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('modifiedBy', None) == 1

    def test_teachers_entities(self):
        """
        Test all possibilities with TEACHER kind entity.
        In spite of is very similar to test over students we need different methods in case it changes in the future.
        """
        url = urlBase + '/entities'

        # At first we don't have any teacher in the database.
        response = requests.get(url='{}/teacher'.format(url))
        assert response.status_code == 204  # Success but without content.

        """
        When we put a teacher in the database we receive as response the same item as is saved inside, with
        all attributes plus another to control.
        """

        # Check put a normal user with all their fields.
        user_data = {'name': u'Jhon', 'surname': u'Stephenson',
                     'dni': 36178276,
                     'locality': u'New Shamphore', 'province': u'Noth Enden',
                     'birthdate': '2000-12-03', 'phone': '4829172',
                     'profileImageUrl': 'http://www.iconsfind.com/wp-content/uploads/2015/10/20151012_561bae5f0713e.png',
                     'email': 'jhon.stephenson@gmail.com',
                     'address': '4th floor, No 65, 25 Laleh street'}

        response = requests.post(url='{}/teacher'.format(url), json=user_data)
        assert response.status_code == 200  # Ok

        # Check if the values that we put are the same received:
        response = response.json()
        for key, value in user_data.iteritems():
            assert response.get(key) == user_data.get(key)

        # Check if all control values are ok:

        # Created METADATA:
        # The date when it was created without seconds:
        assert datetime.datetime.strptime(response.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert response.get('createdBy', None) == example_user
        assert response.get('teacherId') == 1 # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert response.get('deletedBy', None) is None
        assert response.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert response.get('modifiedBy', None) is None
        assert response.get('modifiedAt', None) is None

        # When we insert a new student with fewer attributes:
        response = requests.post(url='{}/teacher'.format(url), json={'name': u'Jhon'})
        assert response.status_code == 200  # Ok

        # Only the attributes that was introduced more the basic control will be received:
        response = response.json()
        assert response.get('name') == u'Jhon'
        assert response.get('createdAt', None)
        assert response.get('createdBy') == 1
        assert response.get('teacherId') == 2
        assert len(response) == 4  # One param and three metadata values.

        # Check if a bad request is correctly answered.  # With EMPTY DATA
        response = requests.post(url='{}/teacher'.format(url), json={})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered, because a required field like name in this case is missing value
        response = requests.post(url='{}/teacher'.format(url), json={'surname': 'Edwards'})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a a bad resource is correctly answered with 404 Not found..
        assert requests.post(url='{}/teacccher'.format(url), json=user_data).status_code == 404  # Not found

        # Check if a bad param name is detected like a bad request.
        assert requests.post(url='{}/teacher'.format(url), json={'namer': u'Jhon'}).status_code == 400

        # Check getter of arrays:
        response = requests.get(url='{}/teacher'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 2 # We only have an element inside array.

        # We check if all attributes of the item are correct.
        for key, value in user_data.iteritems():
            assert value == response_list[0].get(key)  # Compare with the original teacher.
            # Created metadata:
            # The date when it was created without seconds:
            assert datetime.datetime.strptime(response_list[0].get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
                   == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
            assert response_list[0].get('createdBy', None) == example_user
            assert response_list[0].get('teacherId') == 1  # The id of item is returned correctly.

            # The deleted metadata values doesn't exists:
            assert response_list[0].get('deletedBy', None) is None
            assert response_list[0].get('deletedAt', None) is None

            # The modified metadata values doesn't exists:
            assert response_list[0].get('modifiedBy', None) is None
            assert response_list[0].get('modifiedAt', None) is None

        # Put 20 teachers more:
        for a in range(20):
            response = requests.post(url='{}/teacher'.format(url), json={'name': str(a), 'surname': str(a)})
            assert response.status_code == 200  # Ok

        # Check if all is inside:
        response = requests.get(url='{}/teacher'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 22  # We only have an element inside array.

        # Check the values of last inserted:
        for a in range(2, 22):
            assert response_list[a].get('name') == str(a-2)
            assert response_list[a].get('surname') == str(a-2)
            assert response_list[a].get('createdAt', None)
            assert response_list[a].get('createdBy') == 1
            assert response_list[a].get('teacherId') == a+1
            assert len(response_list[a]) == 5 # More the surname

        # DELETIONS

        # We can't have two active items with the same dni because is the unique value in teacher
        # table definition, but we can if these are "logically deleted" items.

        # We insert a nuew item
        response = requests.post(url='{}/teacher'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 200  # Ok
        last_item = response.json();

        # We can't insert the same item again.
        response = requests.post(url='{}/teacher'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 409  # Conflict

        # But if we deleted it:
        response = requests.delete('{}/teacher/{}'.format(url, last_item.get('teacherId')))
        assert response.status_code == 200

        # We can.
        response = requests.post(url='{}/teacher'.format(url), json={'name': str(a), 'dni': 444})
        assert response.status_code == 200  # Ok

        # We only have one item more that before.
        assert len(requests.get(url='{}/teacher'.format(url)).json()) == 23

        # Item's related that don't exists.
        response = requests.get('{}/teacher/{}/student'.format(url, 4))
        assert response.status_code == 204  #The resource exists but we can have items related.

        response = requests.get('{}/teacher/{}/student'.format(url, 44334))
        assert response.status_code == 404  #The item student with id 44334 doesn't exists.

        # UPDATES, specially with metadata:

        # Before:
        response = requests.get(url='{}/teacher/{}'.format(url, 1))
        assert response.status_code == 200  # Ok
        item = response.json()
        assert item.get('modifiedAt', None) is None
        assert item.get('modifiedBy', None) is None

        response = requests.put('{}/teacher/{}'.format(url, 1), json={'name': u'Eduard'})
        assert response.status_code == 200
        item = response.json()

        # After:
        assert item.get('name') == u'Eduard'
        assert datetime.datetime.strptime(item.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('modifiedBy', None) == 1

    def test_subjects_entities(self):
        """
        Test all possibilities with SUBJECT kind entity.
        In spite of is very similar to test over students we need different methods in case it changes in the future.
        """
        url = urlBase + '/entities'

        # At first we don't have any subject in the database.
        response = requests.get(url='{}/subject'.format(url))
        print response.text
        assert response.status_code == 204  # Success but without content.

        """
        When we put a subject in the database we receive as response the same item as is saved inside, with
        all attributes plus another to control.
        """

        # Check put a normal user with all their fields.
        subject_data = {'name': u'Special Subject', 'description': u'A very special subject.'}

        response = requests.post(url='{}/subject'.format(url), json=subject_data)
        assert response.status_code == 200  # Ok

        # Check if the values that we put are the same received:
        response = response.json()
        for key, value in subject_data.iteritems():
            assert response.get(key) == subject_data.get(key)

        # Check if all control values are ok:

        # Created METADATA:
        # The date when it was created without seconds:
        assert datetime.datetime.strptime(response.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert response.get('createdBy', None) == example_user
        assert response.get('subjectId') == 1  # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert response.get('deletedBy', None) is None
        assert response.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert response.get('modifiedBy', None) is None
        assert response.get('modifiedAt', None) is None

        # When we insert a new student with fewer attributes:
        response = requests.post(url='{}/subject'.format(url), json={'name': u'Science'})
        assert response.status_code == 200  # Ok

        # Only the attributes that was introduced more the basic control will be received:
        response = response.json()
        assert response.get('name') == u'Science'
        assert response.get('createdAt', None)
        assert response.get('createdBy') == 1
        assert response.get('subjectId') == 2
        assert len(response) == 4  # One param and three metadata values.

        # Check if a bad request is correctly answered.  # With EMPTY DATA
        response = requests.post(url='{}/subject'.format(url), json={})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered, because a required field like name in this case is missing value.
        response = requests.post(url='{}/subject'.format(url), json={'description': 'Amazing things'})
        assert response.status_code == 400  # Bad request
        assert 'Column \'name\' cannot be null' in response.text  # Because name is required value.

        # Check if a a bad resource is correctly answered with 404 Not found..
        assert requests.post(url='{}/subbbject'.format(url), json=subject_data).status_code == 404  # Not found

        # Check if a bad param name is detected like a bad request.
        assert requests.post(url='{}/subject'.format(url), json={'namer': u'History'}).status_code == 400

        # Check getter of arrays:
        response = requests.get(url='{}/subject'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 2  # We only have an element inside array.

        # We check if all attributes of the item are correct.
        for key, value in subject_data.iteritems():
            assert value == response_list[0].get(key)  # Compare with the original subject.
            # Created metadata:
            # The date when it was created without seconds:
            assert datetime.datetime.strptime(response_list[0].get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime(
                "%Y-%m-%dT%H:%M") \
                   == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
            assert response_list[0].get('createdBy', None) == example_user
            assert response_list[0].get('subjectId') == 1  # The id of item is returned correctly.

            # The deleted metadata values doesn't exists:
            assert response_list[0].get('deletedBy', None) is None
            assert response_list[0].get('deletedAt', None) is None

            # The modified metadata values doesn't exists:
            assert response_list[0].get('modifiedBy', None) is None
            assert response_list[0].get('modifiedAt', None) is None

        # Put 20 subjects more:
        for a in range(20):
            response = requests.post(url='{}/subject'.format(url), json={'name': str(a), 'description': str(a)})
            assert response.status_code == 200  # Ok

        # Check if all is inside:
        response = requests.get(url='{}/subject'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 22  # We only have an element inside array.

        # Check the values of last inserted:
        for a in range(2, 22):
            assert response_list[a].get('name') == str(a - 2)
            assert response_list[a].get('description') == str(a - 2)
            assert response_list[a].get('createdAt', None)
            assert response_list[a].get('createdBy') == 1
            assert response_list[a].get('subjectId') == a + 1
            assert len(response_list[a]) == 5  # More the surname

        # DELETIONS

        # We can't have two active items with the same dni because is the unique value in subject
        # table definition, but we can if these are "logically deleted" items.

        # We insert a new item
        response = requests.post(url='{}/subject'.format(url), json={'name': u'Literature'})
        assert response.status_code == 200  # Ok
        last_item = response.json();

        # We can't insert the same item again.
        response = requests.post(url='{}/subject'.format(url), json={'name': u'Literature'})
        assert response.status_code == 409  # Conflict

        # But if we deleted it:
        response = requests.delete('{}/subject/{}'.format(url, last_item.get('subjectId')))
        assert response.status_code == 200

        # We can.
        response = requests.post(url='{}/subject'.format(url), json={'name': u'Literature'})
        assert response.status_code == 200  # Ok

        # We only have one item more that before.
        assert len(requests.get(url='{}/subject'.format(url)).json()) == 23

        # Item's related that don't exists.
        response = requests.get('{}/subject/{}/student'.format(url, 4))
        assert response.status_code == 204  # The resource exists but we can have items related.

        response = requests.get('{}/subject/{}/student'.format(url, 44334))
        assert response.status_code == 404  # The item student with id 44334 doesn't exists.

        # UPDATES, specially with metadata:

        # Before:
        response = requests.get(url='{}/subject/{}'.format(url, 1))
        assert response.status_code == 200  # Ok
        item = response.json()
        assert item.get('modifiedAt', None) is None
        assert item.get('modifiedBy', None) is None

        # We modify it:
        response = requests.put('{}/subject/{}'.format(url, 1), json={'name': u'Geography'})
        assert response.status_code == 200
        item = response.json()

        # After:
        assert item.get('name') == u'Geography'
        assert datetime.datetime.strptime(item.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('modifiedBy', None) == 1

    def test_classes_entities(self):

        # Test all possibilities with CLASS kind entity.
        # In spite of is very similar to test over students we need different methods in case it changes in the future.

        url = urlBase + '/entities'

        # At first we don't have any class in the database.
        response = requests.get(url='{}/class'.format(url))
        assert response.status_code == 204  # Success but without content.

        # When we put a class in the database we receive as response the same item as is saved inside, with
        # all attributes plus another to control.

        # Check put a normal class with all their fields.
        class_data = {'course': 1, 'word': u'A', 'level': u'Primary', 'description': u'The better class in school.'}

        response = requests.post(url='{}/class'.format(url), json=class_data)
        assert response.status_code == 200  # Ok

        # Check if the values that we put are the same received:
        response = response.json()
        for key, value in class_data.iteritems():
            assert response.get(key) == class_data.get(key)

        # Check if all control values are ok:

        # Created METADATA:
        # The date when it was created without seconds:
        assert datetime.datetime.strptime(response.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert response.get('createdBy', None) == example_user
        assert response.get('classId') == 1  # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert response.get('deletedBy', None) is None
        assert response.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert response.get('modifiedBy', None) is None
        assert response.get('modifiedAt', None) is None

        # When we insert the same we have an error:
        response = requests.post(url='{}/class'.format(url), json={'course': 1, 'word': u'A', 'level': u'Primary'})
        assert response.status_code == 409  # Conflict because it already exists.

        # When we insert a new class with fewer attributes:
        response = requests.post(url='{}/class'.format(url), json={'course': 3, 'word': u'D', 'level': u'Elemental'})
        assert response.status_code == 200  # Conflict because it already exists.

        # Only the attributes that was introduced more the basic control will be received:
        response = response.json()
        assert response.get('course') == 3
        assert response.get('word') == u'D'
        assert response.get('level') == u'Elemental'
        assert response.get('createdAt', None)
        assert response.get('createdBy') == 1
        assert response.get('classId') == 3
        assert len(response) == 6

        # Check if a bad request is correctly answered.  # With EMPTY DATA
        response = requests.post(url='{}/class'.format(url), json={})
        assert response.status_code == 400  # Bad request
        assert 'Column \'course\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered, in this case course, word and level are required.
        response = requests.post(url='{}/class'.format(url), json={'course': 3})
        assert response.status_code == 400  # Bad request
        assert 'Column \'word\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered, in this case course, word and level are required.
        response = requests.post(url='{}/class'.format(url), json={'course': 3, 'word': u'D',})
        assert response.status_code == 400  # Bad request
        assert 'Column \'level\' cannot be null' in response.text  # Because name is required value.

        # Check if a bad request is correctly answered, in this case course, group and subgroup are required.
        response = requests.post(url='{}/class'.format(url), json={'course': 3, 'level': u'Elementary'})
        assert response.status_code == 400  # Bad request
        # Because seems like it wanted create a new special group and two values are required:
        assert 'you need group and subgroup values to create an optional group ' in response.text

        # If we try to delete a class that doesn't exists.
        response = requests.delete('{}/class/{}'.format(url, 123))
        assert response.status_code == 404

        # Special cases with SPECIAL OPTIONAL CLASSES

        # Insert a special OPTIONAL CLASS.
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 1, 'subgroup': 1})
        class_id = response.json().get('classId')
        assert response.status_code == 200
        # Insert again
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 1, 'subgroup': 1})
        assert response.status_code == 409  # 409 Conflict: this resource already exists and can't be create again.
        # Delete the last.
        response = requests.delete('{}/class/{}'.format(url, class_id))
        assert response.status_code == 200
        assert len(response.text) == 0  # When we delete an item we don't receive data in the body of response.

        # If try to del again we can't.
        response = requests.delete('{}/class/{}'.format(url, class_id))
        assert response.status_code == 404

        # Insert again
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 1, 'subgroup': 1})
        class_id = response.json().get('classId')
        assert response.json().get('word') == 'OPT_1_1' # Special nomenclature to OPTIONAL CLASSES.
        assert response.status_code == 200

        # Insert another
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 1, 'subgroup': 2})
        class_id_2 = response.json().get('classId')
        assert response.json().get('word') == 'OPT_1_2'  # Special nomenclature to OPTIONAL CLASSES.
        assert response.status_code == 200

        # Because our definition we can delete a optional group if exists another higher (in group and subgroup).
        response = requests.delete('{}/class/{}'.format(url, class_id))
        assert 'Imposible deleting, there are a subgroup higher, and this broke the consistency.' in response.text
        assert response.status_code == 409  # 409 is Conflict

        # But if we delete it before:
        response = requests.delete('{}/class/{}'.format(url, class_id_2))
        assert response.status_code == 200
        assert len(response.text) == 0

        # Yes now:
        assert requests.delete('{}/class/{}'.format(url, class_id)).status_code == 200

        # Insert another
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 2, 'subgroup': 1})
        assert 'Impossible insert, should be exists a group lower, and this broke the consistency.' in response.text
        assert response.status_code == 409  # 409 is Conflict

        assert requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 1, 'subgroup': 1}).status_code == 200

        # Now we try to insert the same but with the group more higher.
        response = requests.post(url='{}/{}'.format(url, 'class'),
                                 json={'course': 1, 'level': u'ESO', 'group': 2, 'subgroup': 2})
        assert 'Impossible insert, should be exists a subgroup lower, and this broke the consistency.' in response.text
        assert response.status_code == 409  # 409 is Conflict

        assert requests.post(url='{}/{}'.format(url, 'class'),
                             json={'course': 1, 'level': u'ESO', 'group': 2, 'subgroup': 1}).status_code == 200
        assert requests.post(url='{}/{}'.format(url, 'class'),
                             json={'course': 1, 'level': u'ESO', 'group': 2, 'subgroup': 2}).status_code == 200

        # Check if a a bad resource is correctly answered with 404 Not found..
        assert requests.post(url='{}/classs'.format(url), json=class_data).status_code == 404  # Not found

        # Check if a bad param name is detected like a bad request.
        assert requests.post(url='{}/class'.format(url), json={'coursaare': 1, 'word': u'A', 'level': u'Primary'}).status_code == 400

        # Check getter of arrays:
        response = requests.get(url='{}/class'.format(url))
        assert response.status_code == 200
        response_list = response.json()

        # Get method must return an array if we don't specify an id.
        assert isinstance(response_list, list)
        assert len(response_list) == 5  # We only have an element inside array.

    def test_association_relation(self):
        url = urlBase + '/entities'

        # At first we don't have any association relation.
        response = requests.get(url='{}/association'.format(url))
        assert response.status_code == 204  # Success but without content.

        # We can't associate a class and subject that doesn't exists.
        response = requests.post(url='{}/association'.format(url),
                                 json={'subjectId': 1, 'classId': 1})
        print 'the subject related should be exists' in response.text
        assert response.status_code == 409

        # Try now with a couple that exists:
        assert requests.post(url='{}/class'.format(url),
                                 json={'course': 1, 'word': u'A', 'level': u'Primary',
                                       'description': u'The better class in school.'}).status_code == 200

        assert requests.post(url='{}/subject'.format(url),
                                 json={'name': u'Special Subject',
                                       'description': u'A very special subject.'}).status_code == 200

        # We know the how the ids that the database assign.
        response = requests.post(url='{}/association'.format(url),json={'subjectId': 1, 'classId': 1})
        assert response.status_code == 200

        # Created METADATA:

        # The date when it was created without seconds:
        item = response.json()
        assert datetime.datetime.strptime(item.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('createdBy', None) == example_user
        assert item.get('associationId') == 1  # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert item.get('deletedBy', None) is None
        assert item.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert item.get('modifiedBy', None) is None
        assert item.get('modifiedAt', None) is None

        # Now we delete the association relation:
        response = requests.delete('{}/association/{}'.format(url, item.get('associationId')))
        assert response.status_code == 200
        assert len(response.text) == 0

        # Now we DELETE THE SUBJECT in this relation also, in subject table:
        assert requests.delete('{}/subject/{}'.format(url, 1)).status_code == 200

        # If we try to create the same relation, this would be fail, because subject related is deleted in the system.
        response = requests.post(url='{}/association'.format(url),json={'subjectId': 1, 'classId': 1})
        assert 'the subject related should be exists' in response.text
        assert response.status_code == 409  # Conflict

        # But if insert another subject
        assert requests.post(url='{}/subject'.format(url),
                                 json={'name': u'Special Subject',
                                       'description': u'A very special subject.'}).status_code == 200

        # And delete the class:
        assert requests.delete('{}/class/{}'.format(url, 1)).status_code == 200

        # We found a similar error:
        response = requests.post(url='{}/association'.format(url), json={'subjectId': 2, 'classId': 1})
        assert 'the class related should be exists' in response.text
        assert response.status_code == 409  # Conflict

        # SPECIAL CASES IN CLASS TABLE WHEN ASSOCIATION RELATED ITEMS EXISTS

        # If we try to delete a class that is related in association we would see an error.

        # A new class
        assert requests.post(url='{}/class'.format(url),
                     json={'course': 1, 'word': u'A', 'level': u'Primary',
                           'description': u'The better class in school.'}).status_code == 200
        # A new  association relation
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 2, 'classId': 2}).status_code == 200

        # We can't delete the class related with this association
        response = requests.delete('{}/class/{}'.format(url, 2)) # The second association, id: 2
        assert 'Impossible delete the class, this is related with some subject ' in response.text
        assert response.status_code == 409  # Conflict

        # The same occurs with subject table:
        response = requests.delete('{}/subject/{}'.format(url, 2))  # The second association, id: 2
        assert 'Impossible delete the subject, this is related with some class ' in response.text
        assert response.status_code == 409  # Conflict

        # If we delete the association, is possible:
        assert requests.delete('{}/association/{}'.format(url, 2)).status_code == 200
        assert requests.delete('{}/class/{}'.format(url, 2)).status_code == 200
        assert requests.delete('{}/subject/{}'.format(url, 2)).status_code == 200

    def test_enrollment_relation(self):
        url = urlBase + '/entities'

        # At first we don't have any enrollment relation.
        response = requests.get(url='{}/enrollment'.format(url))
        assert response.status_code == 204  # Success but without content.

        # We can't create a enrollment relation between an association and student that doesn't exists.
        response = requests.post(url='{}/enrollment'.format(url), json={'associationId': 1, 'studentId': 1})
        print 'the enrollment related should be exists' in response.text
        assert response.status_code == 409

        # Try now with a couple that exists:
        assert requests.post(url='{}/class'.format(url),
                             json={'course': 1, 'word': u'A', 'level': u'Primary'}).status_code == 200
        assert requests.post(url='{}/subject'.format(url),
                             json={'name': u'Special Subject',}).status_code == 200
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 1}).status_code == 200
        assert requests.post(url='{}/student'.format(url), json={'name': u'Suzan'}).status_code == 200

        # Check the creation of the ENROLLMENT relation
        response = requests.post(url='{}/enrollment'.format(url), json={'associationId': 1, 'studentId': 1})
        assert response.status_code == 200

        # Created METADATA:

        # The date when it was created without seconds:
        item = response.json()
        assert datetime.datetime.strptime(item.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('createdBy', None) == example_user
        assert item.get('associationId') == 1  # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert item.get('deletedBy', None) is None
        assert item.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert item.get('modifiedBy', None) is None
        assert item.get('modifiedAt', None) is None

        # Now we delete the enrollment relation:
        item = requests.delete('{}/enrollment/{}'.format(url, item.get('enrollmentId')))
        assert item.status_code == 200
        assert len(item.text) == 0

        # If we try to insert again the same enrollment relation it will be fine, but not
        # if we delete before the "student" of "association" because to create an
        # enrollment relation should exist both.

        assert requests.delete('{}/association/{}'.format(url, 1)).status_code == 200


        # Check the error
        response = requests.post(url='{}/enrollment'.format(url), json={'associationId': 1, 'studentId': 1})
        assert 'the association related should be exists' in response.text
        assert response.status_code == 409  # Conflict

        # We create the same association to check the same with the student.
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 1}).status_code == 200

        # The student with id 2 doesn't exists
        response = requests.post(url='{}/enrollment'.format(url), json={'associationId': 2, 'studentId': 2})
        assert 'the student related should be exists' in response.text
        assert response.status_code == 409  # Conflict

        # SPECIAL CASES:

        # If we try to delete an association that appear in  enrollment table, should
        # retrieve an error, and the same with student.

        assert requests.post(url='{}/enrollment'.format(url), json={'associationId': 2, 'studentId': 1}).status_code == 200

        # With the student
        response = requests.delete(url='{}/student/{}'.format(url, 1))
        assert response.status_code == 409
        assert 'Impossible delete the student, this is related with some association in enrollment table' in response.text

        # With the association
        response = requests.delete(url='{}/association/{}'.format(url, 2))
        assert response.status_code == 409
        assert 'Impossible delete the association, this is related with some student in enrollment table' in response.text

    def test_impart_relation(self):
        url = urlBase + '/entities'

        # At first we don't have any enrollment relation.
        response = requests.get(url='{}/impart'.format(url))
        assert response.status_code == 204  # Success but without content.

        # We can't create a enrollment relation between an teacher and association that doesn't exists.
        response = requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 1})
        print 'the teacher related should be exists' in response.text
        assert response.status_code == 409

        # Try now with a couple that exists:
        assert requests.post(url='{}/class'.format(url),
                             json={'course': 1, 'word': u'A', 'level': u'Primary'}).status_code == 200
        assert requests.post(url='{}/subject'.format(url),
                             json={'name': u'Special Subject',}).status_code == 200
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 1}).status_code == 200
        assert requests.post(url='{}/teacher'.format(url), json={'name': u'Suzan'}).status_code == 200

        # Check the creation of the IMPART relation
        response = requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 1})
        assert response.status_code == 200

        # Created METADATA:

        # The date when it was created without seconds:
        item = response.json()
        assert datetime.datetime.strptime(item.get('createdAt'), '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%dT%H:%M") \
               == datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        assert item.get('createdBy', None) == example_user
        assert item.get('impartId') == 1  # The id of item is returned correctly.

        # The deleted metadata values doesn't exists:
        assert item.get('deletedBy', None) is None
        assert item.get('deletedAt', None) is None

        # The modified metadata values doesn't exists:
        assert item.get('modifiedBy', None) is None
        assert item.get('modifiedAt', None) is None

        # Now we delete the impart relation:
        item = requests.delete('{}/impart/{}'.format(url, item.get('impartId')))
        assert item.status_code == 200
        assert len(item.text) == 0

        # If we try to insert again the same enrollment relation it will be fine, but not
        # if we delete before the "student" of "association" because to create an
        # enrollment relation should exist both.

        assert requests.delete('{}/association/{}'.format(url, 1)).status_code == 200

        # Check the error
        response = requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 1})
        assert 'the association related should be exists' in response.text
        assert response.status_code == 409  # Conflict

        # We create the same association to check the same with the student.
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 1}).status_code == 200

        # The teacher with id 2 doesn't exists
        response = requests.post(url='{}/impart'.format(url), json={'teacherId': 2, 'associationId': 2})
        assert 'the teacher related should be exists' in response.text
        assert response.status_code == 409  # Conflict


        # SPECIAL CASES:

        # If we try to delete an association that appear in  enrollment table, should
        # retrieve an error, and the same with student.

        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 2}).status_code == 200

        # With the teacher
        response = requests.delete(url='{}/teacher/{}'.format(url, 1))
        assert response.status_code == 409
        assert 'Impossible delete the teacher, this is related with some association in impart table' in response.text

        # With the association
        response = requests.delete(url='{}/association/{}'.format(url, 2))
        assert response.status_code == 409
        assert 'Impossible delete the association, this is related with some teacher in impart table' in response.text

    def test_cascade_deletions(self):

        url = urlBase + '/entities'

        assert requests.get(url='{}/student'.format(url)).status_code == 204  # Success but without content.
        assert requests.get(url='{}/teacher'.format(url)).status_code == 204  # Success but without content.
        assert requests.get(url='{}/class'.format(url)).status_code == 204  # Success but without content.
        assert requests.get(url='{}/association'.format(url)).status_code == 204  # Success but without content.
        assert requests.get(url='{}/enrollment'.format(url)).status_code == 204  # Success but without content.
        assert requests.get(url='{}/impart'.format(url)).status_code == 204  # Success but without content.

        # One student
        assert requests.post(url='{}/student'.format(url), json={'name': u'Jhon'}).status_code == 200  # Ok
        # Insert another for future:
        assert requests.post(url='{}/student'.format(url), json={'name': u'Smith'}).status_code == 200  # Ok

        assert requests.post(url='{}/class'.format(url),
                                 json={'course': 1, 'word': u'A', 'level': u'Primary',}).status_code == 200
        assert requests.post(url='{}/subject'.format(url),json={'name': u'Special Subject'}).status_code == 200

        assert requests.post(url='{}/association'.format(url),json={'subjectId': 1, 'classId': 1}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url),json={'associationId': 1, 'studentId': 1}).status_code == 200

        # If we delete the student with DELETE DEPENDENCIES option:
        assert requests.delete('{}/student/{}?action=dd'.format(url, 1)).status_code == 200

        # The enrollment relation should be deleted also at the same time:
        # Check if the table is empty
        assert requests.get(url='{}/enrollment'.format(url)).status_code == 204  # Success but without content.

        # But in the student table there are another and only one student (Smith):
        assert len(requests.get(url='{}/student'.format(url)).json()) == 1

        # Now we enrollment the second student with the last association:
        assert requests.post(url='{}/enrollment'.format(url),
                             json={'associationId': 1, 'studentId': 2}).status_code == 200
        assert len(requests.get(url='{}/enrollment'.format(url)).json()) == 1
        assert len(requests.get(url='{}/association'.format(url)).json()) == 1

        # If we delete the subject in DD mode the association related and enrollment should be erased too.
        assert requests.delete('{}/subject/{}?action=dd'.format(url, 1)).status_code == 200
        assert requests.get(url='{}/enrollment'.format(url)).status_code == 204 # Success but without content.
        assert requests.get(url='{}/association'.format(url)).status_code == 204 # Success but without content
        assert len(requests.get(url='{}/student'.format(url)).json()) == 1

        # If after we also delete the class:
        assert requests.delete('{}/class/{}'.format(url, 1)).status_code == 200
        assert requests.get(url='{}/class'.format(url)).status_code == 204

        # If after we also delete the student:
        assert requests.delete('{}/student/{}'.format(url, 2)).status_code == 200
        assert requests.get(url='{}/student'.format(url)).status_code == 204


    def test_final_general_relations(self):
        """
        Realistic test with entire domain.
        """
        url = urlBase + '/entities'

        ## MORE COMPLEX TEST ##

        # Basic Scenario Seting
        words = ['A','B','C']
        for a in range(1, 4):
            assert requests.post(url='{}/student'.format(url), json={'name': str(a)}).status_code == 200
            assert requests.post(url='{}/teacher'.format(url), json={'name': str(a)}).status_code == 200
            assert requests.post(url='{}/class'.format(url),
                                 json={'course': a, 'word': words[a-1], 'level': str(a)}).status_code == 200
            assert requests.post(url='{}/subject'.format(url), json={'name': str(a)}).status_code == 200

        # Associations:
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 1}).status_code == 200  # 1
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 2}).status_code == 200  # 2
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 1, 'classId': 3}).status_code == 200  # 3
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 2, 'classId': 2}).status_code == 200  # 4
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 2, 'classId': 3}).status_code == 200  # 5
        assert requests.post(url='{}/association'.format(url), json={'subjectId': 3, 'classId': 3}).status_code == 200  # 6

        # Imparts
        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 3}).status_code == 200
        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 2}).status_code == 200
        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 1, 'associationId': 1}).status_code == 200

        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 2, 'associationId': 4}).status_code == 200
        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 2, 'associationId': 5}).status_code == 200

        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 3, 'associationId': 5}).status_code == 200
        assert requests.post(url='{}/impart'.format(url), json={'teacherId': 3, 'associationId': 6}).status_code == 200

        # Enrollments
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 1, 'associationId': 6}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 1, 'associationId': 3}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 1, 'associationId': 5}).status_code == 200

        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 2, 'associationId': 6}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 2, 'associationId': 3}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 2, 'associationId': 5}).status_code == 200

        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 3, 'associationId': 4}).status_code == 200
        assert requests.post(url='{}/enrollment'.format(url), json={'studentId': 3, 'associationId': 2}).status_code == 200

        # Now we will check the status of relations:

        associations = requests.get(url='{}/association'.format(url)).json()
        assert len(associations) == 6

        association = requests.get(url='{}/association/{}'.format(url, 1)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 1 and association['teachers'][0]['teacherId'] == 1
        assert association.get('students', None) is None
        assert association['subject']['subjectId'] == 1
        assert association['class']['classId'] == 1

        association = requests.get(url='{}/association/{}'.format(url, 2)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 1 and association['teachers'][0]['teacherId'] == 1
        assert len(association.get('students', None)) == 1 and association['students'][0]['studentId'] == 3
        assert association['subject']['subjectId'] == 1
        assert association['class']['classId'] == 2

        association = requests.get(url='{}/association/{}'.format(url, 3)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 1 and association['teachers'][0]['teacherId'] == 1
        assert len(association.get('students', None)) == 2 and association['students'][0]['studentId'] == 1 \
               and association['students'][1]['studentId'] == 2
        assert association['subject']['subjectId'] == 1
        assert association['class']['classId'] == 3

        association = requests.get(url='{}/association/{}'.format(url, 4)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 1 and association['teachers'][0]['teacherId'] == 2
        assert len(association.get('students', None)) == 1 and association['students'][0]['studentId'] == 3
        assert association['subject']['subjectId'] == 2
        assert association['class']['classId'] == 2

        association = requests.get(url='{}/association/{}'.format(url, 5)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 2 and association['teachers'][0]['teacherId'] == 2 \
                and association['teachers'][1]['teacherId'] == 3
        assert len(association.get('students', None)) == 2 and association['students'][0]['studentId'] == 1 \
               and association['students'][1]['studentId'] == 2
        assert association['subject']['subjectId'] == 2
        assert association['class']['classId'] == 3

        association = requests.get(url='{}/association/{}'.format(url, 6)).json()  # Check the data block.
        assert len(association.get('teachers', None)) == 1 and association['teachers'][0]['teacherId'] == 3
        assert len(association.get('students', None)) == 2 and association['students'][0]['studentId'] == 1 \
               and association['students'][1]['studentId'] == 2
        assert association['subject']['subjectId'] == 3
        assert association['class']['classId'] == 3

        enrollments = requests.get(url='{}/enrollment'.format(url)).json()
        assert len(enrollments) == 8

        # Students teaching

        student_teaching = requests.get(url='{}/student/{}/teaching'.format(url, 1)).json()
        assert len(student_teaching) == 1
        assert len(student_teaching[0].get('subjects')) == 3
        assert student_teaching[0].get('class').get('classId') == 3

        # ... the rest of students

        # Teachers teaching
        teacher_teaching = requests.get(url='{}/teacher/{}/teaching'.format(url, 1)).json()
        assert len(teacher_teaching) == 1
        assert len(teacher_teaching[0].get('classes')) == 3
        assert teacher_teaching[0].get('subject').get('subjectId') == 1

        # Teacher related num of items:
        assert len(requests.get(url='{}/teacher/{}/student'.format(url, 1)).json()) == 3
        assert len(requests.get(url='{}/teacher/{}/student'.format(url, 2)).json()) == 3
        assert len(requests.get(url='{}/teacher/{}/student'.format(url, 3)).json()) == 2

        #####
        # SOME ERRORS, the relational tables shouldn't be a valid nested resource.
        #####

        # Check that some nested resource can be accessed from basic items.
        basic_list = ['association', 'impart', 'enrollment']
        for a in ['class', 'subject', 'student', 'teacher']:
            plus_list = list(basic_list)
            plus_list.append(a)
            for item in plus_list:
                res = requests.get(url='{}/{}/{}/{}'.format(url, a, 1, item))
                assert res.status_code == 400 and 'is not a valid nested resource.' in res.text

        # Check that any nested resource can be accessed from enrollment.
        basic_list = ['association', 'impart', 'enrollment', 'subject', 'class', 'student', 'teacher']
        items = ['enrollment', 'impart', 'association']
        for item in items:
            for element in basic_list:
                res = requests.get(url='{}/{}/{}/{}'.format(url, item, 1, element))
                assert res.status_code == 400 and 'is not a valid nested resource.' in res.text

        # There are a lot of test that we could be do still.