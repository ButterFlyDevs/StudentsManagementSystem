# -*- coding: utf-8 -*-

#MAYBE DEPRECATED

# Aprovisionador de la base de datos que inserta datos bajo la
# especificación del creador DBCreator_v0_1 usando sólo los métodos nuevo/a ala entidad o
# relacion que se está añadiendo elementos.

from GestorAlumnosSQL import GestorAlumnos
from GestorAlumnosSQL import GestorAlumnos
from GestorProfesoresSQL import GestorProfesores
from GestorAsignaturasSQL import GestorAsignaturas
from GestorClasesSQL import GestorClases
from GestorAsociacionesSQL import GestorAsociaciones
from GestorImpartesSQL import GestorImpartes
from GestorMatriculasSQL import GestorMatriculas

def aprovisiona():

    #Insertamos 6 alumnos, cada insercción genera un id (unívco) para cada alumno.
    #Cabecera: nuevoAlumno(self,nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL')
    #id 1
    GestorAlumnos.nuevoAlumno('Rocío', 'Prida Ruíz', '99999999', 'C/ Ramon y Cajal Bloque 9. 2ºA', 'Albolote', 'Granada', '1800-03-23', '677112233')
    #id 2
    GestorAlumnos.nuevoAlumno('Eduardo', 'Martín Fernández', '12345678', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'Albolote', 'Granada', '1800-03-23', '677262625')
    #id 3
    GestorAlumnos.nuevoAlumno('Lucas', 'Hernandez Sánchez', '87654321', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'Abrucena', 'Almeria', '1800-03-23', '677262625')
    #id 4
    GestorAlumnos.nuevoAlumno('Juanjo', 'Vilchez Prieto', '12345677', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'Ablea', 'Jaen', '1800-03-23', '677262625')
    #id 5
    GestorAlumnos.nuevoAlumno('Maria', 'Priero Rodriguez', '12345679', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'Rocio Norte', 'Sevilla', '1800-03-23', '677262625')
    #id 6
    GestorAlumnos.nuevoAlumno('Estefanía', 'Cervera Gruillan', '12345670', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'La isleta', 'Málaga', '1800-03-23', '677262625')
    #id 7
    GestorAlumnos.nuevoAlumno('Bob', 'Sponja', '21', 'Cerca de la casa de calamardo', 'Fondo de Bikini', 'Océano', '1984-1-1', '6172524', 'http://www.sempreantenados.com/wp-content/gallery/bob-esponja/bob-esponja-14.jpg')


    #Insertamos 3 profesores:
    #Cabecera: nuevoProfesor(self, nombre, apellidos='NULL', dni='NULL', direccion='NULL', localidad='NULL', provincia='NULL', fecha_nacimiento='NULL', telefono='NULL'):
    #id 1
    GestorProfesores.nuevoProfesor('Juan Carlos', 'Cervera Gruillan', '12345670', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'La isleta', 'Málaga', '1800-03-23', '677262625')
    #id 2
    GestorProfesores.nuevoProfesor('Julian', 'Cervera Gruillan', '12345670', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'La isleta', 'Málaga', '1800-03-23', '677262625')
    #id 3
    GestorProfesores.nuevoProfesor('Francisco', 'Cervera Gruillan', '12345670', 'C/ Ramón y Cajal Bloque 9. 2ºA', 'La isleta', 'Málaga', '1800-03-23', '677262625')


    #Creamos dos Asignaturas:
    #Cabecera: nuevaAsignatura(self, nombre)
    #1
    GestorAsignaturas.nuevaAsignatura('Francés')
    #2
    GestorAsignaturas.nuevaAsignatura('Matemáticas')


    #Creamos dos Clases
    #Cabecera: nuevaClase(self, curso, grupo, nivel)
    #1
    GestorClases.nuevaClase('1','A','ES0')
    #2
    GestorClases.nuevaClase('1','B','ES0')

    #Asociamos cada asignatura a un clase:
    # Cabecera: nuevaAsociacion(self, id_clase, id_asignatura)
    #id 1
    GestorAsociaciones.nuevaAsociacion('1','1') #En 1ºA de ESO  se imparte la asignatura Francés
    #id 2
    GestorAsociaciones.nuevaAsociacion('2','2') #En 1ºB de ESO  se imparte la asignatura Matemáticas
    #id 3
    GestorAsociaciones.nuevaAsociacion('2','1') #En 1ºB de ESO  se imparte la asignatura Francés

    #Especificaremos que profesores imparten las asignaturas:
    # Cabecera: nuevoImparte(self, id_asociacion, id_profesor)
    #id 1
    GestorImpartes.nuevoImparte('1','1') #Francés en 1ºA ESO la imparte el profesor 1
    #id 2
    GestorImpartes.nuevoImparte('1','2') #Francés en 1ºA ESO la imparte el profesor 2, también.
    #id 3
    GestorImpartes.nuevoImparte('2','3') #Matemáticas en 1ºB ESO la imparte el profesor 3
    #id 4
    GestorImpartes.nuevoImparte('3','2') #Francés en 1ºB ESO la imparte el profesor 2


    #Matriculamos alumnos en asignaturas que se dan en clases concretas, que son los objetos Asocia (id_asociacion)
    #Cabecera: nuevaMatricula(self, id_alumno, id_asociacion):
    #id 1
    GestorMatriculas.nuevaMatricula('1','1') #Matriculamos al alumno con id=1 en Francés en 1ºA ESO.
    #id 2
    GestorMatriculas.nuevaMatricula('2','1') #Matriculamos al alumno con id=2 en Francés en 1ºA ESO.
    #id 3
    GestorMatriculas.nuevaMatricula('3','1') #Matriculamos al alumno con id=3 en Francés en 1ºA ESO.
    #id 4
    GestorMatriculas.nuevaMatricula('4','2') #Matriculamos al alumno con id=4 en Matemáticas en 1ºB ESO.
    #id 5
    GestorMatriculas.nuevaMatricula('5','2') #Matriculamos al alumno con id=5 en Matemáticas en 1ºB ESO.
    #id 6
    GestorMatriculas.nuevaMatricula('6','3') #Matriculamos al alumno con id=6 en Francés en 1ºB ESO.




if __name__ == '__main__':
    aprovisiona()
