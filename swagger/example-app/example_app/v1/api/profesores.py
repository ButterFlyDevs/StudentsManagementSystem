# -*- coding: utf-8 -*-
from flask import request, g

from . import Resource
from .. import schemas


#Definición del recurso profsores
class Profesores(Resource):

    def get(self):

        #Código donde se realizará el procesamiento de los datos pedido antes de su devolución.
        cases = [{'nombre': 'juan', 'apellidos': 'fernandez chacón'},
                 {'nombre': 'maria', 'apellidos': 'adelaida gomez'  }]


        return cases, 200, None
