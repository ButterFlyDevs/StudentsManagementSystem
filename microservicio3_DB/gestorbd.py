#!/usr/bin/python3
# -*- coding: utf-8 -*-

import MySQLdb

import sys

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

class Alumno:

    def __init__(self):
        self.dni = ""
        self.nombre = ""

class Asignatura:

    def __init__(self):
        self.id = ""
        self.nombre = ""

class Profesor:

    def __init__(self):
        self.dni = ""
        self.nombre = ""
        self.apellidos = ""
        self.municipio = ""
        self.provincia = ""
        self.domicilio = ""
        self.email = ""
        self.telefono = ""

class Grupo:

    def __init__(self):
        self.curso = ""
        self.letra = ""

class Pertenece:

    def __init__(self):

        self.curso_p = ""
        self.letra_p = ""
        self.idAsignatura = ""
        '''
        self.grupo = Grupo()
        self.Asignatura = Asignatura()
        '''

class Imparte:

    def __init__(self):
        self.curso_i = ""
        self.letra_i = ""
        self.idAsignatura = ""
        self.dniProfesor = ""
        '''
        self.Profesor = Profesor()
        self.Pertenece = Pertenece()
        '''

class Cursa:

    def __init__(self):
        self.curso_c = ""
        self.letra_c = ""
        self.idAsignatura = ""
        self.dniAlumno = ""
        '''
        self.Alumno = Alumno()
        self.Pertenece = Pertenece()
        '''






class GestorAlumno:

    @classmethod
    def nuevoAlumno(self, dni, nombre):
        #db = MySQLdb.connect(host="us-cdbr-azure-central-a.cloudapp.net", user="bfeae6941ba94f", passwd="600dee2e", db="as_d754cdef0225140")
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel= "Select count(*) from Alumno where (dni ='"+str(dni)+"');"
        query="INSERT INTO Alumno values("+"'"+str(dni)+"', "+"'"+nombre+"');"

        cursor = db.cursor()

        cursor.execute(sel)
        existe=int(cursor.fetchone()[0])

        if existe==0:
        	cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getAlumnos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")
        cursor = db.cursor()
        query="select * from Alumno";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.dni=row[0]
            alumno.nombre=row[1]
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

'''
    @classmethod
    def borrarAlumno(self, dnient):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb"); #La conexión está clara.
        query="DELETE FROM Alumno WHERE dni="+dnient+";"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()
'''

