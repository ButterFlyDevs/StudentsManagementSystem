# -*- coding: utf-8 -*-
from Alumno import *
import requests
import json

'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class GestorAlumnos:

    @classmethod
    def getAlumnos(self):
        #alumnos = modeloAlumno.query()
        #GestorAlumnos.nuevosAlumnos()

        ''' De prueba:
        #Vamos a devolver una lista de objetos de tipo Alumno
        lista = []
        for a in range(30):
            lista.append(Alumno("juan","45601217"))
        return lista
        '''

        #Vamos a conectarnos al servicio de BD y vamos a pedirle los alumnos:

        r = requests.get('http://localhost:8001/infoProfesor/hey')
        print "salida de la petición: "
        print r.text

        parsed_input=json.loads(r.text)

        #Extraemos la lista de profesores:
        lista=parsed_input['profesores']
        listaTemplate= []
        #Recorremos la lista
        for a in lista:
            al = Alumno()
            al.nombre= a['nombre']
            al.apellidos= a['apellidos']
            listaTemplate.append(al)





        #j = '{"nombre": "juan", "apellidos": "antonio"}'
        #Ahora vamos a convertir la respuesta en objetos de tipo Alumno
        '''
        alumno=Payload(r.text)

        print alumno.nombre
        print alumno.apellidos

        a = Alumno()
        a.nombre=alumno.nombre
        a.apellidos=alumno.apellidos
        print a.nombre
        '''

        return listaTemplate
