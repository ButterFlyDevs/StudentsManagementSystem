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
            print apiName
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

        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asignatura con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        idAsignatura=''
        try:
            salida = cursor.execute(query);
            idAsignatura = cursor.lastrowid
        except dbParams.MySQLdb.Error, e:
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

        #Creamos un diccionario que nos da una salida comprensible de la lib.
        dic={'status':salida, 'idAsignatura':str(idAsignatura)}

        #Transformación de los estados de MYSQL a mensajes comprensibles.
        if salida==1:
            dic['status']= 'OK'
            #return 'OK'
        if salida==1062:
            dic['status']= 'Elemento duplicado'

        return dic

    @classmethod
    def getAsignaturas(self,idAsignatura=None):
        db = dbParams.conecta()
        cursor = db.cursor()

        if idAsignatura != None: #Buscamos una asignatura en concreto
            query="select * from Asignatura where idAsignatura='"+idAsignatura+"';"
        else: #Queremos todas las asignaturas
            query="select * from Asignatura"

        if v:
            print '\n'+query
        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except dbParams.MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        if idAsignatura != None: #Se busca uno en concreto
            if salida == 1:
                #Creamos un objeto de tipo dict con toda la información delp rofesor extraida de la row de la consulta.
                ret = {'id': row[0], 'nombre': row[1]}
            if salida == 0:
                ret = 'Elemento no encontrado'
        else: #Se quieren todos
            asignaturas = [] #Creamos una lista
            while row is not None:
                #Añadimos a la lista un dict con los datos que queremos de la asignatura
                asignaturas.append({'id': row[0], 'nombre': row[1]})
                row = cursor.fetchone()
            ret = asignaturas

        cursor.close()
        db.close()

        return ret

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
        query="UPDATE Asignatura SET "+campoACambiar+"="+nuevoValor+" WHERE idAsignatura="+idAsignatura+";"
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
        except dbParams.MySQLdb.Error, e:
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
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Asignatura where idAsignatura='"+idAsignatura+"';"
        salida =''
        try:
            salida = cursor.execute(query);
        except dbParams.MySQLdb.Error, e:
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
        except dbParams.MySQLdb.Error, e:
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
        query='select id_clase, curso, grupo, nivel from Clase where id_clase in (select id_clase from Asocia where idAsignatura='+idAsignatura+')'
        #query='select id_profesor, nombre, apellidos from Profesor where id_profesor in (select idAsignatura from Imparte where idAsignatura='+idAsignatura+');'
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
        #query='select distinct id_profesor from Imparte where idAsignatura='+idAsignatura+';'
        query='SELECT id_profesor, nombre, apellidos from Profesor where id_profesor in (select id_profesor from Imparte where id_asociacion IN ( select id_asociacion from Asocia where idAsignatura='+idAsignatura+'));'

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
        #query='select id_alumno, nombre, apellidos from Alumno where id_alumno in (select id_alumno from Matricula where idAsignatura ='+idAsignatura+' )'

        query='SELECT id_alumno, nombre, apellidos from Alumno where id_alumno in (select id_alumno from Matricula where id_asociacion IN ( select id_asociacion from Asocia where idAsignatura='+idAsignatura+'));'

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
