# -*- coding: utf-8 -*-
'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class Alumno:

    def __init__(self):
        self.id = ""
        self.nombre = ""
        self.apellidos= ""
        self.dni = ""
        self.direccion = ""
        self.localidad = ""
        self.provincia = ""
        self.fecha_nacimiento = ""
        self.telefono = ""
