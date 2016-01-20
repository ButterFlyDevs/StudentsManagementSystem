/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

  ## Atención: Cualquier modificación de este fichero implica tener que modificar    ##
  ## el fichero aprovisionadorDB.py que llena de contenido la BD para que no falle.  ##

  #Notas:
    1º. Habría que evaluar el uso de eliminación en cascada en los casos en los que sean necesarios.
    2º. Habrá que justificar el uso del motor innoDB en las tablas

**/

#Borra la versión existente de la base de datos
DROP DATABASE IF EXISTS smm;

#Creamos la base de datos.
CREATE DATABASE smm;

USE smm;

#Creación de la tabla Alumno, con todos los atributos de esta entidad.
CREATE TABLE Alumno(
  nombre CHAR(20),
  dni CHAR(9),
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento DATE,
  telefono CHAR(50),
  PRIMARY KEY (dni)
);

#Creación de la tabla Profesor, con todos los atributos de esta entidad.
CREATE TABLE Profesor(
  nombre CHAR(20),
  dni CHAR(9),
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento CHAR(50),
  telefonoA CHAR(50),
  telefonoB CHAR(50),
  PRIMARY KEY (dni)
);

#Creación de la tabla Asignatura, con todos los atributos de esta entidad.
CREATE TABLE Asignatura(
  id CHAR(10),
  nombre CHAR(20),
  PRIMARY KEY (id)
);

#Creación de la tabla Curso, ejemplo
CREATE TABLE Curso(
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  PRIMARY KEY (curso)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE Grupo(
 #Añadimos la referencia de la entidad Asignatura
 id_asignatura CHAR REFERENCES Asignatura,
 #Añadimos la referencia de la entidad Curso
 id_curso INT REFERENCES Curso,
 PRIMARY KEY (id_asignatura, id_curso)
);

CREATE TABLE Imparte(
  #Necesitamos una referncia del profesor:
  id_profesor CHAR REFERENCES Profesor,
  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR REFERENCES Asignatura,
  #Añadimos la referencia de la entidad Curso
  id_curso INT REFERENCES Curso,
  PRIMARY KEY (id_profesor, id_asignatura, id_curso)
);

CREATE TABLE Matricula(
  id_alumno CHAR REFERENCES Alumno,
  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR REFERENCES Asignatura,
  #Añadimos la referencia de la entidad Curso
  id_curso INT REFERENCES Curso,
  PRIMARY KEY (id_alumno, id_asignatura, id_curso)
);
