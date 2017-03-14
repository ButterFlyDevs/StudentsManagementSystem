"""
Students Control Manager
========================

Give all manager to interact with the different kind of objects saved in the data store.
Is the connector between the API of service and the data store, with a class for each sub api.

.. note:: This manager use the same HTTP status code errors to manage the state of the operations. Getter methods don't be parameterizable.

"""

from termcolor import colored

from models.marks_models import *
from models.ac_models import *
from models.discipline_models import *

import datetime
import pytz


import json
from google.appengine.api import modules
import requests
import requests_toolbelt.adapters.appengine
from google.appengine.ext import ndb

# To can use request lib in GAE.
requests_toolbelt.adapters.appengine.monkeypatch()


def get_item_from_tdbms(kind, id, params):
    """
    Call to TDBmS to get info about a specific item.

    :param kind: Object kind in TDBmS
    :param id: Integer that identify the item there.
    :param params: Attributes that we want receive from service.
    :return: A dict with all info required.
    """

    url = 'http://{}/{}/{}'.format(modules.get_hostname(module='tdbms'), 'entities/'+kind, id)

    if params:
        url += '?params='
        for param in params:
            url += param+','
    url = url[:-1]

    response = requests.get(url)
    status = response.status_code

    if status == 200:
        return json.loads(response.content)
    else:
        return status


def time_now():
    """
    Get actual time with timezone: Europe/Madrid
    :return: Datetime object.
    """
    now = datetime.datetime.utcnow()
    tz = pytz.timezone('Europe/Madrid')
    tzoffset = tz.utcoffset(now)
    mynow = now + tzoffset
    return mynow


class AttendanceControlsManager(object):
    """
    Manage all available interactions with Attendance Control objects in data store.
    """

    @classmethod
    def validate_ac(cls, ac):
        """
        Validate the format of item based of data store model.

        :param ac: Item dict.
        :return: True if format is ok and false in other hand.
        """
        # TODO: Implement.
        return True

    @classmethod
    def get_ac(cls, ac_id=None):
        """
        Get all attendance controls from data store or details of a specific one.
        :param ac_id:
        :return: Standard info dict (with data).

        .. note:: This resource depends of another service to populate some items.
        """

        if ac_id is None:

            query = AC.query()
            attendace_controls = []

            for attendance in query.iter():

                attendance_id = attendance._key.id()
                attendance_dict = attendance.to_dict()

                attendance_dict = dict((k, v) for k, v in attendance_dict.iteritems() if v)

                if attendance_dict.get('deleted', None) is not True:

                    # Students don't be populated (only set the number of items)
                    attendance_dict['students'] = len(attendance_dict['students'])
                    attendance_dict['acId'] = attendance_id

                    # Populating info about TEACHER from TDBMs service.
                    teacher_info = get_item_from_tdbms('teacher', attendance_dict['teacherId'],
                                                       ['name', 'surname', 'profileImageUrl'])
                    del(attendance_dict['teacherId'])
                    attendance_dict['teacher'] = teacher_info

                    # Populating info about SUBJECT from TDBMs service
                    subject_info = get_item_from_tdbms('subject',
                                                       attendance_dict['association']['subjectId'],['name'])
                    del(attendance_dict['association']['subjectId'])
                    attendance_dict['association']['subject']=subject_info

                    # Populating info about CLASS from TDBMs service
                    class_info = get_item_from_tdbms('class',
                                                       attendance_dict['association']['classId'],['course','word', 'level'])
                    del(attendance_dict['association']['classId'])
                    attendance_dict['association']['class']=class_info

                    attendace_controls.append(attendance_dict)

            if len(attendace_controls) != 0:
                return {'status': 200, 'data': attendace_controls, 'log': None}
            else:
                return {'status': 204, 'data': None, 'log': None}

        # The requests is about specific AC item
        else:

            query = AC.get_ac(ac_id)

            item = query.get()

            if item:

                key_id = item._key.id()
                item = item.to_dict()
                # Previous deleting of keys with values to null to reduce the size of response.
                item = dict((k, v) for k, v in item.iteritems() if v)
                item['acId'] = key_id

                if query.count() == 1 and item.get('deleted', None) is not True:

                    # Populating info about TEACHER from TDBMs service.
                    teacher_info = get_item_from_tdbms('teacher', item['teacherId'],
                                                       ['name', 'surname', 'profileImageUrl'])
                    del(item['teacherId'])
                    item['teacher'] = teacher_info

                    # Populating info about CLASS from TDBMs service
                    class_info = get_item_from_tdbms('class', item['association']['classId'],
                                                     ['course', 'word', 'level'])
                    del (item['association']['classId'])
                    item['association']['class'] = class_info

                    # Populating info about SUBJECT from TDBMs service
                    subject_info = get_item_from_tdbms('subject',
                                                       item['association']['subjectId'], ['name'])
                    del (item['association']['subjectId'])
                    item['association']['subject'] = subject_info

                    # Populate all students:
                    students = item['students']
                    populated_students = []
                    for student in students:
                        # Populating info about STUDENT from TDBMs service
                        student_info = get_item_from_tdbms('student',
                                                           student['studentId'], ['name', 'surname', 'profileImageUrl'])
                        del (student['studentId'])
                        student['student'] = student_info

                        populated_students.append(student)

                    item['students'] = populated_students

                    return {'status': 200, 'data': item, 'log': None}
                else:
                    return {'status': 204, 'data': None, 'log': None}

            else:
                return {'status': 404, 'data': None, 'log': 'AC required seem like doesn\'t exists or was deleted.'}

    @classmethod
    def get_ac_base(cls, association_id):
        """
        Get the Attendance Control Base to the association with id passed.
        This service send a request to TDBmS to get all info about this association,
        TDBmS sent this.

        :param association_id: The id of item searched.
        :return: Standard info dict (with data).

        .. note:: This resource depends of another service to populate some items.
        """

        # Definition of basic CKS (Control Kind Specification)
        cks = {"assistance": True,
               "delay": 0,
               "justifiedDelay": None,
               "uniform": True}

        url = 'http://{}/{}/{}'.format(modules.get_hostname(module='tdbms'), 'entities/association', association_id)
        response = requests.get(url)
        status = response.status_code

        # If the call to TDBmS to get association info is correct:
        if status == 200:
            association = json.loads(response.content)

            # Add info about how control must be.
            association['control'] = cks

            return {'status': 200, 'data': association, 'log': None}


        elif status == 204:

            return {'status': status, 'data': None, 'log': None}

    @classmethod
    def post_ac(cls, received_ac):
        """
        Save all info in AC database and extract the records to save in records database.
        :param received_ac: A dict with ac to save.
        :return: Standard info dict with id of item saved, as: {'acId':<int>}
        """

        # 1. First, we must be check that the association passed is correct, it means that it exists
        # in the database and all fields are correct.
        # 2. Before if is correct we save data in AC table.
        #if ac_is_correct:
        if cls.validate_ac(received_ac):

            # Saving the AC object in data store

            association= received_ac['association']
            association = ACAssociation(associationId=association['associationId'],
                                        classId=association['classId'],
                                        subjectId=association['subjectId'])

            students_list = []
            for student in received_ac['students']:

                control = student.get('control', None)
                students_list.append(ACStudent(studentId=student['studentId'],
                                               control=CKS(assistance=control['assistance'],
                                                           delay=control['delay'],
                                                           justifiedDelay=control['justifiedDelay'],
                                                           uniform=control['uniform'])
                                               )
                                     )

            # This field is expected only when the PROVISIONER fill the data store with aleatory data for
            # data analysis or science data purposes (to avoid that all will have the same save date).
            # In the normal case this doesn't exists.
            if received_ac.get('provisionerDateTime',None) is not None:
                date = datetime.datetime.strptime(received_ac['provisionerDateTime'], "%Y-%m-%d %H:%M")

            else:
                date = time_now()

            datastore_ac = AC(association=association,
                              teacherId=received_ac['teacherId'],
                              students=students_list,
                              createdBy=1,
                              createdAt=date)



            ac_key = datastore_ac.put()

            """
            # 3. To end, we extract all records from AC saved and save them in massive records table,
            # that will be used by Analysis Sub System in other processes.

            for student in students:

                control = student.get('control', None)
                if control:
                    record = Record(studentId=student['studentId'],
                                    assistance=control['assistance'], delay=control['delay'],
                                    justifiedDelay=control['justifiedDelay'], uniform=control['uniform'],
                                    associationId=received_ac['association']['associationId'],
                                    subjectId=subject['subjectId'],
                                    classId=classs['classId'],
                                    teacherId=teacher['teacherId'],
                                    recordDate=date, recordWeekday=date.weekday())

                    key = record.put()
            """

            return {'status': 200, 'data': {'acId':ac_key.id()}}

        # If format isn't correct.
        else:
            return {'status': 400, 'data': None, 'log': None}

    @classmethod
    def delete_ac(cls, ac_id):
        """
        Delete an item.
        :param ac_id: Id of item that will be deleted.
        :return: Standard info dict (without data, only status code).
        """

        key = ndb.Key('AC', long(ac_id))
        item = key.get()

        # Check if the item doesn't exists becuause never was create or because was logically deleted:
        if item is not None and item.to_dict().get('deleted',None) is not True:  # If exists:

            item.deletedAt = time_now()
            item.deletedBy = 1
            item.deleted = True
            item.put()

            return {'status': 200, 'data': None, 'log': None}

        else:  # If it doesn't exists:
            return {'status': 404, 'data': None, 'log': 'AC required seem like doesn\'t exists or was deleted.'}

    @classmethod
    def update_ac(cls, ac_id, received_ac):
        """
        Update an item in data store.
        :param ac_id: The if of item to update.
        :param received_ac: A dict with data of ac to update.
        :return: Standard info dict (without data, only status code).
        """
        key = ndb.Key('AC', long(ac_id))
        item = key.get()

        if item:

            if cls.validate_ac(received_ac):

                association = received_ac['association']
                association = ACAssociation(associationId=association['associationId'],
                                            classId=association['classId'],
                                            subjectId=association['subjectId'])

                students_list = []
                for student in received_ac['students']:
                    control = student.get('control', None)
                    students_list.append(ACStudent(studentId=student['studentId'],
                                                   control=CKS(assistance=control['assistance'],
                                                               delay=control['delay'],
                                                               justifiedDelay=control['justifiedDelay'],
                                                               uniform=control['uniform'])
                                                   )
                                         )

                item.association = association
                item.teacherId = received_ac['teacherId']
                item.students = students_list

                item.modifiedAt = time_now()
                item.modifiedBy = 1

                item.put()

                return {'status': 200}

            # If format isn't correct.
            else:
                return {'status': 400, 'data': None, 'log': None}

        else:
            return {'status': 404, 'data': None, 'log': 'AC required seem like doesn\'t exists or was deleted.'}


