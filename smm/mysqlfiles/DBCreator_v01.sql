/**
  Fichero de creación de la base de datos de SMM--
  Versión: 01
  Comentarios: Creación de la base de datos extendiendo el modelo v00.
**/

DROP DATABASE smm;

#Creamos la base de datos.
CREATE DATABASE smm;

USE smm;

#Creación de la tabla Alumno
CREATE TABLE Alumno(
  nombre CHAR(50),
  apellidos CHAR(50),
  dni CHAR(9),
  municipio CHAR(50),
  provincia CHAR(50),
  domicilio CHAR(100),
  email CHAR(100),
  telefono CHAR(10),
  PRIMARY KEY(dni)
);

#Creación de la tabla Asignatura
CREATE TABLE Asignatura(
  nombre CHAR(20),
  id CHAR(9),
  PRIMARY KEY (id)
);

#Creación de la tabla Grupo
/**
Ejemplo de tupla:
nivel: bachillerato
curso: 1
grupo: A
id: 1ABach
**/
CREATE TABLE Grupo(
  nivel CHAR(20),
  curso CHAR(2),
  grupo CHAR(2),
  id CHAR(9),
  PRIMARY KEY (id)
);


#Creación de la tabla Tiene
CREATE TABLE Tiene(
  idGrupo CHAR(9),
  idAsignatura CHAR(9),
  FOREIGN KEY (idGrupo) REFERENCES Grupo(id),
  FOREIGN KEY (idAsignatura) REFERENCES Asignatura(id),
  PRIMARY KEY (idGrupo, idAsignatura)
);

#ENTIDAD Creación de la tabla Profesor
CREATE TABLE Profesor(
  nombre CHAR(50),
  apellidos CHAR(50),
  dni CHAR(9),
  municipio CHAR(50),
  provincia CHAR(50),
  domicilio CHAR(100),
  email CHAR(100),
  telefono CHAR(10),
  PRIMARY KEY(dni)
);

CREATE TABLE Imparte(
  dniProfesor CHAR(9),
  idAsignatura CHAR(20),
  FOREIGN KEY (dniProfesor) REFERENCES Profesor(dni),
  FOREIGN KEY (idAsignatura) REFERENCES Asignatura(id)
);

# RELACIÓN Creación de la tabla Cursa que representa la información de un alumno
#que cursa una asignatura en un grupo específico.
CREATE TABLE Cursa(
  dniAlumno CHAR(9),
  idGrupo CHAR(9),
  idAsignatura CHAR(9),
  FOREIGN KEY (dniAlumno) REFERENCES Alumno(dni),
  FOREIGN KEY (idAsignatura) REFERENCES Asignatura(id),
  FOREIGN KEY (idGrupo) REFERENCES Grupo(id)
);


#Llamamos al script para que provisione de datos de muestra nuestra base de datos.
source addContenido_v01.sql;
