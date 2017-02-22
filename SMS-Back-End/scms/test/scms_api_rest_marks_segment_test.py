import requests
import os
from termcolor import colored
import datetime
from time import sleep


url = 'http://localhost:8003/mark'
original_mark = {
    "studentId": 5,
    "enrollmentId": 3,
    "preFirstEv": 3,
    "firstEv": 5,
    "preSecondEv": 8,
    "secondEv": 9,
    "thirdEv": 10,
    "final": 9
}


class TestClass:

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

    def test_post_and_get_mark(self):

        post_response = requests.post(url=url, json=original_mark)

        assert post_response.status_code == 200  # Successful query.

        # In the get a Mark returned must have all values from original mark plus
        # the metadata 'createdBy', 'createdAt' and 'markId'
        mr = post_response.json()

        TestClass.check_mark_with_original(mr, original_mark)

        # Because the Asynchrony of the server.
        sleep(0.5)  # Time in seconds.

        # Now we are going to check the same with the get method:
        get_response = requests.get(url='{}/{}'.format(url, mr['markId']))
        assert get_response.status_code == 200

        mr = get_response.json()

        TestClass.check_mark_with_original(mr, original_mark)

        # Check when we want all marks in the data store.
        get_all_response = requests.get(url='{}'.format(url))

        assert get_all_response.status_code == 200

        # Data returned must be a list with only one element.
        marks_list = get_all_response.json()

        assert len(marks_list) == 1

        # And the element it's just the waited.
        mr = marks_list[0]
        TestClass.check_mark_with_original(mr, original_mark)

        # And if we add two more
        post_response = requests.post(url=url, json=original_mark)
        post_response = requests.post(url=url, json=original_mark)

        sleep(0.5)
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 200

        # Data returned must be a list with three element.
        marks_list = get_all_response.json()
        assert len(marks_list) == 3

    def test_delete_mark(self):

        # Based of last three insertion, we are going to delete these items, first get the list of all:
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 200
        marks_list = get_all_response.json()

        # After, check if deleted calls are ok.
        for mark in marks_list:
            delete_response = requests.delete(url='{}/{}'.format(url, mark['markId']))
            assert delete_response.status_code == 200

        sleep(0.5)

        # Finally check if the items has been deleted.
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 204  # Status Code: No Content
