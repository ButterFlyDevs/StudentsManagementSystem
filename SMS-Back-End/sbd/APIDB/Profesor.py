# -*- coding: utf-8 -*-
'''
Modelo de la entidad profesor, siguiendo el esquema de la base de datos
'''
class Profesor:

    def __init__(self):
        self.id = ""
        self.nombre = ""
        self.apellidos = ""
        self.dni = ""
        self.direccion = ""
        self.localidad = ""
        self.provincia = ""
        self.fechaNacimiento = ""
        self.telefono = ""


'''
Modelo de la entidad profesor que añade la información del id_imparte para
cuando esa información es necesaria junto a los datos del profesor.
'''
class ProfesorExtendido(Profesor):

    def __init__(self):
        self.idImparte = ""
