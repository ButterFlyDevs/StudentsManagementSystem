from google.appengine.ext import ndb

################################################
# Disciplinary Note Data Block DataStore Model #
################################################

# Attention: We don't respect PEP-8 style guide because we use camelCase in the JSON files that
# the apis manage and the conversion to json is directly using the same name used here.


class DisciplinaryNote(ndb.Model):

    # Student Identification and date of facts
    studentId = ndb.IntegerProperty()
    studentsIdsRelated = ndb.IntegerProperty(repeated=True)
    date = ndb.DateTimeProperty()

    # Disciplinary Note
    kind = ndb.IntegerProperty()
    gravity = ndb.IntegerProperty()
    description = ndb.StringProperty()

    # Disciplinary Note Item Metadata
    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()
    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)
    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt = ndb.DateTimeProperty(default=None)
    deleted = ndb.BooleanProperty(default=False)
