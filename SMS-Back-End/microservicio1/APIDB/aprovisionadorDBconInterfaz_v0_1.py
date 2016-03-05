# -*- coding: utf-8 -*-

# Aprovisionador de la base de datos que inserta datos bajo la
# especificación del creador DBCreator_v0_1 usando sólo los métodos nuevo/a ala entidad o
# relacion que se está añadiendo elementos.

from GestorAlumnosSQL import GestorAlumnos
from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores
from GestorAsignaturasSQL import GestorAsignaturas
from GestorClasesSQL import GestorClases
from GestorAsociacionesSQL import GestorAsociaciones
from GestorImparteSQL import GestorImparte
from GestorMatriculasSQL import GestorMatriculas

def aprovisiona():
    #Insertamos 6 alumnos:
    GestorAlumnos.nuevoAlumno('A')
    GestorAlumnos.nuevoAlumno('B')
    GestorAlumnos.nuevoAlumno('C')
    GestorAlumnos.nuevoAlumno('D')
    GestorAlumnos.nuevoAlumno('E')
    GestorAlumnos.nuevoAlumno('F')

    #Insertamos 3 profesores:
    GestorProfesores.nuevoProfesor('PA','1')
    GestorProfesores.nuevoProfesor('PB','2')
    GestorProfesores.nuevoProfesor('PC','3')

    #Creamos dos Asignaturas:
    GestorAsignaturas.nuevaAsignatura('Frances')
    GestorAsignaturas.nuevaAsignatura('Matematicas')

    #Creamos dos Clases
    GestorClases.nuevaClase('1','A','ES0')
    GestorClases.nuevaClase('1','B','ES0')

    #Asociamos cada asignatura a un curso:
    GestorAsociaciones.nuevaAsociacion('1','1') #En 1ºA de ESO solo se imparte la asignatura Francés
    GestorAsociaciones.nuevaAsociacion('2','2') #En 1ºB de ESO solo se imparte la asignatura Matemáticas
    GestorAsociaciones.nuevaAsociacion('2','1') #En 1ºB de ESO solo se imparte la asignatura Matemáticas

    #Especificaremos que profesores imparten las asignaturas:
    GestorImparte.nuevoImparte('1','1','1') #La imparte el profesor 1
    GestorImparte.nuevoImparte('2','1','2') #La imparte el profesor 2, también.
    GestorImparte.nuevoImparte('2','2','3') #La imparte el profesor 3
    GestorImparte.nuevoImparte('2','2','2')
    #Matriculamos alumnos en las asignatura:
    GestorMatriculas.nuevaMatricula('1','1','1')
    GestorMatriculas.nuevaMatricula('2','1','1')
    GestorMatriculas.nuevaMatricula('3','1','1')
    GestorMatriculas.nuevaMatricula('4','2','1')
    GestorMatriculas.nuevaMatricula('5','2','1')
    GestorMatriculas.nuevaMatricula('6','2','2')




if __name__ == '__main__':
    aprovisiona()
