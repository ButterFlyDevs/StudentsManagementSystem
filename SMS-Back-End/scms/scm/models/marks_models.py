from google.appengine.ext import ndb

####################################
# Mark Data Block DataStore Model #
####################################

# Attention: We don't respect PEP-8 style guide because we use camelCase in the JSON files that
# the apis manage and the conversion to json is directly using the same name used here.

class Mark(ndb.Model):

    # Student Identification and properties
    studentId = ndb.IntegerProperty()
    enrollmentId = ndb.IntegerProperty()

    # Mark base
    preFirstEv = ndb.IntegerProperty()
    firstEv = ndb.IntegerProperty()

    preSecondEv = ndb.IntegerProperty()
    secondEv = ndb.IntegerProperty()

    thirdEv = ndb.IntegerProperty()

    final = ndb.IntegerProperty()

    # Mark Item Metadata
    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()
    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)
    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt = ndb.DateTimeProperty(default=None)
    deleted = ndb.BooleanProperty(default=False)
