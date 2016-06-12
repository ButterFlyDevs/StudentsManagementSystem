# -*- coding: utf-8 -*-
"""
Para ejecutar el test sólo hay que hacer:
python test.py, con -v para más detalles.
Covertura:
Para que genere contenido en html python-coverage html
"""

#Para hacer los tests unitarios de la api.
import unittest
#More about in: https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUp

#Como las respuestas son siempre en json incluimos la librería para decodificarlas y tratarlas.
import jsonpickle
#Para hacer las peticiones a la api de forma simple
import requests
urlBase = 'http://localhost:8003'

"""
Métodos usados para testear el servicio de control de estudiantes
"""
class SCE_API_TESTS(unittest.TestCase):

    def setUp(self):
        pass

    def testPruebaEstado(self):
        import requests
        res = requests.get(urlBase+'/prueba')
        assert 'SCE MicroService is RUNING!\n' in res

    def test_01_insertarAlumno(self):
        url     = urlBase+'/alumnos'

        #Introducir un alumno es correcto:
        payload = { 'idAlumno' : 3134, 'nombreAlumno' : 'Pedro' }
        res = requests.post(url, data=payload)
        res = jsonpickle.decode(res.text)
        if (res['status'] == 'OK'):
            print 'OLE'

        #Introducir un alumno con idAlumno ya existente da el error correcto:
        




        self.assertEqual(res['status'], 'OK', 'Acción no realizada con éxito.')

if __name__ == '__main__':
    unittest.main()
