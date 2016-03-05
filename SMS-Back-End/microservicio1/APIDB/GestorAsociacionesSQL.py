# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Asociacion de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Asociacion import *
from Alumno import *
from Profesor import *
#Uso de variables generales par la conexión a la BD.
import dbParams
#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1

'''Clase controladora de Asociacions. Que usando la clase que define el modelo de Asociacion (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAsociaciones:
    """
    Manejador de Asociacions de la base de datos.
    """

    @classmethod
    def nuevaAsociacion(self, id_clase, id_asignatura):
        '''Introduce entidades en la tabla Asocia'''

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        id_asignatura='\''+id_asignatura+'\''
        id_clase='\''+id_clase+'\''

        query="INSERT INTO Asocia VALUES("+id_clase+","+id_asignatura+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asociacion con clave
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
        if salida==1452:
            return 'Alguno de los elementos no existe'

    @classmethod
    def getAsociaciones(self):
        '''
        Devuelve una lista simplificada de todas las asociaciones dadas de alta en el sistema.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Asocia"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            asociacion = Asociacion()
            asociacion.id_asignatura=row[0]
            asociacion.id_clase=row[1]

            lista.append(asociacion)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAsociacion(self, id_clase, id_asignatura):
        """
        Recupera TODA la información de un Asociacion en concreto a través de la clave primaria, su id.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        id_clase='\''+id_clase+'\''
        id_asignatura='\''+id_asignatura+'\''

        query="select * from Asocia where id_clase="+id_clase+" and id_asignatura="+id_asignatura+";"
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
                #Capturamos el error:
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        if v:
            print "Salida MySQL: "+str(salida)

        cursor.close()
        db.close()

        if salida==1:
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Asociacion.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            asociacion = Asociacion()
            asociacion.id_asignatura=row[0]
            asociacion.id_clase=row[1]

            return asociacion
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modAsociacion(self, id_clase, id_asignatura, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de una Asociacion.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        Este caso puede ser delicado al tener sólo dos atributos y ambos ser claves foráneas. Por eso no permitiremos que
        se haga, para modificar la relación antes tendremos que destruirla y volverla a crear.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        nuevoValor='\''+nuevoValor+'\''
        id_asignatura='\''+id_asignatura+'\''
        id_clase='\''+id_clase+'\''
        query="UPDATE Asocia SET "+campoACambiar+"="+nuevoValor+" WHERE id_asignatura="+id_asignatura+" and id_clase="+id_clase+";"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        #Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asociacion con clave
        #que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
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

    def delAsociacion(self, id_clase, id_asignatura):
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()
        id_asignatura='\''+id_asignatura+'\''
        id_clase='\''+id_clase+'\''
        query="DELETE FROM Asocia WHERE id_clase="+id_clase+" AND id_asignatura="+id_asignatura+";"

        if v:
            print query
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
    def getNumAsociaciones(self):
        '''Devuelve el número de asociaciones de la BD'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select count(*) from Asocia;"
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


    ##DE RELACIONES CON OTRAS##

    @classmethod
    def getAlumnos(sef, id_asignatura, id_clase):
        '''
        Devuelve una lista con los alumnos matriculados en esa asignatura y grupo
        Devuelve: id del alumno, nombre, apellidos y dni
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        id_clase='\''+id_clase+'\''
        id_asignatura='\''+id_asignatura+'\''
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='select id, nombre, apellidos, dni from Alumno where id in (select id_alumno from Matricula where id_clase ='+id_clase+'and id_asignatura ='+id_asignatura+')'
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
                alumno.dni=row[2]
                lista.append(alumno)
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getProfesores(self, id_asignatura, id_Clase):
        '''
        Devuelve todos los profesores que imparte esa asignatura a ese grupo
        Devuelve nombre, apellidos y dni
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        id_clase='\''+id_clase+'\''
        id_asignatura='\''+id_asignatura+'\''
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='SELECT nombre, apellidos, dni from Profesor where dni in (select id_profesor from Imparte where id_clase='+id_clase+'and id_asignatura='+id_asignatura+')'
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
                profesor = Profesor()
                profesor.dni=row[2]
                lista.append(profesor)
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
