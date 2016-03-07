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
from Clase import *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1

class GestorAlumnos:
    """
    Clase manejadora de la entidad Alumno de la base de datos que ofrece una interfaz de gestión que simplifica y abstrae el uso.
    Ofrece gestión de la entidad y obtención de información de relación con el resto de entidades del modelo de la BD.
    """

    @classmethod
    def nuevoAlumno(self, nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL'):
        """
        Introduce un nuevo alumno en la base de datos.
        El único argumento que se necesita como mínimo es el nombre.

        El resto de parámetros pueden pasarse o no. En caso de hacerlo no es necesario que se haga en orden, especificando
        el parámetro que estamos pasando. Esta es una característica de python.
        Así la llamada: GestorAlumnos.nuevoAlumno('Maria')
        realizaría la query: INSERT INTO Alumno VALUES(NULL,'Maria',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
        y la llamada: GestorAlumnos.nuevoAlumno('Maria', apellidos='Fernández García')
        realizaría la query:
        INSERT INTO Alumno VALUES(NULL,'Maria','Fernández García',NULL,NULL,NULL,NULL,NULL,NULL);
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        #query="INSERT INTO Alumno values("+"'"+nombre+"', "+ "'"+dni+"');"

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
        if(fecha_nacimiento!='NULL'):
            fecha_nacimiento='\''+fecha_nacimiento+'\''
        if(telefono!='NULL'):
            telefono='\''+telefono+'\''

        '''
        Como en la base de datos existe un valor id para el alumno que se autoincrementa no podemos introducir los datos así:
        query="INSERT INTO Alumno VALUES("+nombre+","+apellidos+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefono+");"
        hay que especificar los campos sin este id, así:
        query='INSERT INTO Alumno (nombre, apellidos, ...) VALUES (...)
        o pasar simplemente NULL.
        '''

        #NULL por el campo id que es primary key y que se autoincrementa automat por la definición de la tabla Alumno en la BD. (ver DBCreator_v0_1.sql)
        query="INSERT INTO Alumno VALUES(NULL,"+nombre+","+apellidos+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nacimiento+","+telefono+");"

        if v:
            print query

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
        '''
        Devuelve una lista de todos los alumnos almacenados en la base de datos simplificada, solo con los
        campos id, nombre y apellidos.
        '''
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

            alumno.id=row[0]
            alumno.nombre=row[1]
            alumno.apellidos=row[2]
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAlumno(self, idAlumno):
        """
        Recupera ``TODA`` la información de un alumno en concreto a través de su id.

        Argumentos:
            idAlumno: identificador unívoco del alumno en la tabla

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        idAlumno='\''+idAlumno+'\''
        query='select * from Alumno where id='+idAlumno+';'

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
            alm.id=row[0]
            alm.nombre=row[1]
            alm.apellidos=row[2]
            alm.dni=row[3]
            alm.direccion=row[4]
            alm.localidad=row[5]
            alm.provincia=row[6]
            alm.fecha_nacimiento=row[7]
            alm.telefono=row[8]

            return alm
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modAlumno(self, idAlumno, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de un alumno.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        idAlumno='\''+idAlumno+'\''
        query="UPDATE Alumno SET "+campoACambiar+"="+nuevoValor+" WHERE id="+idAlumno+";"



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
    def delAlumno(self, idAlumno):
        #print "Intentado eliminar alumno con dni "+str(dniAlumno)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query='delete from Alumno where id='+idAlumno+';'
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
        query='select dni, nombre, apellidos from Profesor where dni in ( select id_profesor from Imparte where id_asignatura in (select id_asignatura from Matricula where id_alumno='+idAlumno+') and id_clase in  (select id_clase from Matricula where id_alumno='+idAlumno+'))'


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
        query='select * from Asignatura where id in (select id_asignatura from Matricula where id_alumno='+idAlumno+')'

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
    def getClases(self, dniAlumno):
        """
        Devuelve una lista con las clases en las que ese alumno está matriculado, aunque en la mayoría de los casos será una.
        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        #Hacemos un JOIN de las tablas que relacionan alumnos con asociaciones y estas con profesores para luego sacar sólo las de cierto identificador e alumno.
        query='select * from Clase where id in(select id_clase from Matricula where id_alumno='+idAlumno+')'

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
                clase.id=row[3]
                clase.curso=row[4]
                clase.grupo=row[5]
                clase.nivel=row[6]
                lista.append(clase)
                #print row[0], row[1]
                row = cursor.fetchone()

            #Devolvemos la lista de profesores (incluso si no hay y está vacía)
            return lista

            cursor.close()
            db.close()
