"""
Disciplinary Note Model
=======================

.. note:: Attention: We don't respect PEP-8 style.
"""
from google.appengine.ext import ndb

################################################
# Disciplinary Note Data Block DataStore Model #
################################################

# Attention: We don't respect PEP-8 style guide because we use camelCase in the JSON files that
# the api manage and the conversion to json is directly using the same name used here.


class OptionItem(ndb.Model):
    id = ndb.IntegerProperty()
    meaning = ndb.StringProperty()


# This is a singleton MODEL
class DNOptions(ndb.Model):
    kinds = ndb.StructuredProperty(OptionItem, repeated=True)
    gravities = ndb.StructuredProperty(OptionItem, repeated=True)
    modifiedBy = ndb.IntegerProperty()
    modifiedAt = ndb.DateTimeProperty()


class DisciplinaryNote(ndb.Model):
    """
    Model of a disciplinary note. We save only the id of students and teacher. One disciplinary note
    is done over a student and maybe done in a class while a subject is impart, but maybe don't. Because
    of this this attributes can be empty. We don't save enrollmentId, we prefer save directly class and
    subject references.
    """

    # Related academic info.
    studentId = ndb.IntegerProperty()
    teacherId = ndb.IntegerProperty()
    classId = ndb.IntegerProperty()
    subjectId = ndb.IntegerProperty()

    # Disciplinary Note
    kind = ndb.IntegerProperty()
    gravity = ndb.IntegerProperty()
    description = ndb.StringProperty()
    dateTime = ndb.DateTimeProperty()

    # Item Metadata
    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()
    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)
    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt = ndb.DateTimeProperty(default=None)
    deleted = ndb.BooleanProperty(default=False)