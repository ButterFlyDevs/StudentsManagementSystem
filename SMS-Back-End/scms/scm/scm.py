############################
# Students Control Manager #
############################

# NOTICE #

# This mService uses the same error status code that HTML to try if this way is clearer that use a own error
# code numbers. This way is used only here.

from termcolor import colored

from models.marks_models import *
from models.ac_models import *
from models.discipline_models import *

import datetime
import pytz
import copy


from flask import Flask, Response

import json
from google.appengine.api import modules

import requests
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

from google.appengine.ext import ndb

import json




def check_association_data_block(data_block):
    """

    :param data_block:
    :return: {'status': int , 'log': string }
    """

    log = ''
    its_ok = True

    association = data_block.get('association', None)

    # Check if the association key is in the dict
    if association is None:

        log = '\'association\' key fault.'
        return {'log': log}

    else:

        if type(association) is not dict:
            log = '\'association\' must be a dictionary'
            return {'log': log}

        if association.get('associationId', None) is None:
            log = '\'associationId\' id fault.'
            return {'log': log}

        _class = association.get('class', None)
        subject = association.get('subject', None)

        if _class is None:
            log = '\'class\' key fault inside association dict.'
            return {'log': log}

        for val in [['classId', int], ['word', unicode], ['level', unicode], ['course', int]]:
            item = _class.get(val[0], None)
            if item is None:
                return {'log': '\'{}\' key fault in class dict'.format(val)}

            if type(item) is not val[1]:
                return {'log': 'Incorrect type in \'{0}\' key. It must be a {1} '.format(val[0], val[1])}

        if subject is None:
            log = '\'subject\' key fault inside association dict.'
            return {'log': log}

        for val in ['subjectId', 'name']:
            if subject.get(val, None) is None:
                return {'log': '\'{}\' key fault in subject dict'.format(val)}

        # If any of last cases appear:
        return {'status': 1}


    teacher = data_block.get('teacher', None)


def time_now():
    now = datetime.datetime.utcnow()
    tz = pytz.timezone('Europe/Madrid')
    tzoffset = tz.utcoffset(now)
    mynow = now + tzoffset
    return mynow

def get_schema(data_model):

    elements = []

    properties = ADB.__dict__.get('_properties')
    print colored(properties, 'blue')

    for k, v in properties.iteritems():
        print type(v)
        v = str(v)

        elements.append({k: v})

    return elements

