# -*- coding: utf-8 -*-
'''Clase controladora de alumnos. Que usando la clase que define el modelo de Alumno (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class Alumno:

    def __init__(self, id=None, nombre=None, apellidos=None, \
        dni=None, direccion=None, localidad=None, provincia=None, \
        fechaNacimiento=None, telefono=None, urlImagen=None):
        
        self.id = id
        self.nombre = nombre
        self.apellidos= apellidos
        self.dni = dni
        self.direccion = direccion
        self.localidad = localidad
        self.provincia = provincia
        self.fechaNacimiento = fechaNacimiento
        self.telefono = telefono
        self.urlImagen = urlImagen

'''
Modelo de la entidad alumno que añade la información del id_matricula para
cuando esa información es necesaria junto a los datos del alumno.
'''
class AlumnoExtendido(Alumno):

    def __init__(self):
        self.idMatricula = ""