class MarksManager(object):
    """
    Manage all available interactions with Mark objects in data store.
    """

    @classmethod
    def validate_mark(cls, mark):
        """
        Validate the format of item based of data store model.

        :param mark: Item dict.
        :return: True if format is ok and false in other hand.
        """
        # TODO: Implement.
        return True

    @classmethod
    def get_mark(cls, mark_id, args):
        """
        Return a mark or a list of them from data store.
        :param mark_id: Id of mark that will be returned.
        :return: Standard info dict (maybe with data and status code).
        """

        # If isn't passed mark_id is requests all marks from the data store.
        enrollmentId = None
        if mark_id is None:

            if args:
                enrollmentId = args.get('enrollmentId', None)
                if enrollmentId:
                    # Query without params: the simplest way to get all items.
                    query = Mark.query(Mark.enrollment.enrollmentId == int(enrollmentId))
                else:
                    return {'status': 400, 'data': None, 'log': 'Only param available is enrollmentId as /?enrollmentId=<int>'}


            else:
                query = Mark.query()

            marks = []  # Used to return all marks at end.

            for mark in query.iter():

                # Extract the key and the data (dict format) from the mark
                key_id = mark._key.id()
                dict_tmp = mark.to_dict()

                # Better if we delete all useless keys with None as value to simplify the response.
                dict_tmp = dict((k, v) for k, v in dict_tmp.iteritems() if v)

                # If the item hasn't deleted is added to marks list
                if dict_tmp.get('deleted', None) is not True:
                    dict_tmp['markId'] = key_id
                    marks.append(dict_tmp)

            if len(marks) == 0:
                if enrollmentId:
                    return {'status': 404, 'data': None, 'log': None}
                else:
                    return {'status': 204, 'data': None, 'log': None}
            else:

                if len(marks) == 1 and  mark_id is not None:
                    marks = marks[0]

                return {'status': 200, 'data': marks, 'log': None}

        else:

            key = ndb.Key('Mark', long(mark_id))

            mark = Mark.query(Mark.key == key, Mark.deleted == False).get()

            if mark:

                mark_id = mark._key.id()

                # Simplify
                mark = dict((k, v) for k, v in mark.to_dict().iteritems() if v)
                mark['markId'] = mark_id

                return {'status': 200, 'data': mark, 'log': None}

            else:

                return {'status': 404, 'data': None, 'log': None}

    @classmethod
    def post_mark(cls, mark):
        """
        Save a mark item in data store.
        :param mark: A dict with item data.
        :return: Standard info dict with id of item saved, as: {'markId':<int>}
        """

        # If mark has the required format:
        if cls.validate_mark(mark):

            print colored('Posted mark')
            print colored(mark, 'red')

            # Is created the object
            enrollment = mark['enrollment']
            marks = mark['marks']
            mark_to_save = Mark(studentId = mark.get('studentId'),
                                enrollment = Enrollment(enrollmentId = enrollment['enrollmentId'],
                                                        classId = enrollment['classId'],
                                                        subjectId = enrollment['subjectId'],
                                                        teacherId = enrollment['teacherId']),
                                marks = Marks(preFirstEv=marks.get('preFirstEv', None),
                                              firstEv=marks.get('firstEv', None),
                                              preSecondEv=marks.get('preSecondEv', None),
                                              secondEv=marks.get('secondEv', None),
                                              thirdEv=marks.get('thirdEv', None),
                                              final=marks.get('final', None)),
                                createdBy=1, createdAt=time_now())

            # And save using himself
            key = mark_to_save.put()

            return {'status': 200, 'data': {'markId': key.id()}}

        # If format isn't correct.
        else:
            return {'status': 400, 'data': None, 'log': None}

    @classmethod
    def update_mark(cls, mark_id, received_mark):
        """
        Update a mark item of data store.
        :param mark_id: Id of the item that will be updated.
        :param received_mark: Dict with item data.
        :return: Standard info dict (without data, only status code)
        """

        key = ndb.Key('Mark', long(mark_id))
        item = key.get()

        if item:

            if cls.validate_mark(received_mark):

                print colored('Posted mark')
                print colored(received_mark, 'red')

                # Is created the object
                enrollment = received_mark['enrollment']
                marks = received_mark['marks']

                item.studentId = received_mark.get('studentId')
                item.enrollment = Enrollment(enrollmentId=enrollment['enrollmentId'],
                                             classId=enrollment['classId'],
                                             subjectId=enrollment['subjectId'],
                                             teacherId=enrollment['teacherId'])
                item.marks = Marks(preFirstEv=marks.get('preFirstEv', None),
                                   firstEv=marks.get('firstEv', None),
                                   preSecondEv=marks.get('preSecondEv', None),
                                   secondEv=marks.get('secondEv', None),
                                   thirdEv=marks.get('thirdEv', None),
                                   final=marks.get('final',None))

                item.modifiedAt = time_now()
                item.modifiedBy = 1

                item.put()

                return {'status': 200}

            # If format isn't correct.
            else:
                return {'status': 400, 'data': None, 'log': None}
        else:
            return {'status': 404, 'data': None, 'log': 'Mark required seem like doesn\'t exists or was deleted.'}

    @classmethod
    def delete_mark(cls, mark_id):
        """
        Delete an item.
        :param mark_id: Id of item that will be deleted.
        :return: Standard info dict (without data, only status code).
        """

        key = ndb.Key('Mark', long(mark_id))
        item = key.get()

        # Check if the item doesn't exists becuause never was create or because was logically deleted:
        if item is not None and item.to_dict().get('deleted',None) is not True:  # If exists:

            item.deletedAt = time_now()
            item.deletedBy = 1
            item.deleted = True
            item.put()

            return {'status': 200, 'data': None, 'log': None}

        else:  # If it doesn't exists:
            return {'status': 404, 'data': None, 'log': 'Mark required seem like doesn\'t exists or was deleted.'}


