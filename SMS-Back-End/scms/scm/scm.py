############################
# Students Control Manager #
############################

from termcolor import colored
from scm_datastore_models import *
import datetime
import pytz

def check_association_data_block(data_block):
    """

    :param data_block:
    :return: {'status': int , 'log': string }
    """

    log = ''
    its_ok = True

    print colored(data_block,'green')

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
            log = '\'associationId\' key fault.'
            return {'log': log}

        _class = association.get('class', None)
        subject = association.get('subject', None)

        if _class is None:
            log = '\'class\' key fault inside association dict.'
            return {'log': log}

        for val in [['classId', int], ['classWord', unicode], ['classLevel', unicode], ['classCourse', int]]:
            item = _class.get(val[0], None)
            if item is None:
                return {'log': '\'{}\' key fault in class dict'.format(val)}

            if type(item) is not val[1]:
                return {'log': 'Incorrect type in \'{0}\' key. It must be a {1} '.format(val[0], val[1])}

        if subject is None:
            log = '\'subject\' key fault inside association dict.'
            return {'log': log}

        for val in ['subjectId', 'subjectName']:
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

class Association_Manager:
    """
    Standard response data block:
        A dict with three fields, {'status': int,  'log' string, 'data': data }
    """

    @classmethod
    def post(cls, data_block):
        """
        Insert a kind of item "Association Data Block" in the database.
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
                           classWord=classs['classWord'],
                           classCourse=classs['classCourse'],
                           classLevel='Basic')
            subject = Subject(subjectId=subject['subjectId'], subjectName=subject['subjectName'])

            asso = Association(associationId=data_block['association']['associationId'], classs=classs, subject=subject)

            teacher = Teacher(teacherId=teacher['teacherId'], name=teacher['teacherName'], surname=teacher.get('teacherSurname', None))
            students_list = []
            # Optional values must be extracted with ".get()" instead of "[]"
            for student in students:
                students_list.append(Student(studentId=student['studentId'], name=student['studentName'], surname=student.get('studentSurname')))

            now = datetime.datetime.utcnow()
            tz = pytz.timezone('Europe/Madrid')
            tzoffset = tz.utcoffset(now)
            mynow = now + tzoffset


            adb = ADB(association=asso,
                      teacher=teacher,
                      students=students_list,
                      createdBy=1,
                      createdAt=mynow)



            # put() returns a key object.
            key = adb.put()

            return {'status': 1, 'log': None, 'data': {'key':key.id(), 'kind': key.kind()}}

        else:
            return 0

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
                    return {'status': 1, 'data': item, 'log': None}
                else:
                    return {'status': -1, 'data': None, 'log': None}

            else:
                return {'status': -1, 'data': None, 'log': None}

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

                return {'status': 1, 'data': asso_list, 'log': None}
            else:
                return {'status': -1, 'data': None, 'log': None}


        elif not association_id and not teacher_id:

            q = ADB.query()
            items = []

            for result in q.iter():
                dict_tmp = result.to_dict()

                dict_tmp = dict((k, v) for k, v in dict_tmp.iteritems() if v)

                if dict_tmp.get('deleted', None) is not True:

                    dict_tmp['scmsAssociationId'] = result._key.id()
                    items.append(dict_tmp)

            return {'status': 1, 'data': items, 'log': None}

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
