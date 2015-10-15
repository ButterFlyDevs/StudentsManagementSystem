# -*- coding: utf-8 -*-
from model.modeloProfesor import modeloProfesor


class GestorProfesores:

    '''Crea un nuevo usuario en la base de datos del sistema haciendo uso del modelo creado con ndb especificado
    en model.modeloProfesor.py
    '''
    @classmethod
    def nuevoProfesor(self, nombre, apellidos, dni):

        profesor = modeloProfesor()
        profesor.nombre = nombre
        profesor.apellidos = apellidos
        profesor.dni = dni        
        profesor.put()

    @classmethod
    def getProfesores(self):
        profesores = modeloProfesor.query()
        #GestorAlumnos.nuevosAlumnos()
        return profesores.fetch(100)
