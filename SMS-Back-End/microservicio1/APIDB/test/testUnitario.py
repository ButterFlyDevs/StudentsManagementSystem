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

from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores
from GestorAsignaturasSQL import GestorAsignaturas
from GestorClasesSQL import GestorClases
from GestorAsociacionesSQL import GestorAsociaciones
from GestorImparteSQL import GestorImparte
from GestorMatriculasSQL import GestorMatriculas
#import aprovisionadorDBconInterfaz
#Las clases para la realización de los test debe heredar de unittest.TestCase

#####################
###  ENTIDADES    ###
#####################

class TestEntidadAlumno(unittest.TestCase):
    '''
    Testing sobre la entidad Alumno de la BD
    '''

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    #La ejecución de los test se hace por orden alfabético, algo a tener en cuenta cuando queremos hacer ciertas acciones.
    def test_01_IserccionAlumno(self):
        #Nos aseguramos de que la base de datos se encuentra en estado cero creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que el método que inserta un nuevo alumno devuelve el mensaje de confirmación esperado.
        self.assertEqual(GestorAlumnos.nuevoAlumno('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123'), 'OK')

    def test_02_LecturaAlumno(self):
        #Comprobamos que el alumno es accesible en la base de datos.
        #Usamos NotEqual para comprobar que la salida es distinta de "Elemento no encontrado".
        self.assertNotEqual(GestorAlumnos.getAlumno('8888'),'Elemento no encontrado')

    def test_03_ModificacionAlumno(self):
        #modificamos el nombre del alumnos creando en el test anterior.
        salida=GestorAlumnos.modAlumno('8888','nombre','Enrique');
        #sacamos de la base de datos el alumno.
        alumno=GestorAlumnos.getAlumno('8888')
        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(alumno.nombre,'Enrique')


    def test_04_EliminacionAlumno(self):
        '''Eliminamos el alumno de la base de datos y comprobamos el mensaje devuelto'''
        self.assertEqual(GestorAlumnos.delAlumno('8888'),'OK')


    def test_05_NumeroAlumnos(self):
        """
        Comprueba que se obtiene de forma correcta el número de alumnos en la BD.
        """
        #Comprobamos que no existan.
        cero=GestorAlumnos.getNumAlumnos()
        GestorAlumnos.nuevoAlumno('Juan','8888','C/Mesita','Peligros','Granada','1900-2-1','3242123')
        GestorAlumnos.nuevoAlumno('Juan','8889','C/Mesita','Peligros','Granada','1900-2-1','3242123')
        dos=GestorAlumnos.getNumAlumnos()
        GestorAlumnos.delAlumno('8889')
        GestorAlumnos.delAlumno('8888')
        cero2=GestorAlumnos.getNumAlumnos();
        resultado=False
        if cero==0 and dos==2 and cero2==0:
            resultado=True
        self.assertEqual(resultado,True)


    def test_06_ProfesoreQueImparteAAlumno(self):
        #Ejecutamos el aprovisionamiento de la base de datos usando el aprovisionador. (la BD hasta ahora solo tiene la estructura, sin contenido)
        aprovisionadorDBconInterfaz.aprovisiona()
        profesores=GestorAlumnos.getProfesores('1')
        #Devemos devolver la BD a su estado original (solo estructura)
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
        #Comprobamos que al alumno 3 le dan clase tres profesores, según el aprovisionamiento hecho y la función que lo comprueba.
        self.assertEqual(len(profesores), 2)
        '''
        Para probar todas las relaciones, ya que la base de datos debe quedar en su estado original para que
        el resto de test funcionen, puede que sea mejor juntarlas en un solo test, así se aprovisionará y restaurará
        pidiéndonos la contraseña sólo una vez y no tantas como pruebas de joins queramos hacer como la de este test.
        '''


if False:
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

        def test_15_AlumnosALosQueDaClaseUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getAlumnos('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,3)

        def test_16_AsignaturasQueImparteUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getAsignaturas('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

        def test_17_CursosEnLosQueImparteUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getCursos('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

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

        def test_25_CursosDondeSeImparteAsignatura(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorAsignaturas.getCursos('fr'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

        def test_26_ProfesoresQueImparteLaAsignatura(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorAsignaturas.getProfesores('fr'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,2)

        def test_27_AlumnosQueCursanLaAsignatura(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorAsignaturas.getAlumnos('mt'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,4)


    class TestEntidadClase(unittest.TestCase):

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

        def test_35_AsginaturasAsociadasAlCurso(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorCursos.getAsignaturas('1AESO'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

        def test_36_AlumnosMatriculadosEnCurso(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorCursos.getAlumnos('1AESO'))
            self.assertEqual(size,3)

        def test_37_ProfesoresQueImpartenEnCurso(self):
            a=len(GestorCursos.getProfesores('1AESO'))
            b=len(GestorCursos.getProfesores('1BESO'))
            print a
            print b
            salida=False
            if a==2 and b==1:
                salida=True
            #Hemos aprovechado la inicialización anterior y restauramos aquí.
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(salida,True)

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


        def test_45_AlumnosMAtriculadosEnUnaAsignaturaYCurso(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            sizeA=len(GestorAsociaciones.getAlumnos('mt','1AESO'))
            sizeB=len(GestorAsociaciones.getAlumnos('fr','1AESO'))
            sizeC=len(GestorAsociaciones.getAlumnos('mt','1BESO'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            salida=False
            if sizeA==1 and sizeB==3 and sizeC==3:
                salida=True
            self.assertEqual(salida,True)

        def test_46_ProfesoresQueImpartenEnUnCursoYAsignatura(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            sizeA=len(GestorAsociaciones.getProfesores('mt','1AESO'))
            sizeB=len(GestorAsociaciones.getProfesores('fr','1AESO'))
            sizeC=len(GestorAsociaciones.getProfesores('mt','1BESO'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            salida=False
            if sizeA==0 and sizeB==2 and sizeC==1:
                salida=True
            self.assertEqual(salida,True)



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





if __name__ == '__main__':
    #La llamada a main hace que se ejecuten todos los métodos de todas las clases que heredan de TestCase
    unittest.main()
