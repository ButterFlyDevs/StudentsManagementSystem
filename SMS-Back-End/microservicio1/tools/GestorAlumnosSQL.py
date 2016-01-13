# -*- coding: utf-8 -*-
import MySQLdb
from Alumno import *

'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAlumnos:

    @classmethod
    def nuevoAlumno(self, nombre, dni):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        query="INSERT INTO Alumno values("+"'"+nombre+"', "+"'"+dni+"');"
        cursor = db.cursor()
        cursor.execute(query);
        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def getAlumnos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm")
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
            #print alumno.nombre
            #print alumno.dni
            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getAlumno(self, dniAlumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        query="select * from Alumno where dni='"+dniAlumno+"';"

        cursor.execute(query)
        row = cursor.fetchone()

        alm = Alumno()
        alm.nombre=row[0]
        alm.dni=row[1]

        cursor.close()
        db.close()

        return alm