class GestorAsignatura:

    @classmethod
    def nuevaAsignatura(self, id, nombre):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel= "Select count(*) from Asignatura where (id ='"+str(id)+"');"
        query="INSERT INTO Asignatura values("+"'"+str(id)+"', "+"'"+nombre+"');"

        cursor = db.cursor()

        cursor.execute(sel)
        existe=int(cursor.fetchone()[0])

        if existe==0:
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getAsignaturas(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        cursor = db.cursor()
        query="select * from Asignatura";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []


        while row is not None:
            asignatura = Asignatura()
            asignatura.id=row[0]
            asignatura.nombre=row[1]        #str(row[1]).decode('ISO-8859-1')
            lista.append(asignatura)
            #print row[0], row[1]
            row = cursor.fetchone()
        """
        for row in cursor:
            asignatura = Asignatura()
            asignatura.id=row[0]
            asignatura.nombre=row[1]        #str(row[1]).decode('ISO-8859-1')
            lista.append(asignatura)
        """
        cursor.close()
        db.close()

        return lista

'''
    @classmethod
    def borrarAsignatura(self, id):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb"); #La conexión está clara.
        query="DELETE FROM Asignatura WHERE id="+id+";"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()
'''

class GestorProfesor:

    @classmethod
    def nuevoProfesor(self, dni, nombre, apellidos, municipio, provincia, domicilio, email, telefono):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel= "Select count(*) from Profesor where (dni ='"+str(dni)+"');"
        query="INSERT INTO Profesor values("+"'"+str(dni)+"', "+"'"+nombre+"', "+"'"+apellidos+"', "+"'"+municipio+"', "+"'"+provincia+"', "+"'"+domicilio+"', "+"'"+email+"', "+"'"+str(telefono)+"');"

        cursor = db.cursor()

        cursor.execute(sel)
        existe=int(cursor.fetchone()[0])

        if existe==0:
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getProfesores(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        cursor = db.cursor()
        query="select * from Profesor";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            profesor = Profesor()
            profesor.dni=row[0]
            profesor.nombre=row[1]
            profesor.apellidos=row[2]
            profesor.municipio=row[3]
            profesor.provincia=row[4]
            profesor.domicilio=row[5]
            profesor.email=row[6]
            profesor.telefono=row[7]
            lista.append(profesor)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

'''
    @classmethod
    def borrarProfesor(self, id):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")
        query="DELETE FROM Profesor WHERE dni="+dni+";"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()
'''

class GestorGrupo:

    @classmethod
    def nuevoGrupo(self, id, nombre):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel= "Select count(*) from Grupo where (id ='"+str(curso)+"AND letra ='"+letra+"');"
        query="INSERT INTO Grupo values("+"'"+str(curso)+"', "+"'"+letra+"');"

        cursor = db.cursor()

        cursor.execute(sel)
        existe=int(cursor.fetchone()[0])

        if existe==0:
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getGrupos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        cursor = db.cursor()
        query="select * from Grupo";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []
        grupo = Grupo()

        while row is not None:
            grupo.curso=row[0]
            grupo.letra=row[1]
            lista.append(Grupo)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

'''
    @classmethod
    def borrarGrupo(self, curso, letra):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")
        query="DELETE FROM Asignatura WHERE curso="+curso+"AND letra="+letra+";"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()
'''

class GestorPertenece:

    @classmethod
    def nuevaPertenencia(self, curso, letra, idAsignatura):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel_c= "SELECT count(*) from Pertenece where curso_p ="+"'"+str(curso)+"' AND letra_p='"+letra+"' AND idAsignatura_p='"+str(idAsignatura)+"';"
        sel_e= "SELECT count(*) from Asignatura where (id ="+"'"+str(idAsignatura)+"');"
        query="INSERT INTO Pertenece values("+"'"+str(curso)+"', '"+str(letra)+"', '"+str(idAsignatura)+"');"

        cursor = db.cursor()

        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])
        cursor.execute(sel_e)
        existe_e=int(cursor.fetchone()[0])

        if existe_c==0 and existe_e>0:
        	gs.nuevoGrupo(curso, letra)
        	cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def borrarPertenencia(self, curso, letra, dni):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel_c= "SELECT count(*) from Cursa where curso_c ="+"'"+str(curso)+"' AND letra_c='"+letra+"' and  idAsignatura_c='"+str(idAsignatura)+"';"
        query="DELETE FROM Cursa where where curso_c ="+"'"+str(curso)+"' AND letra_c='"+letra+"' and  idAsignatura_c='"+str(idAsignatura)+"';"

        cursor = db.cursor()


        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])


        if existe_c>0 :
        	cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()


    @classmethod
    def getPertenencias(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb");

        cursor = db.cursor()
        query="select * from Pertenece";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            pertenece = Pertenece()
            pertenece.curso_p=row[0]
            pertenece.letra_p=row[1]
            pertenece.idAsignatura=row[2]
            lista.append(pertenece)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

class GestorImparte:

    @classmethod
    def nuevaImparticion(self, curso, letra, idAsignatura, dniProfesor):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")
        gs=GestorUsuario()
        sel_c= "SELECT count(*) from Imparte where curso_i ="+"'"+str(curso)+"' AND letra_i='"+letra+"' and  idAsignatura_i='"+str(idAsignatura)+"', dniProfesor='"+str(dniProfesor)+"';"
        sel_e= "SELECT count(*) from Pertenece where (curso_p ="+"'"+str(curso)+"' AND letra_p='"+letra+"' AND idAsignatura_p ="+"'"+str(idAsignatura)+"');"
        sel_g= "SELECT count(*) from Profesor where (dni="+"'"+str(dniProfesor)+"');"
        query="INSERT INTO Imparte values("+"'"+str(curso)+"', '"+str(letra)+"', '"+str(idAsignatura)+"', '"+str(dniProfesor)+"');"

        cursor = db.cursor()

        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])
        cursor.execute(sel_e)
        existe_e=int(cursor.fetchone()[0])
        cursor.execute(sel_g)
        existe_g=int(cursor.fetchone()[0])

        if existe_c==0 and existe_e>0 and existe_g>0:
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def borrarImparticion(self, curso, letra, idAsignatura, dniProfesor):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel_c= "SELECT count(*) from Imparte where curso_i ="+"'"+str(curso)+"' AND letra_i='"+letra+"' and  idAsignatura_i='"+str(idAsignatura)+"', dniProfesor='"+str(dniProfesor)+"';"
        query="DELETE FROM Imparte where where curso_i ="+"'"+str(curso)+"' AND letra_i='"+letra+"' and  idAsignatura_i='"+str(idAsignatura)+"', dniProfesor='"+str(dniProfesor)+"';"

        cursor = db.cursor()


        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])


        if existe_c>0 :
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()


    @classmethod
    def getImparticiones(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb");

        cursor = db.cursor()
        query="select * from Imparte";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            imparte = Imparte()
            imparte.curso_i=row[0]
            imparte.letra_i=row[1]
            imparte.idAsignatura=row[2]
            imparte.dniProfesor=row[3]
            lista.append(imparte)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista


class GestorCursa:

    @classmethod
    def nuevoCurso(self, curso, letra, idAsignatura, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")
        gs=GestorUsuario()
        sel_c= "SELECT count(*) from Cursa where curso_c ="+"'"+str(curso)+"' AND letra_c='"+letra+"' and  idAsignatura_c='"+str(idAsignatura)+"', dniAlumno='"+str(dniAlumno)+"';"
        sel_e= "SELECT count(*) from Pertenece where (curso_p ="+"'"+str(curso)+"' AND letra_p='"+letra+"' AND idAsignatura_p ="+"'"+str(idAsignatura)+"');"
        sel_g= "SELECT count(*) from Alumno where (dni="+"'"+str(dniAlumno)+"');"
        query="INSERT INTO Cursa values("+"'"+str(curso)+"', '"+str(letra)+"', '"+str(idAsignatura)+"', '"+str(dniAlumno)+"');"

        cursor = db.cursor()

        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])
        cursor.execute(sel_e)
        existe_e=int(cursor.fetchone()[0])
        cursor.execute(sel_g)
        existe_g=int(cursor.fetchone()[0])

        if existe_c==0 and existe_e>0 and existe_g>0:
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def borrarCurso(self, curso, letra, idAsignatura, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb")

        sel_c= "SELECT count(*) from Cursa where curso_c ="+"'"+str(curso)+"' AND letra_c='"+letra+"' and  idAsignatura_c='"+str(idAsignatura)+"', dniAlumno='"+str(dniAlumno)+"';"
        query="DELETE FROM Cursa where where curso_c ="+"'"+str(curso)+"' AND letra_c='"+letra+"' and  idAsignatura_c='"+str(idAsignatura)+"', dniAlumno='"+str(dniAlumno)+"';"

        cursor = db.cursor()


        cursor.execute(sel_c)
        existe_c=int(cursor.fetchone()[0])


        if existe_c>0 :
            cursor.execute(query)

        db.commit()
        cursor.close()
        db.close()


    @classmethod
    def getCursos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="mdb");

        cursor = db.cursor()
        query="select * from Cursa";
        cursor.execute(query);
        row = cursor.fetchone()

        lista = []

        while row is not None:
            cursa = Cursa()
            cursa.curso_c=row[0]
            cursa.letra_c=row[1]
            cursa.idAsignatura=row[2]
            cursa.dniAlumno=row[3]
            lista.append(cursa)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista
