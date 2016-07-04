# -*- coding: utf-8 -*-

'''
Para ejecutar el test sólo hay que hacer:
python test.py, con -v para más detalles.


Covertura:

Para que genere contenido en html python-coverage html


'''

#Para hacer los tests unitarios de la api.
import unittest
#More about in: https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUp


#Importamos la propia api, que es 'app' en el fichero 'main.py'
import sys, os
import requests
import jsonpickle

import json
from termcolor import colored
import time

urlBase = 'http://localhost:8002'

class SBD_API_TEST(unittest.TestCase):


    def setUp(self):
        os.system('mysql -u root -p\'root\' < ../APIDB/DBCreatorv1.sql')

    def test_00_PruebaAPI(self):
        url = urlBase+'/test'
        respuesta = requests.get(url)
        self.assertTrue( ('testOK' in str(respuesta.text)) )


    def test_01_postEntidades(self):
        test = True
        url = urlBase+'/entidades'


        #Entidades normales
        if json.loads(requests.post(url, json={'tipo': 'Alumno', 'datos': {'nombre': 'Juan Antonio'}} ).text)['status'] != 'OK': test = False
        #Llamamos a la función haciendo que falten algunos parámetros para ver que no se realiza con éxito.
        if json.loads(requests.post(url, json={'datos': {'nombre': 'Juan Antonio'}} ).text)['status'] != 'FAIL': test = False

        if json.loads(requests.post(url, json={'tipo': 'Profesor', 'datos': {'nombre': 'Juan Antonio'}} ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, json={'tipo': 'Asignatura', 'datos': {'nombre': 'asig'}} ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, json={'tipo': 'Clase', 'datos': {'curso': '1', 'grupo': 'A', 'nivel': 'ESO'}} ).text)['status'] != 'OK': test = False

        #Entidades de relación
        if json.loads(requests.post(url, json={'tipo': 'Asociacion', 'datos': {'idClase': '1', 'idAsignatura': '1'} } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, json={'tipo': 'Asociacion', 'datos': {'idClase': '1', 'idAsignatura': '1'} } ).text)['status'] != 'FAIL': test = False
        if json.loads(requests.post(url, json={'tipo': 'Asociacion', 'datos': {'idClase': '1', 'idAsignatura': '15'} } ).text)['status'] != 'FAIL': test = False
        if json.loads(requests.post(url, json={'tipo': 'Imparte', 'datos': {'idAsociacion': '1', 'idProfesor': '1'} } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, json={'tipo': 'Imparte', 'datos': {'idAsociacion': '1', 'idProfesor': '1'} } ).text)['status'] != 'FAIL': test = False
        if json.loads(requests.post(url, json={'tipo': 'Matricula', 'datos': {'idAlumno': '1', 'idAsociacion': '1'} } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, json={'tipo': 'Matricula', 'datos': {'idAlumno': '1', 'idAsociacion': '1'} } ).text)['status'] != 'FAIL': test = False

        self.assertTrue(test)


    def test_02_getEntidades(self):
        test = True
        url = urlBase+'/entidades'

        #Introducimos un tipo de Entidad Alumno
        payload={'tipo': 'Alumno', 'datos': {'nombre': 'María'} }
        if  json.loads(requests.post(url, json=payload).text)['status'] != 'OK': test = False
        payload={'tipo': 'Alumno', 'datos': {'nombre': 'María2'} }
        if  json.loads(requests.post(url, json=payload).text)['status'] != 'OK': test = False
        #Extraemos un alumno en concreto
        #data = requests.get(url2, params={'tipo': 'Alumno', 'idEntidad': '1' })
        data = requests.get(url+'/Alumno/1')
        #Decompactamos el json con loads, ya que la API devuelve JSONs
        if json.loads(data.text)['nombre'] != u'María': test = False
        #Extraemos la lista de todas las entidades de tipo Alumno en su versión resumida.
        data = requests.get(url+'/Alumno')
        #Decompactamos el json con loads, ya que la API devuelve JSONs
        if json.loads(data.text)[1]['nombre'] != u'María2': test = False

        #Repetimos con el tipo Profesor
        if  json.loads(requests.post(url, json={'tipo': 'Profesor', 'datos': {'nombre': 'Juan'} }).text)['status'] != 'OK': test = False
        if  json.loads(requests.post(url, json={'tipo': 'Profesor', 'datos': {'nombre': 'Lucas'} }).text)['status'] != 'OK': test = False
        if json.loads(requests.get(url+'/Profesor/1').text)['nombre'] != u'Juan': test = False
        if json.loads(requests.get(url+'/Profesor').text)[1]['nombre'] != u'Lucas': test = False

        #Repetimos con el tipo Asignatura
        if  json.loads(requests.post(url, json={'tipo': 'Asignatura', 'datos': {'nombre': 'química'} }).text)['status'] != 'OK': test = False
        if  json.loads(requests.post(url, json={'tipo': 'Asignatura', 'datos': {'nombre': 'rología'} }).text)['status'] != 'OK': test = False
        if json.loads(requests.get(url+'/Asignatura/1').text)['nombre'] != u'química': test = False
        if json.loads(requests.get(url+'/Asignatura').text)[1]['nombre'] != u'rología': test = False

        #Repetimos con el tipo Clase
        if  json.loads(requests.post(url, json={'tipo': 'Clase', 'datos': {'curso': '1', 'grupo': 'A', 'nivel': 'ESO'} }).text)['status'] != 'OK': test = False
        if  json.loads(requests.post(url, json={'tipo': 'Clase', 'datos': {'curso': '1', 'grupo': 'B', 'nivel': 'ESO'} }).text)['status'] != 'OK': test = False
        if json.loads(requests.get(url+'/Clase/1').text)['nivel'] != u'ESO': test = False
        if json.loads(requests.get(url+'/Clase').text)[1]['nivel'] != u'ESO': test = False


        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()
