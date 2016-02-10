# -*- coding: utf-8 -*-
"""
Fichero de testing unitario a los módulos de conexión y gestión de la lógica con la BD.
Usando la librería unittest, más info en: https://docs.python.org/2/library/unittest.html
@execution: Para ejecutar el test sólo hay que hacer: > python testUnitario.py y añadir la opción -v si queremos ver detalles.
"""

import unittest
from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores
from GestorAsignaturasSQL import GestorAsignaturas
from GestorCursosSQL import GestorCursos
from GestorAsociacionesSQL import GestorAsociaciones
from GestorImparteSQL import GestorImparte
from GestorMatriculasSQL import GestorMatriculas

#Las clases para la realización de los test debe heredar de unittest.TestCase

### ENTIDADES ###

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

    def test_12_LecturaProfesor(self):
        self.assertNotEqual(GestorProfesores.getProfesor('8888'),'Elemento no encontrado')

    def test_13_ModificacionProfesor(self):
        #modificamos el nombre del alumnos creando en el test anterior.
        salida=GestorProfesores.modProfesor('8888','nombre','Enrique');
        #sacamos de la base de datos el alumno.
        profesor=GestorProfesores.getProfesor('8888')
        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(profesor.nombre,'Enrique')

    def test_14_EliminacionProfesor(self):
        self.assertEqual(GestorProfesores.delProfesor('8888'),'OK')

