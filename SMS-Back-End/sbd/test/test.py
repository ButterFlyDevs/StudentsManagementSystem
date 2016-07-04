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
        if json.loads(requests.post(url, data={'tipo': 'Alumno', 'datos': json.dumps({'nombre': 'Juan Antonio'}) } ).text)['status'] != 'OK': test = False
        #Llamamos a la función haciendo que falten algunos parámetros para ver que no se realiza con éxito.
        if json.loads(requests.post(url, data={'datos': json.dumps({'nombra': 'Juan Antonio'}) } ).text)['status'] != 'FAIL': test = False
        if json.loads(requests.post(url, data={'tipo': 'Profesor', 'datos': json.dumps({'nombre': 'Juan Antonio'}) } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, data={'tipo': 'Asignatura', 'datos': json.dumps({'nombre': 'asig'}) } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, data={'tipo': 'Clase', 'datos': json.dumps({'curso': '1', 'grupo': 'A', 'nivel': 'ESO'}) } ).text)['status'] != 'OK': test = False

        #Entidades de relación
        if json.loads(requests.post(url, data={'tipo': 'Asociacion', 'datos': json.dumps({'idClase': '1', 'idAsignatura': '1'}) } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, data={'tipo': 'Asociacion', 'datos': json.dumps({'idClase': '1', 'idAsignatura': '1'}) } ).text)['status'] != 'Elemento duplicado': test = False
        if json.loads(requests.post(url, data={'tipo': 'Asociacion', 'datos': json.dumps({'idClase': '1', 'idAsignatura': '15'}) } ).text)['status'] != 'Alguno de los elementos no existe': test = False
        if json.loads(requests.post(url, data={'tipo': 'Imparte', 'datos': json.dumps({'idAsociacion': '1', 'idProfesor': '1'}) } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, data={'tipo': 'Imparte', 'datos': json.dumps({'idAsociacion': '1', 'idProfesor': '1'}) } ).text)['status'] != 'Elemento duplicado': test = False
        if json.loads(requests.post(url, data={'tipo': 'Matricula', 'datos': json.dumps({'idAlumno': '1', 'idAsociacion': '1'}) } ).text)['status'] != 'OK': test = False
        if json.loads(requests.post(url, data={'tipo': 'Matricula', 'datos': json.dumps({'idAlumno': '1', 'idAsociacion': '1'}) } ).text)['status'] != 'Elemento duplicado': test = False

        self.assertTrue(test)
    
    def test_02_getEntidades(self):
        test = True
        url = urlBase+'/entidades'

        #Introducimos un elemento
        if json.loads(requests.post(url, data={'tipo': 'Alumno', 'datos': json.dumps({'nombre': 'María'}) } ).text)['status'] != 'OK': test = False

        #if json.loads(requests.post(url, data={'tipo': 'Alumno', 'datos': json.dumps({'nombre': 'Maria'}) } ).text)['status'] != 'OK': test = False
        """
        if json.loads(requests.post(url, data={'tipo': 'Alumno', 'datos': json.dumps({'nombre': 'alumno2'}) } ).text)['status'] != 'OK': test = False

        #Extraemos un alumno en concreto
        data = requests.get(url, params={'tipo': 'Alumno', 'idEntidad': '1' })
        #Decompactamos el json con loads, ya que la API devuelve JSONs
        if json.loads(data.text)['nombre'] != u'alumno1': test = False

        #Extraemos la lista de todos
        data = requests.get(url, params={'tipo': 'Alumno'})
        print data.text
        #Decompactamos el json con loads, ya que la API devuelve JSONs
        if json.loads(data.text)[1]['nombre'] != u'alumno2': test = False
        """
        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()
