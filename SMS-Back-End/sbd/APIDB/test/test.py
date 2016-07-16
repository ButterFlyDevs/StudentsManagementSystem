# -*- coding: utf-8 -*-
"""
Fichero de testing unitario a los módulos de conexión y gestión de la lógica con la BD.
Usando la librería unittest, más info en: https://docs.python.org/2/library/unittest.html
@execution: Para ejecutar el test sólo hay que hacer: > python testUnitario.py y añadir la opción -v si queremos ver detalles.
"""
import unittest
#Para poder acceder a los ficheros en el directorio padre, los añadimos al path de python
import sys, os
sys.path.insert(0,os.pardir)

from GestorEntidades import GestorEntidades
from termcolor import colored

########################################################
###  sobre ENTIDADES(tablas) y RELACIONES(tablas)    ###
########################################################

### ENTIDADES, como Alumno, Profesor... ###

#Las clases para la realización de los test debe heredar de unittest.TestCase
class TestGestorEntidades(unittest.TestCase):

    def setUp(self):
        os.system('mysql -u root -p\'root\' < ../DBCreatorv1.sql')

    def test_31_putEntidades(self):
        test = True
        if GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'súperNombre'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'súperNombre'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'Francés'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1', 'grupo': 'B', 'nivel': 'ESO'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Desconocido', datos={'prueba': 'hola'})['status'] != 'FAIL':
            test = False


        #Testeando la asociación de una asignatura a una clase, y sus errores
        if GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '1', 'idAsignatura': '1'})['status'] != 'OK': test = False
        #No se puede realizar la misma asociación si ya existe

        exit=GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '1', 'idAsignatura': '1'})
        print colored(exit, 'green')
        if exit['status'] != 'FAIL' or exit['info'] != 'Elemento duplicado': test = False


        #No se puede realizar una relación con elementos que no existan
        exit = GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '2', 'idAsignatura': '1'})
        if exit['status'] != 'FAIL' or exit['info'] != 'Alguno de los elementos no existe': test = False

        exit = GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '1', 'idAsignatura': '2'})
        if exit['status'] != 'FAIL' or exit['info'] != 'Alguno de los elementos no existe': test = False

        #Testeando la relación Imparte entre una asociacion y un profesor
        if GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '1', 'idProfesor': '1'})['status'] != 'OK': test = False
        if GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '1', 'idProfesor': '1'})['status'] != 'FAIL': test = False
        exit = GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '1', 'idProfesor': '2'})
        if exit['status'] != 'FAIL' or exit['info'] != 'Alguno de los elementos no existe': test = False
        exit = GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '2', 'idProfesor': '1'})
        if exit['status'] != 'FAIL' or exit['info'] != 'Alguno de los elementos no existe': test = False

        #Testeando la relación Matricula entre una asociacion y un alumno
        if GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '1', 'idAsociacion': '1'})['status'] != 'OK': test = False
        if GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '1', 'idAsociacion': '1'})['status'] != 'FAIL': test = False
        if GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '2', 'idAsociacion': '1'})['status'] != 'FAIL': test = False
        if GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '1', 'idAsociacion': '2'})['status'] != 'FAIL': test = False


        self.assertTrue(test)

    def test_32_getEntidades(self):
        test = True

        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'nombrecito'})

        if GestorEntidades.getEntidades(tipo='Alumno')[0]['nombre'] != u'nombrecito' \
            and len(GestorEntidades.getEntidades(tipo='Alumno')) != 1: test = False #Que la lista y el tam is Ok
        if GestorEntidades.getEntidades(tipo='Alumno', idEntidad='1')['nombre'] != u'nombrecito': test = False

        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'profesor'})
        if GestorEntidades.getEntidades(tipo='Profesor')[0]['nombre'] != u'profesor' \
            and len(GestorEntidades.getEntidades(tipo='Profesor')) != 1: test = False #Que la lista y el tam is Ok
        if GestorEntidades.getEntidades(tipo='Profesor', idEntidad='1')['nombre'] != u'profesor': test = False

        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1'})
        if GestorEntidades.getEntidades(tipo='Clase')[0]['curso'] != 1 \
            and len(GestorEntidades.getEntidades(tipo='Clase')) != 1: test = False #Que la lista y el tam is Ok
        if GestorEntidades.getEntidades(tipo='Clase', idEntidad='1')['curso'] != 1: test = False

        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'asignatura'})
        if GestorEntidades.getEntidades(tipo='Asignatura')[0]['nombre'] != u'asignatura' \
            and len(GestorEntidades.getEntidades(tipo='Asignatura')) != 1: test = False #Que la lista y el tam is Ok
        if GestorEntidades.getEntidades(tipo='Asignatura', idEntidad='1')['nombre'] != u'asignatura': test = False

        self.assertTrue(test)

    def test_33_getEntidadesRelacionadas(self):

        test = True

        #Insertamos una entidad de cada tipo
        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'alumnoA'})
        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'profesorA'})
        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'asignaturaA'})
        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1', 'grupo': 'B', 'nivel': 'ESO'})

        #Las relacionamos entre ellas ...
        GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '1', 'idAsignatura': '1'})
        GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '1', 'idProfesor': '1'})
        GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '1', 'idAsociacion': '1'})

        # ... para probar los métodos de relación:

        #Pedimos todos los profesores que imparten clase al alumno con id = 1
        listaProfesores = GestorEntidades.getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Profesor')
        if len(listaProfesores) != 1 or listaProfesores[0]['nombre'] != 'profesorA': test = False

        #Pedimos todos las clases en la que está matriculado el alumno con id = 1
        listaClases = GestorEntidades.getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Clase')
        if len(listaClases) != 1 or listaClases[0]['nivel'] != 'ESO': test = False

        #Pedimos todos las asignaturas en la que está matriculado el alumno con id = 1
        listaAsignaturas = GestorEntidades.getEntidadesRelacionadas(tipoBase='Alumno', idEntidad='1', tipoBusqueda='Asignatura')
        if len(listaAsignaturas) != 1 or listaAsignaturas[0]['nombre'] != 'asignaturaA': test = False



        #Pedimos todos las clases en la que imparte clase el profesor con id = 1
        listaClases = GestorEntidades.getEntidadesRelacionadas(tipoBase='Profesor', idEntidad='1', tipoBusqueda='Clase')
        if len(listaClases) != 1 or listaClases[0]['nivel'] != 'ESO': test = False

        #Pedimos todos las asisnaturas que imparte clase el profesor con id = 1
        listaAsignaturas = GestorEntidades.getEntidadesRelacionadas(tipoBase='Profesor', idEntidad='1', tipoBusqueda='Asignatura')
        if len(listaAsignaturas) != 1 or listaAsignaturas[0]['nombre'] != 'asignaturaA': test = False

        #Pedimos todos los alumnos a los que imparte clase el profesor con id = 1
        listaAlumnos = GestorEntidades.getEntidadesRelacionadas(tipoBase='Profesor', idEntidad='1', tipoBusqueda='Alumno')
        if len(listaAlumnos) != 1 or listaAlumnos[0]['nombre'] != 'alumnoA': test = False



        #Pedimos todos los alumnos matriculados en la clase con id = 1
        listaAlumnos = GestorEntidades.getEntidadesRelacionadas(tipoBase='Clase', idEntidad='1', tipoBusqueda='Alumno')
        if len(listaAlumnos) != 1 or listaAlumnos[0]['nombre'] != 'alumnoA': test = False

        #Pedimos todos las asignaturas que se imparten en la clase con id = 1
        listaAsignaturas = GestorEntidades.getEntidadesRelacionadas(tipoBase='Clase', idEntidad='1', tipoBusqueda='Asignatura')
        if len(listaAsignaturas) != 1 or listaAsignaturas[0]['nombre'] != 'asignaturaA': test = False

        #Pedimos todos los profesores que imparten en la clase con id = 1
        listaProfesores = GestorEntidades.getEntidadesRelacionadas(tipoBase='Clase', idEntidad='1', tipoBusqueda='Profesor')
        if len(listaProfesores) != 1 or listaProfesores[0]['nombre'] != 'profesorA': test = False



        #Pedimos todos los alumnos matriculados en la asignatura con id = 1
        listaAlumnos = GestorEntidades.getEntidadesRelacionadas(tipoBase='Asignatura', idEntidad='1', tipoBusqueda='Alumno')
        if len(listaAlumnos) != 1 or listaAlumnos[0]['nombre'] != 'alumnoA': test = False

        #Pedimos todos los profesores que imparten la asignatura con id = 1
        listaProfesores = GestorEntidades.getEntidadesRelacionadas(tipoBase='Asignatura', idEntidad='1', tipoBusqueda='Profesor')
        if len(listaProfesores) != 1 or listaProfesores[0]['nombre'] != 'profesorA': test = False

        #Pedimos todos las clases en las que se imparte la asignatura con id = 1
        listaClases = GestorEntidades.getEntidadesRelacionadas(tipoBase='Asignatura', idEntidad='1', tipoBusqueda='Clase')
        if len(listaClases) != 1 or listaClases[0]['nivel'] != 'ESO': test = False

        self.assertTrue(test)

    def test_34_modEntidades(self):
        test = True

        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'nombrecito'})
        #Modificamos nombre
        if GestorEntidades.modEntidad(tipo='Alumno', idEntidad='1', campoACambiar='nombre', nuevoValor='nuevoNombre')['status'] != 'OK': test = False
        if GestorEntidades.getEntidades(tipo='Alumno', idEntidad='1')['nombre'] != 'nuevoNombre': test = False
        #Modificamos dni
        if GestorEntidades.modEntidad(tipo='Alumno', idEntidad='1', campoACambiar='dni', nuevoValor='11111111')['status'] != 'OK': test = False
        if GestorEntidades.getEntidades(tipo='Alumno', idEntidad='1')['dni'] != 11111111: test = False
        #Modificamos fechaNacimiento
        if GestorEntidades.modEntidad(tipo='Alumno', idEntidad='1', campoACambiar='fechaNacimiento', nuevoValor='1988-10-29')['status'] != 'OK': test = False
        if str(GestorEntidades.getEntidades(tipo='Alumno', idEntidad='1')['fechaNacimiento']) != '1988-10-29': test = False
        #Que no se puede modificar un elemento que no existe
        if GestorEntidades.modEntidad(tipo='Alumno', idEntidad='5', campoACambiar='nombre', nuevoValor='A')['status'] != 'FAIL': test = False
        #Que no se puede modificar un alumno y ponerle el mismo dni que otro
        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'alumnoPrueba'})
        if GestorEntidades.modEntidad(tipo='Alumno', idEntidad='2', campoACambiar='dni', nuevoValor='11111111')['status'] != 'FAIL': test = False

        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'nombrecito'})
        if GestorEntidades.modEntidad(tipo='Profesor', idEntidad='1', campoACambiar='nombre', nuevoValor='nuevoNombre')['status'] != 'OK': test = False
        if GestorEntidades.getEntidades(tipo='Profesor', idEntidad='1')['nombre'] != 'nuevoNombre': test = False

        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'nombrecito'})
        if GestorEntidades.modEntidad(tipo='Asignatura', idEntidad='1', campoACambiar='nombre', nuevoValor='nuevoNombre')['status'] != 'OK': test = False
        if GestorEntidades.getEntidades(tipo='Asignatura', idEntidad='1')['nombre'] != 'nuevoNombre': test = False

        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1'})
        if GestorEntidades.modEntidad(tipo='Clase', idEntidad='1', campoACambiar='curso', nuevoValor='2')['status'] != 'OK': test = False
        if GestorEntidades.getEntidades(tipo='Clase', idEntidad='1')['curso'] != 2: test = False

        self.assertTrue(test)

    def test_35_delEntidades_numEntidades(self):
        test = True

        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'alumnoPrueba'})
        if GestorEntidades.delEntidad(tipo='Alumno', idEntidad='1')['status'] != 'OK': test = False
        if len(GestorEntidades.getEntidades(tipo='Alumno')) != 0: test = False
        if GestorEntidades.getNumEntidades(tipo='Alumno') != 0: test =False

        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'prof'})
        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'prof2'})
        if GestorEntidades.delEntidad(tipo='Profesor', idEntidad='1')['status'] != 'OK': test = False
        if len(GestorEntidades.getEntidades(tipo='Profesor')) != 1: test = False
        if GestorEntidades.getNumEntidades(tipo='Profesor') != 1: test =False

        #Insertamos una entidad de cada tipo
        GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'alumnoA'})
        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'profesorA'})
        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'asignaturaA'})
        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1', 'grupo': 'B', 'nivel': 'ESO'})

        #Las relacionamos entre ellas ...
        if GestorEntidades.putEntidad(tipo='Asociacion', datos={'idClase': '1', 'idAsignatura': '1'})['status'] != 'OK' : test = False
        if GestorEntidades.putEntidad(tipo='Imparte', datos={'idAsociacion': '1', 'idProfesor': '3'})['status'] != 'OK' : test = False
        if GestorEntidades.putEntidad(tipo='Matricula', datos={'idAlumno': '2', 'idAsociacion': '1'})['status'] != 'OK' : test = False

        if GestorEntidades.getNumEntidades(tipo='Asociacion') != 1: test =False
        if GestorEntidades.getNumEntidades(tipo='Imparte') != 1: test =False
        if GestorEntidades.getNumEntidades(tipo='Matricula') != 1: test =False


        #Si a la asocaicion hay matriculados alumnos y/o la dan profesores tiene dependencias que hace que no se pueda eliminar
        if GestorEntidades.delEntidad(tipo='Asociacion', idEntidad='1')['status'] != 'El elemento que pretentde eliminar tiene dependencias': test = False

        if GestorEntidades.delEntidad(tipo='Matricula', idEntidad='1')['status'] != 'OK': test = False
        if GestorEntidades.delEntidad(tipo='Matricula', idEntidad='1')['status'] != 'Elemento no encontrado': test = False

        if GestorEntidades.delEntidad(tipo='Imparte', idEntidad='1')['status'] != 'OK': test = FAlse
        if GestorEntidades.delEntidad(tipo='Imparte', idEntidad='1')['status'] != 'Elemento no encontrado': test = False

        #Una vez eliminadas las dependencias si se puede eliminar la asociación
        if GestorEntidades.delEntidad(tipo='Asociacion', idEntidad='1')['status'] != 'OK': test = False
        if GestorEntidades.delEntidad(tipo='Asociacion', idEntidad='1')['status'] != 'Elemento no encontrado': test = False

        if GestorEntidades.getNumEntidades(tipo='Asociacion') != 0: test =False
        if GestorEntidades.getNumEntidades(tipo='Imparte') != 0: test =False
        if GestorEntidades.getNumEntidades(tipo='Matricula') != 0: test =False

        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()
