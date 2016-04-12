# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la relacion Imparte de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Imparte import *
#Uso de variables generales par la conexión a la BD.
import dbParams
#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1

'''Clase controladora de Impartes. Que usando la clase que define el modelo de Imparte (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorImpartes:
    """
    Manejador de Impartes de la base de datos.
    """

    @classmethod
    def nuevoImparte(self, id_asociacion, id_profesor):
        '''Introduce una tupla en la tabla Imparte de la base de datos'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db);
        #query="INSERT INTO Imparte values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        id_asociacion='\''+id_asociacion+'\''
        id_profesor='\''+id_profesor+'\''

        query="INSERT INTO Imparte VALUES(NULL, "+id_asociacion+","+id_profesor+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Imparte con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=str(e.args[0])
            except IndexError:
                print "MySQL Error: %s" % str(e)


        print "key"+str(salida)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==1062:
            return 'Elemento duplicado'
        if salida=='1452':
            print 'Alguno de los elemento'
            return 'Alguno de los elementos no existe'

    @classmethod
    def getImpartes(self):
        '''Devuelve una lista simlifacada de todos los elementos Imparte de la tabla imparte de la bd'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Imparte"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            imparte = Imparte()
            imparte.id_clase=row[0]
            imparte.id_asignatura=row[1]
            imparte.id_profesor=row[2]

            lista.append(imparte)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getImparte(self, id_clase, id_asignatura, id_profesor):
        ''' Recupera TODA la información de un Imparte en concreto a través de la clave primaria, su id. '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        id_clase='\''+id_clase+'\''
        id_asignatura='\''+id_asignatura+'\''
        id_profesor='\''+id_profesor+'\''

        query="select * from Imparte where id_clase="+id_clase+" and id_asignatura="+id_asignatura+" and id_profesor="+id_profesor+";"
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

        cursor.close()
        db.close()

        if salida==1:
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Imparte.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            imparte = Imparte()
            imparte.id_clase=row[0]
            imparte.id_asignatura=row[1]
            imparte.id_profesor=row[2]

            return imparte
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def delImparte(self, id_imparte):
        '''Elimina una tupla imparte de la tabla Imparte'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()
        id_imparte='\''+id_imparte+'\''
        query="delete from Imparte where id_imparte="+id_imparte+";"
        if v:
            print query
        salida =''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
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
    def delImparteSinClave(self, id_asociacion, id_profesor):
        '''Elimina una tupla imparte de la tabla Imparte usando los ides de la asociacion y del profesor,
        se usa cuando no se tiene el id de la tupla imparte en concreto.'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()
        id_asociacion='\''+id_asociacion+'\''
        id_profesor='\''+id_profesor+'\''
        query="DELETE FROM Imparte WHERE id_asociacion="+id_asociacion+" AND id_profesor"+id_profesor+";"
        if v:
            print query
        salida =''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
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
    def modImparte(self, id_clase, id_asignatura, id_profesor, campoACambiar, nuevoValor):
        '''
        Esta función permite cambiar cualquier atributo de una Imparte.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.

        Este caso puede ser delicado al tener sólo dos atributos y ambos ser claves foráneas. Por eso no permitiremos que
        se haga, para modificar la relación antes tendremos que destruirla y volverla a crear.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)

        id_clase='\''+id_clase+'\''
        id_asignatura='\''+id_asignatura+'\''
        id_profesor='\''+id_profesor+'\''

        nuevoValor='\''+nuevoValor+'\''

        #query="UPDATE Imparte SET "+campoACambiar+"="+nuevoValor+" WHERE id_clase="+id_clase+" and id_asignatura="+id_asignatura+" and id_profesor"+id_profesor+";"
        query="UPDATE Imparte SET "+campoACambiar+"="+nuevoValor+" WHERE id_clase="+id_clase+" and id_asignatura="+id_asignatura+" and id_profesor="+id_profesor+";"
        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        '''
        #Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Imparte con clave
        #que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=str(e.args[0])
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if v:
            print salida


        if salida==1:
            print 'OK'
            return 'OK'
        elif salida==1062:
            print 'Elemento duplicado'
            return 'Elemento duplicado'
        elif salida==0:
            return 'Elemento no encontrado'
