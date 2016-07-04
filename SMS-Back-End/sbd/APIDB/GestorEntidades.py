# -*- coding: utf-8 -*-
"""
Prueba de unión de métodos de entidades.
"""

#from Asignatura import *
#from Clase import *
#from Profesor import *
#from Alumno import *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Habría que modificar esta función para que detectase que al ser un alumno deben de ser nombre tales que estos o los otros
#para que no puedar realizar la insercción de un alumno y se pase como parámetro el nombre así: 'nombra': 'Juan', NO EXISTE
#un atributo llamado nombra y no puede devolver OK, de ninguna manera.

#PREGUNTAR PSICOBYTE !!!!

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
        Introduce una entidad en el sistema, puede ser de siete tipos: Asignatura, Clase, Profesor, Alumno,
        Asociacion, Imparte o Matricula.
        """
        if v:
            print apiName
            print 'Calling nuevaEntidad() with params:'
            print colored (locals(), 'blue')

            db = dbParams.conecta() #La conexión está clara.

        ## Preparamos la consulta según el tipo ##

        ## ENTIDADES base ##

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

        ## ENTIDADES de tipo RELACIÓN ##

        elif tipo == 'Asociacion': #Si el tipo es Asociacion
            query = 'INSERT INTO Asociacion (idAsociacion, idClase, idAsignatura) VALUES (NULL' + ',' \
            + extraer(datos, 'idClase') + ',' + extraer(datos, 'idAsignatura') + ');'

        elif tipo == 'Imparte': #Si el tipo es Imparte
            query = 'INSERT INTO Imparte (idImparte, idAsociacion, idProfesor) VALUES (NULL' + ',' \
            + extraer(datos, 'idAsociacion') + ',' + extraer(datos, 'idProfesor') + ');'

        elif tipo == 'Matricula': #Si el tipo es Matricula
            query = 'INSERT INTO Matricula (idMatricula, idAlumno, idAsociacion) VALUES (NULL' + ',' \
            + extraer(datos, 'idAlumno') + ',' + extraer(datos, 'idAsociacion') + ');'

        elif tipo == None:
            return {'status': 'FAIL', 'info': 'Necesario pasar tipo'}

        else:
            return {'status': 'FAIL', 'info': 'Tipo no reconocido'}

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
            dic={'status': 'FAIL', 'info': 'Elemento duplicado.'}
        if salida==1452:
            dic={'status': 'FAIL', 'info': 'Alguno de los elementos no existe.'}            

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

        ## ENTIDADES base ##

        if tipo == 'Alumno':
            if idEntidad == None: #Se quieren todos los elementos del tipo Alumno
                query = 'SELECT idAlumno, nombre, apellidos FROM Alumno' #Query resumen de la entidad
            else: #Se quiere uno en concreto
                query = 'SELECT * FROM Alumno WHERE idAlumno='+idEntidad+';'
        elif tipo == 'Profesor':
            if idEntidad == None: #Se quieren todos los elementos del tipo Profesor
                query = 'SELECT idProfesor, nombre, apellidos FROM Profesor' #Query resumen de la entidad
            else: #Se quiere uno en concreto
                query = 'SELECT * FROM Profesor WHERE idProfesor='+idEntidad+';'
        elif tipo == 'Clase':
            #Como el tipo Clase es tan pequeño se muestra toda la información cuando se piden todos los elementos.
            if idEntidad == None: #Se quieren todos los elementos del tipo Clase
                query = 'SELECT idClase, curso, grupo, nivel FROM Clase'
            else: #Se quiere una en concreto
                query = 'SELECT * FROM Clase WHERE idClase='+idEntidad+';'
        elif tipo == 'Asignatura':
            #Como el tipo Asignatura es tan pequeño se muestra toda la información cuando se piden todos los elementos.
            if idEntidad == None: #Se quieren todos los elementos del tipo Asignatura
                query = 'SELECT idAsignatura, nombre FROM Asignatura'
            else: #Se quiere una en concreto
                query = 'SELECT * FROM Asignatura WHERE idAsignatura='+idEntidad+';'

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

    @classmethod
    def modEntidad(self, tipo, idEntidad, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de cualquier Entidad.

        :param tipo: Tipo de entidad de la que se quiere recuperara elementos.
        :type tipo: String de entre: Alumno, Profesor, Clase, Asignatura
        :param idEntidad: Identificador de la entidad (en la base de datos), *no es su DNI*, es **opcional**.
        :type idEntidad: Entero
        :param campoACambiar: Campo de la entidad que se quiere modificar
        :type campoACambiar: String
        :param nuevoValor: Nuevo valor que se le quiere asignar a campo a modificar
        :type nuevoValor: String
        :returns: Diccionario con estado de la ejecución e informe de errores en caso de que existan.
        :rtype: diccionario
        """
        db = dbParams.conecta();

        #Entrecomillamos los valores
        nuevoValor='\''+nuevoValor+'\''
        idEntidad='\''+idEntidad+'\''

        idTipo = 'id'+tipo

        query='UPDATE ' + tipo + ' SET ' + campoACambiar + ' = ' + nuevoValor + ' WHERE ' + idTipo + ' = ' + idEntidad + ';'
        #Ejemplo: UPDATE Alumno SET nombre='nuevoNombre' WHERE idAlumno = '1';

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
            return {'status': 'OK'}
        elif salida==1062:
            return {'status': 'Elemento duplicado'}
        elif salida==0:
            return {'status': 'Elemento no encontrado'}

    @classmethod
    def delEntidad(self, tipo, idEntidad):
        """
        Esta función permite cambiar cualquier atributo de cualquier Entidad.

        :param tipo: Tipo de entidad de la que se quiere recuperara elementos.
        :type tipo: String de entre: Alumno, Profesor, Clase, Asignatura
        :param idEntidad: Identificador de la entidad (en la base de datos), *no es su DNI*, es **opcional**.
        :type idEntidad: Entero
        :param campoACambiar: Campo de la entidad que se quiere modificar
        :type campoACambiar: String
        :param nuevoValor: Nuevo valor que se le quiere asignar a campo a modificar
        :type nuevoValor: String
        :returns: En caso de no pasar id devuelve todos los elementos de la entidad especificada
            de la base de datos de forma muy resumida (lista de diccionarios) de la bd,
            pero si se pasa id entonces se devuelve toda la información del tipo de entidad
            que se tenga almacenada (como un diccionario).
            *En caso de ser Alumno o Profesor la versión resumida solo devuelve nombre, apellidos e id.*
        :rtype: lista de diccionarios o un diccionario.
        """
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()


        idEntidad='\''+idEntidad+'\''
        idTipo = 'id'+tipo

        query='DELETE FROM ' + tipo + ' WHERE ' + idTipo + ' = ' + idEntidad + ';'


        if v:
            print '\n'+query
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



        #print str(cursor)
        db.commit()

        #print cursor.fetchone()
        cursor.close()
        db.close()

        if salida == 1:
            return {'status': 'OK'}
        if salida == 0:
            return {'status': 'Elemento no encontrado'}
        if salida == 1451:
            return {'status': 'El elemento que pretentde eliminar tiene dependencias'}

    @classmethod
    def getNumEntidades(self, tipo):
        '''Devuelve el número de Entidades de un tipo de la BD'''
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query='select count(*) from ' + tipo + ';'
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
            return {'status': 'Error'}

    @classmethod
    def getEntidadesRelacionadas(self, tipoBase, idEntidad, tipoBusqueda):
        """Devuelve una lista de diccionarios con la información pedida."""

        """
        getEntidadesRelacioandas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Profesor')
            Devuelve todos los profesores que imparten clase a ese alumno.
        getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Asignatura')
            Devuelve todas las asignaturas en la que está matriculado ese alumno.
        getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Clases')
            Devuelve todas las clases en las que está matriculado ese alumno.

        Toda la información de las entidades se devuelve en su versión resumida.
        """

        db = dbParams.conecta()
        cursor = db.cursor()


        if tipoBase == 'Alumno': #Queremos buscar entidades relacionadas con una entidad de tipo Alumno
            if tipoBusqueda == 'Profesor': #Todos los profesores que dan clase al alumno.
                query='SELECT idProfesor, nombre, apellidos FROM Profesor WHERE idProfesor IN (SELECT idProfesor FROM Imparte, Matricula WHERE Imparte.idAsociacion=Matricula.idAsociacion and Matricula.idAlumno='+idEntidad+');'
            elif tipoBusqueda == 'Clase': #Todos las clases en las que está matriculado el alumno.
                query='SELECT idClase, curso, grupo, nivel FROM Clase WHERE idClase IN (SELECT idClase FROM Asociacion WHERE idAsociacion IN (SELECT idAsociacion FROM Matricula WHERE idAlumno='+idEntidad+'));'
            elif tipoBusqueda == 'Asignatura': #Todas las asignaturas en la que está matriculado el alumno.
                query='SELECT idAsignatura, nombre FROM Asignatura WHERE idAsignatura IN (SELECT idAsignatura FROM Asociacion WHERE idAsociacion IN (SELECT idAsociacion FROM Matricula WHERE idAlumno='+idEntidad+'));'

        elif tipoBase == 'Profesor': #Queremos buscar entidades relacionadas con una entidad de tipo Profesor
            if tipoBusqueda == 'Alumno': #Todos los alumnos a los que da clase ese profesor.
                query='SELECT idAlumno, nombre, apellidos  FROM Alumno WHERE idAlumno IN (SELECT idAlumno FROM Imparte, Matricula WHERE Imparte.idAsociacion=Matricula.idAsociacion AND Imparte.idProfesor='+idEntidad+');'
            elif tipoBusqueda == 'Clase': #Todos las clases en las que el profesor imparte.
                query='SELECT idClase, curso, grupo, nivel FROM Clase WHERE idClase IN (SELECT idClase FROM Asociacion where idAsociacion IN(SELECT idAsociacion FROM Imparte WHERE idProfesor='+idEntidad+'));'
            elif tipoBusqueda == 'Asignatura': #Todas las asignaturas que el profesor imparte.
                query='SELECT idAsignatura, nombre FROM Asignatura WHERE idAsignatura IN (SELECT idAsignatura FROM Asociacion WHERE idAsociacion IN (SELECT idAsociacion FROM Imparte WHERE idProfesor='+idEntidad+'));'

        elif tipoBase == 'Clase': #Queremos buscar entidades relacionadas con una entidad de tipo Clase.
            if tipoBusqueda == 'Alumno': #Todos los alumnos matriculados en esa clase.
                query= 'SELECT idAlumno, nombre, apellidos FROM Alumno WHERE idAlumno IN (SELECT idAlumno FROM Matricula WHERE idAsociacion IN (SELECT idAsociacion FROM Asociacion WHERE idClase='+idEntidad+'));'
            elif tipoBusqueda == 'Profesor': #Todos los profesores que imparten en esa clase alguna asignatura.
                query='SELECT idProfesor, nombre, apellidos FROM Profesor WHERE idProfesor IN (SELECT idProfesor FROM Imparte WHERE idAsociacion IN (SELECT idAsociacion FROM Asociacion WHERE idClase='+idEntidad+'))';
            elif tipoBusqueda == 'Asignatura': #Todas las asignaturas que se imparten en esa clase.
                query='SELECT idAsignatura, nombre FROM Asignatura WHERE idAsignatura in (SELECT idAsignatura FROM Asociacion WHERE idClase ='+idEntidad+')'

        elif tipoBase == 'Asignatura': #Queremos buscar entidades relacionadas con una entidad de tipo Asignatura.
            if tipoBusqueda == 'Alumno':
                query='SELECT idAlumno, nombre, apellidos from Alumno where idAlumno in (select idAlumno from Matricula where idAsociacion IN ( select idAsociacion from Asociacion where idAsignatura='+idEntidad+'));'
            elif tipoBusqueda == 'Profesor':
                query='SELECT idProfesor, nombre, apellidos from Profesor where idProfesor in (select idProfesor from Imparte where idAsociacion IN ( select idAsociacion from Asociacion where idAsignatura='+idEntidad+'));'
            elif tipoBusqueda == 'Clase':
                query='SELECT idClase, curso, grupo, nivel from Clase where idClase in (select idClase from Asociacion where idAsignatura='+idEntidad+')'

        if v:
            print query

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

        if salida>=0: #La consulta ha tenido exito
            row = cursor.fetchone()
            lista = []

            if tipoBusqueda == 'Alumno':
                while row is not None:
                    lista.append({'idAlumno': row[0], 'nombre': row[1], 'apellidos': row[2]})
                    row = cursor.fetchone()
            elif tipoBusqueda == 'Profesor': #Si el tipo es Profesor iteramos sobre todas las filas extrayendo los datos de la misma forma.
                while row is not None:
                    lista.append({'idProfesor': row[0], 'nombre': row[1], 'apellidos': row[2]})
                    row = cursor.fetchone()
            elif tipoBusqueda == 'Clase':
                while row is not None:
                    lista.append({'idClase': row[0], 'curso': row[1], 'grupo': row[2], 'nivel': row[3]})
                    row = cursor.fetchone()
            elif tipoBusqueda == 'Asignatura':
                while row is not None:
                    lista.append({'idAsignatura': row[0], 'nombre': row[1]})
                    row = cursor.fetchone()


            cursor.close()
            db.close()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

        else:
            return 'error'
