# -*- coding: utf-8 -*-
from model.modeloAsignatura import modeloAsignatura


class GestorAsignaturas:

    '''Crea un nuevo usuario en la base de datos del sistema haciendo uso del modelo creado con ndb especificado
    en model.modeloProfesor.py
    '''
    @classmethod
    def nuevaAsignatura(self, nombre, curso):

        asignatura = modeloAsignatura()
        asignatura.nombre = nombre
        asignatura.curso = curso
        asignatura.put()

    @classmethod
    def getAsignaturas(self):
        asignaturas = modeloAsignatura.query()
        #GestorAlumnos.nuevosAlumnos()
        return asignaturas.fetch(100)
