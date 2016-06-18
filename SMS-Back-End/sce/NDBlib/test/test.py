# -*- coding: utf-8 -*-

##########################
### TESTING NDBLIB lib ###
##########################

"""
Fichero de testing para la libería de conexión NDBlib cuyo conector es gestor.py
@execution: Para ejecutar el test sólo hay que hacer: > python testUnitario.py y añadir la opción -v si queremos ver detalles.
"""

import unittest
import datetime
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

    def test_03_deleteEntity(self):
        """
        Test de comprobación de eliminación en los cuatro tipos de referencia: Alumno, Profesor, Clase, Asignatura
        """

        test=True

        #Comprobamos la modificación de una entidad del tipo Alumno (previamente existente)
        salida = Gestor.insertarEntidad('Alumno', 22488, 'alumnoFantasma')
        print salida
        if ( #Si alguno de las condiciones falla, falla el test de entidad y el test de modificación.
           #La salida es correcta
           salida['status'] != 'OK'
           #Que el elemento es accesible por el id y el nombre es el correcto
           or Alumno.query(Alumno.idAlumno == 22488).get().nombreAlumno != 'alumnoFantasma'
           ): test = False

        n = Alumno.query().count()
        salida = Gestor.eliminarEntidad('Alumno', 22488)
        if Alumno.query(Alumno.idAlumno == 22488).count()!=0: test = False
        if Alumno.query().count() != n-1: test = False

        self.assertEqual(test, True, salida)

    def test_04_insertarMicroControlAsistencia(self):
        """Comprobamos que la función con el mismo nombre funciona correctamente."""
        test=True
        mca={"asistencia" : 1, "retraso": 0, "retrasoTiempo" : 0, "retrasoJustificado" : 0, "uniforme" : 1, "idAlumno" : 11}
        fechaHora = datetime.datetime.now()
        key=Gestor.insertarMicroControlAsistencia(mca, fechaHora, 1, 1, 1)
        if (key==None):
            test=False
        #Comprobamos que se haya guardado
        query = microControlAsistencia.query(microControlAsistencia.key==key)
        mcaExtraido=query.get()
        #Si los datos guardados son los correctos entones se da por bueno
        if (mcaExtraido.asistencia!=1 or mcaExtraido.idAlumno!=11 or mcaExtraido.idClase!=1):
            test=False
        self.assertEqual(test, True)

    def test_05_insertaResumenControlAsistencia(self):
        """ Comprobamos que un resumen se insertar correctamente. """
        test=True
        #Una lista de claves de supuestos microControlAsistencia
        listaMCAs = []
        fechaHora = datetime.datetime.now()
        mca1={"asistencia" : 1, "retraso": 0, "retrasoTiempo" : 0, "retrasoJustificado" : 0, "uniforme" : 1, "idAlumno" : 11}
        key1=Gestor.insertarMicroControlAsistencia(mca1, fechaHora, 1, 3, 1)
        mca2={"asistencia" : 0, "retraso": 1, "retrasoTiempo" : 20, "retrasoJustificado" : 0, "uniforme" : 0, "idAlumno" : 44}
        key2=Gestor.insertarMicroControlAsistencia(mca2, fechaHora, 5, 1, 4)

        listaMCAs.append(key1)
        listaMCAs.append(key2)

        key = Gestor.insertarResumenControlAsistencia(listaMCAs, fechaHora, 1, 1, 1)

        #Si el tipo de dato devuelto no es de tipo 'key' entonces se ha guardado correctamente.
        if 'key' not in str(type(key)):
            test=False

        self.assertEqual(test, True)

    #Una vez pasados los test anteriores se ejecuta este (que usa las funciones anteriores).
    def test_06_insertarControlAsistencia(self):
        """
        Comprobación de la introducción de un control de asistencia completo.
        """
        test=True

        controlAsistencia={"microControlesAsistencia": [
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

        salida=Gestor.insertarControlAsistencia(controlAsistencia)
        print 'SAlida insertarControlAsistencia'
        print salida
        if (salida['status']!='OK' and salida['key']!=0):
            test=False
        self.assertEqual(test, True)

    #Tests de obtención (los más usados en la UI)
    def test_07_obtenerResumenesControlAsistencia(self):
        """Comprueba el método con el mismo nombre, con algunas de las combinaciones de atributos pasados"""
        test = True

        #Los resúmenes se obtienen para la UI y por eso necesitamos que en el Datastore estén almacenados los nombres de referencia.
        #Estas acciones las realizaría el SBD con lanzadores cuando se le inserten nuevas entidades del mismo tipo allí para actualizar aqui
        Gestor.insertarEntidad(tipo='Clase', idEntidad=1, nombreEntidad='1ESOA')
        Gestor.insertarEntidad(tipo='Clase', idEntidad=33, nombreEntidad='1ESAA')
        Gestor.insertarEntidad(tipo='Profesor', idEntidad=1, nombreEntidad='ProfesorA')
        Gestor.insertarEntidad(tipo='Profesor', idEntidad=22, nombreEntidad='ProfesorA')
        Gestor.insertarEntidad(tipo='Asignatura', idEntidad=44, nombreEntidad='Asignatura 44')
        Gestor.insertarEntidad(tipo='Asignatura', idEntidad=1, nombreEntidad='Asignatura 1')

        #Comprobamos que los devuelve todos cuando no se pasan parámetros
        #Conociendo los resúmenes de controles de asistencia guardados por los test_04 y 05 probamos la método que los obtiene.
        resumenes = Gestor.obtenerResumenesControlAsistencia()

        #Debe de haber dos por los introducidos en el test 04 y 05.
        if len(resumenes) is not 2:
            test = False

        #Establecemos un datetime que sea justo ahora
        # https://docs.python.org/2/library/datetime.html
        #  class datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
        dateHoy = datetime.datetime.now()
        dateTomorrow = dateHoy + datetime.timedelta(days=1)
        if len(Gestor.obtenerResumenesControlAsistencia(fechaHoraInicio=dateHoy, fechaHoraFin=dateTomorrow)) != 2 : test = False
        if len(Gestor.obtenerResumenesControlAsistencia(idProfesor=22, fechaHoraInicio=dateHoy))!= 1: test=False
        if len(Gestor.obtenerResumenesControlAsistencia(idProfesor=4828)) != 0 : test=False

        print ' \n### RESUMENES obtenidos: ###\n'
        for r in resumenes:
            print str(r)+'\n'

        self.assertEqual(test, True)

    def test_08_obtenerControlAsistencia(self):
        test = True

        #Insertamos algunas referencias que faltaban
        Gestor.insertarEntidad(tipo='Alumno', idEntidad=11, nombreEntidad='alumno X')
        Gestor.insertarEntidad(tipo='Alumno', idEntidad=15, nombreEntidad='alumno Y')

        #Insertamos un control de asistencia
        controlAsistencia={"microControlesAsistencia": [
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

        salida=Gestor.insertarControlAsistencia(controlAsistencia)
        print ' ##salida insercción ##'
        print salida
        salida2=Gestor.obtenerControlAsistencia(salida['key'])
        print ' ##salida obtencion ##'
        print salida2

        #Algunas comprobaciones
        if salida2 == None:
            test=False


        if salida2['idProfesor']!=22: test = False
        if (salida2['controles'][0])['idAlumno'] != 11 or (salida2['controles'][0])['nombreAlumno'] != 'alumno X': test = False

        self.assertEqual(test, True)

    def test_09_eliminarControlAsistencia(self):
        test = True

        #Primero insertamos un control, sabiendo que ese metodo ha sido ya testeado

        controlAsistencia={"microControlesAsistencia": [
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


        numResumenesA = resumenControlAsistencia.query().count() #Contamos
        salida=Gestor.insertarControlAsistencia(controlAsistencia) #Insertamos
        numResumenesB = resumenControlAsistencia.query().count() #Contamos

        if numResumenesB != numResumenesA+1: test=False  #Pequeña comprobación de inserción

        if salida['status']=='OK': #Si la insercción ha sido correcta comprobamos que se elimina

            #Contamos antes el número de microControles antes tb
            numMCA = microControlAsistencia.query().count()

            salidaDel=Gestor.eliminarControlAsistencia(salida['key'])


            if salidaDel['status']!='OK': test = False #Que la salida de la eliminación sea correcta
            if resumenControlAsistencia.query().count() != numResumenesA : test = False #Que el número haya vuelto al anterior
            if microControlAsistencia.query().count() != numMCA-2 : test = False #Que se hayan elminado lo mcontroles justos que hemos añadido: dos


        else:
            test=False

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
