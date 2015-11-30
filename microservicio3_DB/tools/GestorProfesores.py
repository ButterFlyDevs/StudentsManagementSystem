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

    @classmethod
    def compruebaProfesor(self, nombre, password):
        print 'Comprobando',nombre,password
        #Donde nombre será el campo nombre del profesor y la password su DNI
        qry=modeloProfesor.query(modeloProfesor.nombre==nombre, modeloProfesor.dni==password)
        if qry.count()==1:
            return True