class AssociationManager:
    """
    Standard response data block:
        A dict with three fields, {'status': int,  'log' string, 'data': data }
    """

    @classmethod
    def post(cls, data_block):
        """
        Insert a kind of item "Association Data Block" in the database from an association datablock .
        :param data_block:
        :return: Standard response data block. See above.
        """

        # Checking the format of the data_block received.
        check = check_association_data_block(data_block)

        if check.get('status', None) is 1:

            classs = data_block['association']['class']
            subject = data_block['association']['subject']
            teacher = data_block['teacher']
            students = data_block['students']

            classs = Class(classId=classs['classId'],
                           word=classs['word'],
                           course=classs['course'],
                           level=classs['level'])
            subject = Subject(subjectId=subject['subjectId'], name=subject['name'])

            asso = Association(associationId=data_block['association']['associationId'], classs=classs, subject=subject)

            teacher = Teacher(teacherId=teacher['teacherId'], name=teacher['name'], surname=teacher.get('surname', None))
            students_list = []
            # Optional values must be extracted with ".get()" instead of "[]"
            for student in students:
                students_list.append(Student(studentId=student['studentId'], name=student['name'], surname=student.get('surname', None)))

            adb = ADB(association=asso,
                      teacher=teacher,
                      students=students_list,
                      createdBy=1,
                      createdAt=time_now())

            # put() returns a key object.
            key = adb.put()

            return {'status': 200, 'log': None, 'data': {'key':key.id(), 'kind': key.kind()}}

        else:
            return {'status': 400, 'log': 'Bad format', 'data': None}

    @classmethod
    def get(cls, association_id = None, teacher_id = None):
        """
        Return all associations in scms database (in a simple-resume version), all associations by teacher name
        or all info about specific, id passed.

        get() return all in *resumed version*
        get(id=n) return all info (plus complete list of students) about association with id = n
        get(teacher=t) return all associations *resumed version* for teacher with id = t

        ** Resumed version is differentiated according to instead of have a list of students
        the key students is a n with the number of this and not their info.

        :return: Standard response data block. See above.

        """
        # https://cloud.google.com/appengine/docs/python/datastore/modelclass#Model_all

        if association_id and teacher_id is None:


            query = ADB.get_adb(association_id)

            item = query.get()

            if item:

                key_id = item._key.id()
                item = item.to_dict()
                # Previous deleting of keys with values to null to reduce the size of response.
                item = dict((k, v) for k, v in item.iteritems() if v)
                item['scsmAssociationId'] = key_id

                if query.count() == 1 and item.get('deleted', None) is not True:
                    return {'status': 200, 'data': item, 'log': None}
                else:
                    return {'status': 204, 'data': None, 'log': None}

            else:
                return {'status': 204, 'data': None, 'log': None}

        elif teacher_id and association_id is None:

            query = ADB.get_adbs_for_teacher(teacher_id)
            print colored(query, 'red')
            if query.count() != 0:
                asso_list = []

                for item in query:

                    tmp_item = dict((k, v) for k, v in item.to_dict().iteritems() if v)

                    if tmp_item.get('deleted', None) is not True:

                        if tmp_item.get('students', None):
                            tmp_item['students'] = len(tmp_item['students'])

                        tmp_item['scmsAssociationId'] = item._key.id()

                        asso_list.append(tmp_item)

                return {'status': 200, 'data': asso_list, 'log': None}
            else:
                return {'status': 204, 'data': None, 'log': None}

        elif not association_id and not teacher_id:

            q = ADB.query()
            items = []

            for result in q.iter():
                dict_tmp = result.to_dict()

                dict_tmp = dict((k, v) for k, v in dict_tmp.iteritems() if v)

                if dict_tmp.get('deleted', None) is not True:

                    dict_tmp['scmsAssociationId'] = result._key.id()
                    items.append(dict_tmp)

            if len(items) == 0:
                return {'status': 204, 'data': None, 'log': None}
            else:
                return {'status': 200, 'data': items, 'log': None}

    @classmethod
    def get_association_schema(cls):
        return {'status': 200, 'data': get_schema(ADB), 'log': None}

    @classmethod
    def delete(cls, association_id):
        """
        Delete an association data block in the database.
        :param association_id:
        :return: Standard response data block. See above.
        """
        item = ADB.delete(association_id)
        if item:
            return {'status': 1, 'data': None, 'log': None}
        else:
            return {'status': -1, 'data': None, 'log': None}

    @classmethod
    def put(cls, association_id, data_block):
        """
        Upload an association
        :param association_id:
        :param data_block:
        :return: Standard response data block. See above.
        """

        check = check_association_data_block(data_block)

        if check.get('status', None) is 1:


            query = ADB.get_adb(association_id)

            item = query.get()

            if item is not None:

                json_item = item.to_dict()
                print json_item
                if json_item.get('deleted', None) is True:
                    return {'status': -1, 'data': None, 'log': None}

                else:
                    # If the item exists and is not logic deleted:

                    # We change the values:

                    """
                    Class and subject, in general association object is necesary but the data_block maybe
                    don't have teacher and students.
                    """
                    classs = data_block['association']['class']
                    subject = data_block['association']['subject']
                    teacher = data_block.get('teacher',None)
                    students = data_block.get('students',None)

                    classs = Class(classId=classs['classId'],
                                   classWord=classs['classWord'],
                                   classCourse=classs['classCourse'],
                                   classLevel='Basic')
                    subject = Subject(subjectId=subject['subjectId'], subjectName=subject['subjectName'])

                    asso = Association(associationId=data_block['association']['associationId'], classs=classs,
                                       subject=subject)
                    if teacher:
                        teacher = Teacher(teacherId=teacher['teacherId'], name=teacher['teacherName'],
                                          surname=teacher.get('teacherSurname', None))

                    students_list = []
                    if students:
                        for student in students:
                            students_list.append(Student(studentId=student['studentId'],
                                                         name=student['studentName'],
                                                         surname=student.get('studentSurname')))
                    # Updating values
                    item.association = asso
                    item.teacher = teacher
                    item.students = students_list

                    # Metadata values:
                    item.modifiedBy = 1
                    item.modifiedAt = time_now()

                    # Saving:
                    item.put()

                    # Get the value modified:
                    query = ADB.get_adb(association_id)

                    modified_item = query.get()
                    modified_item = dict((k, v) for k, v in modified_item.to_dict().iteritems() if v)

                    if modified_item:

                        return {'status': 1, 'data': modified_item, 'log': None}

            else:
                return {'status': -1, 'data': None, 'log': None}


        else:
            return {'status': -1, 'data': None, 'log': check.get('log', None)}

    @classmethod
    def updateAssociations(cls, n):
        print 'updateASSociaton'+str(n)

        url = 'http://{}/{}/{}'.format(modules.get_hostname(module='tdbms'), 'entities/association', n)
        response = requests.get(url)
        data = json.loads(response.content)
        status = response.status_code

        # If the call to TDBmS to get association info is correct:
        if status == 200:

            # Try to save the association received in our database. [TDBmS] --> [SCmS]
            response = cls.post(data)

            """
            If we received a 400 error from post method is because the data received from the TDBmS is incorrect or with
            bad format:
            ## 400 Bad Request. The request could not be understood by the server due to malformed syntax. ##
            We translate this internal error in the communication between microservices in 500 Internal Error Server
            with a simple explanation.
            """

            if response['status'] == 400:
                return {'status': 500, 'data': None, 'log': 'Communication between microservices failed! Maybe bad format.'}

            if response['status'] == 200:
                return response


