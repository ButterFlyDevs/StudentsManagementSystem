# -*- coding: utf-8 -*-
"""
Interfaz de interacción con la entidad Alumno de la base de datos.

Última modificación: Feb 2016
"""
import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Alumno import *
from Profesor import *
from Asignatura import *
from Curso import *
#Uso de variables generales par la conexión a la BD.
import dbParams

class GestorAlumnos:
    """
    Clase manejadora de la entidad Alumno de la base de datos que ofrece una interfaz de gestión que simplifica y abstrae el uso.
    Ofrece gestión de la entidad y obtención de información de relación con el resto de entidades del modelo de la BD.
    """

    @classmethod
    def nuevoAlumno(self, nombre, dni, direccion, localidad, provincia, fecha_nac, telefono):
        """
        Introduce un nuevo alumno en la base de datos.
        Argumentos:
        nombre -- Nombre completo del alumno
        dni -- DNI del alumno, que será la clave de este.

        Extra de prog:

        Podríamos programarlo para que independientemente del número de parámetros se guardara en la base de datos,
        así sólo habría que pasarle una lista y funcionaría siempre. Podría sen interesante.
        O que los paŕametros así como sus nombrs se definieran en algún sitio donde poder conslutaros y así cualquier modificación
        se hace solo en un lugar.

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        #query="INSERT INTO Alumno values("+"'"+nombre+"', "+ "'"+dni+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        nombre='\''+nombre+'\''
        dni='\''+dni+'\''
        direccion='\''+direccion+'\''
        localidad='\''+localidad+'\''
        provincia='\''+provincia+'\''
        fecha_nac='\''+fecha_nac+'\''
        telefono='\''+telefono+'\''



        query="INSERT INTO Alumno VALUES("+nombre+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefono+");"

        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el alumno con clave
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
    def getAlumnos(self):
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Alumno"
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            #print "LISTA SUPER CHACHI"

            alumno.nombre=row[0]
            alumno.dni=row[1]
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAlumno(self, dniAlumno):
        """
        Recupera ``TODA`` la información de un alumno en concreto a través de la clave primaria, su DNI.

        Argumentos:
            dniAlumno: El primer parámetro

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Alumno where dni='"+dniAlumno+"';"

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
            #Como se trata de toda la información al completo usaremos todos los campos de la clase alumno.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            alm = Alumno()
            alm.nombre=row[0]
            alm.dni=row[1]
            alm.direccion=row[2]
            alm.localidad=row[3]
            alm.provincia=row[4]
            alm.fecha_nac=row[5]
            alm.telefono=row[6]

            return alm
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modAlumno(self, dniAlumno, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un alumno.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        dniAlumno='\''+dniAlumno+'\''
        query="UPDATE Alumno SET "+campoACambiar+"="+nuevoValor+" WHERE dni="+dniAlumno+";"



        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el alumno con clave
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
    def delAlumno(self, dniAlumno):
        #print "Intentado eliminar alumno con dni "+str(dniAlumno)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Alumno where dni='"+dniAlumno+"';"
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
        """
        Devuelve el número de alumnos de la BD"
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
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

    @classmethod
    def getProfesores(self, dniAlumno):
        """
        Devuelve una lista de los profesores que imparte clase a ese alumno.

        Argumentos:

            dniAlumno: El dni del alumno del que se pide la información.


        Extra: ¿Se debería añadir la comprobación de existencia del alumno?

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query="select * from Matricula, Imparte where Matricula.id_curso = Imparte.id_curso and Matricula.id_asignatura = Imparte.id_asignatura and id_alumno ="+dniAlumno+";"


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

                profesor.dni=row[5]
                lista.append(profesor)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getAsignaturas(self, dniAlumno):
        """Devuelve una lista con las asignaturas en las que ese alumno está matriculado
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query="select * from Matricula, Asignatura where Matricula.id_asignatura=Asignatura.id and id_alumno="+dniAlumno+";"

        #select * from Matricula, Asignatura where Matricula.id_asignatura=Asignatura.id and id_alumno=4;

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
                asignatura.id=row[3]
                asignatura.nombre=row[4]
                lista.append(asignatura)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()

    @classmethod
    def getCursos(self, dniAlumno):
        """
        Devuelve una lista con cursos en los que ese alumno está matriculado, aunque en la mayoría de los casos será uno.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query="select * from Matricula, Curso where Matricula.id_curso=Curso.id and id_alumno="+dniAlumno+";"

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
                curso = Curso()
                #En esta consulta el identificador de la asignatura se encuentra en la primera posicion.
                curso.id=row[3]
                curso.curso=row[4]
                curso.grupo=row[5]
                curso.nivel=row[6]
                lista.append(curso)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
