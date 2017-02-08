# -*- coding: utf-8 -*-
"""
Fichero de definición de los modelos de la base de datos, haciendo
uso de los `tipos NDB <https://cloud.google.com/appengine/docs/python/ndb/entity-property-reference>`_ del Cloud DataStore.

https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses

"""

from google.appengine.ext import ndb


class Class(ndb.Model):
    classId = ndb.IntegerProperty()
    classWord = ndb.StringProperty()
    classCourse = ndb.IntegerProperty()
    classLevel = ndb.StringProperty()

class Subject(ndb.Model):
    subjectId = ndb.IntegerProperty()
    subjectName = ndb.StringProperty()

class Association(ndb.Model):
    associationId = ndb.IntegerProperty()
    classs = ndb.StructuredProperty(Class)
    subject = ndb.StructuredProperty(Subject)

class Student(ndb.Model):
    studentId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()

class Teacher(ndb.Model):
    teacherId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()

# Association Data Block
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

