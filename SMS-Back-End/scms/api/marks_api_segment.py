"""
Marks
=====

This is the section of API that manage the resources related with this kind of objects.

/mark
-----

    **GET**

    Return all marks realized with ALL info in a json **list** plus metadata. All because isn't very heavy.
    If there aren't any item, it will return `204 Not Found Status Code`.

    Example:

    >>> curl -i -X GET localhost:8003/mark
    [
        {
            "createdAt": "2017-03-12T23:12:53.603021",
            "createdBy": 1,
            "enrollment": {
                "classId": 4,
                "enrollmentId": 42,
                "subjectId": 5,
                "teacherId": 8
            },
            "markId": 6016527627190272,
            "marks": {
                "final": null,
                "firstEv": 5,
                "preFirstEv": 3,
                "preSecondEv": 8,
                "secondEv": 9,
                "thirdEv": 10
            },
            "studentId": 5
        }
    ]

    **GET with params**

    It allows request a mark with a enrollmentId identification, as another way to make requests if we don't know
    markId id.

    Example:

    >>> curl -i -X GET localhost:8003/mark?enrollmentId=42

    Any other param aren't available and if item doesn't exists in data store will returned a 404 Not Found error,
    like a normal behaviour.



    **POST**

    Save in database one, return a simple http status code and **id of item stored** as a dictionary with "markId" key.

    Example:

    >>> curl -H "Content-Type: application/json" -X POST -d '...' localhost:8003/association

    Post with example file:

    >>> curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/mark_example_1.json localhost:8003/mark
    {"markId": 5735052650479616}

    An example of the send data is:

    .. code-block:: json

        {
          "studentId": 5,
          "enrollment": {
            "enrollmentId": 42,
            "classId":4,
            "subjectId": 5,
            "teacherId": 8
          },
          "marks":{
            "preFirstEv": 3,
            "firstEv": 5,
            "preSecondEv": 8,
            "secondEv": 9,
            "thirdEv": 10,
            "final": 9
          }
        }

/mark/{id}
-----------

    **GET**

    Return a data block with all details about one mark, **metadata included**.

    Example:

    >>> curl -i -X GET localhost:8003/mark/6649846324789248
    {
        "createdAt": "2017-03-12T23:12:53.603021",
        "createdBy": 1,
        "enrollment": {
            "classId": 4,
            "enrollmentId": 42,
            "subjectId": 5,
            "teacherId": 8
        },
        "markId": 6016527627190272,
        "marks": {
            "final": null,
            "firstEv": 5,
            "preFirstEv": 3,
            "preSecondEv": 8,
            "secondEv": 9,
            "thirdEv": 10
        },
        "studentId": 5
    }

    **DELETE**

    Save in database one. Don't **return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -X DELETE localhost:8003/mark/324
    HTTP/1.1 200 OK


    **PUT**

    Update a item in data store. **Don't return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -H "Content-Type: application/json" -X PUT -d @SMS-Back-End/scms/test/mark_example_1.json localhost:8003/mark/4714705859903488
    HTTP/1.1 200 OK

Code
----

This is the Flask code that implement segment of api use SCM (Students Controls Manager) to do all tasks.

"""

from flask import Blueprint, request
from utils import process_response
import sys
sys.path.append("../")
from scm.scm import MarksManager

marks_api = Blueprint('marks_api', __name__)


@marks_api.route('/mark', methods=['POST'])
def post_mark():
    """
    Save a mark in the database.

    :return: Return HTTP status code and the mark as is saved in the data store.
    """
    return process_response(MarksManager.post_mark(request.get_json()))


@marks_api.route('/mark', methods=['GET'])
@marks_api.route('/mark/<int:mark_id>', methods=['GET'])
def get_mark(mark_id=None):
    """
    Get a list of marks or a specific mark from data store.

    :param mark_id: The id of the mark item to searh in data store.
    :return: A mark object
    """
    print request.args
    return process_response(MarksManager.get_mark(mark_id, request.args))


@marks_api.route('/mark/<int:mark_id>', methods=['DELETE'])
def delete_mark(mark_id):
    """
    Do a logic deletion of a mark in the data store.

    :param mark_id: mark id in data store
    :return: Nothing, normal status code
    """
    return process_response(MarksManager.delete_mark(mark_id))


@marks_api.route('/mark/<int:mark_id>', methods=['PUT'])
def update_mark(mark_id):
    """
    Update a Mark item in the data store.

    :param mark_id: Mark id which will be updated.
    :return: Nothing
    """
    return process_response(MarksManager.update_mark(mark_id, request.get_json()))