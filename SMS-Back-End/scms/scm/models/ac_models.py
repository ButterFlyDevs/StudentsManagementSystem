# -*- coding: utf-8 -*-
"""

Attendance Control Model
========================

This model represent the kind of object **Attendance Control**, that is the object used to save the attendance
control of a group of students in a class and in a specific subject.

.. note:: Attention: We don't respect PEP-8 style guide because we use camelCase in the JSON files that the apis manage and the conversion to json is directly using the same name used here.

"""

from google.appengine.ext import ndb


class ACAssociation(ndb.Model):

    associationId = ndb.IntegerProperty()
    classId = ndb.IntegerProperty()
    subjectId = ndb.IntegerProperty()


class CKS(ndb.Model):

    assistance = ndb.BooleanProperty()
    delay = ndb.IntegerProperty()
    justifiedDelay = ndb.BooleanProperty()
    uniform = ndb.BooleanProperty()


class ACStudent(ndb.Model):

    studentId = ndb.IntegerProperty()
    control = ndb.StructuredProperty(CKS)


class AC(ndb.Model):
    """
    Attendance Control Data Block DataStore Model.
    Is the ...
    """

    association = ndb.StructuredProperty(ACAssociation)
    teacherId = ndb.IntegerProperty()
    students = ndb.StructuredProperty(ACStudent, repeated=True)

    # Metadata #

    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()

    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)

    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt = ndb.DateTimeProperty(default=None)

    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def get_ac(cls, ac_id):
        key = ndb.Key('AC', long(ac_id))
        query = AC.query(AC.key == key)
        return query


#################################################
# Record Data Block DataStore Model #
#################################################
class Record(ndb.Model):

    # Student Identification and properties
    studentId = ndb.IntegerProperty()
    # age = ndb.IntegerProperty()

    # CKS Base
    assistance = ndb.BooleanProperty()
    delay = ndb.IntegerProperty()
    justifiedDelay = ndb.BooleanProperty()
    uniform = ndb.BooleanProperty()

    # Related Items Metadata
    associationId = ndb.IntegerProperty()
    subjectId = ndb.IntegerProperty()
    classId = ndb.IntegerProperty()
    teacherId = ndb.IntegerProperty()

    # Time Metadata
    recordDate = ndb.DateTimeProperty()
    recordWeekday = ndb.IntegerProperty()