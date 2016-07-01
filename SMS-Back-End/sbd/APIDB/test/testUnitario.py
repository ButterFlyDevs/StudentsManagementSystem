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
from GestorImpartesSQL import GestorImpartes
from GestorMatriculasSQL import GestorMatriculas
from GestorEntidades import GestorEntidades
#import aprovisionadorDBconInterfaz
#Las clases para la realización de los test debe heredar de unittest.TestCase
from termcolor import colored
########################################################
###  sobre ENTIDADES(tablas) y RELACIONES(tablas)    ###
########################################################

### ENTIDADES, como Alumno, Profesor... ###

class TestEntidadAlumno(unittest.TestCase):
    '''
    Testing de GestorAlumnosSQL
    '''

    def setUp(self):
        #Esta configuración se realiza antes de cada test.
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento, para cada test.
        os.system('mysql -u root -p\'root\' < ../DBCreatorv1.sql')

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    #La ejecución de los test se hace por orden alfabético, algo a tener en cuenta cuando queremos hacer ciertas acciones.
    def test_01_IserccionAlumno(self):
        test = True
        #1. Insertamos un alumno en la base de datos y comprobamos que la salida es 'OK'
        if GestorAlumnos.nuevoAlumno(nombre='Juan', apellidos='Fernández')['status'] != 'OK':
            test = False
        #2. Comprobamos que insertar un alumno con un dni que ya existe en la base de datos da error por elemento duplicado.
        if GestorAlumnos.nuevoAlumno(nombre='Pedro', apellidos='Garcia', dni='3333')['status']!= 'OK':
            test = False
        if GestorAlumnos.nuevoAlumno(nombre='Maria', dni='3333')['status'] != 'Elemento duplicado':
            test = False

        self.assertEqual(test, True)

    #"""
    def test_02_LecturaAlumnos(self):
        test = True
        GestorAlumnos.nuevoAlumno(nombre='Andrés') #Insertamos un alumno
        GestorAlumnos.nuevoAlumno(nombre='Julián') #Insertamos otro
        lista=GestorAlumnos.getAlumnos()
        print lista
        if len(lista)!= 2 \
            or lista[0]['nombre'] != u'Andrés' \
            or lista[1]['nombre'] != u'Julián': test = False

        alumno = GestorAlumnos.getAlumnos(idAlumno='1')
        print colored (alumno, 'green')
        if alumno['nombre'] != u'Andrés': test = False

        self.assertTrue(test)

    def test_03_ModificacionAlumno(self):
        '''Comprobación de como cualquier atributo de un alumno puede modificarse'''
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
        self.assertEqual(testA , True)

    def test_04_EliminacionAlumno(self):
        '''Eliminamos el alumno de la base de datos y comprobamos el mensaje devuelto'''
        GestorAlumnos.nuevoAlumno('Juan')
        #Si el alumno se elimina y no se encuentra después está bien.
        if GestorAlumnos.delAlumno('1') == 'OK' \
            and GestorAlumnos.getAlumnos(idAlumno='1') == 'Elemento no encontrado' \
            and len(GestorAlumnos.getAlumnos()) == 0:
                testA=True
        else:
            testA=False

        self.assertEqual(testA,True)

    def test_05_NumeroAlumnos(self):
        '''Comprueba que se obtiene de forma correcta el número de alumnos en la BD.'''
        #Comprobamos que no existan.
        cero=GestorAlumnos.getNumAlumnos()
        for x in range(0, 3):
            GestorAlumnos.nuevoAlumno(str(x))
        tres=GestorAlumnos.getNumAlumnos()
        GestorAlumnos.delAlumno('2')

        dos=GestorAlumnos.getNumAlumnos();

        resultado=False
        if cero==0 and tres==3 and dos==2:
            resultado=True

        self.assertEqual(resultado,True)


