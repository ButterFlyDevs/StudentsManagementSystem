# -*- coding: utf-8 -*-
import MySQLdb
from Alumno import *

'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorAlumnos:


    @classmethod
    def nuevoAlumno(self, nombre, apellidos):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        query="insert into Alumno values("+"'"+nombre+"', "+"'"+apellidos+"');"
        db.query(query);

    @classmethod
    def getAlumnos(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm");

        cursor = db.cursor()

        query="select * from Alumno";

        cursor.execute(query);

        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.nombre=row[0]
            alumno.apellidos=row[1]
            lista.append(alumno)
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
