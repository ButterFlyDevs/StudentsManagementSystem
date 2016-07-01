# -*- coding: utf-8 -*-
"""
Prueba de unión de métodos de entidades.
"""

from Asignatura import *
from Clase import *
from Profesor import *
from Alumno import *
#Uso de variables generales par la conexión a la BD.
import dbParams

def extraer(dicc, field):
    dato = dicc.get(field, 'NULL')
    if dato == 'NULL':
        return dato
    else:
        return '\''+dato+'\''

from termcolor import colored

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1
apiName='\n## API DB ##\n'

'''Clase controladora de Asignaturas. Que usando la clase que define el modelo de Asignatura (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorEntidades:
    """
    Gestor de entidades de la base de datos, que abstrae el funcionamiento de MySQL
    """
    @classmethod
    def putEntidad(self, tipo, datos):
        """
        Introduce una entidad en el sistema, puede ser de cuatro tipos: Asignatura, Clase, Profesor, Alumno
        """
        if v:
            print apiName
            print 'Calling nuevaEntidad() with params:'
            print colored (locals(), 'blue')

            db = dbParams.conecta() #La conexión está clara.

        #Preparamos la consulta
        if tipo == 'Alumno': #Si es de tipo Alumno
            query = 'INSERT INTO Alumno (idAlumno, nombre, apellidos, dni, direccion, localidad, provincia, fechaNacimiento, telefono, urlImagen) VALUES (NULL' + \
            ',' + extraer(datos, 'nombre') + ',' + extraer(datos, 'apellidos') + ',' + extraer(datos, 'dni') + ',' + extraer(datos, 'direccion') + ',' + \
            extraer(datos, 'localidad') + ',' + extraer(datos, 'provincia') + ',' + extraer(datos, 'fechaNacimiento') + ',' + extraer(datos, 'telefono') + \
            ',' + extraer(datos, 'urlImagen') + ');'
        elif tipo == 'Profesor': #Si es de tipo Profesor
            query = 'INSERT INTO Profesor (idProfesor, nombre, apellidos, dni, direccion, localidad, provincia, fechaNacimiento, telefono) VALUES (NULL' + \
            ',' + extraer(datos, 'nombre') + ',' + extraer(datos, 'apellidos') + ',' + extraer(datos, 'dni') + ',' + extraer(datos, 'direccion') + ',' + \
            extraer(datos, 'localidad') + ',' + extraer(datos, 'provincia') + ',' + extraer(datos, 'fechaNacimiento') + ',' + extraer(datos, 'telefono') + ');'
        elif tipo == 'Asignatura': #Si es de tipo Asignatura
            query = 'INSERT INTO Asignatura (idAsignatura, nombre) VALUES (NULL' + ',' \
            + extraer(datos, 'nombre') + ');'

        elif tipo == 'Clase': #Si es de tipo Clase
            query = 'INSERT INTO Clase (idClase, curso, grupo, nivel) VALUES (NULL' + ',' \
            + extraer(datos, 'curso') + ',' + extraer(datos, 'grupo') + ',' + extraer(datos, 'nivel') + ');'

        else:
            return {'status': 'Tipo no reconocido'}

        if v:
            print query


        cursor = db.cursor()

        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Asignatura con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        idEntidad=''
        try:
            salida = cursor.execute(query);
            idEntidad = cursor.lastrowid
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
        dic={'status':salida, 'idEntidad':str(idEntidad)}

        #Transformación de los estados de MYSQL a mensajes comprensibles.
        if salida==1:
            dic['status']= 'OK'
            #return 'OK'
        if salida==1062:
            dic['status']= 'Elemento duplicado'

        return dic


    @classmethod
    def getEntidades(self, tipo, idEntidad=None):
        """
        Devuelve entidades de la base de datos, del tipo Alumno, Profesor, Asignatura o Clase

        :param tipo: Tipo de entidad de la que se quiere recuperara elementos.
        :type tipo: String de entre: Alumno, Profesor, Clase, Asignatura
        :param idEntidad: Identificador de la entidad (en la base de datos), *no es su DNI*, es **opcional**.
        :type idEntidad: Entero
        :returns: En caso de no pasar id devuelve todos los elementos de la entidad especificada
            de la base de datos de forma muy resumida (lista de diccionarios) de la bd,
            pero si se pasa id entonces se devuelve toda la información del tipo de entidad
            que se tenga almacenada (como un diccionario).
            *En caso de ser Alumno o Profesor la versión resumida solo devuelve nombre, apellidos e id.*
        :rtype: lista de diccionarios o un diccionario.
        """

        if v:
            print apiName
            print 'Calling getEntidad() with params:'
            print colored (locals(), 'blue')

        db = dbParams.conecta()
        cursor = db.cursor()

        if tipo == 'Alumno':
            if idEntidad == None: #Se quieren todos los elementos del tipo Alumno
                query="select idAlumno, nombre, apellidos from Alumno" #Query resumen de la entidad
            else: #Se quiere uno en concreto
                query='select * from Alumno where idAlumno='+idEntidad+';'
        elif tipo == 'Profesor':
            if idEntidad == None: #Se quieren todos los elementos del tipo Profesor
                query="select idProfesor, nombre, apellidos from Profesor" #Query resumen de la entidad
            else: #Se quiere uno en concreto
                query='select * from Profesor where idProfesor='+idEntidad+';'
        elif tipo == 'Clase':
            #Como el tipo Clase es tan pequeño se muestra toda la información cuando se piden todos los elementos.
            if idEntidad == None: #Se quieren todos los elementos del tipo Clase
                query="select idClase, curso, grupo, nivel from Clase"
            else: #Se quiere una en concreto
                query='select * from Clase where idClase='+idEntidad+';'
        elif tipo == 'Asignatura':
            #Como el tipo Asignatura es tan pequeño se muestra toda la información cuando se piden todos los elementos.
            if idEntidad == None: #Se quieren todos los elementos del tipo Asignatura
                query="select idAsignatura, nombre from Asignatura"
            else: #Se quiere una en concreto
                query='select * from Asignatura where idAsignatura='+idEntidad+';'
        else:
            return {'status': 'Tipo no reconocido'}

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

        if idEntidad != None: #Se busca uno en concreto
            if salida == 1:
                if tipo == 'Alumno':
                    ret = {'idAlumno': row[0], 'nombre': row[1], 'apellidos': row[2], 'dni': row[3],
                           'direccion': row[4], 'localidad': row[5], 'provincia': row[6],
                           'fechaNacimiento': row[7], 'telefono': row[8], 'urlImagen': row[9]}
                elif tipo == 'Profesor':
                    ret = {'idProfesor': row[0], 'nombre': row[1], 'apellidos': row[2], 'dni': row[3],
                                'direccion': row[4], 'localidad': row[5], 'provincia': row[6],
                                'fechaNacimiento': row[7], 'telefono': row[8] }
                elif tipo == 'Clase':
                    ret = {'idClase': row[0], 'curso': row[1], 'grupo': row[2], 'nivel': row[3]}
                elif tipo == 'Asignatura':
                    ret = {'idAsignatura': row[0], 'nombre': row[1]}
            if salida == 0:
                ret = 'Elemento no encontrado'
        else: #Se quieren todos
            lista = [] #Creamos una lista "RESUMIDA de las entidades"
            while row is not None:
                if tipo == 'Alumno':
                    lista.append({'idAlumno': row[0], 'nombre': row[1], 'apellidos': row[2]})
                elif tipo == 'Profesor':
                    lista.append({'idProfesor': row[0], 'nombre': row[1], 'apellidos': row[2]})
                elif tipo == 'Clase':
                    lista.append({'idClase': row[0], 'curso': row[1], 'grupo': row[2], 'nivel': row[3]})
                elif tipo == 'Asignatura':
                    lista.append({'idAsignatura': row[0], 'nombre': row[1]})
                row = cursor.fetchone() #Recuperamos el siguiente

            ret = lista

        cursor.close()
        db.close()

        return ret
