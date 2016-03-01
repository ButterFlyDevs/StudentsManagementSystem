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
v=0

'''Clase controladora de profesores. Que usando la clase que define el modelo de Profesor (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorProfesores:
    """
    Manejador de Profesors de la base de datos.
    """

    @classmethod
    def nuevoProfesor(self, nombre, dni, direccion, localidad, provincia, fecha_nac, telefonoA, telefonoB):

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        #query="INSERT INTO Profesor values("+"'"+nombre+"', "+ "'"+dni+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        nombre='\''+nombre+'\''
        dni='\''+dni+'\''
        direccion='\''+direccion+'\''
        localidad='\''+localidad+'\''
        provincia='\''+provincia+'\''
        fecha_nac='\''+fecha_nac+'\''
        telefonoA='\''+telefonoA+'\''
        telefonoB='\''+telefonoB+'\''

        query="INSERT INTO Profesor VALUES("+nombre+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefonoA+","+telefonoB+");"

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
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Profesor"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            profesor = Profesor()
            #print "LISTA SUPER CHACHI"

            profesor.nombre=row[0]
            profesor.dni=row[1]
            profesor.direccion=row[2];
            profesor.localidad=row[3];
            profesor.provincia=row[4];
            profesor.fecha_nac=row[5];
            profesor.telefonoA=row[6];
            profesor.telefonoB=row[7];


            lista.append(profesor)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getProfesor(self, dniProfesor):
        """
        Recupera TODA la información de un Profesor en concreto a través de la clave primaria, su DNI.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Profesor where dni='"+dniProfesor+"';"

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
            profesor.nombre=row[0]
            profesor.dni=row[1]
            profesor.direccion=row[2];
            profesor.localidad=row[3];
            profesor.provincia=row[4];
            profesor.fecha_nac=row[5];
            profesor.telefonoA=row[6];
            profesor.telefonoB=row[7];

            return profesor
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modProfesor(self, dniProfesor, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un Profesor.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        dniProfesor='\''+dniProfesor+'\''
        query="UPDATE Profesor SET "+campoACambiar+"="+nuevoValor+" WHERE dni="+dniProfesor+";"
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
    def delProfesor(self, dniProfesor):
        #print "Intentado eliminar profesor con dni "+str(dniProfesor)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Profesor where dni='"+dniProfesor+"';"
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
    def getAlumnos(self, dniProfesor):
        """
        Devuelve una lista con los alumnos al que imparte clase ese profesor.

        Argumentos:

            dniProfesor: El dni del profsor del que se pide la información.


        Extra: ¿Se debería añadir la comprobación de existencia del profesor?

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query="select * from Matricula, Imparte where Matricula.curso = Imparte.curso and Matricula.grupo = Imparte.grupo and Matricula.nivel = Imparte.nivel and Matricula.id_asignatura = Imparte.id_asignatura and id_profesor ="+dniProfesor+";"

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
    def getAsignaturas(self, dniProfesor):
        """Devuelve una lista con las asignaturas que ese profesor imparte.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query="select * from Imparte where id_profesor="+dniProfesor+";"

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
                asignatura.id=row[3]
                asignatura.nombre=row[4]
                lista.append(asignatura)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getClases(self, dniProfesor):
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
        query="select distinct curso, grupo, nivel from Imparte where id_profesor="+dniProfesor+";"

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
                clase.id=row[3]
                clase.curso=row[4]
                clase.grupo=row[5]
                clase.nivel=row[6]
                lista.append(clase)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
