# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Profesor de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Profesor import *
from Alumno import *
from Asignatura import *
from Clase import *
#Uso de variables generales par la conexión a la BD.
import dbParams
#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v = 1
apiName='\n## API DB ##\n'

'''Clase controladora de profesores. Que usando la clase que define el modelo de Profesor (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorProfesores:
    """
    Manejador de Profesors de la base de datos.
    """

    @classmethod
    def nuevoProfesor(self, nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL'):
        '''
        Introduce un nuevo elemento Profesor en la base de datos.
        Necesita como mínimo un nombre y un dni
        '''

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.

        nombre='\''+nombre+'\''
        if(apellidos!='NULL'):
            apellidos='\''+apellidos+'\''
        #DNI se pasa como un entero y no es necesario comillarlo.
        if(direccion!='NULL'):
            direccion='\''+direccion+'\''
        if(localidad!='NULL'):
            localidad='\''+localidad+'\''
        if(provincia!='NULL'):
            provincia='\''+provincia+'\''
        if(fecha_nacimiento!='NULL'):
            fecha_nacimiento='\''+fecha_nacimiento+'\''
        if(telefono!='NULL'):
            telefono='\''+telefono+'\''

        query="INSERT INTO Profesor VALUES(NULL,"+nombre+","+apellidos+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nacimiento+","+telefono+");"

        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Profesor con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==1062:
            return 'Elemento duplicado'

    @classmethod
    def getProfesores(self):
        '''Devuelve una lista simplificada de todos los profesores registrados en el sistema, con los campos nombre,
        apellidos y dni.'''

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select nombre, apellidos, id_profesor from Profesor"

        if v:
            print apiName
            print "getProfesores()"
            print "query: "+query

        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            print row
            profesor = Profesor()

            profesor.nombre=row[0]
            profesor.apellidos=row[1]
            profesor.id=row[2]

            lista.append(profesor)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getProfesor(self, idProfesor):
        """
        Recupera TODA la información de un Profesor en concreto a través de la clave primaria, su DNI.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Profesor where id_profesor='"+idProfesor+"';"

        if v:
            print '\n'+query

        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        cursor.close()
        db.close()

        if salida==1:
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Profesor.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            profesor = Profesor()
            profesor.id = row[0]
            profesor.nombre=row[1]
            profesor.apellidos=row[2]
            profesor.dni=row[3]
            profesor.direccion=row[4];
            profesor.localidad=row[5];
            profesor.provincia=row[6];
            profesor.fecha_nacimiento=row[7];
            profesor.telefono=row[8];


            return profesor
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modProfesor(self, idProfesor, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un Profesor.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idProfesor='\''+idProfesor+'\''
        query="UPDATE Profesor SET "+campoACambiar+"="+nuevoValor+" WHERE id_profesor="+idProfesor+";"
        if v:
            print '\n'+query;



        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Profesor con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        elif salida==1062:
            return 'Elemento duplicado'
        elif salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modProfesorCompleto(self, idProfesor, nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL'):
        '''
        Modifica todos los atributos de un profesor dado su id al mismo tiempo.
        '''

        #Info de seguimiento
        if v:
            print apiName
            print "Llamada a modProfesorCompleto"
            print '\n'

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db);
        query="UPDATE Profesor SET"
        query=query+" nombre= "+'\''+nombre+'\''
        query=query+" , apellidos= "+'\''+apellidos+'\''
        if dni=='NULL':
            query=query+" , dni=NULL "
        else:
            query=query+" , dni= "+'\''+dni+'\''
        query=query+" , direccion= "+'\''+direccion+'\''
        query=query+" , localidad= "+'\''+localidad+'\''
        query=query+" , provincia= "+'\''+provincia+'\''

        if fecha_nacimiento=='NULL':
            query=query+" , fecha_nacimiento=NULL "
        else:
            query=query+" , fecha_nacimiento= "+'\''+fecha_nacimiento+'\''


        query=query+" , telefono= "+'\''+telefono+'\''
        query=query+" WHERE id_profesor="+idProfesor+";"

        if v:
            print apiName
            print query

        cursor = db.cursor()
        salida =''

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        if v:
            print "Salida MySQL: "+str(salida)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        elif salida==1062:
            return 'Elemento duplicado'
        elif salida==0:
            return 'Sin cambios realizados'


    @classmethod
    def delProfesor(self, idProfesor):
        #print "Intentado eliminar profesor con dni "+str(dniProfesor)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Profesor where id_profesor='"+idProfesor+"';"
        if v:
            print '\n'+query
        salida =''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)



        #print str(cursor)
        db.commit()

        #print cursor.fetchone()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def getNumProfesores(self):
        '''Devuelve el número de profesores de la BD'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select count(*) from Profesor;"
        salida =''
        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)



        #print str(cursor)
        db.commit()

        #print cursor.fetchone()
        cursor.close()
        db.close()

        if salida==1:
            return row[0]
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def getAlumnos(self, idProfesor):
        """
        Devuelve una lista con los alumnos al que imparte clase ese profesor, incluyendo
        los campos id, nombre, apellidos y dni de los alumnos del profesor

        Argumentos:

            dniProfesor: El dni del profsor del que se pide la información.<

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='SELECT id_alumno, nombre, apellidos from Alumno where id_alumno in (select id_alumno from Matricula where id_asignatura in (select id_asignatura from Imparte where id_profesor='+idProfesor+') AND id_clase in (select id_clase from Imparte where id_profesor='+idProfesor+'))'

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        if salida>=0: #La consulta ha tenido exito
            row = cursor.fetchone()
            lista = []
            while row is not None:
                alumno = Alumno()
                alumno.nombre=row[0]
                alumno.dni=row[1]
                lista.append(alumno)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getAsignaturas(self, idProfesor):
        """Devuelve una lista con las asignaturas que ese profesor imparte.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='select * from Asignatura where id_asignatura in (select id_asignatura from Imparte where id_profesor ='+idProfesor+');'

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        print "SALIDA"+str(salida)
        if salida>=0: #La consulta ha tenido exito
            row = cursor.fetchone()
            lista = []
            while row is not None:
                asignatura = Asignatura()
                #En esta consulta el identificador de la asignatura se encuentra en la primera posicion.
                asignatura.id=row[0]
                asignatura.nombre=row[1]
                lista.append(asignatura)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getClases(self, idProfesor):
        """
        Devuelve una lista con las clases en los que ese profesor da clase, normalmente será al menos uno.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='SELECT * FROM Clase where id_clase in (select id_clase from Imparte where id_profesor='+idProfesor+')'

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        print "SALIDA"+str(salida)
        if salida>=0: #La consulta ha tenido exito
            row = cursor.fetchone()
            lista = []
            while row is not None:
                clase = Clase()
                #En esta consulta el identificador de la asignatura se encuentra en la primera posicion.
                clase.id=row[0]
                clase.curso=row[1]
                clase.grupo=row[2]
                clase.nivel=row[3]
                lista.append(clase)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
