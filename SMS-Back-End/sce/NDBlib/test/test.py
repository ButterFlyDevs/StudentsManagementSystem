# -*- coding: utf-8 -*-

##########################
### TESTING NDBLIB lib ###
##########################

"""
Fichero de testing para la libería de conexión NDBlib cuyo conector es gestor.py
@execution: Para ejecutar el test sólo hay que hacer: > python testUnitario.py y añadir la opción -v si queremos ver detalles.
"""

import unittest
import sys, os
sys.path.insert(0,os.pardir)

sys.path.insert(1, '../../../../google_appengine')

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

    def test_01_insertEntitiy(self):
        """
        Test de comprobación de insercción en los tipos básicos de referencia: Alumno, Profesor, Clase, Asignatura
        """

        test=True

        #Comprobamos la inserción del tipo Alumno
        salida = Gestor.insertarEntidad('Alumno', 22424, 'nombreEjemplo')
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de insercción.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que se ha insertando un elemento
           or Alumno.query().count() != 1
           #Que el elemnto es accesible por el id y el nombre ha sido grabado bien.
           or Alumno.query(Alumno.idAlumno == 22424).get().nombreAlumno != 'nombreEjemplo'
           #Que al intentar insertar otra entidad con el mismo id nos da el error esperado
           or Gestor.insertarEntidad('Alumno', 22424, 'nombreEjemplo')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la inserción del tipo Profesor
        salida = Gestor.insertarEntidad('Profesor', 22424, 'nombreEjemplo')
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de insercción.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que se ha insertando un elemento
           or Profesor.query().count() != 1
           #Que el elemnto es accesible por el id y el nombre ha sido grabado bien.
           or Profesor.query(Profesor.idProfesor == 22424).get().nombreProfesor != 'nombreEjemplo'
           #Que al intentar insertar otra entidad con el mismo id nos da el error esperado
           or Gestor.insertarEntidad('Profesor', 22424, 'nombreEjemplo')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la inserción del tipo Clase
        salida = Gestor.insertarEntidad('Clase', 22424, 'nombreEjemplo')
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de insercción.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que se ha insertando un elemento
           or Clase.query().count() != 1
           #Que el elemnto es accesible por el id y el nombre ha sido grabado bien.
           or Clase.query(Clase.idClase == 22424).get().nombreClase != 'nombreEjemplo'
           #Que al intentar insertar otra entidad con el mismo id nos da el error esperado
           or Gestor.insertarEntidad('Clase', 22424, 'nombreEjemplo')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la inserción del tipo Asignatura
        salida = Gestor.insertarEntidad('Asignatura', 22424, 'nombreEjemplo')
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de insercción.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que se ha insertando un elemento
           or Asignatura.query().count() != 1
           #Que el elemnto es accesible por el id y el nombre ha sido grabado bien.
           or Asignatura.query(Asignatura.idAsignatura == 22424).get().nombreAsignatura != 'nombreEjemplo'
           #Que al intentar insertar otra entidad con el mismo id nos da el error esperado
           or Gestor.insertarEntidad('Asignatura', 22424, 'nombreEjemplo')['status'] != 'FAIL'
           ): test = False

        self.assertEqual(test, True)

    def test_02_updateEntitiy(self):
        """
        Test de comprobación de modificación en los cuatro tipos de referencia: Alumno, Profesor, Clase, Asignatura
        """

        test=True

        #Comprobamos la modificación de una entidad del tipo Alumno (previamente existente)
        salida = Gestor.modificarEntidad('Alumno', 22424, 'nuevoSuperNombre')
        print salida
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de modificación.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que sigue existiendo solo un elemento.
           or Alumno.query().count() != 1
           #Que el elemento es accesible por el id y el nombre ha sido modificado bien.
           or Alumno.query(Alumno.idAlumno == 22424).get().nombreAlumno != 'nuevoSuperNombre'
           #Que al intentar modificar una entidad inexistente da error.
           or Gestor.modificarEntidad('Alumno', 2313, 'nuevoNombre')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la modificación de una entidad del tipo Profesor (previamente existente)
        salida = Gestor.modificarEntidad('Profesor', 22424, 'nuevoSuperNombre')
        print salida
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de modificación.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que sigue existiendo solo un elemento.
           or Profesor.query().count() != 1
           #Que el elemento es accesible por el id y el nombre ha sido modificado bien.
           or Profesor.query(Profesor.idProfesor == 22424).get().nombreProfesor != 'nuevoSuperNombre'
           #Que al intentar modificar una entidad inexistente da error.
           or Gestor.modificarEntidad('Profesor', 2313, 'nuevoNombre')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la modificación de una entidad del tipo Clase (previamente existente)
        salida = Gestor.modificarEntidad('Clase', 22424, 'nuevoSuperNombre')
        print salida
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de modificación.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que sigue existiendo solo un elemento.
           or Clase.query().count() != 1
           #Que el elemento es accesible por el id y el nombre ha sido modificado bien.
           or Clase.query(Clase.idClase == 22424).get().nombreClase != 'nuevoSuperNombre'
           #Que al intentar modificar una entidad inexistente da error.
           or Gestor.modificarEntidad('Clase', 2313, 'nuevoNombre')['status'] != 'FAIL'
           ): test = False

        #Comprobamos la modificación de una entidad del tipo Alumno (previamente existente)
        salida = Gestor.modificarEntidad('Asignatura', 22424, 'nuevoSuperNombre')
        print salida
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de modificación.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que sigue existiendo solo un elemento.
           or Asignatura.query().count() != 1
           #Que el elemento es accesible por el id y el nombre ha sido modificado bien.
           or Asignatura.query(Asignatura.idAsignatura == 22424).get().nombreAsignatura != 'nuevoSuperNombre'
           #Que al intentar modificar una entidad inexistente da error.
           or Gestor.modificarEntidad('Asignatura', 2313, 'nuevoNombre')['status'] != 'FAIL'
           ): test = False

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
