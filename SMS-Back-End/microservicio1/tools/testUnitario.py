# -*- coding: utf-8 -*-
"""
Fichero de testing unitario a los módulos de conexión a la BD.
Usando la librería unittest, más info en: https://docs.python.org/2/library/unittest.html
"""

import unittest
from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores

#La clase para la realización de los test debe heredar de unittest.TestCase
class TestEntidadAlumno(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    #La ejecución de los test se hace por orden alfabético, algo a tener en cuenta cuando queremos hacer ciertas acciones.
    def test_01_IserccionAlumno(self):
        self.assertEqual(GestorAlumnos.nuevoAlumno('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123'), 'OK')

    def test_02_LecturaAlumno(self):
        #Comprobamos que el alumno es accesible en la base de datos.
        self.assertNotEqual(GestorAlumnos.getAlumno('8888'),'Elemento no encontrado')

    def test_03_ModificacionAlumno(self):
        #modificamos el nombre del alumnos creando en el test anterior.
        salida=GestorAlumnos.modAlumno('8888','nombre','Enrique');
        #sacamos de la base de datos el alumno.
        alumno=GestorAlumnos.getAlumno('8888')
        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(alumno.nombre,'Enrique')

    def test_04_EliminacionAlumno(self):
        self.assertEqual(GestorAlumnos.delAlumno('8888'),'OK')





class TestEntidadProfesor(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_11_IserccionProfesor(self):
        self.assertEqual(GestorProfesores.nuevoProfesor('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123','232332'), 'OK')

    def test_12_EliminacionProfesor(self):
        self.assertEqual(GestorProfesores.delProfesor('8888'),'OK')


if __name__ == '__main__':
    #La llamada a main hace que se ejecuten todos los métodos de todas las clases que heredan de TestCase
    unittest.main()
