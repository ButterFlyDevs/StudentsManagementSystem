# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Asignatura de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Asignatura import *
from Clase import *
from Profesor import *
from Alumno import *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=0

'''Clase controladora de Asignaturas. Que usando la clase que define el modelo de Asignatura (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAsignaturas:
    """
    Manejador de Asignaturas de la base de datos.
    """

    @classmethod
    def nuevaAsignatura(self, id, nombre):

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        #query="INSERT INTO Asignatura values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        nombre='\''+nombre+'\''
        id='\''+id+'\''

        query="INSERT INTO Asignatura VALUES("+id+","+nombre+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asignatura con clave
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
    def getAsignaturas(self):
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Asignatura"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            asignatura = Asignatura()
            #print "LISTA SUPER CHACHI"

            asignatura.id=row[0]
            asignatura.nombre=row[1]


            lista.append(asignatura)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAsignatura(self, idAsignatura):
        """
        Recupera TODA la información de un Asignatura en concreto a través de la clave primaria, su id.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Asignatura where id='"+idAsignatura+"';"
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
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Asignatura.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            asignatura = Asignatura()
            asignatura.id=row[0]
            asignatura.nombre=row[1]


            return asignatura
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modAsignatura(self, idAsignatura, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un Asignatura.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idAsignatura='\''+idAsignatura+'\''
        query="UPDATE Asignatura SET "+campoACambiar+"="+nuevoValor+" WHERE id="+idAsignatura+";"
        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asignatura con clave
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
    def delAsignatura(self, idAsignatura):
        if v:
            print "Intentado eliminar asignatura con id "+str(idAsignatura)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Asignatura where id='"+idAsignatura+"';"
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

        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def getClases(self, idAsignatura):
        '''
        Devuelve una lista con todos los clases donde se imparte la asignatura.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idAsignatura='\''+idAsignatura+'\''
        query='select * from Asocia where id_asignatura='+idAsignatura+';'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            clase = Clase()
            #print "LISTA SUPER CHACHI"

            clase.curso=row[0]
            clase.grupo=row[1]
            clase.nivel=row[2]

            lista.append(clase)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getProfesores(self, idAsignatura):
        '''
        Devuelve una lista con todos los profesores que imparte clase en esa asignatura.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idAsignatura='\''+idAsignatura+'\''
        query='select distinct id_profesor from Imparte where id_asignatura='+idAsignatura+';'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            profesor = Profesor()
            profesor.dni=row[0]
            lista.append(profesor)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getAlumnos(self, idAsignatura):
        '''
        Devuelve una lista con todos los alumnos matriculados en esa asignatura en total.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idAsignatura='\''+idAsignatura+'\''
        '''
        Con el distinct evitamos que si un alumno por casualidad esta matriculado en lengua de primero
        y lengua de segundo porque así se permite se contabilice como dos alumnos en el recuento, lo que sería un error.
        '''
        query='select distinct id_alumno from Matricula where id_asignatura='+idAsignatura+';'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.dni=row[0]
            lista.append(alumno)
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista
