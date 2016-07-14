# -*- coding: utf-8 -*-
"""
Para ejecutar el test sólo hay que hacer:
python test.py, con -v para más detalles.
Covertura:
Para que genere contenido en html python-coverage html

..note:
    Para que este test pueda ejecutarse debe estar activado el servidor de desarrollo.

"""

#Para hacer los tests unitarios de la api.
import unittest
#More about in: https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUp

#Como las respuestas son siempre en json incluimos la librería para decodificarlas y tratarlas.
import jsonpickle
#Para hacer las peticiones a la api de forma simple
#http://docs.python-requests.org/en/master/
import requests
#Para los sleeps
import time
urlBase = 'http://localhost:8003'
from termcolor import colored
"""
Métodos usados para testear el servicio de control de estudiantes
"""
class SCE_API_TESTS(unittest.TestCase):

    def setUp(self):
        pass

    def testPruebaEstado(self):
        res = requests.get(urlBase+'/prueba')
        assert 'SCE MicroService is RUNING!\n' in res

    def test_01_insertarEntidad(self):
        test = True
        url     = urlBase+'/entidadesReferencia'
        #Introducir un alumno es correcto:
        res = requests.post(url, data={ 'tipo': 'Alumno', 'idEntidad': 3135, 'nombreEntidad': 'Pedro' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'OK'): test = False

        #Si no esperamos se solapan las llamadas se solapan y las comprobaciones no se hacen correctamente.
        ### WARNING ###
        import time
        time.sleep(1)

        #Introducir un alumno con idAlumno ya existente da el error correcto:
        res = requests.post(url, data={ 'tipo': 'Alumno', 'idEntidad': 3135, 'nombreEntidad': 'Pedro' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'FAIL'): test = False


        #Introducir un alumno es correcto:
        res = requests.post(url, data={ 'tipo': 'Profesor', 'idEntidad': 3135, 'nombreEntidad': 'ProfesorA' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'OK'): test = False

        #Si no esperamos se solapan las llamadas se solapan y las comprobaciones no se hacen correctamente.
        ### WARNING ###
        time.sleep(1)

        #Introducir un alumno con idAlumno ya existente da el error correcto:
        res = requests.post(url, data={ 'tipo': 'Profesor', 'idEntidad': 3135, 'nombreEntidad': 'ProfesorA' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'FAIL'): test = False


        self.assertEqual(test, True)

    def test_02_modificarEntidad(self):
        test = True
        url = urlBase+'/entidadesReferencia'

        res = requests.put(url, data={ 'tipo': 'Alumno', 'idEntidad': 3135, 'nombreEntidad': 'nuevoNombre' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'OK'): test = False

        res = requests.put(url, data={ 'tipo': 'Profesor', 'idEntidad': 3135, 'nombreEntidad': 'nuevoNombre' })
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'OK'): test = False

    def test_03_eliminarEntidad(self):
        test = True
        url = urlBase+'/entidadesReferencia'

        #El método delete no permite payload y hay que pasar los datos por url

        res = requests.delete(url+'/Alumno/3135')
        res = jsonpickle.decode(res.text)
        if (res['status'] != 'OK'): test = False

        res = requests.delete(url+'/Profesor/3135')
        res = jsonpickle.decode(res.text)
        if (res['status'] != 'OK'): test = False

        time.sleep(0.5)

        #Si ya se ha elminado no debe encontrarlo
        res = requests.delete(url+'/Profesor/3135')
        res = jsonpickle.decode(res.text)
        if (res['status'] != 'FAIL'): test = False


        self.assertEqual(test, True)

    def test_04_MetodosControlAsistencia(self):
        test = True

        url     = urlBase+'/controlesAsistencia'

        payload={
                 "microControlesAsistencia": [
                    {
                      "asistencia" : 1,
                      "retraso": 0,
                      "retrasoTiempo" : 0,
                      "retrasoJustificado" : 0,
                      "uniforme" : 1,
                      "idAlumno" : 11
                    },
                    {
                      "asistencia" : 0,
                      "retraso": 1,
                      "retrasoTiempo" : 1,
                      "retrasoJustificado" : 1,
                      "uniforme" : 0,
                      "idAlumno" : 15
                    }
                  ],
                "idProfesor" : 22,
                "idClase" : 33,
                "idAsignatura" : 44
               }

        #1. Lo enviamos para que se guarde con el método post a la url
        res = requests.post(url, json=payload)
        res = jsonpickle.decode(res.text)
        print colored(res, 'red')
        if (res['status'] != 'OK'): test = False
        key = res['key']
        time.sleep(1)

        #2. Ahora lo rescatamos para ver que se ha guardado bien
        res = requests.get(url+'/'+str(key))
        print 'Haciendo petición a: '
        print res.url
        print res.text
        res = jsonpickle.decode(res.text)

        for r in  res['microControlesAsistencia']:
            print 'Control:'
            print r
            print '\n'

        #Comprobamos algunos de los datos que esperamos
        if ( #Si alguno de las condiciones falla, falla el test.
           res['idClase'] != 33
           or len(res['microControlesAsistencia']) != 2
           or (res['microControlesAsistencia'][0])['asistencia'] != 1
           or res['idAsignatura'] != 44
           ): test = False

        time.sleep(1)

        #Comprobamos antes de eliminarlo que se pueden recuperar los resúmenes bien.
        url2 = urlBase+'/resumenesControlesAsistencia'
        if (len(jsonpickle.decode(requests.post(url2, data={ 'idProfesor': '22'}).text)) != 1): test = False #Existe
        if (len(jsonpickle.decode(requests.post(url2, data={ 'idProfesor': '3726'}).text)) != 0): test = False #No existe

        #3. Probamos que se puede eliminar bien
        res = requests.delete(url+'/'+str(key))
        res = jsonpickle.decode(res.text)
        print res
        if (res['status'] != 'OK'): test = False

        time.sleep(1)

        self.assertEqual(test, True)


    @classmethod
    def tearDownClass(self):
        """
        Elimina los datos creados por los test, se ejecuta al finalizar todos los test.
        """
        print 'Tras todos los test'

if __name__ == '__main__':
    unittest.main()
