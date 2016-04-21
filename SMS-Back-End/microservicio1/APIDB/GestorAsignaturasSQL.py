# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Asignatura de la base de datos.
"""


from Asignatura import *
from Clase import *
from Profesor import *
from Alumno import *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1
apiName='\n## API DB ##\n'

'''Clase controladora de Asignaturas. Que usando la clase que define el modelo de Asignatura (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAsignaturas:
    """
    Manejador de Asignaturas de la base de datos.
    """

    @classmethod
    def nuevaAsignatura(self, nombre):

        if v:
            print 'Calling nuevaAsignatura() with params:'
            print locals()

        db = dbParams.conecta() #La conexión está clara.
        #query="INSERT INTO Asignatura values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        nombre='\''+nombre+'\''

        query='INSERT INTO Asignatura VALUES(NULL'+','+nombre+');'

        if v:
            print query


        cursor = db.cursor()
        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
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
        db = dbParams.conecta()
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
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Asignatura where id_asignatura='"+idAsignatura+"';"
        if v:
            print '\n'+query
        try:
            #Sacando los acentos...........
            mysql_query="SET NAMES 'utf8'"
            cursor.execute(mysql_query)
            #-----------------------------#
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
        db = dbParams.conecta(); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idAsignatura='\''+idAsignatura+'\''
        query="UPDATE Asignatura SET "+campoACambiar+"="+nuevoValor+" WHERE id_asignatura="+idAsignatura+";"
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
    def modAsignaturaCompleta(self, idAsignatura, nombre):
        '''
        Modifica todos los atributos de una asignatura dado su id al mismo tiempo.
        '''

        #Info de seguimiento
        if v:
            print apiName
            print "Llamada a modAsignaturaCompleta"
            print '\n'

        db = dbParams.conecta();
        query="UPDATE Asignatura SET"
        query=query+" nombre= "+'\''+nombre+'\''
        query=query+" WHERE id_asignatura="+idAsignatura+";"

        if v:
            print apiName
            print query.encode('utf-8')

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
    def delAsignatura(self, idAsignatura):
        if v:
            print "Intentado eliminar asignatura con id "+str(idAsignatura)
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Asignatura where id_asignatura='"+idAsignatura+"';"
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
    def getNumAsignaturas(self):
        '''Devuelve el número de asignaturas de la BD'''
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query="select count(*) from Asignatura;"
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

    #Métodos que extraen información de relación con otras entidades:

    @classmethod
    def getClases(self, idAsignatura):
        '''
        Devuelve una lista con todos los clases donde se imparte la asignatura.
        '''
        db = dbParams.conecta()
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idAsignatura='\''+idAsignatura+'\''
        query='select id_clase, curso, grupo, nivel from Clase where id_clase in (select id_clase from Asocia where id_asignatura='+idAsignatura+')'
        #query='select id_profesor, nombre, apellidos from Profesor where id_profesor in (select id_asignatura from Imparte where id_asignatura='+idAsignatura+');'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            clase = Clase()
            #print "LISTA SUPER CHACHI"

            clase.id=row[0]
            clase.curso=row[1]
            clase.grupo=row[2]
            clase.nivel=row[3]

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
        db = dbParams.conecta()
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idAsignatura='\''+idAsignatura+'\''
        #query='select distinct id_profesor from Imparte where id_asignatura='+idAsignatura+';'
        query='SELECT id_profesor, nombre, apellidos from Profesor where id_profesor in (select id_profesor from Imparte where id_asociacion IN ( select id_asociacion from Asocia where id_asignatura='+idAsignatura+'));'

        #query='SELECT id_profesor, nombre, apellidos from Profesor where id_profesor IN (select id_profesor from Imparte where id_asociacion = (select id_asociacion from Asocia where id_clase='+idClase+'))';
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            profesor = Profesor()
            profesor.id=row[0]
            profesor.nombre=row[1]
            profesor.apellidos=row[2]
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
        db = dbParams.conecta()
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
        #query='select id_alumno, nombre, apellidos from Alumno where id_alumno in (select id_alumno from Matricula where id_asignatura ='+idAsignatura+' )'

        query='SELECT id_alumno, nombre, apellidos from Alumno where id_alumno in (select id_alumno from Matricula where id_asociacion IN ( select id_asociacion from Asocia where id_asignatura='+idAsignatura+'));'

        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.id=row[0]
            alumno.nombre=row[1]
            alumno.apellidos=row[2]
            lista.append(alumno)
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista
