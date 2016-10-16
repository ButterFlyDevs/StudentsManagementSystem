# -*- coding: utf-8 -*-
"""
Prueba de unión de métodos de entidades.

DATOS:

Si se trata de enteros: enteros
Si se trata de texto: en unicode
Si se trata de booleanos : boolean

"""


# Uso de variables generales par la conexión a la BD.
import dbParams
import datetime
from termcolor import colored

import pytz

# Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v = 1
apiName = '\n## API DB ##\n'

'''Clase controladora de Asignaturas. Que usando la clase que define el modelo de Asignatura (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''

def sql_execute(cursor, query): # References

    status_value = 1  # By default is success.
    num_elements = 0  # By default any entity is retrieved.

    try:
        num_elements = cursor.execute(query);
    except dbParams.MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print "Error number: " + str(e.args[0])
            status_value = e.args[0]
        except IndexError:
            print "MySQL Error: %s" % str(e)

    return status_value, num_elements

class entitiesManager:
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

        db = dbParams.conecta()
        return_dic = {}

        now = datetime.datetime.utcnow()
        tz = pytz.timezone('Europe/Madrid')
        tzoffset = tz.utcoffset(now)
        mynow = now+tzoffset

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

        status_value = 1 # By default is success.
        num_elements = 0 # By default any entity is retrieved.

        try:
            num_elements = cursor.execute(query);
            entity_id = cursor.lastrowid
        except dbParams.MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: " + str(e.args[0])
                status_value = e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        db.commit()

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if status_value == 1:

            retrieve_query = 'select * from ' + kind + ' where ' + kind + 'Id = ' + str(entity_id) + ';'
            print colored(retrieve_query, 'green')

            if cursor.execute(retrieve_query) == 1: # If query obtain one element.
                row = cursor.fetchone()
                # None values are not necessary.
                row = dict((k, v) for k, v in row.iteritems() if v)

                print colored(row, 'magenta')

                return_dic['data'] = row

        return_dic['status'] = status_value

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

        db = dbParams.conecta()
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

        status_value, num_elements = sql_execute(cursor, query)

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

                if num_elements != 0: # If the element exists in database.

                    row = dict((k, v) for k, v in cursor.fetchone().iteritems() if v) # To delete None values
                    return_dic['data'] = row

                else: # If doesn't exists.
                    status_value = -1

        return_dic['status'] = status_value

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

        db = dbParams.conecta();
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

        status_value, num_elements = sql_execute(cursor, query)

        db.commit()

        # If the query execute has success we are going to retrieve all data saved in database about this item.
        if status_value == 1 and num_elements == 1:

            retrieve_query = 'select * from ' + str(kind) + ' where ' + str(kind) + 'Id = ' + str(entity_id) + ';'
            print colored(retrieve_query, 'green')

            if cursor.execute(retrieve_query) == 1:  # If query obtain one element.
                row = cursor.fetchone()
                # None values are not necessary.
                row = dict((k, v) for k, v in row.iteritems() if v)

                print colored(row, 'magenta')

                return_dic['data'] = row

        if num_elements == 1:
            return_dic['status'] = status_value
        else:
            return_dic['status'] = -1

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

        """
        getEntidadesRelacioandas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Profesor')
            Devuelve todos los profesores que imparten clase a ese alumno.
        getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Asignatura')
            Devuelve todas las asignaturas en la que está matriculado ese alumno.
        getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Clases')
            Devuelve todas las clases en las que está matriculado ese alumno.

        Toda la información de las entidades se devuelve en su versión resumida.
        """

        kind = str(kind)
        entity_id = str(entity_id)
        related_kind = str(related_kind)

        return_dic={}

        print locals()

        db = dbParams.conecta()
        cursor = db.cursor()

        query = ''

        if kind == 'student':  # Queremos buscar entidades relacionadas con una entidad de tipo student

            if related_kind == 'teacher':  # Todos los profesores que dan clase al alumno.
                query = 'SELECT teacherId, name, surname FROM teacher WHERE deleted = 0 and teacherId IN (SELECT teacherId FROM impart, enrollment WHERE impart.associationId=enrollment.associationId and enrollment.studentId=' + entity_id + ');'

            elif related_kind == 'class':  # Todos las clases en las que está matriculado el alumno.
                query = 'SELECT classId, course, word, level FROM class WHERE deleted = 0 and classId IN (SELECT classId FROM association WHERE associationId IN (SELECT associationId FROM enrollment WHERE studentId=' + entity_id + '));'

            elif related_kind == 'subject':  # Todas las asignaturas en la que está matriculado el alumno.
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId IN (SELECT subjectId FROM association WHERE associationId IN (SELECT associationId FROM enrollment WHERE studentId=' + entity_id + '));'

        elif kind == 'teacher':  # Queremos buscar entidades relacionadas con una entidad de tipo teacher
            if related_kind == 'student':  # Todos los alumnos a los que da clase ese profesor.
                query = 'SELECT studentId, name, surname  FROM student WHERE deleted = 0 and studentId IN (SELECT studentId FROM impart, enrollment WHERE impart.associationId=enrollment.associationId AND impart.teacherId=' + entity_id + ');'
            elif related_kind == 'class':  # Todos las clases en las que el profesor imparte.
                query = 'SELECT classId, course, word, level FROM class WHERE deleted = 0 and classId IN (SELECT classId FROM association where associationId IN(SELECT associationId FROM impart WHERE teacherId=' + entity_id + '));'
            elif related_kind == 'subject':  # Todas las asignaturas que el profesor imparte.
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId IN (SELECT subjectId FROM association WHERE associationId IN (SELECT associationId FROM impart WHERE teacherId=' + entity_id + '));'

        elif kind == 'class':  # Queremos buscar entidades relacionadas con una entidad de tipo class.
            if related_kind == 'student':  # Todos los alumnos matriculados en esa clase.
                query = 'SELECT studentId, name, surname FROM student WHERE deleted = 0 and studentId IN (SELECT studentId FROM enrollment WHERE associationId IN (SELECT associationId FROM association WHERE classId=' + entity_id + '));'
            elif related_kind == 'teacher':  # Todos los profesores que imparten en esa clase alguna asignatura.
                query = 'SELECT teacherId, name, surname FROM teacher WHERE deleted = 0 and teacherId IN (SELECT teacherId FROM impart WHERE associationId IN (SELECT associationId FROM association WHERE classId=' + entity_id + '))';
            elif related_kind == 'subject':  # Todas las asignaturas que se imparten en esa clase.
                query = 'SELECT subjectId, name FROM subject WHERE deleted = 0 and subjectId in (SELECT subjectId FROM association WHERE classId =' + entity_id + ')'

        elif kind == 'subject':  # Queremos buscar entidades relacionadas con una entidad de tipo subject.
            if related_kind == 'student':
                query = 'SELECT studentId, name, surname from student where deleted = 0 and studentId in (select studentId from enrollment where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'
            elif related_kind == 'teacher':
                query = 'SELECT teacherId, name, surname from teacher where deleted = 0 and teacherId in (select teacherId from impart where associationId IN ( select associationId from association where subjectId=' + entity_id + '));'
            elif related_kind == 'class':
                query = 'SELECT classId, course, word, level from class where deleted = 0 and idClase in (select idClase from association where subjectId=' + entity_id + ')'

        if v:
            print colored(query, 'yellow')

        status_value, num_elements = sql_execute(cursor, query)

        if status_value == 1:

            if num_elements > 0:

                row = cursor.fetchone()
                entities_list = []
                while row is not None:
                    row = dict((k, v) for k, v in row.iteritems() if v)  # To delete None values
                    entities_list.append(row)
                    row = cursor.fetchone()

                print entities_list
                return_dic['data'] = entities_list

            else: # If doesn't exists.
                status_value = -1

        return_dic['status'] = status_value

        db.commit()
        cursor.close()
        db.close()

        return return_dic
