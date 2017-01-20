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


def sql_executor(query, expected_kind=None, last_row_id=False):  # References
    """
    :param query:
    :param expected_kind: Is the type of data expected, if they can be returned.
    For example: list, if there are elements, even one, is returned like a list, not like a element.
    list
    item
    :param last_row_id: If you want retrieve in the info data_block the id achieve from cursor.lastrowid

    Example of use:

        sql_execute('select * from student', list)
        sql_execute('select * from student where studentId = 4', item)

    Both are dicts, alone or list of they.

    :return:

     return_dic['data'] = entities_list
     return_dic['status'] = status
     return_dic['log'] = log
     return_dic['last_row_id'] = 3


    """

    print colored('sql_executor IN: {}'.format(locals()), 'red')

    db = db_params.conecta()
    cursor = db.cursor()

    status = 1  # By default is success.
    num_elements = 0  # By default any entity is retrieved.
    lr_id = 0 # Last row id
    log = None

    return_dic = {}

    try:
        num_elements = cursor.execute(query)
        lr_id = cursor.lastrowid

        print(num_elements)

    except db_params.MySQLdb.Error, e:
        try:
            error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print error
            log = error
            status = e.args[0]
        except IndexError:
            print "MySQL Error: %s" % str(e)

    if last_row_id:
        print 'last_row_id:' + colored(lr_id, 'red')

    if status == 1:

        if num_elements == 1:
            if expected_kind == 'list':
                entities_list = []
            row = cursor.fetchone() # When is POST fetchone return None.
            if row is not None:
                row = dict((k, v) for k, v in row.iteritems() if v is not None)  # To delete None values
                if expected_kind == 'list':
                    entities_list.append(row)
                    return_dic['data'] = entities_list
                else:
                    return_dic['data'] = row

        if num_elements > 1:
            entities_list = []
            row = cursor.fetchone()
            while row is not None:
                row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                entities_list.append(row)
                row = cursor.fetchone()
            return_dic['data'] = entities_list

        if num_elements == 0:
            if expected_kind == 'item':
                status = -1  # Code for element not found.
            else:
                return_dic['data'] = []  # Code for element found, but without content.

    if last_row_id:
        return_dic['last_row_id'] = lr_id

    db.commit()
    cursor.close()
    db.close()

    return_dic['status'] = status
    return_dic['log'] = log

    print colored('sql_executor OUT: {}'.format(return_dic), 'red')
    return return_dic


