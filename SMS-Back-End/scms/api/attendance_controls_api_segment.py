"""
Attendance Controls
===================

This is the section of API that manage the resources related with this kind of objects.
These specifications must be understanding **like a contract** with the functionality of the service.

/ac
---

    **GET**

    Return all attendance controls realized with minimal info in a json **list**.  In this case only
    the subitems **class**, **subject** and **teacher** will be return populated with info from TDBmS. Students
    is only a int with how many this are.

    Example:

    >>> curl -i -X GET localhost:8003/ac

    An example of response of the resource is:

    .. code-block:: json

        [
            {
                "acId": 4785074604081152,
                "association": {
                    "associationId": 13,
                    "class": {
                        "classId": 1,
                        "course": 1,
                        "level": "ESO",
                        "word": "A"
                    },
                    "subject": {
                        "name": "Prueba",
                        "subjectId": 1
                    }
                },
                "createdAt": "2017-03-12T13:20:23.906080",
                "createdBy": 1,
                "students": 2,
                "teacher": {
                    "name": "mariano",
                    "profileImageUrl": "dfasdfa",
                    "surname": "dslk",
                    "teacherId": 1
                }
            }
        ]

    .. note:: This resource depends of another service (to get extra info about items). *Resource don't parameterizable.*

    **POST**

    Save in database one, return a simple http status code and **id of item stored** as a dictionary with "acId" key.

    Example:

    >>> curl -H "Content-Type: application/json" -X POST -d '...' localhost:8003/association

    Post with example file:

    >>> curl -i -H "Content-Type: application/json" -X POST -d @SMS-Back-End/scms/test/AC_example_1.json localhost:8003/ac
    {"acId": 6333186975989760}j

    An example of the data is:

    .. code-block:: json

        {
          "students": [
            {
              "control": {
                "delay": 0,
                "assistance": true,
                "uniform": true,
                "justifiedDelay": true
              },
              "studentId": 113
            },
            {
              "control": {
                "delay": 0,
                "assistance": true,
                "uniform": true,
                "justifiedDelay": true
              },
              "studentId": 213
            }
          ],
          "teacherId": 23,
          "association": {
            "associationId": 13,
            "classId": 24,
            "subjectId": 17
          }
        }

    .. note:: Normally before to do POSt is necesary get base data block, using **/ac/base/{id}**

/ac/base/{id}
-------------

    **GET**

    Return a data block with the data block that represent the Attendance Control to be showed in the user interface.
    All subitem will returned populated.

    Example:

    >>> curl -i -X GET localhost:8003/ac/base/434

    .. note:: This resource depends of another service. *Resource don't parameterizable.*


/ac/{id}
--------

    **GET**

    Return a data block with all details about one attendance control, **metadata included**.
    In this case all subitems are returned populated with all info necessary to the UI.

    Example:

    >>> curl -i -X GET localhost:8003/ac/5576722976079872
    {
        "acId": 5576722976079872,
        "association": {
            "associationId": 1,
            "class": {
                "classId": 1,
                "course": 1,
                "level": "ESO",
                "word": "A"
            },
            "subject": {
                "name": "Prueba",
                "subjectId": 1
            }
        },
        "createdAt": "2017-03-13T16:16:30.575214",
        "createdBy": 1,
        "students": [
            {
                "control": {
                    "assistance": true,
                    "delay": 0,
                    "justifiedDelay": true,
                    "uniform": true
                },
                "student": {
                    "name": "Juan",
                    "studentId": 2,
                    "surname": "adsf"
                }
            },
            {
                "control": {
                    "assistance": true,
                    "delay": 0,
                    "justifiedDelay": true,
                    "uniform": true
                },
                "student": {
                    "name": "Maria",
                    "studentId": 1,
                    "surname": "adsf"
                }
            }
        ],
        "teacher": {
            "name": "mariano",
            "profileImageUrl": "dfasdfa",
            "surname": "dslk",
            "teacherId": 1
        }
    }



    **DELETE**

    Save in database one. Don't **return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -X DELETE localhost:8003/ac/324
    HTTP/1.1 200 OK


    **PUT**

    Update a item in data store. **Don't return nothing**, you can see operation status in http response **status code**.

    Example:

    >>> curl -i -H "Content-Type: application/json" -X PUT -d @SMS-Back-End/scms/test/AC_example_1.json localhost:8003/ac/4714705859903488
    HTTP/1.1 200 OK


Code
----

This is the Flask code that implement segment of api use SCM (Students Controls Manager) to do all tasks.

"""

from flask import Blueprint, request
from utils import process_response
import sys
sys.path.append("../")
from scm.scm import AttendanceControlsManager

attendance_controls_api = Blueprint('attendance_controls_api', __name__)


@attendance_controls_api.route('/ac', methods=['GET'])
@attendance_controls_api.route('/ac/<int:ac_id>', methods=['GET'])
def get_ac(ac_id=None):
    """
    Return all attendance controls realized with minimal info or a specific with all.

    :param ac_id: Id of the ac that will be returned.
    :return: A json data block with ac data or a list of them.
    """
    return process_response(AttendanceControlsManager.get_ac(ac_id))


@attendance_controls_api.route('/ac/base/<int:ac_id>', methods=['GET'])
def get_ac_base(ac_id):
    """
    Get the Attendance Control Base to the association with id passed in url.

    :param association_id: id of the association saved in TDBmS.
    :return: A json data block with the base to do an ac in the UI.
    """
    return process_response(AttendanceControlsManager.get_ac_base(ac_id))


@attendance_controls_api.route('/ac', methods=['POST'])
def post_ac():
    """
    Save an AC in the data store.

    :return: A dict with the key of item saved, some as {'acId': <int>}
    """
    return process_response(AttendanceControlsManager.post_ac(request.get_json()))


@attendance_controls_api.route('/ac/<int:ac_id>', methods=['DELETE'])
def delete_ac(ac_id):
    """
    Delete an AC ite from data store.

    :param ac_id: Id of the ac that will be deleted.
    :return: Nothing
    """
    return process_response(AttendanceControlsManager.delete_ac(ac_id))


@attendance_controls_api.route('/ac/<int:ac_id>', methods=['PUT'])
def update_ac(ac_id):
    """
    Update a AC item in the data store.

    :param ac_id: Id of the ac that will be updated.
    :return: Nothing
    """
    return process_response(AttendanceControlsManager.update_ac(ac_id, request.get_json()))