class TestEntidadAsignatura(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_21_IserccionAsignatura(self):
        self.assertEqual(GestorAsignaturas.nuevaAsignatura('mt3','Matematicas Aplicadas'), 'OK')

    def test_22_LecturaAsignatura(self):
        self.assertNotEqual(GestorAsignaturas.getAsignatura('mt3'),'Elemento no encontrado')

    def test_23_ModificacionAsignatura(self):
        #modificamos el nombre del alumnos creando en el test anterior.
        salida=GestorAsignaturas.modAsignatura('mt3','nombre','Matematicas Basicas');
        #sacamos de la base de datos el alumno.
        asignatura=GestorAsignaturas.getAsignatura('mt3')
        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(asignatura.nombre,'Matematicas Basicas')

    def test_24_EliminacionAsignatura(self):
        self.assertEqual(GestorAsignaturas.delAsignatura('mt3'),'OK')

class TestEntidadCurso(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_31_IserccionCurso(self):
        self.assertEqual(GestorCursos.nuevoCurso('hhjj','1','A','ESO'), 'OK')

    def test_32_LecturaCurso(self):
        self.assertNotEqual(GestorCursos.getCurso('hhjj'),'Elemento no encontrado')

    def test_33_ModificacionCurso(self):
        #modificamos el nombre del alumnos creando en el test anterior.
        salida=GestorCursos.modCurso('hhjj','nivel','BACH');

        '''
        Si la clave es el compuesto del resto de campos entonces hay que cambiar la clave si se cambia un
        campo, entonces si existen relaciones con otras entidades en otras tablas con esa clave habrá
        que cambiarlas todas. Hay que ver eso y tenerlo en cuenta. Por eso por ahora no se hara así.
        '''

        #sacamos de la base de datos el alumno.
        curso=GestorCursos.getCurso('hhjj')
        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(curso.nivel,'BACH')

    def test_34_EliminacionCurso(self):
        self.assertEqual(GestorCursos.delCurso('hhjj'),'OK')

### RELACIONES ###

class TestRelacionAsocia(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Asocia que relaciona las entidades Curso y Asignatura de la BD.
    '''


    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_41_InserccionRelacionAsocia(self):
        #Creamos una asignatura
        salidaA=GestorAsignaturas.nuevaAsignatura('fr','Frances')
        if salidaA=='OK':
            salidaA=True
        else:
            salidaA=False

        #Creamos un curso
        salidaB=GestorCursos.nuevoCurso('curso','1','A','ESO')
        if salidaB=='OK':
            salidaB=True
        else:
            salidaB=False
        #Testeamos la creación de la asociación
        salidaC=GestorAsociaciones.nuevaAsociacion('fr','curso')
        if salidaC=='OK':
            salidaC=True
        else:
            salidaC=False

        self.assertEqual(salidaA and salidaB and salidaC, True)

    def test_42_LecturaRelacionAsocia(self):
        self.assertNotEqual(GestorAsociaciones.getAsociacion('fr','curso'),'Elemento no encontrado')
    '''
    def test_43_ModificacionRelacionAsocia(self):
        #Intentamos modificar el cambio de la asociación de un curso a una asignatura
        #cambiando el curso en el que se impartía esa asignatura
        salida=GestorAsociaciones.modAsociacion('fr','curso','id_curso','curso2')

        #Comprobamos que se puede extraer la asociación modificada.
        self.assertEqual(GestorAsociaciones.getAsociacion('fr','curso2'),'OK')
    '''

    def test_44_EliminacionRelacionAsocia(self):
        #Vamos a comprobar que se pueden eliminar asociaciones borrando la anterior.
        salida=GestorAsociaciones.delAsociacion('fr','curso')
        #Eliminamos los objetos creados para el test.
        if salida=='OK':
            GestorAsignaturas.delAsignatura('fr')
            GestorCursos.delCurso('curso')
        self.assertEqual(salida,'OK')

class TestRelacionImparte(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Imparte que relaciona las entidades Curso, Asignatura y profesor de la BD.
    '''
    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_51_InserccionRelacionImparte(self):

        #Creamos una asignatura
        salidaA=GestorAsignaturas.nuevaAsignatura('fr','Frances')
        if salidaA=='OK':
            salidaA=True
        else:
            salidaA=False

        #Creamos un curso
        salidaB=GestorCursos.nuevoCurso('curso','1','A','ESO')
        if salidaB=='OK':
            salidaB=True
        else:
            salidaB=False

        #Creamos un profesor:
        salidaC=GestorProfesores.nuevoProfesor('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123','232332');


        #Testeamos la creación de la asociación
        salidaD=GestorImparte.nuevoImparte('fr','curso','8888')
        if salidaD=='OK':
            salidaD=True
        else:
            salidaD=False

        #Testeamos que todas las acciones han sido correctas
        self.assertEqual(salidaA and salidaB and salidaC and salidaD, True)


    def test_52_LecturaRelacionImparte(self):
        self.assertNotEqual(GestorImparte.getImparte('fr','curso','8888'),'Elemento no encontrado')


    def test_54_EliminacionRelacionImparte(self):
        #Vamos a comprobar que se pueden eliminar asociaciones borrando la anterior.
        salida=GestorImparte.delImparte('fr','curso','8888')
        #Eliminamos los objetos creados para el test.
        if salida=='OK':
            GestorAsignaturas.delAsignatura('fr')
            GestorCursos.delCurso('curso')
            GestorProfesores.delProfesor('8888')
        self.assertEqual(salida,'OK')

class TestRelacionMatricula(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Matricula que relaciona las entidades Curso, Asignatura y alumno de la BD.
    '''
    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_51_InserccionRelacionMatricula(self):

        #Creamos una asignatura
        salidaA=GestorAsignaturas.nuevaAsignatura('fr','Frances')
        if salidaA=='OK':
            salidaA=True
        else:
            salidaA=False

        #Creamos un curso
        salidaB=GestorCursos.nuevoCurso('curso','1','A','ESO')
        if salidaB=='OK':
            salidaB=True
        else:
            salidaB=False

        #Creamos un alumno:
        salidaC=GestorAlumnos.nuevoAlumno('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123')


        #Testeamos la creación de la asociación
        salidaD=GestorMatriculas.nuevaMatricula('fr','curso','8888')
        if salidaD=='OK':
            salidaD=True
        else:
            salidaD=False

        #Testeamos que todas las acciones han sido correctas
        self.assertEqual(salidaA and salidaB and salidaC and salidaD, True)


    def test_52_LecturaRelacionMatricula(self):
        self.assertNotEqual(GestorMatriculas.getMatricula('fr','curso','8888'),'Elemento no encontrado')


    def test_54_EliminacionRelacionMatricula(self):
        #Vamos a comprobar que se pueden eliminar asociaciones borrando la anterior.
        salida=GestorMatriculas.delMatricula('fr','curso','8888')
        #Eliminamos los objetos creados para el test.
        if salida=='OK':
            GestorAsignaturas.delAsignatura('fr')
            GestorCursos.delCurso('curso')
            GestorAlumnos.delAlumno('8888')
        self.assertEqual(salida,'OK')



### PRUEBAS DE CONJUNTO ###
#> insercciones, relaciones, reuniones y resultados esperados <#





if __name__ == '__main__':
    #La llamada a main hace que se ejecuten todos los métodos de todas las clases que heredan de TestCase
    unittest.main()