class EntitiesManager:
    """
    Gestor de entidades de la base de datos, que abstrae el funcionamiento de MySQL y que añade muchísima funcionalidad.
    """

    @classmethod
    def multiple_enrollment(cls, kind, data):
        """
        Special method to make multiple enrollments in the same call.
        :param kind:
        :param data:
        :return:
        """

        return_dic = {}
        data_list = []
        log = ''

        associations_ids_list = data.get('associationsIds', None)
        student_id = data.get('studentId', None)
        process_ok = True

        if associations_ids_list is not None and student_id is not None:

            for association in associations_ids_list:
                response = cls.post('enrollment', {'associationId': association, 'studentId': student_id})
                print response
                if response.get('status') != 1:
                    process_ok = False
                    return response
                    break
                else:
                    data_list.append(response.get('data'))

        if process_ok:
            return_dic['status'] = 1
            return_dic['data'] = data_list

        return return_dic

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

        return_dic = {}

        now = datetime.datetime.utcnow()
        tz = pytz.timezone('Europe/Madrid')
        tzoffset = tz.utcoffset(now)
        mynow = now + tzoffset

        control_fields = {'createdBy': 1, 'createdAt': mynow, 'deleted': 0}

        query = 'insert into {0} ({0}Id, '.format(kind)

        # Control to special case:
        if data.get('course', None) and data.get('level', None) and not data.get('word', None) and \
                (not data.get('group', None) or not data.get('subgroup', None)):
            return_dic['status'] = 1048  # Because cause a 400 Bad Request fail with log message included.
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

        # We insert the keys:
        for key, value in data.iteritems():
            query += '{}, '.format(key)

        # The same with control_fields keys
        for key, value in control_fields.iteritems():
            query += '{}, '.format(key)

        # We insert now the values:
        query = query[:-2]
        query += ') values (NULL, '

        for key, value in data.iteritems():
            if isinstance(value, int):
                value = str(value)
            query += '{0}{1}{0}, '.format('\'', value)

        # The same with control_fields values
        for key, value in control_fields.iteritems():
            query += '{0}{1}{0}, '.format('\'', value)

        query = query[:-2]
        query += ');'

        data_block = sql_executor(query=query, expected_kind='item', last_row_id=True)

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if data_block.get('status') == 1:

            retrieve_query = 'select * from {0} where {0}Id = {1};'.format(kind, data_block.get('last_row_id'))

            data_block_2 = sql_executor(retrieve_query, 'item')
            entity_data = data_block_2.get('data', None)
            if entity_data.get('deleted') is not None:
                del entity_data['deleted']

            return_dic['data'] = entity_data
            return_dic['status'] = data_block['status']
            return_dic['log'] = data_block['log']

            return return_dic

        else:
            return data_block # With possibles errors.

    @classmethod
    def get(cls, kind, entity_id=None, params=None):
        """
        Return entities from the database, all info about one or a summary list of all of a specific kind.

        :param kind: Type of data, student, teacher, class, etc.
        :param entity_id: Entity id that we want retrieve. Can be None, in this case we want all entities of this kind.
        :param params: When we want retrieve a list with specific data from entities we pass here.
        :return: A dict with all info about one or a list with dict with the format: [status][data][log]

        An exception is when the kind of the query is 'association' because it will build a
        special kind of response.

        """

        if v:
            print colored(locals(), 'blue')

        if kind == 'association' and entity_id is not None:

            return_dic = {}

            query = 'select a.*, c.course as \'classCourse\', c.level as \'classLevel\', c.word as \'classWord\', ' \
                    's.name as \'subjectName\' from association a INNER JOIN subject s ' \
                    'ON (a.subjectId = s.subjectId) INNER JOIN class c ON (a.classId = c.classId) ' \
                    'where a.associationId = {} and a.deleted = {};'.format(entity_id, 0)

            query_for_teachers = 'select t.teacherId as \'teacherId\', t.name as \'teacherName\', t.surname as' \
                                 ' \'teacherSurname\' from impart i inner join teacher t on ' \
                                 '(i.teacherId = t.teacherId) where i.associationId = {} and ' \
                                 'i.deleted = {};'.format(entity_id, 0)

            query_for_students = 'select s.studentId as \'studentId\', s.name as \'studentName\', s.surname as' \
                                 ' \'studentSurname\' from enrollment e inner join student s on ' \
                                 '(e.studentId = s.studentId) where e.associationId = {} ' \
                                 'and e.deleted = {};'.format(entity_id, 0)

            return_data_block = sql_executor(query)

            if return_data_block['status'] == -1:
                # The associations doesn't exists and we return the same response from sql_execute2
                return return_data_block

            elif return_data_block['status'] == 1 and return_data_block.get('data', None) is not None:
                data = return_data_block['data']
                # The composition of the special data block:
                data_block = {
                    'class': {'classId': data.get('classId', None),
                              'course': data.get('classCourse', None),
                              'level': data.get('classLevel', None),
                              'word': data.get('classWord', None)
                              },
                    'subject': {'subjectId': data.get('subjectId', None),
                                'name': data.get('subjectName', None)
                                }
                }

                for key, value in data.items():
                    if 'class' in str(key) or 'subject' in str(key):
                        del data[key]

                # Update with the rest of data without special format.
                data_block.update(data)


                # Now we search all teachers and students related with this association and we will insert them in
                # the data block.
                return_data_block = sql_executor(query_for_teachers, 'list')
                data = return_data_block.get('data', None)
                if return_data_block.get('status', None) == 1 and data is not None and len(data) > 0:
                    data_block['teachers'] = data

                # we do the same with students:
                return_data_block = sql_executor(query_for_students, 'list')
                data = return_data_block.get('data', None)
                if return_data_block.get('status', None) == 1 and data is not None and len(data) >0:
                    data_block['students'] = data

            return_dic['data'] = data_block
            return_dic['status'] = return_data_block['status']

            return return_dic

        else:
            query = 'select '
            expected_kind = None

            # We need all entities of specify kind from database that haven't the column delete to true or 1,
            # and whe don't want all info, only the most relevant, name and id.
            if entity_id is None:
                if params is not None:
                    # It always included entity id.
                    query += str(kind) + 'Id, '
                    for param in str(params).split(','):
                        query += param + ', '
                    query = query[:-2]

                else:
                    query += ' * '

                query += ' from {} where deleted = 0;'.format(kind) # '#' is a special character, means that there aren't a entity_id
                expected_kind = 'list'

            # We want all info about one entity.
            else:
                query += '* from {} where {}Id = {} and deleted = 0;'.format(kind, kind, entity_id)
                expected_kind = 'item'

            # Is returned directly the block returned from sql_execute2
            return sql_executor(query, expected_kind)

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

        if data.get('deleted', None) == 'NULL':  # If is a deleting the control_fieds are others.
            control_fields = {'deletedBy': 1, 'deletedAt': mynow}
        else:
            control_fields = {'modifiedBy': 1, 'modifiedAt': mynow}

        query = 'UPDATE {} SET '.format(kind)

        for key, value in data.iteritems():
            if isinstance(value, int):
                value = str(value)
            if value == 'NULL':
                query += '{} = {} ,'.format(key, value)
            else:
                query += '{} = \'{}\','.format(key, value)

        # The same with control_fields values
        for key, value in control_fields.iteritems():
            query += '{} = \'{}\','.format(key, value)

        query = query[:-1]

        query += ' WHERE {}Id = {};'.format(kind, entity_id)

        data_block = sql_executor(query)

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if data_block['status'] == 1:

            retrieve_query = 'select * from {0} where {0}Id = {1};'.format(kind, entity_id)
            print colored('Populating item', 'green')
            print colored(retrieve_query, 'green')

            item_data_block = sql_executor(retrieve_query, 'item')

            if item_data_block['status'] == 1:
                return item_data_block

        return data_block

    @classmethod
    def nested_delete(cls, kind, entity_id, optional_nested_kind, onk_entity_id):
        """
        Attention: For now only works for [class, subject] as kind and student as optional_nested_kind!
        :param kind:
        :param entity_id:
        :param optional_nested_kind:
        :param onk_entity_id:
        :return:
        """

        return_dic = {}

        if kind in ['class', 'subject'] and entity_id != 0 and optional_nested_kind == 'student' and onk_entity_id != 0:
            data_block = cls.get_related(kind='student', entity_id=onk_entity_id, related_kind='teaching', internal_call=True)
            data_block = data_block.get('data',None)

            enrollments_ids_list = []

            status_ok = True

            # Que hace cuando no está en ninguna clase, enviar un not found.
            if data_block:
                for cl in data_block: # cl is class in each teaching data block from student.
                    subjects = cl.get('subjects', None)
                    if subjects:
                        for sub in subjects:
                            enrollments_ids_list.append(sub.get('enrollmentId'))
                print enrollments_ids_list

                for enrollment_id in enrollments_ids_list:
                    response = cls.delete('enrollment', enrollment_id)
                    if response.get('status', None) != 1:
                        status_ok = False

                if status_ok:
                    return_dic['status'] = 1
                    return_dic['data'] = None

                else:
                    return_dic = {'status': 99}  # Something gone wrong.

                return return_dic

            else:
                return_dic['status'] = -1
                #TODO: Maybe we can insert a more specific message ;)
                return return_dic


        else:
            # Los parámetros no son los correctos.
            print 'ERROR'




    @classmethod
    def delete(cls, kind, entity_id, actions=None):
        # If the update is delete an item, we not want send the erased data.
        # We only update the item with the value to NULL

        # First check if the item exists to be deleted.
        item = cls.get(kind, entity_id)
        if item.get('status') == -1:
            return item

        dd_status = True

        if actions == 'dd':  # Delete dependencies.  (BEFORE)

            if kind == 'student':
                response = cls.get(kind='enrollment', params='studentId, enrollmentId')
                if response.get('status') == 1:
                    enrollments_list = response.get('data', None)
                    if not isinstance(enrollments_list, list): # If the data isn't a list because is only one, we convert it.
                        enrollments_list = [enrollments_list]
                    if len(enrollments_list) > 0:  # If the student haven't relation, stop here.
                        for item in enrollments_list:
                            if item.get('studentId', None) == entity_id:
                                # Delete the enrollment associated with the student.
                                if cls.delete(kind='enrollment', entity_id=item.get('enrollmentId')).get('status',
                                                                                                         None) != 1:
                                    dd_status = False  # Something gone wrong.
            if kind == 'subject':
                association_relations = cls.get_related(kind='subject', entity_id=entity_id, related_kind='association',
                                                        params=None, with_special_sorter=False,
                                                        internal_call=True).get('data',None)

                impart_relations = cls.get_related(kind='subject', entity_id=entity_id,
                                                   related_kind='impart', params=None,
                                                   with_special_sorter=False,
                                                   internal_call=True).get('data', None)

                enrollment_relations = cls.get_related(kind='subject', entity_id=entity_id,
                                                       related_kind='enrollment', params=None,
                                                       with_special_sorter=False, internal_call=True).get('data',None)


                if len(impart_relations) > 0 and dd_status:
                    for impart in impart_relations:
                        if cls.delete('impart', impart.get('impartId')).get('status') != 1:
                            dd_status = False

                if len(enrollment_relations) > 0 and dd_status:
                    for enrollment in enrollment_relations:
                        print 'ENROLLMENT'
                        print colored(enrollment, 'red')
                        if cls.delete('enrollment', enrollment.get('enrollmentId')).get('status') != 1:
                            dd_status = False

                if len(association_relations) > 0 and dd_status:
                    for association in association_relations:
                        if cls.delete('association', association.get('associationId')).get('status') != 1:
                            dd_status = False

            # Delete an association with all elements related with it.
            if kind == 'association':
                print 'Deleting association relations'

                enrollments_data_block = cls.get(kind='enrollment', params='enrollmentId, associationId')
                imparts_data_block = cls.get(kind='impart', params='impartId, associationId')

                if enrollments_data_block.get('status') == 1 and imparts_data_block.get('status') == 1:

                    enrollments_list = enrollments_data_block.get('data', None)
                    imparts_list = imparts_data_block.get('data', None)

                    if len(enrollments_list) > 0:
                        for item in enrollments_list:
                            if item.get('associationId', None) == entity_id:
                                # Delete the enrollment associated with the association.
                                if cls.delete(kind='enrollment', entity_id=item.get('enrollmentId')).get('status', None) != 1:
                                    dd_status = False  # Something gone wrong.

                    if len(imparts_list) > 0:
                        for item in imparts_list:
                            if item.get('associationId', None) == entity_id:
                                # Delete the impart associated with the association.
                                if cls.delete(kind='impart', entity_id=item.get('impartId')).get('status', None) != 1:
                                    dd_status = False  # Something gone wrong.

            if kind == 'class':

                association_relations = cls.get_related('class', entity_id, 'association', internal_call=True).get(
                    'data', None)
                impart_relations = cls.get_related('class', entity_id, 'impart', internal_call=True).get('data', None)
                enrollment_relations = cls.get_related('class', entity_id, 'enrollment', internal_call=True).get(
                    'data', None)

                if impart_relations and len(impart_relations) > 0 and dd_status:
                    for impart in impart_relations:
                        if cls.delete('impart', impart.get('impartId')).get('status') != 1:
                            dd_status = False

                if enrollment_relations and len(enrollment_relations) > 0 and dd_status:
                    for enrollment in impart_relations:
                        if cls.delete('enrollment', enrollment.get('enrollmentId')).get('status') != 1:
                            dd_status = False

                if association_relations and len(association_relations) > 0 and dd_status:
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
                                if cls.delete(kind='impart', entity_id=item.get('impartId')).get('status', None) != 1:
                                    dd_status = False  # Something gone wrong.

        # Finally we delete the proper object.
        if dd_status:
            item_dict = cls.update(kind, entity_id, {'deleted': 'NULL'})
            if item_dict['status'] == 1:
                item_dict['data'] = None

        else:
            item_dict = {'status': 99}  # Something gone wrong.

        return item_dict

    @classmethod
    def get_related(cls, kind, entity_id, related_kind, params=None, with_special_sorter=True, internal_call=False):
        """Devuelve una lista de diccionarios con la información pedida."""

        print 'get_related'
        print locals()

        kind = str(kind)
        entity_id = str(entity_id)
        related_kind = str(related_kind)
        return_dic = {}

        # Avoiding errors with nested resources :

        if kind == related_kind:
            return_dic['status'] = 1048  # Bad requests with log.
            return_dic['log'] = '{} is not a valid nested resource.'.format(related_kind)

            return return_dic

        if not internal_call:
            if kind in ['teacher', 'student', 'class', 'subject'] and related_kind in ['association', 'enrollment',
                                                                                       'impart'] and internal_call == False:
                return_dic['status'] = 1048  # Bad requests with log.
                return_dic['log'] = '{} is not a valid nested resource.'.format(related_kind)

                return return_dic

        if kind in ['association', 'impart', 'enrollment'] and related_kind in ['impart', 'association', 'enrollment',
                                                                                'teacher', 'class',
                                                                                'subject'] and internal_call == False:
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

        #status_value, num_elements, log = sql_execute(cursor, query)

        data_block = sql_executor(query)

        if data_block['status'] == 1:
            count = data_block['data']['COUNT(*)']



        # If the query execute has success we are going to retrieve all data saved in database about this item.
        #if status_value == 1:
        #    result = cursor.fetchone()
        #    exists = result.items()[0][1]  # Because with our way to get data we have a dict.

        #db.commit()

        # IF element doesn't exists we need abort here.
        if count != 1:
            return_dic['status'] = -1
            #cursor.close()
            #db.close()
            return return_dic

        query = ''


        # Preparation of params passed if they exists:
        query_params = ''

        if params is not None:

            # Always the related_kind type:
            if kind == 'association' and related_kind == 'student':
                query_params += 'e.studentId as studentId, enrollmentId,  '
            else:
                query_params += str(related_kind) + 'Id, '

            list_params = str(params).split(',')
            for param in list_params:
                query_params += param + ', '

            query_params = query_params[:-2]

        else:
            query_params += ' * '



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
            else:
                log = '   {}    is not a valid nested resource to student. There are the valid options: teacher,' \
                      ' class, subject, enrollment'.format(related_kind)
                status = 1054 # Bad request
                return ({'status': status, 'log': log})

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
            else:
                log = '   {}    is not a valid nested resource to teacher. There are the valid options: student, ' \
                      'class, subject, impart'.format(related_kind)
                status = 1054 # Bad request
                return ({'status': status, 'log': log})


        elif kind == 'association':
            if related_kind == 'student':
                #query = 'select {0} from student where studentId IN (SELECT studentId, enrollmentId FROM enrollment where associationId={1} and deleted={2});'.format(query_params, entity_id, 0)

                # TODO: review to avoid e.studentId in the response.
                query = 'select {0} from student s join (select enrollmentId, studentId from enrollment where associationId = {1} and deleted = {2}) e where s.studentId = e.studentId and s.deleted = {2};'.format(query_params, entity_id, 0)

            else:
                log = '   {}    is not a valid nested resource to association. There are the valid options: ' \
                      'student'.format(related_kind)
                status = 1054  # Bad request
                return ({'status': status, 'log': log})


        elif kind == 'class': # Info about entities related with the class kind entity.

            # Normal queries:

            if related_kind == 'student':  # Simple query that get the students related with the class passed and show the params pased or all of them in another case.
                query = 'SELECT {0} FROM student WHERE deleted = {2} and studentId IN (SELECT studentId FROM enrollment WHERE associationId IN (SELECT associationId FROM association WHERE classId={1} and deleted = {2}) and deleted = {2});'.format(query_params, entity_id, 0)
                #query_params += ', enrollmentId '
                # TODO: review this query!
                #query = 'select {0} from (SELECT e.enrollmentId, e.studentId from enrollment e join (SELECT associationId FROM association WHERE classId={1} and deleted = {2}) a  where e.associationId = a.associationId and e.deleted = {2}) ae JOIN (SELECT * FROM student)s where s.deleted = {2} and ae.studentId = s.studentId;'.format(query_params, entity_id, 0)

            elif related_kind == 'teacher':  # Todos los profesores que imparten en esa clase alguna asignatura.
                query = 'SELECT {0} FROM teacher WHERE deleted = {2} and teacherId IN (SELECT teacherId FROM impart WHERE associationId IN (SELECT associationId FROM association WHERE classId={1} and deleted = {2}));'.format(query_params, entity_id, 0)

            # Special queries:

            elif related_kind == 'subject':  # Todas las asignaturas que se imparten en esa clase.
                query = 'select sbs.subjectId, sbs.name as \'subjectName\', t.name as \'teacherName\', t.surname as \'teacherSurname\', t.teacherId, i.impartId, sbs.associationId from impart i JOIN (select name, s.subjectId, a.associationId from (select name, subjectId from subject) s JOIN ' \
                        '(select subjectId, associationId from association where classId=' + entity_id + ' AND association.deleted = 0) a where s.subjectId = a.subjectId) sbs JOIN teacher t where i.associationId = sbs.associationId and i.teacherId = t.teacherId AND i.deleted = 0 union  select s.subjectId, ' \
                        's.name, null, null, null, null,  a.associationId   from (select subjectId, associationId from association where classId=' + entity_id + ' AND association.deleted = 0) a JOIN subject s where a.subjectId = s.subjectId;'


            else:
                log = '   {}    is not a valid nested resource to class. There are the valid options: ' \
                      'student, teacher, subject'.format(related_kind)
                status = 1054  # Bad request
                return ({'status': status, 'log': log})

            # Only for internal calls:
            if internal_call:

                if related_kind == 'association':
                    query = 'SELECT associationId, subjectId, classId FROM association WHERE deleted = {} and classId = {};'.format(0, entity_id)

                elif related_kind == 'impart':
                    query = 'SELECT impartId, teacherId, associationId FROM impart WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and classId = {});'.format(
                        0, 0, entity_id)
                elif related_kind == 'enrollment':
                    query = 'SELECT enrollmentId, associationId, studentId FROM enrollment WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and classId = {});'.format(
                        0, 0, entity_id)




        elif kind == 'subject':  # Queremos buscar entidades relacionadas con una entidad de tipo subject.
            if related_kind == 'student':
                query = 'SELECT studentId, name, surname from student where deleted = {1} and studentId in ' \
                        '(SELECT studentId from enrollment where associationId IN ( select associationId ' \
                        'from association where subjectId={0} and deleted = {1}) and deleted = {1});'.format(entity_id, 0)
            elif related_kind == 'teacher':
                query = 'SELECT teacherId, name, surname from teacher where deleted = 0 and teacherId in (select teacherId from impart where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'

            elif related_kind == 'association':
                query = 'SELECT associationId, subjectId, classId FROM association WHERE deleted = {} and subjectId = {};'.format(
                    0, entity_id)
            elif related_kind == 'impart':
                query = 'SELECT impartId, teacherId, associationId FROM impart WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and subjectId = {});'.format(
                    0, 0, entity_id)
            elif related_kind == 'enrollment':
                query = 'SELECT enrollmentId, associationId, studentId FROM enrollment WHERE deleted = {} AND associationId IN (SELECT associationId FROM association where deleted = {} and subjectId = {});'.format(
                    0, 0, entity_id)

            elif related_kind == 'class':
                # An especial case, it needed info in special format to show in the view.
                query = 'select cls.classId, cls.course, cls.word, cls.level, t.name, t.surname, t.teacherId, i.impartId, cls.associationId from (select * from impart where impart.deleted = 0) i JOIN (select course, word, level, c.classId, a.associationId from (select course, word, level, classId from class) c ' \
                        'JOIN (select classId, associationId from association where subjectId=' + entity_id + ' AND association.deleted = 0 ) a where c.classId = a.classId) cls JOIN teacher t where i.associationId = cls.associationId and i.teacherId = t.teacherId union select c.classId, c.course, c.word, c.level, null, null, null, null,  a.associationId   ' \
                        'from (select classId, associationId from association where subjectId=' + entity_id + ' AND association.deleted = 0 ) a JOIN class c where a.classId = c.classId;'

            # TODO: La gestión de este error como en las llamadas anteriores puede reducirse en código:

            else:
                log = '   {}    is not a valid nested resource to subject. There are the valid options: ' \
                      'student, teacher, association, impart, enrollment, class'.format(related_kind)
                status = 1054  # Bad request
                return ({'status': status, 'log': log})



        #status_value, num_elements, log = sql_executor(cursor, query)
        return_dic = sql_executor(query, 'list')

        """
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
        """

        # Optional SORTERS CALLs

        if with_special_sorter:

            if kind == 'teacher' and related_kind == 'impart' and return_dic['status'] == 1:
                return_dic['data'] = sorters.special_sort(return_dic['data'])

            if kind == 'student' and related_kind == 'enrollment' and return_dic['status'] == 1:
                return_dic['data'] = sorters.special_sort_2(return_dic['data'])

            if kind == 'subject' and related_kind == 'class' and return_dic['status'] == 1:
                return_dic['data'] = sorters.special_sort_3(return_dic['data'])

            if kind == 'class' and related_kind == 'subject' and return_dic['status'] == 1:
                return_dic['data'] = sorters.special_sort_4(return_dic['data'])

        return return_dic

    @classmethod
    def get_report(cls, kind, entity_id):

        print colored('GET REPORT', 'red')
        return_dic = {}
        set_lack_data_message = False

        if kind in ['class', 'subject']:  # We will made the reports of this kind of item.

            data_block = {}

            # Students analysis:
            #students = cls.get(kind='student', params='birthdate,gender').get('data', None)
            students = cls.get_related(kind=kind, entity_id=entity_id, related_kind='student').get('data', None)


            # Count:
            num_students = len(students)

            if num_students == 0:
                data_block['report_log'] = None

                return_dic['data'] = data_block
                return_dic['status'] = 1

                return return_dic

            data_block['students'] = {}

            data_block['students']['count'] = num_students

            # Gender:
            f = 0
            m = 0
            for student in students:
                print student
                gender = student.get('gender', None)
                if gender is not None:
                    if gender == 'F':
                        f += 1
                    elif gender == 'M':
                        m += 1
                else:
                    set_lack_data_message = True

            # Gender percentage:
            if f+m != 0:
                f_per = (f * 100) / (f + m)
                m_per = (m * 100) / (f + m)
            else:
                f_per = 0
                m_per = 0

            data_block['students']['gender_percentage'] = {'M': m_per, 'F': f_per}

            # Medium age:
            if f + m != 0:
                ages = []
                medium_age = 0
                for student in students:
                    print student
                    birthdate = student.get('birthdate', None)
                    if birthdate != None:
                        print birthdate
                        print type(birthdate)
                        # birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
                        ages.append(datetime.date.today().year - birthdate.year)
                    else:
                        set_lack_data_message = True

                medium_age = sum(ages) / len(ages)

            else:
                medium_age = None

            data_block['students']['medium_age'] = medium_age

            if set_lack_data_message:
                data_block['report_log'] = 'data lack'  # Meaning that some data is missing .

            return_dic['data'] = data_block
            return_dic['status'] = 1

            return return_dic



        pass
