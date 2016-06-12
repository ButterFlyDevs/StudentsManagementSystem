# -*- coding: utf-8 -*-

##########################
### TESTING NDBLIB lib ###
##########################

"""
Fichero de testing para la libería de conexión NDBlib cuyo conector es gestor.py
@execution: Para ejecutar el test sólo hay que hacer: > python testUnitario.py y añadir la opción -v si queremos ver detalles.
"""



import unittest

#Para poder acceder a los ficheros en el directorio padre, los añadimos al path de python
import sys, os
sys.path.insert(0,os.pardir)

sys.path.insert(1, '/home/juan/Documentos/TFG/StudentsManagementSystem/google_appengine')
sys.path.insert(1, '/home/juan/Documentos/TFG/StudentsManagementSystem/google_appengine/lib/yaml/lib')

if 'google' in sys.modules:
    del sys.modules['google']

from google.appengine.ext import ndb
from google.appengine.ext import testbed

#Importamos la librería que vamos a testear:
from gestor import *

class TestNDBlib(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub(enable=True, save_changes=True, datastore_file='./prueba')
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()


    def test_01_insertStudent(self):
        test=False
        salida = Gestor.insertarAlumno(22424,'nombreEjemplo')

        #Comprobamos que se haya realizado una insercción
        consulta = Alumno.query()
        numElementos = consulta.count()

        #Comprobamos que se ha insertado bien
        consulta = Alumno.query(Alumno.idAlumno == 22424)
        alumno  = consulta.get();

        #Comprobamos que insertar otro con el mismo idAlumno da error
        salida2 = Gestor.insertarAlumno(22424, 'nombreEjemplo2')

        if (salida['status'] == 'OK' and numElementos == 1 and alumno.idAlumno == 22424 and salida2['status']=='FAIL'):
            test=True

        self.assertEqual(test, True)

    def test_02_updateStudent(self):
        test=False
        salida=Gestor.modificarAlumno(22424,'nombreModificado')

        #Extraemos al alumno y comprobamos si se ha modificado bien el nombre
        consulta = Alumno.query(Alumno.idAlumno == 22424)
        alumno = consulta.get()

        salida2=Gestor.modificarAlumno(4383, 'nombre')

        if (salida['status'] == 'OK' and
            alumno.nombreAlumno == 'nombreModificado' and
            salida2['status'] == 'FAIL' and
            salida2['info'] == 'Alumno con id 4383 no existe en el sistema'):
            test=True

        self.assertEqual(test, True)

    def test_03_deleteStudent(self):
        test=False
        salida=Gestor.eliminarAlumno(22424)
        if (salida['status'] == 'OK'):
            test=True
        self.assertEqual(test, True)



    def tearDown(self):
        self.testbed.deactivate()

    @classmethod
    def tearDownClass(self):
        """
        Elimina el fichero de la bd temporal tras la ejecución de todos los tests.
        """
        os.remove('./prueba')



if __name__ == '__main__':
    #La llamada a main hace que se ejecuten todos los métodos de todas las clases que heredan de TestCase
    unittest.main()
