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
    GestorAlumnos.nuevoAlumno('A','A1','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('B','A2','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('C','A3','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('D','A4','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('E','A5','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('F','A6','---','---','---','1900-1-1','---')

    #Insertamos 3 profesores:
    GestorProfesores.nuevoProfesor('PA','P1','---','---','---','1900-2-1','---','---')
    GestorProfesores.nuevoProfesor('PB','P2','---','---','---','1900-2-1','---','---')
    GestorProfesores.nuevoProfesor('PC','P3','---','---','---','1900-2-1','---','---')

    #Creamos dos Asignaturas:
    GestorAsignaturas.nuevaAsignatura('fr','Frances')
    GestorAsignaturas.nuevaAsignatura('mt','Matematicas')
    '''
    #Creamos dos Cursos
    GestorCursos.nuevoCurso('1AESO','1','A','ES0')
    GestorCursos.nuevoCurso('1BESO','1','B','ES0')

    #Asociamos cada asignatura a un curso:
    GestorAsociaciones.nuevaAsociacion('fr','1AESO') #En 1ºA de ESO solo se imparte la asignatura Francés
    GestorAsociaciones.nuevaAsociacion('mt','1BESO') #En 1ºB de ESO solo se imparte la asignatura Matemáticas


    #Especificaremos que profesores imparten las asignaturas:
    GestorImparte.nuevoImparte('fr','1AESO','1') #La imparte el profesor 1
    GestorImparte.nuevoImparte('fr','1AESO','2') #La imparte el profesor 2, también.
    GestorImparte.nuevoImparte('mt','1BESO','3') #La imparte el profesor 3

    #Matriculamos alumnos en las asignatura:
    GestorMatriculas.nuevaMatricula('fr','1AESO','1')
    GestorMatriculas.nuevaMatricula('mt','1AESO','1') #Matriculamos al mismo en dos asignaturas

    GestorMatriculas.nuevaMatricula('fr','1AESO','2')
    GestorMatriculas.nuevaMatricula('fr','1AESO','3')
    GestorMatriculas.nuevaMatricula('mt','1BESO','4')
    GestorMatriculas.nuevaMatricula('mt','1BESO','5')
    GestorMatriculas.nuevaMatricula('mt','1BESO','6')


    '''

if __name__ == '__main__':
    aprovisiona()
