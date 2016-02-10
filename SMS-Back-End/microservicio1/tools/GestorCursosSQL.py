# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Curso de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Curso import *

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=0

'''Clase controladora de Cursos. Que usando la clase que define el modelo de Curso (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorCursos:
    """
    Manejador de Cursos de la base de datos.
    """

    @classmethod
    def nuevoCurso(self, id, curso, grupo, nivel):

        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        #query="INSERT INTO Curso values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        id='\''+id+'\''
        curso='\''+curso+'\''
        grupo='\''+grupo+'\''
        nivel='\''+nivel+'\''

        query="INSERT INTO Curso VALUES("+id+","+curso+","+grupo+","+nivel+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Curso con clave
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
    def getCursos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm")
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Curso"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            curso = Curso()
            curso.id=row[0]
            curso.curso=row[1]
            curso.grupo=row[2];
            curso.nivel=row[3];


            lista.append(curso)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getCurso(self, idCurso):
        """
        Recupera TODA la información de un Curso en concreto a través de la clave primaria, su id.
        """
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Curso where id='"+idCurso+"';"
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
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Curso.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            curso = Curso()
            curso.id=row[0]
            curso.curso=row[1]
            curso.grupo=row[2]
            curso.nivel=row[3]


            return curso
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modCurso(self, idCurso, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un Curso.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idCurso='\''+idCurso+'\''
        query="UPDATE Curso SET "+campoACambiar+"="+nuevoValor+" WHERE id="+idCurso+";"
        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Curso con clave
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
    def delCurso(self, idCurso):
        if v:
            print "Intentado eliminar Curso con id "+str(idCurso)
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Curso where id='"+idCurso+"';"
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
