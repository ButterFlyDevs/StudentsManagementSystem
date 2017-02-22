import requests
import os
from termcolor import colored
import datetime
from time import sleep


url = 'http://localhost:8003/disciplinarynote'

original_disciplinary_note = {
    'studentId': 5,
    'studentsIdsRelated': [3, 7, 2],
    'date': '2000-12-03 10:30',

    'kind': 1,
    'gravity': 5,
    'description': 'A little problem with new boy.'
}

class TestClass:

    @classmethod
    def check_disciplinary_note_with_original(cls, disciplinary_note, disciplinary_note2):

        # In the get a Disciplinary Note returned must have all values from original disciplinary_note plus
        # the metadata 'createdBy', 'createdAt' and 'disciplinaryNoteId'
        assert disciplinary_note.get('createdBy', None)
        assert disciplinary_note.get('createdAt', None)
        assert disciplinary_note.get('disciplinaryNoteId', None)

        # And the rest of values of the disciplinary_note saved:
        for k, v in disciplinary_note2.items():
            if k == 'date':
                # Data Store return the data in ISO8601 format, to compare is needed convert it.
                assert datetime.datetime.strptime(disciplinary_note[k], "%Y-%m-%dT%H:%M:%S") == datetime.datetime.strptime(v, "%Y-%m-%d %H:%M")
            else:
                assert disciplinary_note[k] == v

    def test_post_and_get_disciplinary_note(self):

        post_response = requests.post(url=url, json=original_disciplinary_note)

        assert post_response.status_code == 200  # Successful query.

        # In the get a Disciplinary Note returned must have all values from original disciplinary_note plus
        # the metadata 'createdBy', 'createdAt' and 'disciplinaryNoteId'
        dn = post_response.json()

        TestClass.check_disciplinary_note_with_original(dn, original_disciplinary_note)

        # Because the Asynchrony of the server.
        sleep(0.5)  # Time in seconds.

        # Now we are going to check the same with the get method:
        get_response = requests.get(url='{}/{}'.format(url, dn['disciplinaryNoteId']))
        assert get_response.status_code == 200

        dn = get_response.json()

        TestClass.check_disciplinary_note_with_original(dn, original_disciplinary_note)

        # Check when we want all disciplinary notes in the data store.
        get_all_response = requests.get(url='{}'.format(url))

        assert get_all_response.status_code == 200

        # Data returned must be a list with only one element.
        disciplinary_notes_list = get_all_response.json()

        assert len(disciplinary_notes_list) == 1

        # And the element it's just the waited.
        dn = disciplinary_notes_list[0]
        TestClass.check_disciplinary_note_with_original(dn, original_disciplinary_note)

        # And if we add two more
        post_response = requests.post(url=url, json=original_disciplinary_note)
        post_response = requests.post(url=url, json=original_disciplinary_note)

        sleep(0.5)
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 200

        # Data returned must be a list with three element.
        disciplinary_notes_list = get_all_response.json()
        assert len(disciplinary_notes_list) == 3

    def test_delete_disciplinary_note(self):

        # Based of last three insertion, we are going to delete these items, first get the list of all:
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 200
        disciplinary_notes_list = get_all_response.json()

        # After, check if deleted calls are ok.
        for dn in disciplinary_notes_list:
            delete_response = requests.delete(url='{}/{}'.format(url, dn['disciplinaryNoteId']))
            assert delete_response.status_code == 200

        sleep(0.5)

        # Finally check if the items has been deleted.
        get_all_response = requests.get(url='{}'.format(url))
        assert get_all_response.status_code == 204  # Status Code: No Content