class AttendanceControlsManager:

    @classmethod
    def get_ac(cls, ac_id=None):
        """
        Get all attendance controls from data store or details of specific.
        :param ac_id:
        :return:
        """

        if ac_id is None:

            query = AC.query()
            attendace_controls = []

            for attendance in query.iter():

                attendance_id = attendance._key.id()
                attendance_dict = attendance.to_dict()

                attendance_dict = dict((k, v) for k, v in attendance_dict.iteritems() if v)

                if attendance_dict.get('deleted', None) is not True:
                    attendance_dict['students'] = len(attendance_dict['students'])
                    attendace_controls.append(attendance_dict)
                    attendance_dict['acId'] = attendance_id

            if len(attendace_controls) != 0:
                return {'status': 200, 'data': attendace_controls, 'log': None}
            else:
                return {'status': 204, 'data': None, 'log': None}

        else:

            query = AC.get_ac(ac_id)

            item = query.get()

            if item:

                key_id = item._key.id()
                item = item.to_dict()
                # Previous deleting of keys with values to null to reduce the size of response.
                item = dict((k, v) for k, v in item.iteritems() if v)
                item['acId'] = key_id
                item['association']['class'] = item['association'].pop('classs')

                if query.count() == 1 and item.get('deleted', None) is not True:
                    return {'status': 200, 'data': item, 'log': None}
                else:
                    return {'status': 204, 'data': None, 'log': None}

            else:
                return {'status': 204, 'data': None, 'log': None}

    @classmethod
    def get_ac_base(cls, association_id):
        """
        Get the Attendance Control Base to the association with id passed
        :param association_id:
        :return:
        """



        # Definition of basic CKS (Control Kind Specification)
        cks = {"assistance": True,
               "delay": 0,
               "justifiedDelay": None,
               "uniform": True}

        # 1. First, we extract the association data block related.

        """
        Second way: WHEN WE HAVE A INTERMEDIE DATABASE AVAILABLE
        query = ADB.get_adb(association_id)

        item = query.get()
        print colored(item, 'blue')
        if not item:
            print 'NO HAY ASOCIACION, La BUSCO'
            response = Association_Manager.updateAssociations(association_id)

            if response['status'] == 500:
                print colored(response, 'red')
                return response

            if response['status'] == 200:
                print 'OK'

        item_id = item._key.id()

        item = item.to_dict()
        item = dict((k, v) for k, v in item.iteritems() if v)
        """


        """
        Like a first approach we search the association directly from TDBmS
        """

        url = 'http://{}/{}/{}'.format(modules.get_hostname(module='tdbms'), 'entities/association', association_id)
        response = requests.get(url)
        status = response.status_code



        # If the call to TDBmS to get association info is correct:
        if status == 200:
            association = json.loads(response.content)
            print colored('Association from TDBmS', 'red')
            print colored(json.dumps(association, indent=2), 'red')

            # Check if the info received has the correct format.
            check = check_association_data_block(association)

            if check['status'] == 1:

                # 2. After, We add cks to each student.
                for student in association['students']:
                    student['control'] = cks

                return {'status': 200, 'data': association, 'log': None}

            else:
                return {'status': 400, 'data': None, 'log': None}

        elif status == 204:
            print status
            return {'status': status, 'data': None, 'log': None}

    @classmethod
    def post_ac(cls, received_ac):
        """
        Save all info in AC database and extract the records to save in records database.
        :param received_ac:
        :return:
        """

        print colored(received_ac, 'blue')
        print colored('-------', 'red')

        """
        # 1. First, we must be check that the association passed is correct, it means that it exists
        # in the database and all fields are correct.

        ac_is_correct = True

        association = received_ac.get('association', None)
        ADB_id = association.get('associationDataBlockId', None)
        del received_ac['association']['associationDataBlockId']

        query = ADB.get_adb(ADB_id)

        adb = query.get()

        item_id = adb._key.id()

        adb = adb.to_dict()
        adb = dict((k, v) for k, v in adb.iteritems() if v)

        print colored(adb, 'blue')
        print colored('-------', 'red')


        # The id
        if item_id != ADB_id:
            ac_is_correct = False
        else:
            print 'item_id correct'

        # Correct the name of class from the database.
        adb['association']['class'] = adb['association'].pop('classs')


        # Association Check
        if received_ac['association'] != adb['association']:
            ac_is_correct = False
            print 'association incorrect'
            print received_ac['association']
            print adb['association']
        else:
            print 'association correct'

        # Teacher Check
        if received_ac['teacher'] != adb['teacher']:
            ac_is_correct = False

        # Students Check
        print colored(received_ac['students'], 'red')

        ac_students = copy.deepcopy(received_ac['students'])

        for student in ac_students:
            del student['control']

        print colored(received_ac['students'], 'green')

        item_students = adb['students']

        if ac_students != item_students:
            ac_is_correct = False
        else:
            print 'FALSE'

        """
        # 2. Before if is correct we save data in AC table.

        #if ac_is_correct:
        if True:

            # Saving the AC object in data store

            classs = received_ac['association']['class']
            datastore_classs = Class(classId=classs['classId'], word=classs['word'], course=classs['course'], level=classs['level'])

            subject = received_ac['association']['subject']
            datastore_subject = Subject(subjectId=subject['subjectId'], name=subject['name'])

            asso = ACAssociation(associationDataBlockId=None, associationId=received_ac['association']['associationId'],
                                 classs=datastore_classs, subject=datastore_subject)

            teachers = received_ac['teachers']
            teachers_list = []
            for teacher in teachers:
                teachers_list.append(Teacher(teacherId=teacher['teacherId'], name=teacher['name'], surname=teacher.get('surname', None)))

            students = received_ac['students']

            students_list = []


            for student in students:

                control = student.get('control', None)

                if control['delay'] != None:
                    control['delay'] = int(control['delay'])

                if control:
                    control_tmp = CKS(assistance=control['assistance'], delay=control['delay'],
                                      justifiedDelay=control['justifiedDelay'], uniform=control['uniform'])

                    students_list.append(ACStudent(studentId=student['studentId'], name=student['name'],
                                                   surname=student.get('surname'), control=control_tmp))

            if received_ac.get('provisionerDateTime',None) is not None:
                date = datetime.datetime.strptime(received_ac['provisionerDateTime'], "%Y-%m-%d %H:%M")

            else:
                date = time_now()

            datastore_ac = AC(association=asso,
                      teachers=teachers_list,
                      students=students_list,
                      createdBy=1,
                      createdAt=date)

            ac_key = datastore_ac.put()

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

            return {'status': 200}

        else:
            return {'status': 400, 'data': None, 'log': None}


