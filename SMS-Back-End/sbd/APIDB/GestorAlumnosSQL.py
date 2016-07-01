# -*- coding: utf-8 -*-
"""
Interfaz de interacción con la entidad Alumno de la base de datos.

Última modificación: Feb 2016

Para mostrar texto por terminal usar -> dbParams.formatOutputText(cadena) <-
"""

#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Alumno import *
from Profesor import *
from Asignatura import *
from Clase import *
#Uso de variables generales par la conexión a la BD.
import dbParams
from termcolor import colored

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
apiName='\n## API DB ##\n'

class GestorAlumnos:

    """
    Clase manejadora de la entidad Alumno de la base de datos que ofrece una interfaz de gestión que simplifica y abstrae el uso.
    Ofrece gestión de la entidad y obtención de información de relación con el resto de entidades del modelo de la BD.
    """

    ## Métodos propios ##

    @classmethod
    def nuevoAlumno(self,nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fechaNacimiento='NULL', telefono='NULL', urlImagen='NULL'):
        """
        Intruduce un nuevo alumno en la base de datos.

        :param nombre: Nombre del alumno, incluso si es compuesto, único parámetro **obligatorio**.
        :type nombre: String
        :param apellidos: Apellidos de alumnos, separados por un espacio.
        :type apellidos: String
        :param dni: Documento Nacional de Identidad, en caso de que lo tenga.
        :type dni: Entero
        :param direccion: Dirección de la residencia del estudiante.
        :type direccion: String
        :param localidad: Localida de residencia.
        :type localidad: String
        :param provincia: Provincia donde se encuentra la localidad.
        :type provincia: String
        :param fechaNacimiento: Fecha de nacimiento del alumno.
        :type fechaNacimiento: Date con formato (dd-mm-aaaa)
        :param telefono: Número de teléfono del alumno.
        :type telefono: Entero
        :param urlImagen: URL a una imagen para el perfil del alumno.
        :type urlImagen: URL
        :returns: Mensaje con estado de la acción e id en caso de haberse creado correctamente.
        :rtype: diccionario

        Ejemplo de salida::

            ...
            {'status': 'OK', 'idAlumno': '3'}
            ...
            {'status': 'Elemento duplicado'}
        """

        print '\n\n ### calling nuevoAlumno() ### \n\n'
        print colored(locals(), 'red')

        """
        #Recorremos el diccionario que representa los parámetros de la función, y añadimos a los parámetros presentes las comillas
        for key, value in locals().iteritems():
            if value != 'NULL' and key != 'self':
                print value
        """

        locals()['nombre']='PerroFlauta'

        print colored(locals()['nombre'], 'blue')
        print colored(nombre)

        db = dbParams.conecta() #Conecta a la BD

        #Añadimos al principio y al final una comilla simple a todos los elementos que no sean NULL(si lo son no queremos ponerle dos '' )
        nombre='\''+nombre+'\''
        if(apellidos!='NULL'):
            apellidos='\''+apellidos+'\''
        #DNI se pasa como un entero y no es necesario comillarlo.
        if(direccion!='NULL'):
            direccion='\''+direccion+'\''
        if(localidad!='NULL'):
            localidad='\''+localidad+'\''
        if(provincia!='NULL'):
            provincia='\''+provincia+'\''
        if(fechaNacimiento!='NULL'):
            fechaNacimiento='\''+fechaNacimiento+'\''
        if(telefono!='NULL'):
            telefono='\''+telefono+'\''
        if(urlImagen!='NULL'):
            urlImagen='\''+urlImagen+'\''

        """
        Como en la base de datos existe un valor id para el alumno que se autoincrementa no podemos introducir los datos así:
        query="INSERT INTO Alumno VALUES("+nombre+","+apellidos+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefono+");"
        hay que especificar los campos sin este id, así:
        query='INSERT INTO Alumno (nombre, apellidos, ...) VALUES (...)
        o pasar simplemente NULL.
        """

        #NULL por el campo id que es primary key y que se autoincrementa automat por la definición de la tabla Alumno en la BD. (ver DBCreator_v0_1.sql)

        query='INSERT INTO Alumno VALUES(NULL'+','+nombre+','+apellidos+','+dni+','+direccion+','+localidad+','+provincia+','+fechaNacimiento+','+telefono+','+urlImagen+');'
        #query2='INSERT INTO Alumno VALUES(NULL'+','+nombre+','+apellidos+','+dni+');'


        if v:
            print apiName
            print "nuevoAlumno()"
            print query

        cursor = db.cursor()

        salida =''
        idAlumno=''

        try:

            salida = cursor.execute(query);
            idAlumno = cursor.lastrowid

            #idAlumno=cursor.execute('SELECT LAST_INSERT_ID();')
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



        if v:
            print "salida MySQL: "+str(salida)
            print "salida idAlumno:"+str(idAlumno)

        dic={}


        if salida==1:
            return {'status': 'OK', 'idAlumno': str(idAlumno)}
        elif salida==1062:
            return {'status': 'Elemento duplicado'}
        else:
            return {'status': 'desconocido'}

    @classmethod
    def getAlumnos(self, idAlumno=None):
        """
        Devuelve alumnos de la base de datos.

        :param idAlumno: Identificador del alumno (en la base de datos), *no es su DNI*, es **opcional**.
        :type idAlumno: Entero
        :returns: En caso de no pasar id devuelve todos los alumnos de la base de datos de forma muy resumida (lista
            de diccionarios), solo *nombre*,
            *apellidos* e *identificador* de la bd, pero si se pasa id entonces se devuelve toda la información de ese alumno
            que se tenga almacenada (como un diccionario).
        :rtype: lista de diccionarios o diccionario.

        Ejemplo de salida::

            >>> GestorAlumnosSQL.nuevoAlumno(nombre='Juan')
            {'status': 'OK', 'idAlumno': '1'}
            >>> GestorAlumnosSQl.getAlumnos(idAlumno=1)
            {'apellidos': None, 'urlImagen': None, 'provincia': None, 'telefono': None,
             'localidad': None, 'nombre': u'Juan', 'fechaNacimiento': None, 'dni': None,
             'idAlumno': 1L, 'direccion': None}
        """


        db = dbParams.conecta()
        cursor = db.cursor()

        if idAlumno != None:
            query='select * from Alumno where idAlumno='+idAlumno+';'
        else:
            query="select nombre, apellidos, idAlumno from Alumno"

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

        if idAlumno != None: #Se busca uno en concreto
            if salida == 1:
                ret = {'idAlumno': row[0], 'nombre': row[1], 'apellidos': row[2], 'dni': row[3],
                       'direccion': row[4], 'localidad': row[5], 'provincia': row[6],
                       'fechaNacimiento': row[7], 'telefono': row[8], 'urlImagen': row[9]}
            if salida == 0:
                ret = 'Elemento no encontrado'
        else: #Se quieren todos
            lista = [] #Creamos una lista
            while row is not None:
                #Añadimos un dict a la lista con los datos básicos del alumno.
                lista.append({'nombre': row[0], 'apellidos': row[1], 'idAlumno': row[2]})
                row = cursor.fetchone() #Recuperamos el siguiente

            ret = lista

        cursor.close()
        db.close()

        return ret

    @classmethod
    def modAlumno(self, idAlumno, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un alumno, dado su id.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = dbParams.conecta(); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idAlumno='\''+idAlumno+'\''
        query="UPDATE Alumno SET "+campoACambiar+"="+nuevoValor+" WHERE idAlumno="+idAlumno+";"



        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el alumno con clave
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
    def delAlumno(self, idAlumno):
        #print "Intentado eliminar alumno con dni "+str(dniAlumno)
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        idAlumno='\''+idAlumno+'\''
        query='delete from Alumno WHERE idAlumno='+idAlumno+';'
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
    def getNumAlumnos(self):
        '''Devuelve el número de alumnos de la BD'''
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        query="select count(*) from Alumno;"
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

    ## Métodos de relaciones con otros ##

    @classmethod
    def getProfesores(self, idAlumno):
        """
        Devuelve una lista de los profesores que imparte clase a ese alumno.

        Argumentos:

            idAlumno: El id del alumno del que se pide la información.
        """
        db = dbParams.conecta()
        cursor = db.cursor()
        idAlumno='\''+idAlumno+'\''

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        #query='SELECT id_profesor, nombre, apellidos from Profesor where id_profesor in ( select id_profesor from Imparte where id_asignatura in (select id_asignatura from Matricula where idAlumno='+idAlumno+') and id_clase in  (select id_clase from Matricula where idAlumno='+idAlumno+'))'

        query='SELECT nombre, apellidos, id_profesor FROM Profesor WHERE id_profesor IN (SELECT id_profesor FROM Imparte, Matricula WHERE Imparte.id_asociacion=Matricula.id_asociacion and Matricula.idAlumno='+idAlumno+');'

        if v:
            print query

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

                print "Info profesor recibida: "+str(row)

                profesor = Profesor()

                profesor.id=row[2]
                profesor.nombre=row[0]
                profesor.apellidos=row[1]
                lista.append(profesor)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getAsignaturas(self, idAlumno):
        """Devuelve una lista con las asignaturas en las que ese alumno está matriculado
        """
        db = dbParams.conecta()
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='select * from Asignatura where id in (select id_asignatura from Matricula where idAlumno='+idAlumno+')'

        query='SELECT * FROM Asignatura WHERE id_asignatura IN (SELECT id_asignatura FROM Asocia WHERE id_asociacion IN (SELECT id_asociacion FROM Matricula WHERE idAlumno='+idAlumno+'));'

        #select * from Matricula, Asignatura where Matricula.id_asignatura=Asignatura.id and idAlumno=4;

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
                asignatura.id=row[0]
                asignatura.nombre=row[1]
                lista.append(asignatura)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getClases(self, idAlumno):
        """
        Devuelve una lista con las clases en las que ese alumno está matriculado, aunque en la mayoría de los casos será una.
        """
        db = dbParams.conecta()
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='SELECT * FROM Clase WHERE id_clase IN (SELECT id_clase FROM Asocia WHERE id_asociacion IN (SELECT id_asociacion FROM Matricula WHERE idAlumno='+idAlumno+'));'

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
                clase.id=row[0]
                clase.curso=row[1]
                clase.grupo=row[2]
                clase.nivel=row[3]
                lista.append(clase)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
