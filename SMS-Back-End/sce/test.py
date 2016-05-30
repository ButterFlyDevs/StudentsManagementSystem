# -*- coding: utf-8 -*-

#Para hacer los tests unitarios de la api.
import unittest
#More about in: https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUp


#Importamos la propia api, que es 'app' en el fichero 'main.py'
import sys, os
sys.path.insert(0,os.pardir)
from api import app

import jsonpickle
# === Clase de pruebas (testeo) ===
"""
Métodos usados para testear el servicio de control de estudiantes
"""
class SCE_API_TESTS(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_prueba(self):
        respuesta = self.app.get('/prueba')
        assert 'SCE MicroService is RUNING!\n' in respuesta.data


if __name__ == '__main__':
    unittest.main()
