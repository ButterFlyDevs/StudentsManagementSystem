# -*- coding: utf-8 -*-
from GestorAlumnosSQL import GestorAlumnos
from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores
from GestorAsignaturasSQL import GestorAsignaturas
from GestorCursosSQL import GestorCursos
from GestorAsociacionesSQL import GestorAsociaciones
from GestorImparteSQL import GestorImparte
from GestorMatriculasSQL import GestorMatriculas

'''
Vamos a introducir contenido relacionado en la base de datos.
'''
def aprovisiona():
    #Creamos 6 alumnos:
    GestorAlumnos.nuevoAlumno('A','1','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('B','2','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('C','3','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('D','4','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('E','5','---','---','---','1900-1-1','---')
    GestorAlumnos.nuevoAlumno('F','6','---','---','---','1900-1-1','---')

    #Creamos 3 profesores:
    GestorProfesores.nuevoProfesor('PA','1','---','---','---','1900-2-1','---','---')
    GestorProfesores.nuevoProfesor('PB','2','---','---','---','1900-2-1','---','---')
    GestorProfesores.nuevoProfesor('PC','3','---','---','---','1900-2-1','---','---')

    #Creamos dos Asignaturas:
    GestorAsignaturas.nuevaAsignatura('fr','Frances')
    GestorAsignaturas.nuevaAsignatura('mt','Matematicas')

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
    GestorMatriculas.nuevaMatricula('mt','1BESO','1') #Matriculamos al mismo en dos asignaturas

    GestorMatriculas.nuevaMatricula('fr','1AESO','2')
    GestorMatriculas.nuevaMatricula('fr','1AESO','3')
    GestorMatriculas.nuevaMatricula('mt','1BESO','4')
    GestorMatriculas.nuevaMatricula('mt','1BESO','5')
    GestorMatriculas.nuevaMatricula('mt','1BESO','6')


if __name__ == '__main__':
    aprovisiona()