class TestEntidadProfesor(unittest.TestCase):

    def setUp(self):
        os.system('mysql -u root -p\'root\' < ../DBCreatorv1.sql')

    def test_11_IserccionProfesor(self):
        test = True
        #1. Insertamos un alumno en la base de datos y comprobamos que la salida es 'OK'
        if GestorProfesores.nuevoProfesor(nombre='nombre', apellidos='apellidos')['status'] != 'OK': test = False
        #2. Comprobamos que insertar un alumno con un dni que ya existe en la base de datos da error por elemento duplicado.
        GestorProfesores.nuevoProfesor(nombre='Pedro', dni='3333', apellidos='Garcia', )
        if GestorProfesores.nuevoProfesor(nombre='Maria', dni='3333')['status'] != 'Elemento duplicado': test = False
        self.assertTrue(test)

    def test_12_LecturaProfesores(self):
        'Comprobamos que getProfesores devuelve el número correcto de elementos'
        test = True
        antes=len(GestorProfesores.getProfesores())
        GestorProfesores.nuevoProfesor(nombre='Juan', dni='24242')
        GestorProfesores.nuevoProfesor(nombre='Andrés', dni='2878' )
        lista=GestorProfesores.getProfesores()
        if len(lista)!= 2 \
            or antes != 0 \
            or lista[0]['nombre'] != u'Juan' \
            or lista[1]['nombre'] != u'Andrés': test = False
        profesor = GestorProfesores.getProfesores(idProfesor='1')
        if profesor == 'Elemento no encontrado' \
        or profesor['nombre'] != u'Juan' \
        or profesor['dni'] != 24242:
            test = False
        self.assertTrue(test)

    def test_13_ModificacionProfesor(self):
        '''Comprobación de como cualquier atributo de un profesor puede modificarse'''
        test=True
        #Creamos un alumno con nombre Juan.
        GestorProfesores.nuevoProfesor(nombre='Juan', dni='222')
        #modificamos el nombre del profesor creado:
        if GestorProfesores.modProfesor(idProfesor='1', campoACambiar='Nombre', nuevoValor='Enrique') != 'OK':
            testA=False
        #Cambiamos el dni
        if GestorProfesores.modProfesor(idProfesor='1', campoACambiar='dni', nuevoValor='1414') != 'OK':
            testB=False
        #Cambiamos el dni de un profesor por uno que ya existe en la base de datos.
        GestorProfesores.nuevoProfesor(nombre='Luis', dni='1010')
        #Debe decirnos que ya existe uno con ese campo por tanto estaría duplicado.
        if GestorProfesores.modProfesor(idProfesor='1', campoACambiar='dni', nuevoValor='1414') != 'Elemento duplicado':
            testC=False
        #Comprobamos que el nombre ha sido cambiado.
        self.assertTrue(test)

    def test_14_EliminacionProfesor(self):
        '''Eliminamos el profesor de la base de datos y comprobamos el mensaje devuelto'''
        test = True
        GestorProfesores.nuevoProfesor(nombre='Luis')
        #Si el alumno se elimina y no se encuentra después está bien.
        if GestorProfesores.delProfesor(idProfesor='1') != 'OK' and GestorProfesores.delProfesor(idProfesor='1') != 'Elemento no encontrado':
            test = False
        self.assertTrue(test)

    def test_15_NumeroProfesores(self):
        '''Comprueba que se obtiene de forma correcta el número de profesores en la BD.'''
        #Comprobamos que no existan.
        test=False
        cero=GestorProfesores.getNumProfesores()
        for x in range(0, 3):
            GestorProfesores.nuevoProfesor(nombre=str(x))
        tres=GestorProfesores.getNumProfesores()
        GestorProfesores.delProfesor(idProfesor='1')
        dos=GestorProfesores.getNumProfesores();
        if cero==0 and tres==3 and dos==2:
            test=True
        self.assertTrue(test)