class DisciplinaryNotesManager(object):

    @classmethod
    def validate_dn(cls, disciplinary_note):
        """
        Validate the format of item based of data store model.

        :param disciplinary_note: Item dict.
        :return: True if format is ok and false in other hand.
        """
        # TODO: Implement.
        return True

    @classmethod
    def get_dn(cls, disciplinary_note_id):
        """
        Get all disciplinary notes with a specific params o with all or a specific dNote with
        all params.

        Params only can be used when the requirements if to get all dNotes (note_id = None)

        :param disciplinary_note_id:
        :param params:
        :return: An array of items, empty if hasn't any ([]).
        """

        # If isn't passed disciplinary_note_id is requests all marks from the data store (it will don't populate)
        if disciplinary_note_id is None:

            # Query without params: the simplest way to get all items.
            query = DisciplinaryNote.query()

            disciplinary_notes = []  # Used to return all disciplinary notes at end.

            for disciplinary_note in query.iter():

                # Extract the key and the data (dict format) from the disciplinary_note
                key_id = disciplinary_note._key.id()
                dict_tmp = disciplinary_note.to_dict()

                # Better if we delete all useless keys with None as value to simplify the response.
                dict_tmp = dict((k, v) for k, v in dict_tmp.iteritems() if v)

                # If the item hasn't deleted is added to disciplinary notes list
                if dict_tmp.get('deleted', None) is not True:
                    dict_tmp['disciplinaryNoteId'] = key_id

                    disciplinary_notes.append(dict_tmp)

            if len(disciplinary_notes) == 0:
                return {'status': 204, 'data': None, 'log': None}
            else:
                return {'status': 200, 'data': disciplinary_notes, 'log': None}

        else:

            key = ndb.Key('DisciplinaryNote', long(disciplinary_note_id))

            disciplinary_note = DisciplinaryNote.query(DisciplinaryNote.key == key, DisciplinaryNote.deleted == False).get()

            if disciplinary_note:

                disciplinary_note_id = disciplinary_note._key.id()

                # Simplify
                disciplinary_note = dict((k, v) for k, v in disciplinary_note.to_dict().iteritems() if v)
                disciplinary_note['disciplinaryNoteId'] = disciplinary_note_id


                # Populating items

                # Populating info about STUDENT from TDBMs service
                student = get_item_from_tdbms('student',
                                              disciplinary_note.get('studentId'), ['name', 'surname', 'profileImageUrl'])

                # Populating info about TEACHER from TDBMs service
                teacher = get_item_from_tdbms('teacher',
                                              disciplinary_note.get('teacherId'), ['name', 'surname', 'profileImageUrl'])

                del (disciplinary_note['studentId'])
                disciplinary_note['student'] = student

                del (disciplinary_note['teacherId'])
                disciplinary_note['teacher'] = teacher

                # If there are subject, populate also:
                if disciplinary_note.get('subjectId', None) is not None:
                    # Populating info about SUBJECT from TDBMs service
                    subject = get_item_from_tdbms('subject', disciplinary_note.get('subjectId'),['name'])
                    del (disciplinary_note['subjectId'])
                    disciplinary_note['subject'] = subject

                # If there are class, populate also:
                if disciplinary_note.get('classId', None) is not None:
                    # Populating info about CLASS from TDBMs service
                    class_item = get_item_from_tdbms('class', disciplinary_note.get('classId'), ['course','word','level'])
                    del (disciplinary_note['classId'])
                    disciplinary_note['class'] = class_item

                return {'status': 200, 'data': disciplinary_note, 'log': None}

            else:

                return {'status': 404, 'data': None, 'log': None}

    @classmethod
    def post_dn(cls, disciplinary_note):

        # If disciplinary note has the required format:
        if cls.validate_dn(disciplinary_note):

            # Is created the object
            dn_to_save = DisciplinaryNote(
                studentId=disciplinary_note.get('studentId'),
                teacherId=disciplinary_note.get('teacherId'),
                classId=disciplinary_note.get('classId'),
                subjectId=disciplinary_note.get('subjectId'),
                dateTime=datetime.datetime.strptime(disciplinary_note.get('dateTime'),"%Y-%m-%d %H:%M"),
                kind=disciplinary_note.get('kind'), gravity=disciplinary_note.get('gravity'),
                description=disciplinary_note.get('description'), createdBy=1, createdAt=time_now())

            # And save using himself
            key = dn_to_save.put()

            return {'status': 200, 'data': {'disciplinaryNoteId': key.id()}}

        # If format isn't correct.
        else:
            return {'status': 400, 'data': None, 'log': None}

    @classmethod
    def update_dn(cls, dn_id, disciplinary_note):

        key = ndb.Key('DisciplinaryNote', long(dn_id))
        item = key.get()

        if item:

            if cls.validate_dn(disciplinary_note):

                # The object is rewrite.
                item.studentId = disciplinary_note['studentId']
                item.teacherId = disciplinary_note['teacherId']
                item.classId = disciplinary_note.get('classId', None)
                item.subjectId = disciplinary_note.get('subjectId', None)
                item.dateTime = datetime.datetime.strptime(disciplinary_note.get('dateTime'),"%Y-%m-%d %H:%M")
                item.kind = disciplinary_note['kind']
                item.gravity = disciplinary_note['gravity']
                item.description = disciplinary_note['description']

                item.modifiedAt = time_now()
                item.modifiedBy = 1

                item.put()

                return {'status': 200}

            # If format isn't correct.
            else:
                return {'status': 400, 'data': None, 'log': None}
        else:
            return {'status': 404, 'data': None, 'log': 'Disciplinary Note required seem like doesn\'t exists or was deleted.'}

    @classmethod
    def delete_dn(cls, disciplinary_note):

        key = ndb.Key('DisciplinaryNote', long(disciplinary_note))
        item = key.get()

        # Check if the item doesn't exists because never was create or because was logically deleted:
        if item is not None and item.to_dict().get('deleted',None) is not True:  # If exists:

            item.deletedAt = time_now()
            item.deletedBy = 1
            item.deleted = True
            item.put()

            return {'status': 200, 'data': None, 'log': None}

        else:  # If it doesn't exists:
            return {'status': 404, 'data': None, 'log': 'Disciplinary Note required seem like doesn\'t exists or was deleted.'}