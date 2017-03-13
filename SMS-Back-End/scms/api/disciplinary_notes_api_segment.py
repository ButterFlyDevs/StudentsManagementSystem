"""
Disciplinary Notes
==================

This is the section of API that manage the resources related with this kind of objects.

/disciplinarynote
-----------------

    **GET**

    Return all attendance controls realized with minimal info in a json **list**, all items with all info.

    Example:

    >>> curl -i -X GET localhost:8003/disciplinarynote
    [
        {
            "classId": 3,
            "createdAt": "2017-03-13T11:12:23.846126",
            "createdBy": 1,
            "dateTime": "2000-12-03T10:30:00",
            "description": "A little problem with new boy.",
            "disciplinaryNoteId": 5224879255191552,
            "gravity": 5,
            "kind": 3,
            "student": {
                "name": "Maria",
                "studentId": 1,
                "surname": "adsf"
            },
            "subjectId": 21,
            "teacher": {
                "name": "Jesus",
                "profileImageUrl": "dfasdfa",
                "surname": "dslk",
                "teacherId": 1
            }
        }
    ]

    .. note:: This resource depends of another service (to get extra info about items)

    **POST**

        Save in database one, return a simple http status code and **id of item stored** as a dictionary with "disciplinaryNoteId" key.
        The attributes classId and subjectId are *OPTIONALS*. Maybe the problem happened out of class.

        Example, sending a json:
        >>> curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/disciplinary_note_example_1.json localhost:8003/disciplinarynote
        {"disciplinaryNoteId": 6333186975989760}

        An example of the data is:

        .. code-block:: json

            {
                "studentId": 5,
                "teacherId": 42,
                "classId": 3,
                "subjectId": 21,
                "dateTime": "2000-12-03 10:30",
                "kind": 1,
                "gravity": 5,
                "description": "A little problem with new boy."
            }

/disciplinarynote/{id}
--------

    **GET**

    Return a data block with all details about one disciplinary note, **metadata included**, with all items with all info.
    As class and subject are optional maybe don't be received in some requests.

    Example:

    >>> curl -i -X GET localhost:8003/disciplinarynote/6649846324789248
    {
        "class": {
            "classId": 1,
            "course": 1,
            "level": "ESO",
            "word": "A"
        },
        "createdAt": "2017-03-13T13:28:55.409175",
        "createdBy": 1,
        "dateTime": "2000-12-03T10:30:00",
        "deletedAt": "2017-03-13T13:28:58.011052",
        "deletedBy": 1,
        "description": "A little problem with new boy.",
        "disciplinaryNoteId": 5295247999369216,
        "gravity": 5,
        "kind": 1,
        "student": {
            "name": "Maria",
            "studentId": 1,
            "surname": "adsf"
        },
        "subject": {
            "name": "Prueba",
            "subjectId": 1
        },
        "teacher": {
            "name": "mariano",
            "profileImageUrl": "dfasdfa",
            "surname": "dslk",
            "teacherId": 1
        }
    }

    .. note:: This resource depends of another service (to get extra info about items)

    **DELETE**

    Save in database one. Don't **return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -X DELETE localhost:8003/disciplinary_note/324
    HTTP/1.1 200 OK


    **PUT**

    Update a item in data store. **Don't return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -H "Content-Type: application/json" -X PUT -d @SMS-Back-End/scms/test/disciplinary_note_example_1.json localhost:8003/disciplinarynote/4714705859903488
    HTTP/1.1 200 OK

Code
----

This is the Flask code that implement segment of api use SCM (Students Controls Manager) to do all tasks.
"""

from flask import Blueprint, request
from utils import process_response

import sys
sys.path.append("../")
from scm.scm import DisciplinaryNotesManager

disciplinary_notes_api = Blueprint('disciplinary_notes_api', __name__)


@disciplinary_notes_api.route('/disciplinarynote', methods=['POST'])
def post_disciplinary_note():
    """
    Save a Disciplinary Note in the database.

    :return: A dict with the key of item saved, some as {'disciplinaryNoteId': <int>}
    """
    return process_response(DisciplinaryNotesManager.post_dn(request.get_json()))


@disciplinary_notes_api.route('/disciplinarynote', methods=['GET'])
@disciplinary_notes_api.route('/disciplinarynote/<int:disciplinary_note_id>', methods=['GET'])
def get_disciplinary_note(disciplinary_note_id=None):
    """
    Get a list of disciplinary_notes or a specific disciplinary note from data store.

    :param disciplinary_note_id: Id of dn block.
    :return: A json data block with ac data or a list of them.
    """
    return process_response(DisciplinaryNotesManager.get_dn(disciplinary_note_id))


@disciplinary_notes_api.route('/disciplinarynote/<int:disciplinary_note_id>', methods=['DELETE'])
def delete_disciplinary_note(disciplinary_note_id):
    """
    Do a logic deletion of a disciplinary note in the data store.

    :param disciplinary_note_id: Id of the disciplinary note that will be deleted
    :return: Nothing.
    """
    return process_response(DisciplinaryNotesManager.delete_dn(disciplinary_note_id))


@disciplinary_notes_api.route('/disciplinarynote/<int:disciplinary_note_id>', methods=['PUT'])
def update_disciplinary_note(disciplinary_note_id):
    """
    Update a DN item in the data store.

    :param disciplinary_note_id: Id of the dn that will be updated.
    :return: Nothing.
    """
    return process_response(DisciplinaryNotesManager.update_dn(disciplinary_note_id, request.get_json()))