class TestEntidadAsignatura(unittest.TestCase):

    def setUp(self):
        os.system('mysql -u root -p\'root\' < ../DBCreatorv1.sql')

    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_21_IserccionAsignatura(self):
        """Comprueba que nuevaAsignatura funciona correctamente"""
        test = True
        #1. Insertamos una asignatura en la base de datos y comprobamos que la salida es 'OK'
        if GestorAsignaturas.nuevaAsignatura(nombre='Metodología de la ciencia')['status'] != 'OK': test = False
        #2. Comprobamos que insertar una asignatura con un nombre que ya existe en la base de datos da error por elemento duplicado.
        if GestorAsignaturas.nuevaAsignatura(nombre='Metodología de la ciencia')['status'] != 'Elemento duplicado': test = False
        self.assertTrue(test)


    def test_22_LecturaAsignaturas(self):
        """Comprobamos que getAsignaturas devuelve el número correncto de elementos"""
        test = True
        GestorAsignaturas.nuevaAsignatura(nombre='ásigA')
        GestorAsignaturas.nuevaAsignatura(nombre='ásigB')
        asignaturas = GestorAsignaturas.getAsignaturas()
        if len(asignaturas) != 2: test = False
        if asignaturas[0]['nombre'] != u'ásigA' or asignaturas[1]['nombre'] != u'ásigB': test = False
        asigA = GestorAsignaturas.getAsignaturas(idAsignatura='1')
        if asigA['nombre'] != u'ásigA': test = False
        self.assertTrue(test)


    def test_23_ModificacionAsignatura(self):
        '''Comprobación de como cualquier atributo de un asignatura puede modificarse'''
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


    def test_24_EliminacionAsignatura(self):
        '''Eliminamos una asignatura de la base de datos y comprobamos el mensaje devuelto'''
        GestorAsignaturas.nuevaAsignatura('fis')
        #Si la asig se elimina y no se encuentra después está bien.
        if GestorAsignaturas.delAsignatura('1') == 'OK' and GestorAsignaturas.delAsignatura('1') == 'Elemento no encontrado':
            testA=True
        else:
            testA=False

        self.assertEqual(testA,True)

    def test_25_NumeroAsignaturas(self):
        '''Comprueba que se obtiene de forma correcta el número de asignaturas en la BD.'''
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

