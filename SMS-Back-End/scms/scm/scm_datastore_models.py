# -*- coding: utf-8 -*-
"""
Fichero de definición de los modelos de la base de datos, haciendo
uso de los `tipos NDB <https://cloud.google.com/appengine/docs/python/ndb/entity-property-reference>`_ del Cloud DataStore.

https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses

"""

from google.appengine.ext import ndb


class Class(ndb.Model):
    classId = ndb.IntegerProperty()
    word = ndb.StringProperty()
    course = ndb.IntegerProperty()
    level = ndb.StringProperty()


class Subject(ndb.Model):
    subjectId = ndb.IntegerProperty()
    name = ndb.StringProperty()


class Association(ndb.Model):
    associationId = ndb.IntegerProperty()
    classs = ndb.StructuredProperty(Class)
    subject = ndb.StructuredProperty(Subject)


class ACAssociation(ndb.Model):

    associationDataBlockId = ndb.IntegerProperty()
    associationId = ndb.IntegerProperty()
    classs = ndb.StructuredProperty(Class)
    subject = ndb.StructuredProperty(Subject)


class CKS(ndb.Model):

    assistance = ndb.BooleanProperty()
    delay = ndb.IntegerProperty()
    justifiedDelay = ndb.BooleanProperty()
    uniform = ndb.BooleanProperty()


class ACStudent(ndb.Model):

    studentId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()

    control = ndb.StructuredProperty(CKS)


class Student(ndb.Model):
    studentId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()


class Teacher(ndb.Model):
    teacherId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()


##########################################
# Association Data Block DataStore Model #
##########################################
class ADB(ndb.Model):
    """A main model for representing an individual Guestbook entry.

    the association value is necessary, but not teacher and students ( this is optionals).

    """
    association = ndb.StructuredProperty(Association)
    teacher = ndb.StructuredProperty(Teacher)
    students = ndb.StructuredProperty(Student, repeated=True)

    createdBy = ndb.IntegerProperty()
    createdAt = ndb.DateTimeProperty()

    modifiedBy = ndb.IntegerProperty(default=None)
    modifiedAt = ndb.DateTimeProperty(default=None)

    deletedBy = ndb.IntegerProperty(default=None)
    deletedAt =ndb.DateTimeProperty(default=None)

    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def get_adb(cls, association_id):
        key = ndb.Key('ADB', long(association_id))
        query = ADB.query(ADB.key == key)
        return query

    @classmethod
    def get_adbs_for_teacher(cls, teacher_id):
        query = ADB.query(ADB.teacher.teacherId == teacher_id)
        return query

    @classmethod
    def delete(cls, association_id):
        """
        Do a logic deletion of an item, set "deleted = True"
        :param association_id:
        :return:
        """

        key = ndb.Key('ADB', long(association_id))
        item = key.get()

        # If the item exists:
        if item is not None:
            item.deleted = True
            item.put()

        return item


#################################################
# Attendance Control Data Block DataStore Model #
#################################################
class AC(ndb.Model):

    association = ndb.StructuredProperty(ACAssociation)
    teacher = ndb.StructuredProperty(Teacher)
    students = ndb.StructuredProperty(ACStudent, repeated=True)

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