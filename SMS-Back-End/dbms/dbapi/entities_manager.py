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

import pytz

# Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v = 1

def special_sort(list):
    """
    Sort with a special way the items of the list.
    :param list:
    :return:
    See example in newTest.py test file.
    """

    sorted_list = []

    for list_element in list:

        if len(sorted_list) == 0:
            new_subject = {'subjectId': list_element.get('subjectId'),
                           'name': list_element.get('name')
                           }
            new_class = {'classId': list_element.get('classId'),
                         'course': list_element.get('course'),
                         'level': list_element.get('level'),
                         'word': list_element.get('word'),
                         'impartId': list_element.get('impartId')}

            sorted_list.append({'subject': new_subject, 'classes': [new_class]})

        else:
            index = -1
            for item in sorted_list:
                if item["subject"]["subjectId"] == list_element.get("subjectId"):
                    index = sorted_list.index(item)

            if index != -1:
                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word'),
                             'impartId': list_element.get('impartId')}

                sorted_list[index]["classes"].append(new_class)

            else:
                new_subject = {'subjectId': list_element.get('subjectId'),
                               'name': list_element.get('name')
                               }
                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word'),
                             'impartId': list_element.get('impartId')}

                sorted_list.append({'subject': new_subject, 'classes': [new_class]})

    return sorted_list


def special_sort_2(list):
    """
    Sort with a special way the items of the list.
    :param list:
    :return:
    See example in newTest.py test file.
    """

    sorted_list = []

    for list_element in list:

        if len(sorted_list) == 0:
            new_class = {'classId': list_element.get('classId'),
                         'course': list_element.get('course'),
                         'level': list_element.get('level'),
                         'word': list_element.get('word')}

            new_subject = {'subjectId': list_element.get('subjectId'),
                           'name': list_element.get('name'),
                           'enrollmentId': list_element.get('enrollmentId')
                           }

            sorted_list.append({'class': new_class, 'subjects': [new_subject]})

        else:
            index = -1
            for item in sorted_list:
                if item["class"]["classId"] == list_element.get("classId"):
                    index = sorted_list.index(item)

            if index != -1:
                new_subject = {'subjectId': list_element.get('subjectId'),
                               'name': list_element.get('name'),
                               'enrollmentId': list_element.get('enrollmentId')
                               }
                sorted_list[index]["subjects"].append(new_subject)

            else:
                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word')}

                new_subject = {'subjectId': list_element.get('subjectId'),
                               'name': list_element.get('name'),
                               'enrollmentId': list_element.get('enrollmentId')
                               }

                sorted_list.append({'class': new_class, 'subjects': [new_subject]})

    return sorted_list



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
    Gestor de entidades de la base de datos, que abstrae el funcionamiento de MySQL
    """

    @classmethod
    def put(cls, kind, data):
        """
        Insert data entity in the database or a relation entity between two of them.
        :param kind: Type of data, student, teacher, class, etc.
        :param data: A dict with the data, like : {"name": "Juan", "dni": 9999999}
        :return: A dict with two fields, the status code and the row that is inserted retrieved just after that be
        saved in database.
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

        for key, value in data.iteritems():
            query += str(key) + ', '

        # The same with control_fields keys
        for key, value in control_fields.iteritems():
            query += str(key) + ', '

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
                row = dict((k, v) for k, v in row.iteritems() if v)

                print colored(row, 'magenta')

                return_dic['data'] = row

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
        :return: A dict with all info about one or a list with dicts.
        """

        if v:
            print colored(locals(), 'blue')

        db = db_params.conecta()
        return_dic = {}
        cursor = db.cursor()

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

            query += ' from ' + str(kind) + ' where deleted = 0;'

        # We want all info about one entity.
        else:
            query += '* from ' + str(kind) + ' where ' + str(kind) + 'Id = ' + str(entity_id) + ' and deleted = 0;'

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
        Update info about a entity.
        :param kind:
        :param entity_id:
        :param data:
        :return:
        """

        if v:
            print colored(locals(), 'blue')

        db = db_params.conecta();
        return_dic = {}

        control_fields = {'modifiedBy': 1, 'modifiedAt': datetime.datetime.now()}

        query = 'UPDATE ' + str(kind) + ' SET '

        for key, value in data.iteritems():
            if isinstance(value, int):
                value = str(value)
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

        # Confirm the changes
        db.commit()
        cursor.close()
        db.close()

        return return_dic

    @classmethod
    def delete(cls, kind, entity_id):

        return cls.update(kind, entity_id, {'deleted': 1})

    @classmethod
    def get_related(cls, kind, entity_id, related_kind):
        """Devuelve una lista de diccionarios con la información pedida."""

        kind = str(kind)
        entity_id = str(entity_id)
        related_kind = str(related_kind)

        return_dic = {}

        print locals()

        db = db_params.conecta()
        cursor = db.cursor()

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
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId in (SELECT subjectId FROM association WHERE classId =' + entity_id + ')'

        elif kind == 'subject':  # Queremos buscar entidades relacionadas con una entidad de tipo subject.
            if related_kind == 'student':
                query = 'SELECT studentId, name, surname from student where deleted = 0 and studentId in (SELECT studentId from enrollment where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'
            elif related_kind == 'teacher':
                query = 'SELECT teacherId, name, surname from teacher where deleted = 0 and teacherId in (select teacherId from impart where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'
            elif related_kind == 'class':
                query = 'SELECT classId, course, word, level from class where deleted = 0 and idClase in (select idClase from association where subjectId=' + entity_id + ')'

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

        if related_kind == 'impart' and status_value == 1:
            return_dic['data'] = special_sort(return_dic['data'])

        if related_kind == 'enrollment' and status_value == 1:
            return_dic['data'] = special_sort_2(return_dic['data'])


        return return_dic