class TestGestorEntidades(unittest.TestCase):

    def setUp(self):
        os.system('mysql -u root -p\'root\' < ../DBCreatorv1.sql')

    def test_31_putEntidades(self):
        test = True
        if GestorEntidades.putEntidad(tipo='Alumno', datos={'nombre': 'súperNombre'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Profesor', datos={'nombre': 'súperNombre'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Asignatura', datos={'nombre': 'Francés'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Clase', datos={'curso': '1', 'grupo': 'B', 'nivel': 'ESO'})['status'] != 'OK' or \
        GestorEntidades.putEntidad(tipo='Desconocido', datos={'prueba': 'hola'})['status'] != 'Tipo no reconocido':
            test = False

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


"""
class TestEntidadClase(unittest.TestCase):

    def test_31_IserccionClase(self):
        '''
        Comprueba el método nuevaClase del gestor GestorClasesSQL.py
        '''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #1. Insertamos una clase en la base de datos y comprobamos que la salida es 'OK'
        if GestorClases.nuevaClase('1','A','ESO') == 'OK':
            testA=True
        else:
            testA=False

        #2. Comprobamos que insertar una asignatura con un nombre que ya existe en la base de datos da error por elemento duplicado.
        if GestorClases.nuevaClase('1','A','ESO') == 'Elemento duplicado':
            testB=True
        else:
            testB=False

        self.assertEqual(testA and testB, True)

    def test_32_LecturaClases(self):
        ''' Comprobación de recuperación correcta de todas las clases de la base de datos'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorClases.nuevaClase('1','A','ESO')
        GestorClases.nuevaClase('1','B','ESO')
        GestorClases.nuevaClase('1','C','ESO')
        self.assertEqual(len(GestorClases.getClases()),3)

    def test_33_LecturaClase(self):
        ''' Comprobación de la lectura correcta de una clase'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorClases.nuevaClase('1','A','ESO')
        self.assertNotEqual(GestorClases.getClase('1'),'Elemento no encontrado')

    def test_34_ModificacionClase(self):
        '''Comprobación de como cualquier atributo de una clase puede modificarse, método modClase de GestorClasesSQL.py'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Preparamos las variables
        testA=testB=testC=False;

        #Creamos una asignatura.
        GestorClases.nuevaClase('1','A','ESO')
        #1. modificamos el nombre de la asignatura creada, que podremos porque no hay ninguna igual.
        if GestorClases.modClase('1','nivel','BACH') == 'OK':
            testA=True

        #Intentamos cambiar un elemento que no existe
        if GestorClases.modClase('2', 'nivel', 'Primaria') == 'Elemento no encontrado':
            testB=True

        #Creamos una nueva clase
        GestorClases.nuevaClase('1','A','ESO') #LA anterior quedó como 1ABACH
        #Intentamos cambiar un parámetro quedando como tra existente, debe de dar Elemento duplicado como error.
        if GestorClases.modClase('2', 'nivel', 'BACH') == 'Elemento duplicado':
            testC=True #El error se da.

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB and testC, True)

    def test_35_EliminacionClase(self):
        ''' Comprobación del funcionamiento de delClase de GestorClaseSQL.py'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        GestorClases.nuevaClase('1','A','ESO')
        if GestorClases.delClase('1') == 'OK' and GestorClases.delClase('1') == 'Elemento no encontrado':
            testA=True
        else:
            testA=False
        self.assertEqual(testA, True)

    def test_36_NumeroClases(self):
        '''Comprueba que se obtiene de forma correcta el número de clases en la BD con getNumClases de GestorClasesSQL.py'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Comprobamos que no existan.
        resultado=False
        cero=GestorClases.getNumClases()
        print cero
        for x in range(1, 4):
            GestorClases.nuevaClase(str(x),'A','ESO')
        tres=GestorClases.getNumClases()
        GestorClases.delClase('1')
        dos=GestorClases.getNumClases()

        if cero==0 and tres==3 and dos==2:
            resultado=True

        self.assertEqual(resultado,True)

###################################################################################
### RELACIONES, (entre entidades u otras relaciones), como Matricula, Asocia... ###
###################################################################################

class TestRelacionAsocia(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Asocia que relaciona las entidades Curso y Asignatura de la BD.
    '''
    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_41_InserccionRelacionAsocia(self):
        '''
        Comprueba el método nuevaClase del gestor GestorAsociacionesSQL.py
        '''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Preparamos las variables
        testA=testB=testC=False;

        #1. Insertamos una asociacion en la base de datos y comprobamos que la salida es 'OK'
        #Primero creamos una clase.
        GestorClases.nuevaClase('1','A','ESO')
        #Después creamos una asignatura:
        GestorAsignaturas.nuevaAsignatura('frances')
        #Usamos ambos ides (1 y 1 porque se acaban de introducir y son autoincrementables) para relacionarlos.
        if GestorAsociaciones.nuevaAsociacion('1','1') == 'OK':
            testA=True
        else:
            testA=False

        #2. Comprobamos que no podemos introducir una asociación entre una Clase y una Asignatura si alguna de las dos
        # no existe previamente (por las foreing keys)
        print "GestorAsociaciones"+str(GestorAsociaciones.nuevaAsociacion('1','2'))
        if GestorAsociaciones.nuevaAsociacion('1','2') == 'Alguno de los elementos no existe':
            testB=True
        else:
            testB=False

        #3. Comprobamos que insertar una asociació que ya existe nos da un error.
        print GestorAsociaciones.nuevaAsociacion('1','1')
        if GestorAsociaciones.nuevaAsociacion('1','1') == 'Elemento duplicado':
            testC=True
        else:
            testC=False

        self.assertEqual(testA and testB and testC, True)

    def test_42_LecturaAsociaciones(self):
        '''Recupera la lista de todas las asociaciones (Clase-Asignatura) almacenadas en la base de datos.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Creamos una clase
        GestorClases.nuevaClase('1','A','ESO')
        #Después creamos dos asignaturas:
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsignaturas.nuevaAsignatura('lengua')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorAsociaciones.nuevaAsociacion('1','2')

        self.assertEqual(len(GestorAsociaciones.getAsociaciones()),2)

    def test_43_LecturaAsociacion(self):
        ''' Comprobación de la lectura correcta de una asociacion concreta'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Damos de alta una clase
        GestorClases.nuevaClase('1','A','ESO')
        #Después creamos dos asignaturas:
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')

        if GestorClases.getClase('1') != 'Elemento no encontrado' and GestorClases.getClase('2') == 'Elemento no encontrado':
            test=True
        else:
            test=False

        self.assertEqual(test, True)

    def test_44_ModificacionAsociacion(self):
        '''Comprobación de como cualquier atributo de una asociación puede modificarse, método modAsociacion de GestorAsociacionesSQL.py'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        #Preparamos las variables
        testA=testB=testC=False;

        #Creamos una asociación:
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsignaturas.nuevaAsignatura('ingles')
        #Relacionamos la clase con la primera asignatura.
        GestorAsociaciones.nuevaAsociacion('1','1')

        #1. Modificamos la asignatura de la asociación por la asignatura 2
        if GestorAsociaciones.modAsociacion('1','1','id_asignatura', '2') == 'OK':
            testA=True


        #Intentamos asociar una clase con una asignatura que no existe (la asignatura con id 3, inexistente):
        if GestorAsociaciones.modAsociacion('1','1','id_asignatura', '3') == 'Elemento no encontrado':
            testB=True


        #Comprobamos que si realizamos una modificación que da lugar a una asociacioón que ya existe lo detecta.
        '''
        #Creamos una nueva clase
        GestorClases.nuevaClase('1','A','ESO') #LA anterior quedó como 1ABACH
        #Intentamos cambiar un parámetro quedando como tra existente, debe de dar Elemento duplicado como error.
        if GestorClases.modClase('2', 'nivel', 'BACH') == 'Elemento duplicado':
            testC=True #El error se da.
        '''

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB, True)

    def test_45_EliminacionAsocia(self):
        '''Elimina una tupla de la tabla Asocia usando delAsociaciones de GestorAsociacionesSQL'''
        #Vamos a comprobar que se pueden eliminar asociaciones borrando la anterior.
        #Eliminamos los objetos creados para el test.
        if GestorAsociaciones.delAsociacion('1','2') == 'OK' and GestorAsociaciones.delAsociacion('3','3') == 'Elemento no encontrado':
            test=True
        else:
            test=False
        self.assertEqual(test, True)

    def test_46_NumeroAsociaciones(self):
        '''Comprueba que se obtiene de forma correcta el número de asociaciones en la BD con getNumAsociaciones de GestorAsociacionesSQL.py'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')
        cero=GestorAsociaciones.getNumAsociaciones()
        #Primero creamos una clase.
        GestorClases.nuevaClase('1','A','ESO')
        #Después creamos una asignatura:
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsignaturas.nuevaAsignatura('len')
        #Usamos ambos ides (1 y 1 porque se acaban de introducir y son autoincrementables) para relacionarlos.
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorAsociaciones.nuevaAsociacion('1','2')
        dos=GestorAsociaciones.getNumAsociaciones()
        GestorAsociaciones.delAsociacion('1','2')
        una=GestorAsociaciones.getNumAsociaciones()

        if cero==0 and dos==2 and una==1:
            resultado=True
        else:
            resultado=False

        self.assertEqual(resultado,True)


class TestRelacionImparte(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Imparte que relaciona las entidades Curso, Asignatura y profesor de la BD.
    '''
    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_51_InserccionRelacionImparte(self):
        '''Comprueba el método nuevoImparte del gestor GestorImpargeSQL.py'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Preparamos las variables
        testA=testB=testC=False;

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorProfesores.nuevoProfesor('Juan', '222')

        #Creamos una entidad en la tabla Imparte. id_clase=1, id_asignatura=1 y dni=222
        if GestorImpartes.nuevoImparte('1','1','222') == 'OK':
            testA=True
        else:
            testA=False

        #Creamos una entidad de la tabla Imparte con algún elemento que no existe en Asocia.
        if GestorImpartes.nuevoImparte('1','1','333') == 'Alguno de los elementos no existe':
            testB=True
        else:
            testB=False

        #Testeamos que todas las acciones han sido correctas
        self.assertEqual(testA and testB, True)

    def test_52_LecturaImpartes(self):
        '''Recupera la lista de todas las entidades Imparte (Clase-Asignatura-Profesor) almacenadas en la base de datos.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        cero = len(GestorAsociaciones.getAsociaciones())

        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorProfesores.nuevoProfesor('Juan', '222')

        #Creamos la entidad en la tabla Imparte
        GestorImpartes.nuevoImparte('1','1','222')

        uno = len(GestorImpartes.getImpartes())

        print cero
        print uno
        if cero == 0 and uno == 1:
            test = True
        else:
            test = False

        self.assertEqual(test, True)

    def test_53_LecturaImparte(self):
        ''' Comprobación de la lectura correcta de una entidad Imparte concreta'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una entidad en la tabla Imparte con las tres entidades que necesita para realizarse
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorProfesores.nuevoProfesor('Juan', '222')
        GestorImpartes.nuevoImparte('1','1','222')

        #La tupla 1, 1, 222 existe y la 1, 1 ,333 no existe.
        if GestorImpartes.getImparte('1','1','222') != 'Elemento no encontrado' and GestorImpartes.getImparte('1','1','333') == 'Elemento no encontrado':
            test=True
        else:
            test=False

        self.assertEqual(test, True)

    def test_54_ModificacionImparte(self):
        '''Comprobación de como cualquier atributo de una tupla en la tabla Impparte puede modificarse'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una entidad en la tabla Imparte con las tres entidades que necesita para realizarse
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorProfesores.nuevoProfesor('Juan', '222')
        GestorProfesores.nuevoProfesor('Antonio', '333')
        GestorImpartes.nuevoImparte('1','1','222')

        testA=testB=testC=False;

        #Modificamos la tupla imparte para que a esa asociacion (clase-asignatura) le imparta otro profesor.
        if GestorImpartes.modImparte('1','1','222', 'id_profesor', '333') == 'OK':
            testA=True

        #Intenamos realizar otra modificación sobre una tupla que no existe
        if GestorImpartes.modImparte('1','1','222', 'id_asignatura', '6') == 'Elemento no encontrado':
            testB=True

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB, True)

    def test_55_EliminacionRelacionImparte(self):
        ''' Comprobación de la lectura correcta de una entidad Imparte concreta'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una entidad en la tabla Imparte con las tres entidades que necesita para realizarse
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        GestorProfesores.nuevoProfesor('Juan', '222')
        GestorImpartes.nuevoImparte('1','1','222')

        if GestorImpartes.delImparte('1','1','222') == 'OK' and GestorImpartes.delImparte('2','2','333') == 'Elemento no encontrado':
            test = True
        else:
            test = False

        self.assertEqual(test, True)


class TestRelacionMatricula(unittest.TestCase):
    '''
    Comprobación de las operaciones CRUD sobre la tabla Matricula que relaciona las entidades Clase, Asignatura y Alumno.
    '''
    #Los métodos, por convención empiezan por la palabra test, representando que métodos componen el test.
    def test_61_InserccionRelacionMatricula(self):
        '''Comprueba el método nuevaMatricula del gestor GestorMatriculasSQL.py'''
        #Nos aseguramos de que la base de datos se encuentra en estado CERO creándola en el momento.
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Preparamos las variables
        testA=testB=testC=False;

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')

        GestorAlumnos.nuevoAlumno('Juan')

        #Creamos una entidad en la tabla Matricula. id_alumno=1, id_clase=1 y id_asignatura=1.
        if GestorMatriculas.nuevaMatricula('1','1','1') == 'OK':
            testA=True
        else:
            testA=False

        #Creamos una entidad de la tabla Imparte con algún elemento que no existe, en este caso la asignatura con id 333.
        if GestorImpartes.nuevoImparte('1','1','333') == 'Alguno de los elementos no existe':
            testB=True
        else:
            testB=False

        #Testeamos que todas las acciones han sido correctas
        self.assertEqual(testA and testB, True)

    def test_62_LecturaMatriculas(self):
        '''Recupera la lista de todas las entidades de la tabla Matricula (Alumno-Clase-Asignatura) almacenadas en la base de datos.'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #No debe de haber nada.
        cero = len(GestorMatriculas.getMatriculas())

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        #Creamos un alumno
        GestorAlumnos.nuevoAlumno('Juan')

        #Creamos una entidad en la tabla Matricula. id_alumno=1, id_clase=1 y id_asignatura=1.
        GestorMatriculas.nuevaMatricula('1','1','1')
        #Ahora hay una
        uno = len(GestorMatriculas.getMatriculas())


        if cero == 0 and uno == 1:
            test = True
        else:
            test = False

        self.assertEqual(test, True)

    def test_63_LecturaMatricula(self):
        ''' Comprobación de la lectura correcta de una entidad de a tabla Matricula concreta'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        #Creamos un alumno
        GestorAlumnos.nuevoAlumno('Juan')
        #Creamos una entidad en la tabla Matricula. id_alumno=1, id_clase=1 y id_asignatura=1.
        GestorMatriculas.nuevaMatricula('1','1','1')

        #La tupla 1, 1, 222 existe y la 1, 1 ,333 no existe.
        if GestorMatriculas.getMatricula('1','1','1') != 'Elemento no encontrado' and GestorMatriculas.getMatricula('1','1','333') == 'Elemento no encontrado':
            test=True
        else:
            test=False

        self.assertEqual(test, True)

    def test_64_ModificacionMatricula(self):
        '''Comprobación de como cualquier atributo de una tupla en la tabla Impparte puede modificarse'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        #Creamos un alumno
        GestorAlumnos.nuevoAlumno('Juan')
        GestorAlumnos.nuevoAlumno('Maria')
        #Creamos una entidad en la tabla Matricula. id_alumno=1, id_clase=1 y id_asignatura=1.
        GestorMatriculas.nuevaMatricula('1','1','1')

        testA=testB=testC=False;

        #Modificamos la tupla Matricula para que a esa asociacion (clase-asignatura) que está matriculado otro alumno.
        if GestorMatriculas.modMatricula('1','1','1', 'id_alumno', '2') == 'OK':
            testA=True

        #Intenamos realizar otra modificación sobre una tupla que no existe, la matricula no existe.
        if GestorMatriculas.modMatricula('1','1','1', 'id_asignatura', '6') == 'Elemento no encontrado':
            testB=True

        #Comprobamos que el nombre ha sido cambiado.
        self.assertEqual(testA and testB, True)


    def test_64_EliminacionMatricula(self):
        '''Comprobación de la eliminación de una tupla de la tabla Matricula'''
        os.system('mysql -u root -p\'root\' < ../DBCreator_v0_1.sql')

        #Creamos una realación asocia y antes una clas y una asignatura
        GestorClases.nuevaClase('1','A','ESO')
        GestorAsignaturas.nuevaAsignatura('frances')
        GestorAsociaciones.nuevaAsociacion('1','1')
        #Creamos un alumno
        GestorAlumnos.nuevoAlumno('Juan')
        GestorAlumnos.nuevoAlumno('Maria')
        #Creamos una entidad en la tabla Matricula. id_alumno=1, id_clase=1 y id_asignatura=1.
        GestorMatriculas.nuevaMatricula('1','1','1')

        if GestorMatriculas.delMatricula('1','1','1') == 'OK' and GestorMatriculas.delMatricula('1','1','1') == 'Elemento no encontrado':
            test = True
        else:
            test = False

        self.assertEqual(test, True)



#### léeme ####
'''
Una vez que se han testeado los métodos que trabajan sobre las entidades (Alumno, Profesor, Asignatura, Clase) y sobre
las relaciones (Matricula, Asocia e Imparte) se procede a testear los métodos de las anteriores, tanto entidades
como relaciones que comprueban que entidades concretas se relacionan bien con otras puesto que para comprobar esto
los métodos de insercción como mínimo de todas las tablas (tanto entidades como Alumno y relaciones como Matricula)
deben estar implementados para que el aprovisionador pueda funcionar asegurándonos de que los métodos que usa están
testeados.
Es por esto anterior por lo que los siguientes métodos se implementan a continuación y no antes.
'''
###############

########################################################
###  sobre la relación de entidades con otras        ###
########################################################

#Los métodos de las entidades que dan información de como se relacionan con otras.

class Test_RELACIONES_CON_OTROS_EntidadAlumno(unittest.TestCase):
    '''
    Testing de los métodos que obtienen relaciones con otras entidades de la base de datos.
    '''

    ####
    #   TESTS DE RELACIONES CON OTRAS ENTIDADES, usando aprovisionadorDBconInterfaz.py
    ####
    if False:
        def test_07_ProfesoreQueImparteAAlumno(self):
            #Ejecutamos el aprovisionamiento de la base de datos usando el aprovisionador. (la BD hasta ahora solo tiene la estructura, sin contenido)
            aprovisionadorDBconInterfaz.aprovisiona() #PAra usarlo deben de pasarse los test anteriores.
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

class Test_RELACIONES_CON_OTROS_EntidadProfesor(unittest.TestCase):
    '''
    Testing de los métodos que obtienen relaciones con otras entidades de la base de datos.
    '''
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

        def test_18_ClasesEnLosQueImparteUnProfesor(self):
            aprovisionadorDBconInterfaz.aprovisiona()
            size=len(GestorProfesores.getCursos('1'))
            os.system('mysql -u root -p\'root\' < ../DBCreator_v0.sql')
            self.assertEqual(size,1)

class Test_RELACIONES_CON_OTROS_EntidadAsignatura(unittest.TestCase):
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

class Test_RELACIONES_CON_OTROS_EntidadClase(unittest.TestCase):


    #Consultas sobre las relaciones de datos.
    if 0:

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


class Test_RELACIONES_CON_OTROS_RelacionAsocia(unittest.TestCase):

    if 0:

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
"""



if __name__ == '__main__':
    #La llamada a main hace que se ejecuten todos los métodos de todas las clases que heredan de TestCase
    unittest.main()
