# -*- coding: utf-8 -*-
"""
Prueba de unión de métodos de entidades.

DATOS:

Si se trata de enteros: enteros
Si se trata de texto: en unicode
Si se trata de booleanos : boolean

"""

# Uso de variables generales par la conexión a la BD.
import db_params
import datetime
from termcolor import colored
from utils import *

import pytz

# Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v = 1


def sql_execute(cursor, query):  # References

    status = 1  # By default is success.
    num_elements = 0  # By default any entity is retrieved.
    log = None

    try:
        num_elements = cursor.execute(query);
    except db_params.MySQLdb.Error, e:
        try:
            error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print error
            log = error
            status = e.args[0]
        except IndexError:
            print "MySQL Error: %s" % str(e)

    print 'status: ' + colored(status, 'red')
    print 'num_elements: ' + colored(num_elements, 'red')

    return status, num_elements, log


class EntitiesManager:
    """
    Gestor de entidades de la base de datos, que abstrae el funcionamiento de MySQL y que añade muchísima funcionalidad.
    """

    @classmethod
    def post(cls, kind, data):
        """
        INSERT data entity in the database or a relation entity between two of them.

        :param kind: Type of data, student, teacher, class, etc. Any table of database.
        :param data: A dict with the data, like : {"name": "Jhon", "dni": 9999999}
        :return: A dict with three fields:
            data: A dict with the item updated as it has been saved in the database.
            status: MySQL status code to debug and customize the return of queries.
            log: String with info about the query result, like detail about errors.
        """
        if v:
            print colored(locals(), 'blue')

        db = db_params.conecta()
        return_dic = {}

        now = datetime.datetime.utcnow()
        tz = pytz.timezone('Europe/Madrid')
        tzoffset = tz.utcoffset(now)
        mynow = now + tzoffset

        control_fields = {'createdBy': 1,
                          'createdAt': mynow,
                          'deleted': 0}

        query = 'insert into ' + str(kind) + ' (' + str(kind) + 'Id, '

        # Control special case:
        if data.get('course', None) and data.get('level', None) and not data.get('word', None) and \
                (not data.get('group', None) or not data.get('subgroup',None)):
            return_dic['status'] = 1048 #  Because cause a 400 Bad Request fail with log message included.
            return_dic['log'] = 'In this special case you need group and subgroup values to create an optional group ' \
                                ' , please review it.'
            return return_dic



        # Only when is a special optional group we create a new value to word value:
        if not data.get('word', None) and data.get('group', None) and data.get('subgroup'):
            print colored('HERE, is a special optative group', 'red')
            new_value = 'OPT_{}_{}'.format(data.get('group'), data.get('subgroup'))
            data['word'] = new_value
            del data['group']
            del data['subgroup']

        ## We insert the keys:
        for key, value in data.iteritems():
            query += str(key) + ', '

        # The same with control_fields keys
        for key, value in control_fields.iteritems():
            query += str(key) + ', '

        ## We insert now the values:
        query = query[:-2]
        query += ') values (NULL, '

        for key, value in data.iteritems():
            if isinstance(value, int):
                value = str(value)

            query += '\'' + value + '\', '

        # The same with control_fields values
        for key, value in control_fields.iteritems():
            query += '\'' + str(value) + '\', '

        query = query[:-2]
        query += ');'

        print colored(query, 'red')

        cursor = db.cursor()

        status_value = 1  # By default is success.
        num_elements = 0  # By default any entity is retrieved.
        log = None

        try:
            num_elements = cursor.execute(query);
            entity_id = cursor.lastrowid
        except db_params.MySQLdb.Error, e:
            try:
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                log = error
                status_value = e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        db.commit()

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if status_value == 1:

            retrieve_query = 'select * from ' + kind + ' where ' + kind + 'Id = ' + str(entity_id) + ';'
            print colored('Populating item', 'green')
            print colored(retrieve_query, 'green')

            if cursor.execute(retrieve_query) == 1:  # If query obtain one element.
                row = cursor.fetchone()
                # None values are not necessary.
                row = dict((k, v) for k, v in row.iteritems() if v is not None)

                print colored(row, 'magenta')

                return_dic['data'] = row

                # The deleted value isn't relevant in the UI and because of this it will not sended.
                if return_dic['data'].get('deleted') != None:
                    del return_dic['data']['deleted']

        return_dic['status'] = status_value
        return_dic['log'] = log

        # Confirm the changes
        db.commit()
        cursor.close()
        db.close()

        return return_dic

    @classmethod
    def get(cls, kind, entity_id=None, params=None):
        """
        Return entities from the database, all info about one or a summary list of all of a specific kind.

        :param kind: Type of data, student, teacher, class, etc.
        :param entity_id: Entity id that we want retrieve. Can be None, in this case we want all entities of this kind.
        :param params: When we want retrieve a list with specific data from entities we pass here.
        :return: A dict with all info about one or a list with dict with the format: [status][data][log]

        An exception is when the kind of the query is 'association' because is will builded a
        special kind of response.

        """

        if v:
            print colored(locals(), 'blue')

        db = db_params.conecta()
        return_dic = {}
        cursor = db.cursor()

        if kind == 'association' and entity_id is not None:
            query = 'select a.*, c.course as \'classCourse\', c.level as \'classLevel\', c.word as \'classWord\', ' \
                    's.name as \'subjectName\' from association a INNER JOIN subject s ' \
                    'ON (a.subjectId = s.subjectId) INNER JOIN class c ON (a.classId = c.classId) ' \
                    'where a.associationId = {} and a.deleted = {};'.format(entity_id, 0)

            status_value, num_elements, log = sql_execute(cursor, query)

            print 'HERE'
            print status_value
            print num_elements

            if num_elements == 0:
                return_dic['status'] = -1  # Element not found
                return return_dic

            elif status_value == 1 and num_elements == 1:
                print colored('ALL IS GOOD!!', 'red')
                raw_data = cursor.fetchone()
                raw_data = dict((k, v) for k, v in raw_data.iteritems() if v)  # To delete None values

                # The composition of the special data block:
                data_block = {
                    'class': {'classId': raw_data.get('classId', None),
                              'course': raw_data.get('classCourse', None),
                              'level': raw_data.get('classLevel', None),
                              'word': raw_data.get('classWord', None)
                              },
                    'subject': {'subjectId': raw_data.get('subjectId', None),
                                'name': raw_data.get('subjectName', None)
                                }
                }

                for key, value in raw_data.items():
                    if 'class' in str(key) or 'subject' in str(key):
                        del raw_data[key]

                # Update with the rest of data without special format.
                data_block.update(raw_data)

                print colored(data_block, 'red')

                # Now we search all teachers and students related with this association and we will insert them in
                # the data block.

                query_for_teachers = 'select t.teacherId as \'teacherId\', t.name as \'teacherName\', t.surname as' \
                                     ' \'teacherSurname\' from impart i inner join teacher t on ' \
                                     '(i.teacherId = t.teacherId) where i.associationId = {} and ' \
                                     'i.deleted = {};'.format(entity_id, 0)

                status_value, num_elements, log = sql_execute(cursor, query_for_teachers)

                if status_value == 1 and num_elements >= 1:
                    row = cursor.fetchone()
                    teachers = []
                    while row is not None:
                        row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                        teachers.append(row)
                        row = cursor.fetchone()

                    data_block['teachers'] = teachers

                    query_for_students = 'select s.studentId as \'studentId\', s.name as \'studentName\', s.surname as' \
                                         ' \'studentSurname\' from enrollment e inner join student s on ' \
                                         '(e.studentId = s.studentId) where e.associationId = {} ' \
                                         'and e.deleted = {};'.format(entity_id, 0)

                    status_value, num_elements, log = sql_execute(cursor, query_for_students)

                    if status_value == 1 and num_elements >= 1:
                        row = cursor.fetchone()
                        students = []
                        while row is not None:
                            row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                            students.append(row)
                            row = cursor.fetchone()


                        data_block['students'] = students


            return_dic['data'] = data_block
            return_dic['status'] = status_value

            return return_dic

        else:
            query = 'select '

            # We need all entities of specify kind from database that haven't the column delete to true or 1,
            # and whe don't want all info, only the most relevant, name and id.
            if entity_id is None:

                if params is not None:

                    # It always included entity id.
                    query += str(kind) + 'Id, '

                    print colored(params, 'red')
                    list_params = str(params).split(',')
                    print list_params
                    for param in list_params:
                        query += param + ', '

                    query = query[:-2]

                else:
                    query += ' * '

                query += ' from {} where deleted = 0;'.format(kind)

            # We want all info about one entity.
            else:
                query += '* from {} where {}Id = {} and deleted = 0;'.format(kind,kind,entity_id)


            print colored(query, 'yellow')

            cursor = db.cursor()

            status_value, num_elements, log = sql_execute(cursor, query)

            # If the query execute has success we are going to retrieve all data saved in database about this item.
            if status_value == 1:

                # Info about all
                if entity_id is None:

                    print entity_id

                    row = cursor.fetchone()
                    entities_list = []
                    while row is not None:
                        row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                        entities_list.append(row)
                        row = cursor.fetchone()

                    print entities_list
                    return_dic['data'] = entities_list



                # All info about one
                else:

                    if num_elements != 0:  # If the element exists in database.

                        row = dict((k, v) for k, v in cursor.fetchone().iteritems() if v)  # To delete None values
                        return_dic['data'] = row

                    else:  # If doesn't exists.
                        status_value = -1

            return_dic['status'] = status_value
            return_dic['log'] = log

        db.commit()
        cursor.close()
        db.close()

        return return_dic

    @classmethod
    def update(cls, kind, entity_id, data):
        """
        UPDATE info about a entity.
        :param kind:
        :param entity_id:
        :param data:
        :return:
        """

        if v:
            print colored(locals(), 'blue')

        db = db_params.conecta();
        return_dic = {}

        now = datetime.datetime.utcnow()
        tz = pytz.timezone('Europe/Madrid')
        tzoffset = tz.utcoffset(now)
        mynow = now + tzoffset

        if data.get('deleted', None) == 'NULL': # If is a deleting the control_fieds are others.
            control_fields = {'deletedBy': 1, 'deletedAt': mynow}
        else:
            control_fields = {'modifiedBy': 1, 'modifiedAt': mynow}

        query = 'UPDATE ' + str(kind) + ' SET '

        for key, value in data.iteritems():
            if isinstance(value, int):
                value = str(value)
            if value == 'NULL':
                query += str(key) + ' = ' + value + ' ,'
            else:
                query += str(key) + ' = \'' + value + '\','

        # The same with control_fields values
        for key, value in control_fields.iteritems():
            query += str(key) + ' = \'' + str(value) + '\','

        query = query[:-1]

        query += ' WHERE ' + str(kind) + 'Id = ' + str(entity_id) + ';'

        print colored(query, 'yellow')

        cursor = db.cursor()

        status_value, num_elements, log = sql_execute(cursor, query)

        print colored(status_value, 'yellow')
        print colored(num_elements, 'yellow')

        db.commit()

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if status_value == 1:

            retrieve_query = 'select * from ' + str(kind) + ' where ' + str(kind) + 'Id = ' + str(entity_id) + ';'
            print colored('Populating item', 'green')
            print colored(retrieve_query, 'green')

            if cursor.execute(retrieve_query) == 1:  # If query obtain one element.
                row = cursor.fetchone()
                # None values are not necessary.
                row = dict((k, v) for k, v in row.iteritems() if v)

                print colored(row, 'magenta')

                return_dic['data'] = row

        return_dic['status'] = status_value
        return_dic['log'] = log

        if 'deleted = NULL' in query and num_elements == 0 and status_value != 1644:
            return_dic['log'] = 'not found element to del'

        # Confirm the changes
        db.commit()
        cursor.close()
        db.close()

        return return_dic

    @classmethod
    def delete(cls, kind, entity_id, actions=None):
        # If the update is delete an item, we not want send the erased data.
        # We only update the item with the value to NULL

        dd_status = True;

        if actions == 'dd':  # Delete dependencies.  (BEFORE)
            if kind == 'student':
                response = cls.get(kind='enrollment', params='studentId, enrollmentId')
                if response.get('status') == 1:
                    enrollments_list = response.get('data', None)
                    if len(enrollments_list) > 0:  # If the student haven't relation, stop here.
                        for item in enrollments_list:
                            if item.get('studentId', None) == entity_id:
                                # Delete the enrollment associated with the student.
                                if cls.delete(kind='enrollment', entity_id=item.get('enrollmentId')).get('status', None) != 1:
                                    dd_status = False  # Something gone wrong.
            if kind == 'subject':
                association_relations = cls.get_related('subject', entity_id, 'association', False, True).get('data', None)
                impart_relations = cls.get_related('subject', entity_id, 'impart', False, True).get('data',None)
                enrollment_relations = cls.get_related('subject', entity_id, 'enrollment', False, True).get('data',None)

                print 'ENROLLMENTs'
                print enrollment_relations

                if len(impart_relations) > 0 and dd_status:
                    for impart in impart_relations:
                        if cls.delete('impart',impart.get('impartId')).get('status') != 1:
                            dd_status = False

                if len(enrollment_relations) > 0 and dd_status:
                    for enrollment in enrollment_relations:
                        print 'ENROLLMENT'
                        print colored(enrollment, 'red')
                        if cls.delete('enrollment',enrollment.get('enrollmentId')).get('status') != 1:
                            dd_status = False

                if len(association_relations) > 0 and dd_status:
                    for association in association_relations:
                        if cls.delete('association', association.get('associationId')).get('status') != 1:
                            dd_status = False

            if kind == 'class':
                association_relations = cls.get_related('class', entity_id, 'association').get('data', None)
                impart_relations = cls.get_related('class', entity_id, 'impart').get('data', None)
                enrollment_relations = cls.get_related('class', entity_id, 'enrollment').get('data', None)

                if len(impart_relations) > 0 and dd_status:
                    for impart in impart_relations:
                        if cls.delete('impart', impart.get('impartId')).get('status') != 1:
                            dd_status = False

                if len(enrollment_relations) > 0 and dd_status:
                    for enrollment in impart_relations:
                        if cls.delete('enrollment', enrollment.get('enrollmentId')).get('status') != 1:
                            dd_status = False

                if len(association_relations) > 0 and dd_status:
                    for association in association_relations:
                        if cls.delete('association', association.get('associationId')).get('status') != 1:
                            dd_status = False

            if kind == 'teacher':
                response = cls.get(kind='impart', params='teacherId, impartId')
                if response.get('status') == 1:
                    imparts_list = response.get('data', None)
                    if len(imparts_list) > 0:  # If the teacher haven't relation, stop here.
                        for item in imparts_list:
                            if item.get('teacherId', None) == entity_id:
                                # Delete the impart associated with the teacher.
                                if cls.delete(kind='impart', entity_id=item.get('impartId')).get('status',None) != 1:
                                    dd_status = False  # Something gone wrong.


        if dd_status:
            item_dict = cls.update(kind, entity_id, {'deleted': 'NULL'})
            if item_dict['status'] == 1:
                item_dict['data'] = None

        else:
            item_dict = {'status': 99} # Something gone wrong.

        return item_dict

    @classmethod
    def get_related(cls, kind, entity_id, related_kind, with_special_sorter=True, internall_call=False):
        """Devuelve una lista de diccionarios con la información pedida."""

        kind = str(kind)
        entity_id = str(entity_id)
        related_kind = str(related_kind)
        return_dic = {}


        # Avoiding errors with nested resources :

        if kind == related_kind:
            return_dic['status'] = 1048  # Bad requests with log.
            return_dic['log'] = '{} is not a valid nested resource.'.format(related_kind)

            return return_dic

        if kind in ['teacher','student', 'class', 'subject'] and related_kind in ['association', 'enrollment', 'impart'] and internall_call == False:
            return_dic['status'] = 1048  # Bad requests with log.
            return_dic['log'] = '{} is not a valid nested resource.'.format(related_kind)

            return return_dic

        if kind in ['association','impart', 'enrollment'] and related_kind in ['impart', 'association', 'enrollment', 'teacher', 'student', 'class', 'subject'] and internall_call == False:
            return_dic['status'] = 1048  # Bad requests with log.
            return_dic['log'] = '{} is not a valid nested resource.'.format(related_kind)

            return return_dic

        # Pre adjust:
        if kind == 'teacher' and related_kind == 'teaching':  # teaching = "docencia" in Spanish
            related_kind = 'impart'  # The real meaning.

        if kind == 'student' and related_kind == 'teaching':
            related_kind = 'enrollment'  # The real meaning.

        if kind == 'subject' and related_kind == 'teaching':
            related_kind = 'class'  # The real meaning.

        if kind == 'class' and related_kind == 'teaching':
            related_kind = 'subject'  # The real meaning.

        print locals()

        db = db_params.conecta()
        cursor = db.cursor()

        # First check if the base kind exists: ##

        status_value = 1  # By default is success.
        num_elements = 0  # By default any entity is retrieved.
        log = None

        query = "SELECT COUNT(*) FROM {} where {}Id = {};".format(kind, kind, entity_id)
        print query
        exists = 0;

        status_value, num_elements, log = sql_execute(cursor, query)
        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if status_value == 1:
            result = cursor.fetchone()
            exists = result.items()[0][1] # Because with our way to get data we have a dict.


        db.commit()

        # IF element doesn't exists we need abort here.
        if not exists:
            return_dic['status'] = -1
            cursor.close()
            db.close()
            return return_dic

        query = ''

        if kind == 'student':  # Queremos buscar entidades relacionadas con una entidad de tipo student

            if related_kind == 'teacher':  # Todos los profesores que dan clase al alumno.
                query = 'SELECT teacherId, name, surname FROM teacher WHERE deleted = 0 and teacherId IN (SELECT teacherId FROM impart, enrollment WHERE impart.associationId=enrollment.associationId and enrollment.studentId=' + entity_id + ');'
            elif related_kind == 'class':  # Todos las clases en las que está matriculado el alumno.
                query = 'SELECT classId, course, word, level FROM class WHERE deleted = 0 and classId IN (SELECT classId FROM association WHERE associationId IN (SELECT associationId FROM enrollment WHERE studentId=' + entity_id + '));'
            elif related_kind == 'subject':  # Todas las asignaturas en la que está matriculado el alumno.
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId IN (SELECT subjectId FROM association WHERE associationId IN (SELECT associationId FROM enrollment WHERE studentId=' + entity_id + '));'
            elif related_kind == 'enrollment':
                # More bit complex query:
                query = 'SELECT e.enrollmentId, c.classId, c.course, c.word, c.level, s.subjectId, s.name FROM ' \
                        '( SELECT enrollment.associationId, enrollmentId , association.subjectId, association.classId ' \
                        'FROM enrollment JOIN association WHERE enrollment.associationId = association.associationId ' \
                        'AND enrollment.studentId = ' + entity_id + ' AND enrollment.deleted = 0) e JOIN class c JOIN subject s on (e.classId = c.classId ' \
                                                                    'AND e.subjectId = s.subjectId);'

        elif kind == 'teacher':  # Queremos buscar entidades relacionadas con una entidad de tipo teacher
            if related_kind == 'student':  # Todos los alumnos a los que da clase ese profesor.
                query = 'SELECT studentId, name, surname  FROM student WHERE deleted = 0 and studentId IN (SELECT studentId FROM impart, enrollment WHERE impart.associationId=enrollment.associationId AND impart.teacherId=' + entity_id + ');'
            elif related_kind == 'class':  # Todos las clases en las que el profesor imparte.
                query = 'SELECT classId, course, word, level FROM class WHERE deleted = 0 and classId IN (SELECT classId FROM association where associationId IN(SELECT associationId FROM impart WHERE teacherId=' + entity_id + '));'
            elif related_kind == 'subject':  # Todas las asignaturas que el profesor imparte.
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId IN (SELECT subjectId FROM association WHERE associationId IN (SELECT associationId FROM impart WHERE teacherId=' + entity_id + '));'
            elif related_kind == 'impart':
                # More bit complex query:
                query = 'SELECT i.impartId, c.classId, c.course, c.word, c.level, s.subjectId, s.name FROM ' \
                        '( SELECT impart.associationId, impartId , association.subjectId, association.classId ' \
                        'FROM impart JOIN association WHERE impart.associationId = association.associationId ' \
                        'AND impart.teacherId = ' + entity_id + ' AND impart.deleted = 0) i JOIN class c JOIN subject s on (i.classId = c.classId ' \
                                                                'AND i.subjectId = s.subjectId);'

        elif kind == 'class':  # Queremos buscar entidades relacionadas con una entidad de tipo class.
            if related_kind == 'student':  # Todos los alumnos matriculados en esa clase.
                query = 'SELECT studentId, name, surname FROM student WHERE deleted = 0 and studentId IN (SELECT studentId FROM enrollment WHERE associationId IN (SELECT associationId FROM association WHERE classId=' + entity_id + '));'
            elif related_kind == 'teacher':  # Todos los profesores que imparten en esa clase alguna asignatura.
                query = 'SELECT teacherId, name, surname FROM teacher WHERE deleted = 0 and teacherId IN (SELECT teacherId FROM impart WHERE associationId IN (SELECT associationId FROM association WHERE classId=' + entity_id + '))';
            elif related_kind == 'subject':  # Todas las asignaturas que se imparten en esa clase.
                query = 'select sbs.subjectId, sbs.name as \'subjectName\', t.name as \'teacherName\', t.surname as \'teacherSurname\', t.teacherId, i.impartId, sbs.associationId from impart i JOIN (select name, s.subjectId, a.associationId from (select name, subjectId from subject) s JOIN ' \
                        '(select subjectId, associationId from association where classId=' + entity_id + ' AND association.deleted = 0) a where s.subjectId = a.subjectId) sbs JOIN teacher t where i.associationId = sbs.associationId and i.teacherId = t.teacherId AND i.deleted = 0 union  select s.subjectId, ' \
                                                                                                         's.name, null, null, null, null,  a.associationId   from (select subjectId, associationId from association where classId=' + entity_id + ' AND association.deleted = 0) a JOIN subject s where a.subjectId = s.subjectId;'
            elif related_kind == 'association':
                query = 'SELECT associationId, subjectId, classId FROM association WHERE deleted = {} and classId = {};'.format(0, entity_id)
            elif related_kind == 'impart':
                query = 'SELECT impartId, teacherId, associationId FROM impart WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and classId = {});'.format(0, 0, entity_id)
            elif related_kind == 'enrollment':
                query = 'SELECT enrollmentId, associationId, studentId FROM enrollment WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and classId = {});'.format(0, 0, entity_id)


        elif kind == 'subject':  # Queremos buscar entidades relacionadas con una entidad de tipo subject.
            if related_kind == 'student':
                query = 'SELECT studentId, name, surname from student where deleted = 0 and studentId in (SELECT studentId from enrollment where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'
            elif related_kind == 'teacher':
                query = 'SELECT teacherId, name, surname from teacher where deleted = 0 and teacherId in (select teacherId from impart where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'

            elif related_kind == 'association':
                query = 'SELECT associationId, subjectId, classId FROM association WHERE deleted = {} and subjectId = {};'.format(0,entity_id)
            elif related_kind == 'impart':
                query = 'SELECT impartId, teacherId, associationId FROM impart WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and subjectId = {});'.format(0,0,entity_id)
            elif related_kind == 'enrollment':
                query = 'SELECT enrollmentId, associationId, studentId FROM enrollment WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and subjectId = {});'.format(0,0,entity_id)


            elif related_kind == 'class':
                # An especial case, it needed info in special format to show in the view.
                query = 'select cls.classId, cls.course, cls.word, cls.level, t.name, t.surname, t.teacherId, i.impartId, cls.associationId from (select * from impart where impart.deleted = 0) i JOIN (select course, word, level, c.classId, a.associationId from (select course, word, level, classId from class) c ' \
                        'JOIN (select classId, associationId from association where subjectId=' + entity_id + ' AND association.deleted = 0 ) a where c.classId = a.classId) cls JOIN teacher t where i.associationId = cls.associationId and i.teacherId = t.teacherId union select c.classId, c.course, c.word, c.level, null, null, null, null,  a.associationId   ' \
                                                                                                              'from (select classId, associationId from association where subjectId=' + entity_id + ' AND association.deleted = 0 ) a JOIN class c where a.classId = c.classId;'


        if v:
            print colored(query, 'yellow')

        status_value, num_elements, log = sql_execute(cursor, query)

        if status_value == 1:

            entities_list = []

            if num_elements > 0:

                row = cursor.fetchone()
                while row is not None:
                    row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                    entities_list.append(row)
                    row = cursor.fetchone()

            return_dic['data'] = entities_list

        return_dic['status'] = status_value
        return_dic['log'] = log

        db.commit()
        cursor.close()
        db.close()

        # Optional SORTERS CALLs

        if with_special_sorter:

            if kind == 'teacher' and related_kind == 'impart' and status_value == 1:
                return_dic['data'] = sorters.special_sort(return_dic['data'])

            if kind == 'student' and related_kind == 'enrollment' and status_value == 1:
                return_dic['data'] = sorters.special_sort_2(return_dic['data'])

            if kind == 'subject' and related_kind == 'class':
                return_dic['data'] = sorters.special_sort_3(return_dic['data'])

            if kind == 'class' and related_kind == 'subject':
                return_dic['data'] = sorters.special_sort_4(return_dic['data'])

        return return_dic

    @classmethod
    def get_report(cls, kind, entity_id):

        print colored('GET REPORT', 'red')
        return_dic = {}
        set_lack_data_message = False

        if kind == 'class':  # We will made the reports of this kind of item.

            data_block = {}

            data_block['students'] = {}

            # Students analysis:
            students = cls.get(kind='student', params='birthdate,gender').get('data', None)

            # Count:
            num_students = len(students)
            data_block['students']['count'] = num_students

            # Gender:
            f = 0
            m = 0
            for student in students:
                gender = student.get('gender', None)
                if gender != None:
                    if gender == 'F':
                        f+=1
                    elif gender == 'M':
                        m+=1
                else:
                    set_lack_data_message = True

            # percentage
            f_per = (f * 100) / (f + m)
            m_per = (m * 100) / (f + m)

            data_block['students']['gender_percentage'] = {'M': m_per, 'F': f_per}

            print f_per
            print m_per
            print 'here'

            # Medium age:
            ages = []
            medium_age = 0
            for student in students:
                print student
                birthdate = student.get('birthdate', None)
                if birthdate != None:
                    print birthdate
                    print type(birthdate)
                    #birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
                    ages.append(datetime.date.today().year - birthdate.year)
                else:
                    set_lack_data_message = True

            medium_age = sum(ages)/len(ages)

            data_block['students']['medium_age'] = medium_age


            if set_lack_data_message:
                data_block['report_log'] = 'data lack' # Meaning that some data is missing .


            return_dic['data'] = data_block
            return_dic['status'] = 1

            return return_dic


        pass