class MarksManager:

    @classmethod
    def mark_format_is_ok(self, mark):
        return True

    @classmethod
    def get(cls, mark_id):

        # If isn't passed mark_id is requests all marks from the data store.
        if mark_id is None:

            # Query without params: the simplest way to get all items.
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
                return {'status': 204, 'data': None, 'log': None}
            else:
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
    def post(cls, mark):

        # If mark has the required format:
        if cls.mark_format_is_ok(mark):

            # Is created the object
            mark_to_save = Mark(studentId = mark.get('studentId'), enrollmentId = mark.get('enrollmentId'),
                                preFirstEv = mark.get('preFirstEv', None),firstEv = mark.get('firstEv', None),
                                preSecondEv = mark.get('preSecondEv', None),secondEv = mark.get('secondEv', None),
                                thirdEv = mark.get('thirdEv', None),
                                final = mark.get('final',None),
                                createdBy=1, createdAt=time_now())

            # And save using himself
            key = mark_to_save.put()
            mark_saved = key.get().to_dict()
            mark_saved = dict((k, v) for k, v in mark_saved.iteritems() if v)
            mark_saved['markId'] = key.id()

            return {'status': 200, 'log': None, 'data': mark_saved}

    @classmethod
    def put(cls, mark):
        pass

    @classmethod
    def delete(cls, mark_id):

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


class DisciplinaryNotesManager:

    @classmethod
    def disciplinary_notes_format_is_ok(self, disciplinary_note):
        return True

    @classmethod
    def get(cls, disciplinary_note_id):

        # If isn't passed disciplinary_note_id is requests all marks from the data store.
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

                return {'status': 200, 'data': disciplinary_note, 'log': None}

            else:

                return {'status': 404, 'data': None, 'log': None}

    @classmethod
    def post(cls, disciplinary_note):

        # If disciplinary note has the required format:
        if cls.disciplinary_notes_format_is_ok(disciplinary_note):

            # Is created the object
            dn_to_save = DisciplinaryNote(studentId=disciplinary_note.get('studentId'),
                              studentsIdsRelated=disciplinary_note.get('studentsIdsRelated'),
                              date=datetime.datetime.strptime(disciplinary_note.get('date'),"%Y-%m-%d %H:%M"),
                              kind=disciplinary_note.get('kind'),
                              gravity=disciplinary_note.get('gravity'),
                              description=disciplinary_note.get('description'),
                              createdBy=1, createdAt=time_now())

            # And save using himself

            key = dn_to_save.put()
            dn_saved = key.get().to_dict()
            dn_saved = dict((k, v) for k, v in dn_saved.iteritems() if v)
            dn_saved['disciplinaryNoteId'] = key.id()
            print colored(dn_saved, 'red')

            return {'status': 200, 'log': None, 'data': dn_saved}

    @classmethod
    def put(cls, disciplinary_note):
        pass

    @classmethod
    def delete(cls, disciplinary_note):

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