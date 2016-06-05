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

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
apiName='\n## API DB ##\n'

class GestorAlumnos:
    """
    Clase manejadora de la entidad Alumno de la base de datos que ofrece una interfaz de gestión que simplifica y abstrae el uso.
    Ofrece gestión de la entidad y obtención de información de relación con el resto de entidades del modelo de la BD.
    """

    @classmethod
    def nuevoAlumno(self,nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL', imagen='NULL'):
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

        print '\n\n ### calling nuevoAlumno() ### \n\n'
        print locals()



        db = dbParams.conecta(); #La conexión está clara.
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
        if(imagen!='NULL'):
            imagen='\''+imagen+'\''

        '''
        Como en la base de datos existe un valor id para el alumno que se autoincrementa no podemos introducir los datos así:
        query="INSERT INTO Alumno VALUES("+nombre+","+apellidos+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefono+");"
        hay que especificar los campos sin este id, así:
        query='INSERT INTO Alumno (nombre, apellidos, ...) VALUES (...)
        o pasar simplemente NULL.
        '''

        #NULL por el campo id que es primary key y que se autoincrementa automat por la definición de la tabla Alumno en la BD. (ver DBCreator_v0_1.sql)

        query='INSERT INTO Alumno VALUES(NULL'+','+nombre+','+apellidos+','+dni+','+direccion+','+localidad+','+provincia+','+fecha_nacimiento+','+telefono+','+imagen+');'
        #query2='INSERT INTO Alumno VALUES(NULL'+','+nombre+','+apellidos+','+dni+');'


        if v:
            print apiName
            print "nuevoAlumno()"
            print query

        cursor = db.cursor()

        salida =''
        idAlumno=''

        import MySQLdb
        try:

            salida = cursor.execute(query);
            idAlumno = cursor.lastrowid

            #idAlumno=cursor.execute('SELECT LAST_INSERT_ID();')
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



        if v:
            print "salida MySQL: "+str(salida)
            print "salida idAlumno:"+str(idAlumno)

        dic={'status':salida, 'idAlumno':str(idAlumno)}


        if salida==1:
            dic['status']= 'OK'
            #return 'OK'
        if salida==1062:
            dic['status']= 'Elemento duplicado'
            #return 'Elemento duplicado'

        #Devolvemos el diccionario
        print dic
        return dic

    @classmethod
    def getAlumnos(self):
        '''
        Devuelve una lista de todos los alumnos almacenados en la base de datos simplificada, solo con los
        campos id, nombre y apellidos.
        '''

        db = dbParams.conecta()

        #db = dbParams.conecta()
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
            #print 'Nombre alumno: '+alumno.nombre

        cursor.close()
        db.close()

        return lista


    @classmethod
    def getAlumno(self, idAlumno):
        """
        Recupera ``TODA`` la información de un alumno en concreto a través de su id.

        Argumentos:
            idAlumno: identificador unívoco del alumno en la tabla

        """
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        idAlumno='\''+idAlumno+'\''
        query='select * from Alumno where id_alumno='+idAlumno+';'
        if v:
            print 'Query in GestorAlumnosSQL.getAlumno()'
            print query

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
            alm.urlImagen = row[9]

            print 'Nombre alumno: '+dbParams.formatOutputText(alm.nombre)

            return alm
        if salida==0:
            return 'Elemento no encontrado'

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
        query="UPDATE Alumno SET "+campoACambiar+"="+nuevoValor+" WHERE id_alumno="+idAlumno+";"



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
    def modAlumnoCompleto(self, idAlumno, nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL',  imagen='NULL'):
        '''
        Modifica todos los atributos de un alumno dado su id al mismo tiempo.
        '''

        #Info de seguimiento
        if v:
            print apiName
            print "Llamada a modAlumnoCompleto"
            print '\n'
            print locals()

        db = dbParams.conecta();
        query="UPDATE Alumno SET"
        query=query+" nombre= "+'\''+nombre+'\''
        query=query+" , apellidos= "+'\''+apellidos+'\''
        if dni=='NULL':
            query=query+" , dni=NULL "
        else:
            query=query+" , dni= "+'\''+dni+'\''
        query=query+" , direccion= "+'\''+direccion+'\''
        query=query+" , localidad= "+'\''+localidad+'\''
        query=query+" , provincia= "+'\''+provincia+'\''

        if fecha_nacimiento=='NULL':
            query=query+" , fecha_nacimiento=NULL "
        else:
            query=query+" , fecha_nacimiento= "+'\''+fecha_nacimiento+'\''


        query=query+" , telefono= "+'\''+telefono+'\''
        query=query+" , url_imagen= "+'\''+imagen+'\''

        #Codificamos el id porque es el único que no viene codificado desde la api para que no de problema al concatenar con la sentencia SQL
        query=query+" WHERE id_alumno="+dbParams.formatOutputText(idAlumno)+";"

        if v:
            print apiName
            print '\n'+query

        cursor = db.cursor()
        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
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
    def delAlumno(self, idAlumno):
        #print "Intentado eliminar alumno con dni "+str(dniAlumno)
        db = dbParams.conecta(); #La conexión está clara.
        cursor = db.cursor()
        idAlumno='\''+idAlumno+'\''
        query='delete from Alumno WHERE id_alumno='+idAlumno+';'
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
        #query='SELECT id_profesor, nombre, apellidos from Profesor where id_profesor in ( select id_profesor from Imparte where id_asignatura in (select id_asignatura from Matricula where id_alumno='+idAlumno+') and id_clase in  (select id_clase from Matricula where id_alumno='+idAlumno+'))'

        query='SELECT nombre, apellidos, id_profesor FROM Profesor WHERE id_profesor IN (SELECT id_profesor FROM Imparte, Matricula WHERE Imparte.id_asociacion=Matricula.id_asociacion and Matricula.id_alumno='+idAlumno+');'

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
        query='select * from Asignatura where id in (select id_asignatura from Matricula where id_alumno='+idAlumno+')'

        query='SELECT * FROM Asignatura WHERE id_asignatura IN (SELECT id_asignatura FROM Asocia WHERE id_asociacion IN (SELECT id_asociacion FROM Matricula WHERE id_alumno='+idAlumno+'));'

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
        query='SELECT * FROM Clase WHERE id_clase IN (SELECT id_clase FROM Asocia WHERE id_asociacion IN (SELECT id_asociacion FROM Matricula WHERE id_alumno='+idAlumno+'));'

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
