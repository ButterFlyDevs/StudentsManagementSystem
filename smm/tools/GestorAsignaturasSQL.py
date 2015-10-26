# -*- coding: utf-8 -*-
import MySQLdb
from Asignatura import *
from Profesor import *
from Alumno import *

'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAsignaturas:


    @classmethod
    def nuevaAsignatura(self, nombre, ide):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        query="insert into Asignatura values("+"'"+nombre+"', "+"'"+ide+"');"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def delAsignatura(self, idAsignatura):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Asignatura where id='"+idAsignatura+"';"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getAlumnosMatriculados(self, idAsignatura):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select Alumno.* from Alumno, Cursa, Asignatura where Alumno.dni=Cursa.dniAlumno and Cursa.idAsignatura=Asignatura.id and Asignatura.id='"+idAsignatura+"';"

        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.nombre=row[0]
            alumno.dni=row[1]
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getProfesoresQueImpartenLaAsignatura(self, idAsignatura):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select Profesor.*  from Profesor, Imparte, Asignatura where Profesor.dni=Imparte.dniProfesor and Imparte.idAsignatura=Asignatura.id and Asignatura.id='"+idAsignatura+"';"

        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            prf = Profesor()
            prf.nombre=row[0]
            prf.apellidos=row[1]
            #El profesor tiene más atributos pero no los vamos a usar en principio.
            lista.append(prf)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista




    @classmethod
    def getAsignatura(self, idAsignatura):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Asignatura where id='"+idAsignatura+"';"

        cursor.execute(query)
        row = cursor.fetchone()

        asig = Asignatura()
        asig.nombre=row[0]
        asig.id=row[1]

        cursor.close()
        db.close()

        return asig


    @classmethod
    def getAsignaturas(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm");

        cursor = db.cursor()

        query="select * from Asignatura";

        cursor.execute(query);

        row = cursor.fetchone()

        lista = []

        while row is not None:
            asg = Asignatura()
            asg.nombre=row[0]
            asg.id=row[1]
            lista.append(asg)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo


    '''Registro masivo de usuarios a partir de fichero CSV.
    Como opción para el Admin del Sistema se ofrece la subida masiva de usuarios al sistema mediante
    fichero CSV. Así podrá cargar todos los usuarios que el sistema de la Junta de Andalucía le ofrece para no
    tener que subirlos uno a uno.
    '''
    @classmethod
    def nuevosAlumnos(self):
        import csv
        import sys

        f = open('RegTutores.csv', 'r')

        csv.register_dialect('prueba', delimiter=',')


        reader = csv.reader(f, dialect='prueba')

        #Habilitar para el procesamiento del fichero completo.
        #for row in reader:
        for i in range(10):
                row = reader.next()
                nombre = row[0]
                nombreDividido = nombre.split(',')
                if len(nombreDividido)==2:
                        #print nombreDividido[1],nombreDividido[0]
                        nombre=unicode(nombreDividido[1], errors='replace')
                        apellidos=unicode(nombreDividido[0], errors='replace')

                    #    GestorAlumnos.nuevoAlumno(nombre, apellidos)

                else:
                        print nombreDividido[0]

    @classmethod
    def getNumeroAlumnos(self):
        pass # place magic here


    @classmethod
    def loadAlumnosFromCSVFile(self, file):
        pass #place magic here



    def all_unique(word):

        #Toda la palabra se pasa a mayúsculas
        word=word.upper()

        #Se recorren todas las letras de la palabra:
        for letter in range(len(word)):
            #Se extrae la letra de la palabra
            sectionWord=word[:letter]+word[letter+1:]
            #Se busca en el resto de la palabra si aparece la extraida.
            if sectionWord.find(word[letter]) != -1 :
                #Si se encuentra otra ocurrencia find devuelve la pos (-1 si no la encuentra) y
                #la función devuelve False porque no es una palabra sin elementos repetidos.
                return False
        #Si no se encuentran elementos repetidos se devuelve True.
        return True
