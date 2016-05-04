# -*- coding: utf-8 -*-
"""
@author: Juan A. Fernández
@about: Interfaz de interacción con la entidad Credenciales de la base de datos.
"""


from Asignatura import *
from Clase import *
from Profesor import *
from Alumno import *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1
apiName='\n ## API DB ##'


class Credenciales:

    def __init__(self):
        self.idCredenciales = ""
        self.idUsuario = ""
        self.nombre = ""
        self.username= ""
        self.password = ""
        self.rol = ""

class GestorCredenciales:
    """
    Manejador de Credenciales de la base de datos.
    """

    @classmethod
    def getCredenciales(self):

        #Estandar de seguimiento:
        if v:
            print apiName
            print ' Calling '+ str(locals()['self'])

        #Realizamos la conexión con el conector.
        db = dbParams.conecta()

        cursor = db.cursor()

        query="select * from Credenciales"

        if v:
            print ' SQL query: '+query+'\n'


        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            cred = Credenciales()

            cred.idCredenciales=row[0]
            cred.idUsuario=row[1]
            cred.username=row[2]
            cred.password=row[3]
            cred.rol=row[4]


            lista.append(cred)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista


    @classmethod
    def postCredenciales(self, idUsuario, nombre, username, password, rol):
        '''
        Introduce una nueva tupla con la credenciales de algún usuario dado de alta en el sistema.
        '''

        if v:
            print apiName
            print ' Calling '+ str(locals()['self'])
            print ' '+str(locals())

        #Usamos el gestor para la conexión
        db = dbParams.conecta()


        #Añadimos al principio y al final una comilla simple a todos los elementos.
        idUsuario='\''+idUsuario+'\''
        username='\''+username+'\''
        password='\''+password+'\''
        nombre='\''+nombre+'\''
        rol='\''+rol+'\''

        query='INSERT INTO Credenciales VALUES(NULL'+','+idUsuario+','+nombre+','+username+','+password+','+rol+');'

        if v:
            print ' '+query+'\n'


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
        if salida==1062:
            return 'Elemento duplicado'


    @classmethod
    def comprobarUsuario(self, username, password):
        '''
        Comprueba si el usuario tiene permisos de acceso al sistema.
        '''

        if v:
            print apiName
            print ' Calling '+ str(locals()['self'])
            print ' '+str(locals())

        #Usamos el gestor para la conexión
        db = dbParams.conecta()


        #Añadimos al principio y al final una comilla simple a todos los elementos.
        username='\''+username+'\''
        password='\''+password+'\''

        query='SELECT * FROM Credenciales WHERE username='+username+' and password='+password+';'

        if v:
            print ' '+query

        cursor = db.cursor()

        salida =''
        cred = Credenciales()


        encontrado = True
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asignatura con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        try:
            #Cuando el usuario no es encontrado devuelve 0
            salida = cursor.execute(query)
            row = cursor.fetchone()

            if row != None:                
                cred.idUsuario=row[1]
                cred.nombre=row[2]
                cred.rol=row[5]

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

        mensajeSalida = ''
        if salida==1:
            if v:
                print cred
            return cred
        if salida==0:
            mensajeSalida =  'Usuario no encontrado'
        if salida==1062:
            mensajeSalida =  'Elemento duplicado'


        return mensajeSalida
