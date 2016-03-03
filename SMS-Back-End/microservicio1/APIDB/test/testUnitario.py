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

        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que el método que inserta un nuevo alumno devuelve el mensaje de confirmación esperado.

        #1. Insertamos un alumno en la base de datos y comprobamos que la salida es 'OK'
        if GestorAlumnos.nuevoAlumno('Juan') == 'OK':
            testA=True
        else:
            testA=False

        #2. Comprobamos que insertar un alumno con un dni que ya existe en la base de datos da error por elemento duplicado.
        GestorAlumnos.nuevoAlumno('Pedro', apellidos='Garcia', dni='3333')
        if GestorAlumnos.nuevoAlumno('Maria', dni='3333') == 'Elemento duplicado':
            testB=True
        else:
            testB=False

        #3. Comprobamos que un alumno con el mismo nombre y apellidos no puede introducirse si ya existe.
        if GestorAlumnos.nuevoAlumno('Pedro', apellidos='Martinez') == 'OK' and GestorAlumnos.nuevoAlumno('Pedro', apellidos='Garcia') == 'Elemento duplicado':
            testC=True
        else:
            testC=False

        self.assertEqual(testA and testB and testC, True)

    def test_02_LecturaAlumnos(self):
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAlumnos.nuevoAlumno('Juan')
        GestorAlumnos.nuevoAlumno('Andrés')
        #Comprobamos que son dos los alumnos que devuelve el método getAlumnos()
        self.assertEqual(len(GestorAlumnos.getAlumnos()),2)

    def test_03_LecturaAlumno(self):
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAlumnos.nuevoAlumno('Juan')
        #Usamos NotEqual para comprobar que la salida es distinta de "Elemento no encontrado".
        self.assertNotEqual(GestorAlumnos.getAlumno('1'),'Elemento no encontrado')

    def test_04_ModificacionAlumno(self):
        '''Comprobación de como cualquier atributo de un alumno puede modificarse'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        testA=testB=testC=False;
        #Creamos un alumno con nombre Juan.
        GestorAlumnos.nuevoAlumno('Juan')
        #modificamos el nombre del alumnos creando:
        if GestorAlumnos.modAlumno('1','nombre','Enrique') == 'OK':
            testA=True

        #Cambiamos el dni
        GestorAlumnos.nuevoAlumno('Pedro', dni='1212')
        if GestorAlumnos.modAlumno('2', 'dni', '1414') == 'OK':
            testB=True

        #Cambiamos el dni de un alumno por uno que ya existe en la base de datos.
        GestorAlumnos.nuevoAlumno('Luis', dni='1010')
        GestorAlumnos.nuevoAlumno('Carlos', dni='1111')
        #Debe decirnos que ya existe uno con ese campo por tanto estaría duplicado y aborta.
        if GestorAlumnos.modAlumno('3', 'dni', '1111') == 'Elemento duplicado':
            testC=True #El error se da.

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB and testC, True)


    def test_05_EliminacionAlumno(self):
        '''Eliminamos el alumno de la base de datos y comprobamos el mensaje devuelto'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAlumnos.nuevoAlumno('Juan')
        #Si el alumno se elimina y no se encuentra después está bien.
        if GestorAlumnos.delAlumno('1') == 'OK' and GestorAlumnos.getAlumno('1') == 'Elemento no encontrado':
            testA=True
        else:
            testA=False

        self.assertEqual(testA,True)


    def test_06_NumeroAlumnos(self):
        '''Comprueba que se obtiene de forma correcta el número de alumnos en la BD.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que no existan.
        cero=GestorAlumnos.getNumAlumnos()
        for x in range(0, 3):
            GestorAlumnos.nuevoAlumno(str(x))
        tres=GestorAlumnos.getNumAlumnos()
        GestorAlumnos.delAlumno('2')

        dos=GestorAlumnos.getNumAlumnos();

        if cero==0 and tres==3 and dos==2:
            resultado=True

        self.assertEqual(resultado,True)



    ####
    #   TESTS DE RELACIONES CON OTRAS ENTIDADES, usando aprovisionadorDBconInterfaz.py
    ####
    if False:
        def test_07_ProfesoreQueImparteAAlumno(self):
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

class TestEntidadProfesor(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_11_IserccionProfesor(self):
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que el método que inserta un nuevo alumno devuelve el mensaje de confirmación esperado.

        #1. Insertamos un alumno en la base de datos y comprobamos que la salida es 'OK'
        if GestorProfesores.nuevoProfesor('Juan', '222') == 'OK':
            testA=True
            print 'true'
        else:
            testA=False
            print 'false'

        #2. Comprobamos que insertar un alumno con un dni que ya existe en la base de datos da error por elemento duplicado.
        GestorProfesores.nuevoProfesor('Pedro', '3333', apellidos='Garcia', )
        if GestorProfesores.nuevoProfesor('Maria', '3333') == 'Elemento duplicado':
            testB=True

        else:
            testB=False


        #3. Comprobamos que un alumno con el mismo nombre y apellidos no puede introducirse si ya existe.
        if GestorProfesores.nuevoProfesor('Pedro', '1212', apellidos='Martinez') == 'OK' and GestorProfesores.nuevoProfesor('Pedro', '8989', apellidos='Garcia') == 'Elemento duplicado':
            testC=True
        else:
            testC=False

        self.assertEqual(testA and testB and testC, True)

    def test_12_LecturaProfesores(self):
        'Comprobamos que getProfesores devuelve el número correncto de elementos'
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorProfesores.nuevoProfesor('Juan', '24242')
        GestorProfesores.nuevoProfesor('Andrés', '2878' )
        #Comprobamos que son dos los alumnos que devuelve el método getAlumnos()
        self.assertEqual(len(GestorProfesores.getProfesores()),2)


    def test_13_LecturaProfesor(self):
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorProfesores.nuevoProfesor('Juan', '2422')
        self.assertNotEqual(GestorProfesores.getProfesor('2422'),'Elemento no encontrado')



    def test_14_ModificacionProfesor(self):
        '''Comprobación de como cualquier atributo de un profesor puede modificarse'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        testA=testB=testC=False;
        #Creamos un alumno con nombre Juan.
        GestorProfesores.nuevoProfesor('Juan', '222')
        #modificamos el nombre del profesor creado:
        if GestorProfesores.modProfesor('222','nombre','Enrique') == 'OK':
            testA=True
            print "yah"
        else:
            print 'fuck'

        #Cambiamos el dni
        GestorProfesores.nuevoProfesor('Pedro','1212')
        if GestorProfesores.modProfesor('1212', 'dni', '1414') == 'OK':
            testB=True

        #Cambiamos el dni de un profesor por uno que ya existe en la base de datos.
        GestorProfesores.nuevoProfesor('Luis', '1010')
        GestorProfesores.nuevoProfesor('Carlos', '1111')
        #Debe decirnos que ya existe uno con ese campo por tanto estaría duplicado y aborta.
        if GestorProfesores.modProfesor('1010', 'dni', '1111') == 'Elemento duplicado':
            testC=True #El error se da.

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB and testC, True)


    def test_15_EliminacionProfesor(self):
        '''Eliminamos el profesor de la base de datos y comprobamos el mensaje devuelto'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorProfesores.nuevoProfesor('Luis', '1010')
        #Si el alumno se elimina y no se encuentra después está bien.
        if GestorProfesores.delProfesor('1010') == 'OK' and GestorProfesores.delProfesor('1') == 'Elemento no encontrado':
            testA=True
        else:
            testA=False

        self.assertEqual(testA,True)


    def test_16_NumeroProfesores(self):
        '''Comprueba que se obtiene de forma correcta el número de profesores en la BD.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que no existan.
        resultado=False
        cero=GestorProfesores.getNumProfesores()
        print cero
        for x in range(0, 3):
            GestorProfesores.nuevoProfesor(str(x), str(x))
        tres=GestorProfesores.getNumProfesores()
        GestorProfesores.delProfesor('0')

        dos=GestorProfesores.getNumProfesores();

        if cero==0 and tres==3 and dos==2:
            resultado=True

        self.assertEqual(resultado,True)

    ####
    #   TESTS DE RELACIONES CON OTRAS ENTIDADES, usando aprovisionadorDBconInterfaz.py
    ####

    if False:
        def test_16_AlumnosALosQueDaClaseUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getAlumnos('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,3)

        def test_17_AsignaturasQueImparteUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getAsignaturas('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

        def test_18_CursosEnLosQueImparteUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getCursos('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

class TestEntidadAsignatura(unittest.TestCase):

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_21_IserccionAsignatura(self):
        '''Comprueba que nuevaAsignatura funciona correctamente'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #1. Insertamos una asignatura en la base de datos y comprobamos que la salida es 'OK'
        if GestorAsignaturas.nuevaAsignatura('Metodología de la ciencia') == 'OK':
            testA=True
        else:
            testA=False

        #2. Comprobamos que insertar una asignatura con un nombre que ya existe en la base de datos da error por elemento duplicado.
        if GestorAsignaturas.nuevaAsignatura('Metodología de la ciencia') == 'Elemento duplicado':
            testB=True
        else:
            testB=False

        self.assertEqual(testA and testB, True)

    def test_22_LecturaAsignaturas(self):
        '''Comprobamos que getAsignaturas devuelve el número correncto de elementos'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAsignaturas.nuevaAsignatura('Metodología de la ciencia')
        GestorAsignaturas.nuevaAsignatura('Matemática aplicada')
        #Comprobamos que son dos los alumnos que devuelve el método getAlumnos()
        self.assertEqual(len(GestorAsignaturas.getAsignaturas()),2)

    def test_23_LecturaAsignatura(self):
        '''Comprobación de la extracción de los datos de una asignatura concreta'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAsignaturas.nuevaAsignatura('Matemática aplicada')
        self.assertNotEqual(GestorAsignaturas.getAsignatura('1'),'Elemento no encontrado')

    def test_24_ModificacionAsignatura(self):
        '''Comprobación de como cualquier atributo de un asignatura puede modificarse'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        testA=testB=testC=False;

        #Creamos una asignatura.
        GestorAsignaturas.nuevaAsignatura('Matemática aplicada')
        #1. modificamos el nombre de la asignatura creada:
        if GestorAsignaturas.modAsignatura('1','nombre','Matemáticas Avanzadas') == 'OK':
            testA=True
            print "yeah"

        #Intentamos cambiar un elemento que no existe
        if GestorAsignaturas.modAsignatura('2', 'nombre', 'Física') == 'Elemento no encontrado':
            testB=True

        #Cambiamos un param de un asignatura por uno que ya existe en la base de datos.
        GestorAsignaturas.nuevaAsignatura('mat')
        GestorAsignaturas.nuevaAsignatura('fis')
        #Debe decirnos que ya existe uno con ese campo por tanto estaría duplicado y aborta.
        if GestorAsignaturas.modAsignatura('2', 'nombre', 'fis') == 'Elemento duplicado':
            testC=True #El error se da.

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB and testC, True)

    def test_15_EliminacionAsignatura(self):
        '''Eliminamos una asignatura de la base de datos y comprobamos el mensaje devuelto'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorAsignaturas.nuevaAsignatura('fis')
        #Si la asig se elimina y no se encuentra después está bien.
        if GestorAsignaturas.delAsignatura('1') == 'OK' and GestorAsignaturas.delAsignatura('1') == 'Elemento no encontrado':
            testA=True
        else:
            testA=False

        self.assertEqual(testA,True)

    def test_16_NumeroAsignaturas(self):
        '''Comprueba que se obtiene de forma correcta el número de asignaturas en la BD.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que no existan.
        resultado=False
        cero=GestorAsignaturas.getNumAsignaturas()
        print cero
        for x in range(0, 3):
            GestorAsignaturas.nuevaAsignatura(str(x))
        tres=GestorAsignaturas.getNumAsignaturas()
        GestorAsignaturas.delAsignatura('1')

        dos=GestorAsignaturas.getNumAsignaturas()

        if cero==0 and tres==3 and dos==2:
            resultado=True

        self.assertEqual(resultado,True)

    ####
    #   TESTS DE RELACIONES CON OTRAS ENTIDADES, usando aprovisionadorDBconInterfaz.py
    ####


    if False:

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

if False:
    class TestEntidadClase(unittest.TestCase):

        # QUEDA HACER LO MISMO CON CLASE !!!!!!!


        seguir aquí!

        #HABRÍA QUE PONER LOS TEST DE RELACIONES DESPUÉS DE TODOS LOS TEST DE COLECCIONES, YA QUE LOS TEST DE
        #RELACIONES COMPRUEBAN COSAS QUE SE TIENEN QUE ESTABLECER CON MÉTODOS DE COLLECCIONES PRIMRO.


        #SERÍA INTERESANTE PONERLO EN OTRAS CUATRO CLASES como TestRelacionesClase que
        irían al final después de las de entidad de Matrícula, Asocia e Imparte


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
