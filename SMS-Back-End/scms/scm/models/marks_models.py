"""
Mark Model
==========

.. note:: Attention: We don't respect PEP-8 style.
"""
from google.appengine.ext import ndb

####################################
# Mark Data Block DataStore Model #
####################################

# Attention: We don't respect PEP-8 style guide because we use camelCase in the JSON files that
# the apis manage and the conversion to json is directly using the same name used here.


class Enrollment(ndb.Model):
    enrollmentId = ndb.IntegerProperty()
    classId = ndb.IntegerProperty()
    subjectId = ndb.IntegerProperty()
    teacherId = ndb.IntegerProperty()


class Marks(ndb.Model):

    # Mark base
    preFirstEv = ndb.FloatProperty()
    firstEv = ndb.FloatProperty()

    preSecondEv = ndb.FloatProperty()
    secondEv = ndb.FloatProperty()

    thirdEv = ndb.FloatProperty()

    final = ndb.FloatProperty()


class Mark(ndb.Model):

    # Student Identification and properties
    studentId = ndb.IntegerProperty()
    enrollment = ndb.StructuredProperty(Enrollment)

    marks = ndb.StructuredProperty(Marks)

    # Mark Item Metadata
    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()

    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)

    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt = ndb.DateTimeProperty(default=None)

    deleted = ndb.BooleanProperty(default=False)
